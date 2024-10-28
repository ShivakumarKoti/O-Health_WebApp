import os
import datetime
import dotenv
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from rapidfuzz import process, fuzz
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import spacy
import re
import logging
from spacy.matcher import Matcher
from gtts import gTTS
import io

# -------------------- Environment Setup -------------------- #

# Load environment variables from .env file
dotenv.load_dotenv()

# Set the OpenAI API key from environment variables
openai.api_key = st.secrets["OPENAI_API_KEY"]

if not OPENAI_API_KEY:
    st.error("OpenAI API key not found. Please set it in the .env file.")
    st.stop()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- Load BioBERT NER Model -------------------- #

# Path to the BioBERT model directory
BIOBERT_MODEL_DIR = 'medical-bert-symptom-ner'  # Ensure this directory exists

def load_biobert_ner_pipeline(model_dir):
    """
    Load the BioBERT NER pipeline.
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_dir, add_prefix_space=True)
        model = AutoModelForTokenClassification.from_pretrained(model_dir)
        device = 0 if torch.cuda.is_available() else -1
        ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple", device=device)
        logger.info("BioBERT NER pipeline loaded successfully.")
        return ner_pipeline
    except Exception as e:
        st.error(f"Failed to load BioBERT NER pipeline: {e}")
        logger.error(f"Failed to load BioBERT NER pipeline: {e}")
        st.stop()

@st.cache_resource
def get_biobert_pipeline():
    return load_biobert_ner_pipeline(BIOBERT_MODEL_DIR)

ner_pipeline = get_biobert_pipeline()
st.sidebar.success("BioBERT NER model loaded successfully!")

# -------------------- Load SpaCy Model -------------------- #

@st.cache_resource
def load_spacy_model():
    """
    Load the SpaCy model for additional NLP tasks.
    """
    try:
        nlp = spacy.load('en_core_web_sm')
        logger.info("SpaCy model 'en_core_web_sm' loaded successfully.")
        return nlp
    except OSError as e:
        st.error("SpaCy model 'en_core_web_sm' not found. Please install it using 'python -m spacy download en_core_web_sm'.")
        logger.error(f"SpaCy model loading error: {e}")
        st.stop()

nlp = load_spacy_model()

# -------------------- Load Disease-Symptom Mapping -------------------- #

@st.cache_data
def load_disease_symptom_mapping():
    """
    Load the disease-symptom mapping from a CSV file.
    """
    csv_file = "disease_symptom_mapping.csv"
    if not os.path.exists(csv_file):
        st.error(f"'{csv_file}' not found in the current directory.")
        logger.error(f"'{csv_file}' not found.")
        st.stop()
    try:
        df = pd.read_csv(csv_file)
        if 'DiseaseName' not in df.columns or 'SymptomName' not in df.columns:
            st.error("CSV file must contain 'DiseaseName' and 'SymptomName' columns.")
            logger.error("CSV file missing required columns.")
            st.stop()
        logger.info(f"'{csv_file}' loaded successfully.")
        return df
    except Exception as e:
        st.error(f"Failed to load '{csv_file}': {e}")
        logger.error(f"Failed to load '{csv_file}': {e}")
        st.stop()

df_disease_symptom = load_disease_symptom_mapping()

# Prepare a list of known symptoms
known_symptoms = df_disease_symptom['SymptomName'].unique()

# -------------------- Define Follow-Up Questions -------------------- #

# Define a dictionary mapping symptoms to potential follow-up questions in Hindi and their English translations
symptom_followup_questions = {
    "Fever": [
        {"hi": "क्या आपकी बुखार लगातार है या बार-बार आती है?", "en": "Is your fever constant or intermittent?"},
        {"hi": "क्या आपने अपने बुखार के लिए कोई दवा ली है?", "en": "Have you taken any medication for your fever?"},
        {"hi": "क्या आप ठंडक महसूस कर रहे हैं?", "en": "Are you experiencing any chills?"},
        {"hi": "क्या आपने हाल ही में किसी उच्च जोखिम वाले क्षेत्र की यात्रा की है?", "en": "Have you recently traveled to any high-risk areas?"},
        {"hi": "क्या आपको सिरदर्द हो रहा है?", "en": "Are you experiencing headaches?"}
    ],
    "Cough": [
        {"hi": "क्या आपकी खांसी सूखी है या बलगम के साथ है?", "en": "Is your cough dry or productive?"},
        {"hi": "क्या खांसी के दौरान आपको छाती में दर्द होता है?", "en": "Have you experienced any chest pain while coughing?"},
        {"hi": "क्या आपको सांस लेने में कोई तकलीफ हो रही है?", "en": "Do you have any shortness of breath?"},
        {"hi": "क्या आपकी खांसी के साथ खून भी आता है?", "en": "Do you cough up blood?"},
        {"hi": "क्या आपकी खांसी रात में ज्यादा होती है?", "en": "Is your cough worse at night?"}
    ],
    "Abdominal Pain": [
        {"hi": "क्या आपने हाल ही में कोई तीव्र व्यायाम किया है या गिर पड़े हैं?", "en": "Did you do any intense workouts or fall recently?"},
        {"hi": "क्या आपको मिचली या उल्टी हुई है?", "en": "Have you experienced any nausea or vomiting?"},
        {"hi": "क्या आपके मल त्याग में कोई बदलाव आया है?", "en": "Do you have any changes in your bowel movements?"},
        {"hi": "क्या आपने किसी भी प्रकार का फुलावट या गैस महसूस किया है?", "en": "Have you noticed any bloating or gas?"},
        {"hi": "क्या दर्द स्थानीयकृत है या सामान्यीकृत?", "en": "Is the pain localized or generalized?"}
    ],
    "High Fever": [
        {"hi": "क्या आपकी बुखार में रात को अधिक होती है?", "en": "Is your fever higher at night?"},
        {"hi": "क्या आपके शरीर में दर्द होता है?", "en": "Do you experience body aches?"},
        {"hi": "क्या आपको पसीना आ रहा है?", "en": "Are you sweating?"},
        {"hi": "क्या आपकी बुखार कम हो रही है या बढ़ रही है?", "en": "Is your fever decreasing or increasing?"},
        {"hi": "क्या आपके पास कोई अन्य लक्षण हैं?", "en": "Do you have any other symptoms?"}
    ],
    # Add more symptoms and their corresponding follow-up questions as needed
}

# Additional questions for missing information in Hindi and English
additional_followup_questions = [
    {"hi": "आपकी उम्र क्या है?", "en": "What is your age?"},
    {"hi": "आपका लिंग क्या है?", "en": "What is your gender?"},
    {"hi": "आप वर्तमान में कहां स्थित हैं?", "en": "Where are you currently located?"},
    {"hi": "क्या आप कोई अन्य लक्षण महसूस कर रहे हैं?", "en": "Are you experiencing any other symptoms?"},
    {"hi": "आपने हाल ही में क्या खाया है?", "en": "What have you eaten recently?"}  # Added food intake question
]

# -------------------- Core Functions -------------------- #

def save_audio_file(audio_bytes, file_extension):
    """
    Save audio bytes to a file with the specified extension.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"audio_{timestamp}.{file_extension}"

    try:
        with open(file_name, "wb") as f:
            f.write(audio_bytes)
        logger.info(f"Audio saved as {file_name}")
        return file_name
    except Exception as e:
        st.error(f"Failed to save audio file: {e}")
        logger.error(f"Failed to save audio file: {e}")
        return None

def transcribe_audio(file_path):
    """
    Transcribe the audio file at the specified path using OpenAI's Whisper API.
    Uses the 'translate' endpoint to get English transcription.
    """
    try:
        import openai  # Ensure OpenAI is installed
        openai.api_key = OPENAI_API_KEY

        with open(file_path, "rb") as audio_file:
            transcript = openai.Audio.translate("whisper-1", audio_file)
            transcribed_text = transcript.get("text", "").strip()
            logger.info("Audio transcription (translation) successful.")
            return transcribed_text
    except Exception as e:
        st.error(f"Transcription failed: {e}")
        logger.error(f"Transcription failed: {e}")
        return None
    finally:
        # Delete the audio file after transcription
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Audio file {file_path} deleted successfully after transcription.")
            except Exception as e:
                st.warning(f"Could not delete audio file {file_path}: {e}")
                logger.warning(f"Could not delete audio file {file_path}: {e}")

def generate_audio(text, lang='hi'):
    """
    Generate audio from text using Google Text-to-Speech.
    Returns audio bytes.
    """
    try:
        tts = gTTS(text=text, lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        logger.info("Audio generated successfully.")
        return fp.read()
    except Exception as e:
        st.error(f"Failed to generate audio: {e}")
        logger.error(f"Failed to generate audio: {e}")
        return None

def extract_symptoms(text):
    """
    Extract symptoms from the input text using BioBERT-based NER and detect negations.
    Returns a set of affirmed symptoms.
    """
    try:
        entities = ner_pipeline(text)
        if not entities:
            logger.info("No entities extracted by BioBERT NER.")
            return set()

        # Initialize SpaCy Doc for negation detection
        doc = nlp(text)

        # Dictionary to hold symptom presence
        symptoms_presence = {}

        for entity in entities:
            symptom = entity['word'].title()
            # Initialize as True (present) by default
            symptoms_presence[symptom] = True

            # Find the token in SpaCy Doc
            for token in doc:
                if token.text.lower() == entity['word'].lower():
                    # Check if there's a negation modifier
                    neg = False
                    for child in token.children:
                        if child.dep_ == "neg":
                            neg = True
                            break
                    symptoms_presence[symptom] = not neg
                    break

        # Remove symptoms that are negated
        symptoms_present = {symptom for symptom, present in symptoms_presence.items() if present}
        logger.info(f"Extracted Symptoms after negation handling: {symptoms_present}")
        return symptoms_present
    except Exception as e:
        st.error(f"An error occurred during symptom extraction: {e}")
        logger.error(f"Symptom extraction error: {e}")
        return set()

def match_symptoms(extracted_symptoms):
    """
    Match extracted symptoms with known symptoms using RapidFuzz.
    Returns a set of matched symptoms.
    """
    matched_symptoms = set()
    for symptom in extracted_symptoms:
        match = process.extractOne(symptom, known_symptoms, scorer=fuzz.WRatio, score_cutoff=80)
        if match:
            matched_symptoms.add(match[0])
    logger.info(f"Matched Symptoms: {matched_symptoms}")
    return matched_symptoms

def extract_additional_entities(text):
    """
    Extract additional entities like age, gender, location, duration, medications, and food intake from text.
    """
    doc = nlp(text.lower())  # Normalize text to lowercase for consistent matching
    age = None
    gender = None
    location = None
    duration = None
    medications = []
    food_intake = None

    # Initialize Matcher with the shared vocab
    matcher = Matcher(nlp.vocab)

    # Define patterns for duration
    duration_patterns = [
        [{"LOWER": {"IN": ["since", "for", "from"]}}, {"LOWER": {"IN": ["the", "past", "last"]}, "OP": "?"}, {"LIKE_NUM": True}, {"LOWER": {"IN": ["day", "days", "week", "weeks", "month", "months", "year", "years"]}}],
        [{"LOWER": {"IN": ["the", "past", "last"]}}, {"LIKE_NUM": True}, {"LOWER": {"IN": ["day", "days", "week", "weeks", "month", "months", "year", "years"]}}],
        [{"LOWER": {"IN": ["over", "during"]}}, {"LOWER": {"IN": ["the"]}}, {"LOWER": {"IN": ["past", "last"]}}, {"LIKE_NUM": True}, {"LOWER": {"IN": ["day", "days", "week", "weeks", "month", "months", "year", "years"]}}],
        [{"LIKE_NUM": True}, {"LOWER": {"IN": ["day", "days", "week", "weeks", "month", "months", "year", "years"]}}, {"LOWER": {"IN": ["ago", "back"]}}],
        [{"LOWER": {"IN": ["a", "an"]}}, {"LOWER": {"IN": ["day", "week", "month", "year"]}}]
    ]
    matcher.add("DURATION", duration_patterns)

    # Define patterns for medications
    medication_patterns = [
        [{"LOWER": {"IN": ["taking", "taken", "take", "using", "prescribed", "prescription"]}}, {"LOWER": "the", "OP": "?"}, {"POS": {"IN": ["NOUN", "PROPN"]}}, {"LOWER": {"IN": [",", "and"]}, "OP": "*"}, {"POS": {"IN": ["NOUN", "PROPN", "NUM"]}, "OP": "+"}],
        [{"LOWER": {"IN": ["prescribed"]}}, {"POS": {"IN": ["NOUN", "PROPN"]}}, {"LOWER": {"IN": [",", "and"]}, "OP": "*"}, {"POS": {"IN": ["NOUN", "PROPN", "NUM"]}, "OP": "+"}]
    ]
    matcher.add("MEDICATION", medication_patterns)

    # Define patterns for food intake
    food_patterns = [
        [{"LOWER": {"IN": ["ate", "eaten", "have eaten", "had"]}}, {"POS": {"IN": ["NOUN", "PROPN"]}, "OP": "+"}],
        [{"LOWER": {"IN": ["what", "have"]}}, {"LOWER": "you"}, {"LOWER": "eaten"}, {"LOWER": "recently"}, {"LOWER": "?"}]
    ]
    matcher.add("FOOD", food_patterns)

    matches = matcher(doc)

    for match_id, start, end in matches:
        span = doc[start:end]
        rule_id = nlp.vocab.strings[match_id]
        if rule_id == "DURATION":
            duration = span.text
        elif rule_id == "MEDICATION":
            meds = span.text.split()
            # Clean and title case
            meds = [med.strip(",").title() for med in meds if med.lower() not in ['taking', 'taken', 'take', 'using', 'prescribed', 'prescription', 'the']]
            # Split medications by commas or 'and'
            meds_list = re.split(r',| and ', ' '.join(meds))
            for med in meds_list:
                med = med.strip().title()
                if med:  # Ensure it's not empty
                    medications.append(med)
        elif rule_id == "FOOD":
            food_intake = span.text

    # Extract entities using SpaCy's NER
    for ent in doc.ents:
        if ent.label_ == 'GPE':
            location = ent.text.title()
        elif ent.label_ in ['DATE', 'TIME']:
            # Attempt to extract duration from DATE and TIME entities
            if not duration:
                duration = ent.text

    # Extract age using regex patterns
    age_patterns = [
        r'(\b\d{1,2}\b)\s*(years old|year old|y/o|yo|yrs old)',
        r'age\s*(\b\d{1,2}\b)',
        r'i am\s*(\b\d{1,2}\b)',
        r'my age is\s*(\b\d{1,2}\b)'
    ]
    for pattern in age_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            age = int(match.group(1))
            break

    # Extract gender using regex patterns
    gender_patterns = [
        r'\b(male|female|man|woman|boy|girl)\b',
        r'i am\s+(male|female)',
        r'my gender is\s+(male|female)'
    ]
    for pattern in gender_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            gender = match.group(1).lower()
            if gender in ['man', 'boy']:
                gender = 'male'
            elif gender in ['woman', 'girl']:
                gender = 'female'
            break

    # Log extracted entities for debugging
    logger.info(f"Extracted Entities: Age={age}, Gender={gender}, Location={location}, Duration={duration}, Medications={medications}, Food Intake={food_intake}")

    return {
        'age': age,
        'gender': gender,
        'location': location,
        'duration': duration,
        'medications': medications,
        'food_intake': food_intake
    }

def map_symptoms_to_diseases(matched_symptoms, additional_info, causes):
    """
    Map the matched symptoms to probable diseases based on the disease-symptom mapping.
    Include causes in the final report if available.
    """
    # Create disease-symptom mapping
    disease_symptom_map = df_disease_symptom.groupby('DiseaseName')['SymptomName'].apply(set).to_dict()

    # Assume prior probabilities are equal for all diseases
    disease_prior = {disease: 1 / len(disease_symptom_map) for disease in disease_symptom_map}

    # Adjust priors based on age, gender, and location (simplified example)
    for disease in disease_prior:
        # Example adjustments (in reality, use actual data)
        if additional_info['age']:
            if disease in ['Chickenpox', 'Measles'] and additional_info['age'] > 12:
                disease_prior[disease] *= 0.5  # Less likely in adults
        if additional_info['gender']:
            if disease == 'Prostate Cancer' and additional_info['gender'] == 'female':
                disease_prior[disease] = 0  # Females do not get prostate cancer
        if additional_info['location']:
            if disease == 'Altitude Sickness' and 'Mountain' in additional_info['location']:
                disease_prior[disease] *= 2  # More likely in mountains

    # Calculate likelihoods and posterior probabilities
    disease_scores = {}
    for disease, symptoms_set in disease_symptom_map.items():
        matched = matched_symptoms.intersection(symptoms_set)
        total_symptoms = len(symptoms_set)
        if total_symptoms == 0:
            continue
        # Simple likelihood estimation
        likelihood = len(matched) / total_symptoms
        # Posterior probability proportional to likelihood * prior
        posterior = likelihood * disease_prior[disease]
        disease_scores[disease] = posterior

    if disease_scores:
        # Remove diseases with zero probability
        disease_scores = {k: v for k, v in disease_scores.items() if v > 0}

        if not disease_scores:
            return {}
        else:
            # Normalize the probabilities
            total = sum(disease_scores.values())
            for disease in disease_scores:
                disease_scores[disease] = round((disease_scores[disease] / total) * 100, 2)
            # Sort diseases by probability
            sorted_diseases = dict(sorted(disease_scores.items(), key=lambda item: item[1], reverse=True))
            # Attach causes if any
            if causes:
                sorted_diseases['Causes'] = ', '.join(causes)
            return sorted_diseases
    else:
        return {}

def determine_followup_questions(matched_symptoms, additional_info):
    """
    Determine up to 5 follow-up questions based on matched symptoms and missing information.
    """
    followup_questions = []
    asked_questions = set()

    # Add symptom-specific follow-up questions
    for symptom in matched_symptoms:
        if symptom in symptom_followup_questions:
            for q in symptom_followup_questions[symptom]:
                question_en = q['en']
                if question_en not in asked_questions and len(followup_questions) < 5:
                    followup_questions.append(q)
                    asked_questions.add(question_en)
                if len(followup_questions) >= 5:
                    break
        if len(followup_questions) >= 5:
            break

    # Add additional questions for missing information
    if additional_info['duration'] is None and len(followup_questions) < 5:
        for q in additional_followup_questions:
            if "age" not in q['en'].lower() and "gender" not in q['en'].lower() and "location" not in q['en'].lower() and "medication" not in q['en'].lower() and "other" not in q['en'].lower() and "food" not in q['en'].lower():
                question_en = q['en']
                if question_en not in asked_questions:
                    followup_questions.append(q)
                    asked_questions.add(question_en)
                    break  # Only one question for duration

    if additional_info['age'] is None and len(followup_questions) < 5:
        for q in additional_followup_questions:
            if "age" in q['en'].lower() and q['en'] not in asked_questions:
                followup_questions.append(q)
                asked_questions.add(q['en'])
                break

    if additional_info['gender'] is None and len(followup_questions) < 5:
        for q in additional_followup_questions:
            if "gender" in q['en'].lower() and q['en'] not in asked_questions:
                followup_questions.append(q)
                asked_questions.add(q['en'])
                break

    if additional_info['location'] is None and len(followup_questions) < 5:
        for q in additional_followup_questions:
            if "location" in q['en'].lower() and q['en'] not in asked_questions:
                followup_questions.append(q)
                asked_questions.add(q['en'])
                break

    if not additional_info['medications'] and len(followup_questions) < 5:
        for q in additional_followup_questions:
            if "medication" in q['en'].lower() and q['en'] not in asked_questions:
                followup_questions.append(q)
                asked_questions.add(q['en'])
                break

    if additional_info['food_intake'] is None and len(followup_questions) < 5:
        for q in additional_followup_questions:
            if "food" in q['en'].lower() and q['en'] not in asked_questions:
                followup_questions.append(q)
                asked_questions.add(q['en'])
                break

    return followup_questions

def extract_and_prepare_questions(conversation_history):
    """
    Extract information from the conversation history and prepare follow-up questions.
    """
    matched_symptoms, additional_info = extract_all_symptoms(conversation_history)
    followup_questions = determine_followup_questions(matched_symptoms, additional_info)
    return followup_questions

def generate_report(conversation_history):
    """
    Generate an analytical report based on the conversation history.
    """
    # Extract all necessary information
    matched_symptoms, additional_info = extract_all_symptoms(conversation_history)

    # Map symptoms to diseases
    probable_diseases = map_symptoms_to_diseases(matched_symptoms, additional_info, causes=[])

    # Display the report
    st.subheader("📄 **Analytical Report:**")
    st.write("**Initial Information:**")
    st.write(f"**Symptoms:** {', '.join(matched_symptoms) if matched_symptoms else 'Not specified'}")
    if additional_info['duration']:
        st.write(f"**Duration:** {additional_info['duration']}")
    if additional_info['age']:
        st.write(f"**Age:** {additional_info['age']} years old")
    if additional_info['gender']:
        st.write(f"**Gender:** {additional_info['gender'].title()}")
    if additional_info['location']:
        st.write(f"**Location:** {additional_info['location']}")
    if additional_info['medications']:
        st.write(f"**Medications Taken:** {', '.join(additional_info['medications'])}")
    if additional_info['food_intake']:
        st.write(f"**Recent Food Intake:** {additional_info['food_intake']}")

    # Summary of answers
    st.subheader("📝 **Summary of Your Responses:**")
    summary_data = []
    for entry in conversation_history:
        if 'followup_question' in entry and 'response' in entry:
            # Find the English version of the follow-up question
            question_en = next((q['en'] for q in additional_followup_questions + [q for symptom in symptom_followup_questions for q in symptom_followup_questions[symptom]] if q['hi'] == entry['followup_question']), entry['followup_question'])
            summary_data.append({
                'Question': question_en,
                'Your Answer': entry['response']
            })
    df_summary = pd.DataFrame(summary_data)
    st.table(df_summary)

    if probable_diseases:
        st.subheader("🩺 **Probable Diseases:**")
        # Remove 'Causes' if present
        causes_report = probable_diseases.pop('Causes', None)
        for disease, prob in probable_diseases.items():
            st.write(f"**{disease}**: {prob}%")

        if causes_report:
            st.write(f"**Possible Causes:** {causes_report}")

        # Plot bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=list(probable_diseases.keys()), y=list(probable_diseases.values()), ax=ax)
        ax.set_xlabel("Disease")
        ax.set_ylabel("Probability (%)")
        ax.set_title("Probable Diseases")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
    else:
        st.info("No probable diseases found based on the entered symptoms and information.")

def generate_followup_report(conversation_history):
    """
    Generate a follow-up report based on the conversation history.
    """
    generate_report(conversation_history)

def extract_all_symptoms(conversation_history):
    """
    Extract and match symptoms from the entire conversation history.
    """
    matched_symptoms = set()
    additional_info = {
        'age': None,
        'gender': None,
        'location': None,
        'duration': None,
        'medications': [],
        'food_intake': None
    }

    # Process each entry in the conversation history
    for entry in conversation_history:
        if 'user' in entry:
            user_text = entry['user']
            symptoms = extract_symptoms(user_text)
            matched_symptoms.update(match_symptoms(symptoms))
            info = extract_additional_entities(user_text)
            for key in additional_info:
                if key in info and info[key]:
                    if isinstance(info[key], list):
                        # Extend the list and remove duplicates
                        additional_info[key].extend(info[key])
                        additional_info[key] = list(set(additional_info[key]))
                    else:
                        if not additional_info[key]:
                            additional_info[key] = info[key]
        if 'response' in entry:
            response_text = entry['response']
            symptoms = extract_symptoms(response_text)
            matched_symptoms.update(match_symptoms(symptoms))
            info = extract_additional_entities(response_text)
            for key in additional_info:
                if key in info and info[key]:
                    if isinstance(info[key], list):
                        # Extend the list and remove duplicates
                        additional_info[key].extend(info[key])
                        additional_info[key] = list(set(additional_info[key]))
                    else:
                        if not additional_info[key]:
                            additional_info[key] = info[key]
        if 'additional_symptoms' in entry:
            additional_symptoms = entry['additional_symptoms']
            if isinstance(additional_symptoms, list):
                matched_symptoms.update(additional_symptoms)
            elif isinstance(additional_symptoms, str):
                matched_symptoms.add(additional_symptoms)

    logger.info(f"Final Matched Symptoms: {matched_symptoms}")
    logger.info(f"Additional Information: {additional_info}")
    return matched_symptoms, additional_info

def play_greetings():
    """
    Generate and play a greeting message in Hindi.
    """
    # Greeting in Hindi
    greeting_text = "ओ-हेल्थ में आपका स्वागत है। कृपया नीचे दिए गए विकल्पों में से एक चुनें ताकि हम आपकी सहायता कर सकें।"

    # Generate audio
    audio_bytes = generate_audio(greeting_text, lang='hi')

    if audio_bytes:
        # Provide audio playback
        st.markdown("### 📢 **Welcome!**")
        st.audio(audio_bytes, format='audio/mp3')

# -------------------- Custom CSS for Microphone Button -------------------- #

def inject_custom_css():
    """
    Inject custom CSS to style the microphone button.
    """
    custom_css = """
    <style>
    /* Style the microphone button */
    .custom-mic-button button {
        background-color: #28a745 !important; /* Green color */
        color: white !important;
        font-size: 24px !important;
        width: 120px !important;
        height: 120px !important;
        border-radius: 50% !important;
        border: none !important;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .custom-mic-button button.recording {
        background-color: #dc3545 !important; /* Red color when recording */
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# -------------------- Streamlit Interface -------------------- #

def main():
    """
    Main function to run the integrated Whisper Transcription and BioBERT-based Symptom-to-Disease Mapper app.
    """
    # Inject custom CSS
    inject_custom_css()

    # Initialize session state for dynamic questioning
    if 'conversation_step' not in st.session_state:
        st.session_state.conversation_step = 0  # 0: Initial Input, 1: Follow-up Questions, 2: Report Generation
        st.session_state.conversation_history = []  # Stores the conversation
        st.session_state.report_generated = False  # Flag to indicate if report is generated
        st.session_state.input_method = None  # Tracks which input method was used
        st.session_state.followup_questions = []  # List of follow-up questions to ask
        st.session_state.current_followup = 0  # Index of the current follow-up question

    # Play greetings when the app loads
    if st.session_state.conversation_step == 0:
        play_greetings()

    st.title("🩺 O-Health Diagnostic Tool")
    st.write("""
        Welcome to the O-Health Diagnostic Tool. You can either speak your symptoms in Hindi or type them in English to receive potential disease recommendations based on your inputs.
    """)

    # Create two tabs: Voice Input and Text Input
    tab1, tab2 = st.tabs(["🔊 Voice Input", "✍️ Text Input"])

    # ----------------- Voice Input Tab ----------------- #
    with tab1:
        if st.session_state.input_method is None and st.session_state.conversation_step == 0:
            st.header("Record Your Symptoms in Hindi")
            st.write("Click the **Record** button below, speak your symptoms in Hindi, and then click **Stop**.")

            # Single, persistent microphone button with custom styling
            if 'mic_button_state' not in st.session_state:
                st.session_state.mic_button_state = False  # False: not recording, True: recording

            # Placeholder for the microphone button
            mic_placeholder = st.empty()

            if not st.session_state.mic_button_state:
                # Display green microphone button
                if mic_placeholder.button("🎤 Record", key="initial_record_button", on_click=lambda: toggle_recording('start')):
                    pass
            else:
                # Display red microphone button during recording
                if mic_placeholder.button("⏺️ Recording...", key="initial_recording_button", on_click=lambda: toggle_recording('stop')):
                    pass

            # Function to toggle recording state
            def toggle_recording(action):
                if action == 'start':
                    st.session_state.mic_button_state = True
                elif action == 'stop':
                    st.session_state.mic_button_state = False

            # If recording started, initiate audio recording
            if st.session_state.mic_button_state:
                audio_bytes = audio_recorder(key="initial_voice_input")

                if audio_bytes:
                    # Display the recorded audio
                    st.audio(audio_bytes, format="audio/wav")

                    # Save the recorded audio to a file
                    file_name = save_audio_file(audio_bytes, "wav")

                    if file_name:
                        st.success("Audio recorded and saved successfully!")
                        st.info("Transcribing your audio... Please wait.")
                        # Transcribe the audio to English
                        transcribed_text = transcribe_audio(file_name)

                        if transcribed_text:
                            st.subheader("📝 Transcribed Text (English):")
                            st.write(transcribed_text)
                            # Store the translated text in session state for diagnosis
                            st.session_state.conversation_history.append({
                                'user': transcribed_text
                            })
                            # Determine follow-up questions based on initial input
                            st.session_state.followup_questions = extract_and_prepare_questions(st.session_state.conversation_history)
                            st.session_state.conversation_step = 1  # Move to follow-up questions
                            st.session_state.input_method = 'voice'  # Set input method
                        else:
                            st.error("Failed to transcribe the audio.")
        else:
            st.info(f"You have already provided input via the '{st.session_state.input_method}' method.")

    # ----------------- Text Input Tab ----------------- #
    with tab2:
        if st.session_state.input_method is None and st.session_state.conversation_step == 0:
            st.header("Enter Your Symptoms in English")
            st.write("Type your symptoms below and click **Submit** to receive disease recommendations based on your inputs.")

            # Text area for user input
            user_input = st.text_area(
                "📋 Enter your symptoms and additional information:",
                height=150,
                placeholder="e.g., I have been suffering from fever and cough for the past 3 days. I have taken Ibuprofen and Dolo 650 medications."
            )

            if st.button("Submit"):
                if user_input.strip() == "":
                    st.warning("Please enter your symptoms for diagnosis.")
                else:
                    st.session_state.conversation_history.append({
                        'user': user_input
                    })
                    # Determine follow-up questions based on initial input
                    st.session_state.followup_questions = extract_and_prepare_questions(st.session_state.conversation_history)
                    st.session_state.conversation_step = 1  # Move to follow-up questions
                    st.session_state.input_method = 'text'  # Set input method
                    st.success("Input received! The app will now ask you some follow-up questions.")
        else:
            st.info(f"You have already provided input via the '{st.session_state.input_method}' method.")

    # ----------------- Follow-Up Questions ----------------- #

    if st.session_state.conversation_step == 1 and st.session_state.followup_questions:
        # Display the current follow-up question based on the current_followup index
        if st.session_state.current_followup < len(st.session_state.followup_questions) and st.session_state.current_followup < 5:
            current_question = st.session_state.followup_questions[st.session_state.current_followup]
            st.header(f"🔍 **Follow-Up Question {st.session_state.current_followup + 1}**")
            st.write(current_question['en'])
            st.write("🗣️ **Speak Now:**")

            # Generate and play audio for the question automatically in Hindi
            audio_bytes = generate_audio(current_question['hi'], lang='hi')  # Hindi voice
            if audio_bytes:
                st.audio(audio_bytes, format='audio/mp3', start_time=0)

            # Single, persistent microphone button with custom styling
            if 'mic_button_state_q' not in st.session_state:
                st.session_state.mic_button_state_q = False  # False: not recording, True: recording

            # Placeholder for the microphone button
            mic_placeholder_q = st.empty()

            if not st.session_state.mic_button_state_q:
                # Display green microphone button
                if mic_placeholder_q.button("🎤 Record", key=f"record_button_q{st.session_state.current_followup + 1}", on_click=lambda: toggle_recording_q('start')):
                    pass
            else:
                # Display red microphone button during recording
                if mic_placeholder_q.button("⏺️ Recording...", key=f"recording_button_q{st.session_state.current_followup + 1}", on_click=lambda: toggle_recording_q('stop')):
                    pass

            # Function to toggle recording state for questions
            def toggle_recording_q(action):
                if action == 'start':
                    st.session_state.mic_button_state_q = True
                elif action == 'stop':
                    st.session_state.mic_button_state_q = False

            # If recording started, initiate audio recording
            if st.session_state.mic_button_state_q:
                response_audio = audio_recorder(key=f"voice_input_q{st.session_state.current_followup + 1}")

                if response_audio:
                    # Display the recorded audio
                    st.audio(response_audio, format="audio/wav")

                    # Save the recorded audio to a file
                    response_file = save_audio_file(response_audio, "wav")

                    if response_file:
                        st.success("Your audio response has been recorded and saved successfully!")
                        st.info("Transcribing your audio... Please wait.")
                        # Transcribe the response
                        response_transcribed = transcribe_audio(response_file)

                        if response_transcribed:
                            st.subheader(f"📝 Response to Follow-Up Question {st.session_state.current_followup + 1} (English):")
                            st.write(response_transcribed)
                            # Store the response in conversation history
                            st.session_state.conversation_history.append({
                                'followup_question': current_question['en'],
                                'response': response_transcribed
                            })
                            # Extract any new symptoms from the response
                            new_symptoms = extract_symptoms(response_transcribed)
                            matched_new_symptoms = match_symptoms(new_symptoms)
                            if matched_new_symptoms:
                                st.session_state.conversation_history.append({
                                    'additional_symptoms': list(matched_new_symptoms)
                                })
                                # Notify the user about new symptoms detected
                                st.info(f"New symptoms detected: {', '.join(matched_new_symptoms)}")
                            # Extract additional information from the response
                            additional_info = extract_additional_entities(response_transcribed)
                            # Check if follow-up questions need to be updated based on new information
                            if any(additional_info.values()):
                                st.session_state.followup_questions = extract_and_prepare_questions(st.session_state.conversation_history)
                            # Move to the next follow-up question or generate report
                            st.session_state.current_followup += 1
                            if st.session_state.current_followup >= len(st.session_state.followup_questions) or st.session_state.current_followup >= 5:
                                st.session_state.conversation_step = 2  # Proceed to report generation
                            else:
                                # Prompt the user for the next response
                                st.success("The next question is ready. Please click the Record button to answer.")
                        else:
                            st.error("Failed to transcribe your audio response.")
                    else:
                        st.error("Failed to save your response audio.")
        else:
            pass  # No more follow-up questions or reached maximum limit

    # ----------------- Generate Report ----------------- #
    if st.session_state.conversation_step == 2 and not st.session_state.report_generated:
        st.session_state.report_generated = True
        with st.spinner("Analyzing your information..."):
            generate_followup_report(st.session_state.conversation_history)

    # -------------------- Debugging -------------------- #
    # Display the current conversation step for debugging
    st.sidebar.markdown("## 🔍 **Debugging Information**")
    st.sidebar.write(f"**Input Method:** {st.session_state.input_method}")
    st.sidebar.write(f"**Conversation Step:** {st.session_state.conversation_step}")
    st.sidebar.write(f"**Report Generated:** {st.session_state.report_generated}")
    st.sidebar.write("**Conversation History:**")
    st.sidebar.json(st.session_state.conversation_history)

# -------------------- Run the App -------------------- #

if __name__ == "__main__":
    main()
