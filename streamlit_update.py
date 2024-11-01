import os
import datetime
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import pandas as pd
from rapidfuzz import process, fuzz
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import spacy
import re
import logging
from gtts import gTTS
import io
import openai
import requests
import zipfile
import base64

# -------------------- Environment Setup -------------------- #

# Set the OpenAI API key from environment variable
openai.api_key = st.secrets["OPENAI_API_KEY"]

if not openai.api_key:
    st.error("OpenAI API key not found. Please set it as an environment variable 'OPENAI_API_KEY'.")
    st.stop()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- Load BioBERT NER Model -------------------- #

BIOBERT_MODEL_URL = "https://www.dropbox.com/scl/fi/bsphlpwlt7jclb9ybiyx6/medical-bert-symptom-ner.zip?rlkey=j1066ivw1qvkp0c8urpm8pjv6&st=bk4e923j&dl=1"
BIOBERT_MODEL_DIR = 'medical-bert-symptom-ner'

def download_and_unzip_biobert_model(model_url, model_dir):
    if not os.path.exists(model_dir):
        st.info("Downloading the BioBERT NER model. Please wait...")
        # Download the model zip file
        with st.spinner('Downloading BioBERT NER model...'):
            try:
                response = requests.get(model_url, stream=True)
                response.raise_for_status()
                with open('biobert_model.zip', 'wb') as out_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            out_file.write(chunk)
                logger.info("BioBERT NER model downloaded successfully.")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to download the BioBERT NER model: {e}")
                logger.error(f"Failed to download the BioBERT NER model: {e}")
                st.stop()
        # Unzip the model
        try:
            with zipfile.ZipFile('biobert_model.zip', 'r') as zip_ref:
                zip_ref.extractall('.')
            st.success("BioBERT NER model downloaded and extracted successfully.")
            logger.info("BioBERT NER model extracted successfully.")
        except zipfile.BadZipFile as e:
            st.error("Downloaded BioBERT model file is not a valid zip file.")
            logger.error(f"Invalid zip file: {e}")
            st.stop()
        finally:
            if os.path.exists('biobert_model.zip'):
                try:
                    os.remove('biobert_model.zip')
                    logger.info("biobert_model.zip removed successfully.")
                except Exception as e:
                    st.warning(f"Could not remove biobert_model.zip: {e}")
                    logger.warning(f"Could not remove biobert_model.zip: {e}")

# Download and unzip the BioBERT model if it doesn't exist
download_and_unzip_biobert_model(BIOBERT_MODEL_URL, BIOBERT_MODEL_DIR)

# Load the tokenizer and model using caching
@st.cache_resource(show_spinner=False)
def load_biobert_ner_pipeline():
    try:
        tokenizer = AutoTokenizer.from_pretrained(BIOBERT_MODEL_DIR, add_prefix_space=True)
        model = AutoModelForTokenClassification.from_pretrained(BIOBERT_MODEL_DIR)
        device = 0 if torch.cuda.is_available() else -1
        ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple", device=device)
        logger.info("BioBERT NER pipeline loaded successfully.")
        return ner_pipeline
    except Exception as e:
        st.error(f"Failed to load BioBERT NER pipeline: {e}")
        logger.error(f"Failed to load BioBERT NER pipeline: {e}")
        st.stop()

ner_pipeline = load_biobert_ner_pipeline()
st.sidebar.success("BioBERT NER model loaded successfully!")

# -------------------- Load SpaCy Model -------------------- #

@st.cache_resource
def load_spacy_model():
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
known_symptoms = df_disease_symptom['SymptomName'].unique()

# -------------------- Define Follow-Up Questions -------------------- #

symptom_followup_questions = {
    "Fever": [
        {"hi": "क्या आपकी बुखार लगातार है या बार-बार आती है?", "en": "Is your fever constant or intermittent?", "category": "fever_type"},
        {"hi": "क्या आपने अपने बुखार के लिए कोई दवा ली है?", "en": "Have you taken any medication for your fever?", "category": "medications"},
        {"hi": "क्या आप ठंडक महसूस कर रहे हैं?", "en": "Are you experiencing any chills?", "category": "chills"},
        {"hi": "क्या आपने हाल ही में किसी उच्च जोखिम वाले क्षेत्र की यात्रा की है?", "en": "Have you recently traveled to any high-risk areas?", "category": "travel_history"},
        {"hi": "क्या आपको सिरदर्द हो रहा है?", "en": "Are you experiencing headaches?", "category": "headache"}
    ],
    "Cough": [
        {"hi": "क्या आपका खांसी सूखी है या कफ के साथ है?", "en": "Is your cough dry or productive with phlegm?", "category": "cough_type"},
        {"hi": "क्या आपके खांसी के साथ बुखार है?", "en": "Do you have a fever along with your cough?", "category": "fever"},
        {"hi": "क्या आप सांस लेने में कठिनाई महसूस करते हैं?", "en": "Are you experiencing difficulty breathing?", "category": "breathing"},
        {"hi": "क्या आपने किसी धुएँ या प्रदूषण के संपर्क में आए हैं?", "en": "Have you been exposed to smoke or pollution?", "category": "exposure"},
        {"hi": "क्या आपकी खांसी रात में ज्यादा होती है?", "en": "Does your cough worsen at night?", "category": "time"}
    ],
    # Add more symptoms and their corresponding follow-up questions as needed
}

additional_followup_questions = [
    {"hi": "आपकी उम्र क्या है?", "en": "What is your age?", "category": "age"},
    {"hi": "आपका लिंग क्या है?", "en": "What is your gender?", "category": "gender"},
    {"hi": "आप वर्तमान में कहां स्थित हैं?", "en": "Where are you currently located?", "category": "location"},
    {"hi": "क्या आप कोई अन्य लक्षण महसूस कर रहे हैं?", "en": "Are you experiencing any other symptoms?", "category": "other_symptoms"},
    {"hi": "लक्षण कब से हैं?", "en": "How long have you had these symptoms?", "category": "duration"}
]

# -------------------- Core Functions -------------------- #

def save_audio_file(audio_bytes, file_extension):
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
    try:
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
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Audio file {file_path} deleted successfully after transcription.")
            except Exception as e:
                st.warning(f"Could not delete audio file {file_path}: {e}")
                logger.warning(f"Could not delete audio file {file_path}: {e}")

def generate_audio(text, lang='hi'):
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

def embed_audio_autoplay(audio_bytes):
    audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

def extract_symptoms(text):
    try:
        entities = ner_pipeline(text)
        if not entities:
            logger.info("No entities extracted by BioBERT NER.")
            return set()

        symptoms = set()
        for ent in entities:
            if ent['entity_group'] == 'SYMPTOM':
                symptoms.add(ent['word'].title())

        logger.info(f"Extracted Symptoms: {symptoms}")
        return symptoms
    except Exception as e:
        st.error(f"An error occurred during symptom extraction: {e}")
        logger.error(f"Symptom extraction error: {e}")
        return set()

def match_symptoms(extracted_symptoms):
    matched_symptoms = set()
    for symptom in extracted_symptoms:
        match = process.extractOne(symptom, known_symptoms, scorer=fuzz.WRatio, score_cutoff=80)
        if match:
            matched_symptoms.add(match[0])
    logger.info(f"Matched Symptoms: {matched_symptoms}")
    return matched_symptoms

def extract_additional_entities(text):
    doc = nlp(text)
    age = None
    gender = None
    location = None
    duration = None
    medications = []

    # Medications list (extend as needed)
    medications_list = ["ibuprofen", "dolo650", "paracetamol", "aspirin", "acetaminophen", "amoxicillin", "antibiotic", "metformin", "lisinopril", "atorvastatin"]
    tokens = [token.text.lower() for token in doc]
    for med in medications_list:
        if med.lower() in tokens:
            medications.append(med.title())
    medications = list(set(medications))  # remove duplicates

    # Extract age
    age_patterns = [
        r'(\b\d{1,3}\b)\s*(years old|year old|y/o|yo|yrs old|yrs|years)',
        r'age\s*(\b\d{1,3}\b)',
        r'i am\s*(\b\d{1,3}\b)',
        r'my age is\s*(\b\d{1,3}\b)',
        r'(\b\d{1,3}\b)\s*(male|female)'
    ]
    for pattern in age_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            age_candidate = match.group(1)
            try:
                age = int(age_candidate)
                break
            except ValueError:
                continue

    # Extract gender
    gender_keywords = {'male', 'female', 'man', 'woman', 'boy', 'girl'}
    for token in doc:
        if token.text.lower() in gender_keywords:
            gender = token.text.lower()
            break

    # Extract location
    for ent in doc.ents:
        if ent.label_ == 'GPE' or ent.label_ == 'LOC':
            location = ent.text
            break

    # Extract duration
    duration_patterns = [
        r'(since|for|from)\s+(\d+\s+(day|days|week|weeks|month|months|year|years))',
        r'(\d+\s+(day|days|week|weeks|month|months|year|years))\s+(ago|back)'
    ]
    for pattern in duration_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            duration = match.group(2)
            break
    if not duration:
        # Try to extract DATE entities
        for ent in doc.ents:
            if ent.label_ == 'DATE':
                duration = ent.text
                break

    logger.info(f"Extracted Entities: Age={age}, Gender={gender}, Location={location}, Duration={duration}, Medications={medications}")
    return {
        'age': age,
        'gender': gender,
        'location': location,
        'duration': duration,
        'medications': medications
    }

def determine_followup_questions(matched_symptoms, additional_info):
    followup_questions = []
    asked_categories = set()

    # Determine questions based on matched symptoms
    for symptom in matched_symptoms:
        if symptom in symptom_followup_questions:
            for q in symptom_followup_questions[symptom]:
                category = q.get('category')
                if category not in asked_categories and len(followup_questions) < 5:
                    # Skip questions if the information is already provided
                    if category == 'medications' and additional_info.get('medications'):
                        continue
                    if category == 'duration' and additional_info.get('duration'):
                        continue
                    if category == 'age' and additional_info.get('age'):
                        continue
                    if category == 'gender' and additional_info.get('gender'):
                        continue
                    followup_questions.append(q)
                    asked_categories.add(category)
                if len(followup_questions) >= 5:
                    break
        if len(followup_questions) >= 5:
            break

    # Add additional follow-up questions if needed
    for q in additional_followup_questions:
        category = q.get('category')
        if category in additional_info and additional_info[category]:
            continue  # Skip if info already provided
        if category in asked_categories:
            continue  # Skip if already asked
        if len(followup_questions) >= 5:
            break
        followup_questions.append(q)
        asked_categories.add(category)

    logger.info(f"Determined Follow-Up Questions: {followup_questions}")
    return followup_questions

def extract_and_prepare_questions(conversation_history):
    matched_symptoms, additional_info = extract_all_symptoms(conversation_history)
    st.session_state.additional_info = additional_info  # Store in session state for access elsewhere
    followup_questions = determine_followup_questions(matched_symptoms, additional_info)
    return followup_questions

def extract_all_symptoms(conversation_history):
    matched_symptoms = set()
    additional_info = {
        'age': None,
        'gender': None,
        'location': None,
        'duration': None,
        'medications': []
    }

    for entry in conversation_history:
        if 'user' in entry:
            user_text = entry['user']
            symptoms = extract_symptoms(user_text)
            matched_symptoms.update(match_symptoms(symptoms))
            info = extract_additional_entities(user_text)
            for key in additional_info:
                if key in info and info[key]:
                    if isinstance(info[key], list):
                        additional_info[key].extend(info[key])
                        additional_info[key] = list(set(additional_info[key]))
                    else:
                        additional_info[key] = info[key]
        if 'response' in entry:
            response_text = entry['response']
            symptoms = extract_symptoms(response_text)
            matched_symptoms.update(match_symptoms(symptoms))
            info = extract_additional_entities(response_text)
            for key in additional_info:
                if key in info and info[key]:
                    if isinstance(info[key], list):
                        additional_info[key].extend(info[key])
                        additional_info[key] = list(set(additional_info[key]))
                    else:
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

def generate_report(conversation_history):
    matched_symptoms, additional_info = extract_all_symptoms(conversation_history)
    st.subheader("📄 **Final Report:**")
    st.write("**Symptoms:**", ', '.join(matched_symptoms) if matched_symptoms else 'Not specified')
    if additional_info['age']:
        st.write(f"**Age:** {additional_info['age']} years old")
    if additional_info['gender']:
        st.write(f"**Gender:** {additional_info['gender'].title()}")
    if additional_info['location']:
        st.write(f"**Location:** {additional_info['location']}")
    if additional_info['duration']:
        st.write(f"**Duration of Symptoms:** {additional_info['duration']}")
    if additional_info['medications']:
        st.write(f"**Medications Taken:** {', '.join(additional_info['medications'])}")

    st.subheader("📝 **Transcript of Questions and Answers:**")
    question_count = 1
    for entry in conversation_history:
        if 'followup_question_en' in entry and 'response' in entry:
            st.write(f"**Question {question_count} (English):** {entry['followup_question_en']}")
            st.write(f"**Your Answer:** {entry['response']}")
            st.write("---")
            question_count += 1

# -------------------- Custom CSS for Microphone Button -------------------- #

def inject_custom_css():
    custom_css = """
    <style>
    .custom-mic-button button {
        background-color: #28a745 !important;
        color: white !important;
        font-size: 24px !important;
        width: 120px !important;
        height: 120px !important;
        border-radius: 50% !important;
        border: none !important;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .custom-mic-button button:active {
        background-color: #dc3545 !important;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# -------------------- Streamlit Interface -------------------- #

def main():
    inject_custom_css()

    # Initialize session state variables
    if 'conversation_step' not in st.session_state:
        st.session_state.conversation_step = 0
        st.session_state.conversation_history = []
        st.session_state.report_generated = False
        st.session_state.followup_questions = []
        st.session_state.current_followup = 0
        st.session_state.mic_pressed = False
        st.session_state.waiting_for_response = False
        st.session_state.additional_info = {
            'age': None,
            'gender': None,
            'location': None,
            'duration': None,
            'medications': []
        }

    st.title("🩺 O-Health Diagnostic Tool")
    st.write("""
        Welcome to the O-Health Diagnostic Tool. You can either speak your symptoms in Hindi or type them in English to receive potential disease recommendations based on your inputs.
    """)

    if st.session_state.conversation_step == 0:
        # Play welcome audio
        welcome_text = "ओ-हेल्थ में आपका स्वागत है। कृपया माइक्रोफ़ोन बटन दबाएं और अपने लक्षण बोलें।"
        audio_bytes = generate_audio(welcome_text, lang='hi')
        if audio_bytes:
            embed_audio_autoplay(audio_bytes)
        st.session_state.conversation_step = 1
        st.session_state.waiting_for_response = False
        st.session_state.mic_pressed = False

    # Conversation Step 1: Initial symptom input
    if st.session_state.conversation_step == 1:
        st.header("🗣️ Please Press the Microphone Button and Speak Your Symptoms:")

        if not st.session_state.mic_pressed:
            if st.button("🎤", key="mic_button_initial"):
                st.session_state.mic_pressed = True
        elif st.session_state.mic_pressed:
            # Record audio
            audio_bytes = audio_recorder(key="voice_input_initial")
            if audio_bytes:
                st.audio(audio_bytes, format="audio/wav")
                file_name = save_audio_file(audio_bytes, "wav")
                if file_name:
                    st.success("Audio recorded and saved successfully!")
                    st.info("Transcribing your audio... Please wait.")
                    transcribed_text = transcribe_audio(file_name)
                    if transcribed_text:
                        st.subheader("📝 Transcribed Text (English):")
                        st.write(transcribed_text)
                        st.session_state.conversation_history.append({
                            'user': transcribed_text
                        })
                        st.session_state.followup_questions = extract_and_prepare_questions(st.session_state.conversation_history)
                        st.session_state.mic_pressed = False  # Reset mic_pressed for next use
                        st.session_state.current_followup = 0
                        st.session_state.conversation_step = 2  # Proceed to follow-up questions
                        st.experimental_rerun()
                    else:
                        st.error("Failed to transcribe the audio.")
                        st.session_state.mic_pressed = False

    # Conversation Step 2: Follow-up questions
    if st.session_state.conversation_step == 2:
        total_questions = len(st.session_state.followup_questions)
        if st.session_state.current_followup < total_questions:
            current_question = st.session_state.followup_questions[st.session_state.current_followup]
            if not st.session_state.waiting_for_response:
                # Play question audio
                question_audio = generate_audio(current_question['hi'], lang='hi')
                if question_audio:
                    embed_audio_autoplay(question_audio)
                st.subheader(f"🔍 Follow-Up Question {st.session_state.current_followup + 1} of {total_questions}:")
                st.write(f"**Hindi:** {current_question['hi']}")
                st.write(f"**English:** {current_question['en']}")
                st.session_state.waiting_for_response = True
            else:
                st.header("🗣️ Please Press the Microphone Button and Speak Your Answer:")
                if not st.session_state.mic_pressed:
                    if st.button("🎤", key=f"mic_button_followup_{st.session_state.current_followup}"):
                        st.session_state.mic_pressed = True
                elif st.session_state.mic_pressed:
                    # Record response
                    response_audio_bytes = audio_recorder(key=f"response_voice_input_{st.session_state.current_followup}")
                    if response_audio_bytes:
                        st.audio(response_audio_bytes, format="audio/wav")
                        response_file_name = save_audio_file(response_audio_bytes, "wav")
                        if response_file_name:
                            st.success("Audio recorded and saved successfully!")
                            st.info("Transcribing your audio... Please wait.")
                            response_transcribed = transcribe_audio(response_file_name)
                            if response_transcribed:
                                st.subheader(f"📝 Response to Follow-Up Question {st.session_state.current_followup + 1} (English):")
                                st.write(response_transcribed)
                                st.session_state.conversation_history.append({
                                    'followup_question_en': current_question['en'],
                                    'response': response_transcribed
                                })
                                # Process the response (e.g., extract symptoms)
                                new_symptoms = extract_symptoms(response_transcribed)
                                matched_new_symptoms = match_symptoms(new_symptoms)
                                if matched_new_symptoms:
                                    st.session_state.conversation_history.append({
                                        'additional_symptoms': list(matched_new_symptoms)
                                    })
                                # Also extract additional entities from the response
                                info = extract_additional_entities(response_transcribed)
                                # Update additional_info in session_state
                                for key, value in info.items():
                                    if value:
                                        if isinstance(value, list):
                                            st.session_state.additional_info[key].extend(value)
                                            st.session_state.additional_info[key] = list(set(st.session_state.additional_info[key]))
                                        else:
                                            st.session_state.additional_info[key] = value
                                st.session_state.current_followup += 1
                                st.session_state.mic_pressed = False
                                st.session_state.waiting_for_response = False
                                st.experimental_rerun()
                            else:
                                st.error("Failed to transcribe your audio response.")
                                st.session_state.mic_pressed = False
                    else:
                        st.error("No audio recorded. Please try again.")
                        st.session_state.mic_pressed = False
        else:
            # All follow-up questions have been asked
            st.session_state.conversation_step = 3
            st.experimental_rerun()

    # Conversation Step 3: Generate Report
    if st.session_state.conversation_step == 3 and not st.session_state.report_generated:
        st.session_state.report_generated = True
        with st.spinner("Analyzing your information..."):
            generate_report(st.session_state.conversation_history)

    # Display conversation logs on the sidebar
    with st.sidebar:
        st.header("📝 Conversation Log")
        for idx, entry in enumerate(st.session_state.conversation_history):
            if 'user' in entry:
                st.write(f"**User Input:** {entry['user']}")
            if 'followup_question_en' in entry:
                st.write(f"**Question {idx+1}:** {entry['followup_question_en']}")
                st.write(f"**Answer:** {entry['response']}")
            if 'additional_symptoms' in entry:
                st.write(f"**Additional Symptoms Extracted:** {', '.join(entry['additional_symptoms'])}")
        # Display extracted information
        matched_symptoms, additional_info = extract_all_symptoms(st.session_state.conversation_history)
        st.write("**Extracted Information:**")
        st.write(f"**Symptoms:** {', '.join(matched_symptoms) if matched_symptoms else 'Not specified'}")
        if additional_info['age']:
            st.write(f"**Age:** {additional_info['age']} years old")
        if additional_info['gender']:
            st.write(f"**Gender:** {additional_info['gender'].title()}")
        if additional_info['location']:
            st.write(f"**Location:** {additional_info['location']}")
        if additional_info['duration']:
            st.write(f"**Duration:** {additional_info['duration']}")
        if additional_info['medications']:
            st.write(f"**Medications Taken:** {', '.join(additional_info['medications'])}")

if __name__ == "__main__":
    main()
