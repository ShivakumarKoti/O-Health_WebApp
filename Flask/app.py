from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import datetime
import pandas as pd
import torch
import spacy
import re
import logging
from gtts import gTTS
import io
import openai
import base64
import random
import requests
import zipfile
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import uuid

# -------------------- Environment Setup -------------------- #

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "123456789"  # Replace with a secure key

# Set the OpenAI API key from environment variable
openai.api_key = "OPEN-API-KEY"

if not openai.api_key:
    raise Exception("OpenAI API key not found. Please set it as an environment variable 'OPENAI_API_KEY'.")

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- Load BioBERT NER Model -------------------- #

# URL to your BioBERT NER model zip file hosted externally
BIOBERT_MODEL_URL = "https://www.dropbox.com/s/bsphlpwlt7jclb9/medical-bert-symptom-ner.zip?dl=1"

# Path to the BioBERT model directory
BIOBERT_MODEL_DIR = 'medical-bert-symptom-ner'  # Path where the model will be extracted

def download_and_unzip_biobert_model(model_url, model_dir):
    if not os.path.exists(model_dir):
        print("Downloading the BioBERT NER model. Please wait...")
        # Download the model zip file
        try:
            response = requests.get(model_url, stream=True)
            response.raise_for_status()
            with open('biobert_model.zip', 'wb') as out_file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        out_file.write(chunk)
            logger.info("BioBERT NER model downloaded successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download the BioBERT NER model: {e}")
            logger.error(f"Failed to download the BioBERT NER model: {e}")
            raise e
        # Unzip the model
        try:
            with zipfile.ZipFile('biobert_model.zip', 'r') as zip_ref:
                zip_ref.extractall('.')
            print("BioBERT NER model downloaded and extracted successfully.")
            logger.info("BioBERT NER model extracted successfully.")
        except zipfile.BadZipFile as e:
            print("Downloaded BioBERT model file is not a valid zip file.")
            logger.error(f"Invalid zip file: {e}")
            raise e
        finally:
            # Remove the zip file if it exists
            if os.path.exists('biobert_model.zip'):
                try:
                    os.remove('biobert_model.zip')
                    logger.info("biobert_model.zip removed successfully.")
                except Exception as e:
                    print(f"Could not remove biobert_model.zip: {e}")
                    logger.warning(f"Could not remove biobert_model.zip: {e}")

# Download and unzip the BioBERT model if it doesn't exist
download_and_unzip_biobert_model(BIOBERT_MODEL_URL, BIOBERT_MODEL_DIR)

# Check if the BioBERT model directory exists after extraction
if not os.path.exists(BIOBERT_MODEL_DIR):
    raise Exception(f"BioBERT model directory '{BIOBERT_MODEL_DIR}' not found after extraction.")

# Load the tokenizer and model
def load_biobert_ner_pipeline():
    try:
        from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
        tokenizer = AutoTokenizer.from_pretrained(BIOBERT_MODEL_DIR, add_prefix_space=True)
        model = AutoModelForTokenClassification.from_pretrained(BIOBERT_MODEL_DIR)
        device = 0 if torch.cuda.is_available() else -1
        ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple", device=device)
        logger.info("BioBERT NER pipeline loaded successfully.")
        return ner_pipeline
    except Exception as e:
        print(f"Failed to load BioBERT NER pipeline: {e}")
        logger.error(f"Failed to load BioBERT NER pipeline: {e}")
        raise e

ner_pipeline = load_biobert_ner_pipeline()
print("BioBERT NER model loaded successfully!")

# -------------------- Load SpaCy Model -------------------- #

def load_spacy_model():
    """
    Load the SpaCy model for additional NLP tasks.
    """
    try:
        nlp = spacy.load('en_core_web_sm')
        logger.info("SpaCy model 'en_core_web_sm' loaded successfully.")
        return nlp
    except OSError as e:
        print("SpaCy model 'en_core_web_sm' not found. Please install it using 'python -m spacy download en_core_web_sm'.")
        logger.error(f"SpaCy model loading error: {e}")
        raise e

nlp = load_spacy_model()

# -------------------- Load Disease-Symptom Mapping -------------------- #

def load_disease_symptom_mapping():
    """
    Load the disease-symptom mapping from a CSV file.
    """
    if not os.path.exists("disease_symptom_mapping.csv"):
        print("'disease_symptom_mapping.csv' not found in the current directory.")
        logger.error("'disease_symptom_mapping.csv' not found.")
        raise FileNotFoundError("'disease_symptom_mapping.csv' not found.")
    try:
        df = pd.read_csv("disease_symptom_mapping.csv")
        logger.info("'disease_symptom_mapping.csv' loaded successfully.")
        return df
    except Exception as e:
        print(f"Failed to load 'disease_symptom_mapping.csv': {e}")
        logger.error(f"Failed to load 'disease_symptom_mapping.csv': {e}")
        raise e

df_disease_symptom = load_disease_symptom_mapping()

# Prepare a list of known symptoms
known_symptoms = df_disease_symptom['SymptomName'].unique()

# -------------------- Define Symptom and Medication Lists -------------------- #

# Expanded symptom list with more symptoms and variations
symptom_list = [
    'fever', 'cough', 'headache', 'nausea', 'abdominal pain', 'chills',
    'vomiting', 'diarrhea', 'fatigue', 'shortness of breath', 'sore throat',
    'runny nose', 'sneezing', 'rash', 'dizziness', 'weakness', 'loss of appetite',
    'muscle pain', 'joint pain', 'chest pain', 'back pain', 'constipation',
    'throat pain', 'cold', 'flu', 'breathlessness', 'stomach ache', 'migraine',
    'pain', 'ache', 'sore', 'burning', 'itching', 'swelling', 'infection',
    'inflammation', 'cramps', 'ulcers', 'bleeding', 'irritation', 'anxiety',
    'depression', 'insomnia', 'cancer', 'diabetes', 'hypertension', 'allergies',
    'weight loss', 'weight gain', 'hair loss', 'blurred vision', 'ear pain',
    'palpitations', 'urinary frequency', 'urinary urgency', 'numbness', 'tingling',
    'night sweats', 'dry mouth', 'excessive thirst', 'frequent urination',
    'acne', 'bruising', 'confusion', 'memory loss', 'hoarseness', 'wheezing',
    'itchy eyes', 'dry eyes', 'difficulty swallowing', 'difficulty sleeping',
    'restlessness', 'yellow skin', 'yellow eyes', 'bloating', 'gas', 'hiccups',
    'indigestion', 'heartburn', 'mouth sores', 'nosebleeds', 'ear ringing',
    'decreased appetite', 'increased appetite', 'feeling full quickly',
    'unusual sweating', 'dark urine', 'light-colored stools', 'blood in urine',
    'blood in stool', 'frequent infections', 'delayed healing',
    'high temperature', 'high blood pressure', 'low blood pressure',
    # Add more symptoms and their variations as needed
]

# Expanded medications list
medications_list = [
    "ibuprofen", "dolo650", "paracetamol", "aspirin", "acetaminophen",
    "amoxicillin", "antibiotic", "metformin", "lisinopril", "atorvastatin",
    "cetirizine", "azithromycin", "hydrochlorothiazide", "omeprazole",
    "sertraline", "naproxen", "albuterol", "simvastatin", "loratadine",
    "furosemide", "clopidogrel", "prednisone", "insulin", "levothyroxine",
    "gabapentin", "citalopram", "hydrocodone", "codeine", "tramadol",
    "doxycycline", "ciprofloxacin", "lorazepam", "diazepam", "clonazepam",
    "pantoprazole", "escitalopram", "rosuvastatin", "omeprazole", "esomeprazole",
    "tamsulosin", "atenolol", "amlodipine", "sildenafil", "tadalafil",
    "clindamycin", "metronidazole", "acetylsalicylic acid", "nifedipine",
    "warfarin", "heparin", "digoxin", "fexofenadine", "salbutamol",
    "montelukast", "levocetirizine", "betahistine", "melatonin", "zinc",
    "vitamin c", "vitamin d", "multivitamin", "antacid", "antidepressant",
    # Add more medications as needed
]

# -------------------- Symptom Follow-Up Questions -------------------- #

# Define symptom-specific follow-up questions with associated symptoms
symptom_followup_questions = {
    "Fever": [
        {"hi": "क्या आपका बुखार लगातार है या बीच-बीच में आता है?", "en": "Is your fever constant or intermittent?", "category": "fever_type", "symptom": None},
        {"hi": "क्या आपको ठंड लग रही है?", "en": "Are you experiencing any chills?", "category": "chills", "symptom": "Chills"},
        {"hi": "क्या आपने कोई दवा ली है?", "en": "Have you taken any medication?", "category": "medications", "symptom": None},
        {"hi": "क्या आपको सिरदर्द है?", "en": "Are you experiencing headaches?", "category": "headache", "symptom": "Headache"},
        {"hi": "क्या आपको उल्टी जैसा महसूस हो रहा है?", "en": "Are you feeling nauseous?", "category": "nausea", "symptom": "Nausea"},
        {"hi": "क्या आपका तापमान सामान्य से अधिक है?", "en": "Is your temperature higher than normal?", "category": "high_temperature", "symptom": "High temperature"},
        {"hi": "क्या आपको रात में पसीना आता है?", "en": "Do you experience night sweats?", "category": "night_sweats", "symptom": "Night sweats"},
        {"hi": "क्या आपको भूख कम लग रही है?", "en": "Are you experiencing loss of appetite?", "category": "loss_of_appetite", "symptom": "Loss of appetite"},
    ],
    "Cough": [
        {"hi": "क्या आपकी खांसी सूखी है या बलगम के साथ?", "en": "Is your cough dry or with phlegm?", "category": "cough_type", "symptom": None},
        {"hi": "क्या आपके खांसी के साथ बुखार है?", "en": "Do you have a fever along with your cough?", "category": "fever", "symptom": "Fever"},
        {"hi": "क्या आपको सांस लेने में कठिनाई हो रही है?", "en": "Are you experiencing difficulty breathing?", "category": "breathing", "symptom": "Shortness of breath"},
        {"hi": "क्या आपकी खांसी रात में बढ़ जाती है?", "en": "Does your cough worsen at night?", "category": "time", "symptom": None},
        {"hi": "क्या आपको सीने में दर्द है?", "en": "Are you experiencing chest pain?", "category": "chest_pain", "symptom": "Chest pain"},
        {"hi": "क्या आपको गले में खराश है?", "en": "Do you have a sore throat?", "category": "sore_throat", "symptom": "Sore throat"},
        {"hi": "क्या आपकी आवाज़ बदल गई है?", "en": "Has your voice changed?", "category": "voice_change", "symptom": "Hoarseness"},
        {"hi": "क्या आपको सांस लेने में सीटी जैसी आवाज़ आती है?", "en": "Do you experience wheezing?", "category": "wheezing", "symptom": "Wheezing"},
    ],
    "Abdominal Pain": [
        {"hi": "क्या दर्द पेट के ऊपरी हिस्से में है?", "en": "Is the pain in the upper abdomen?", "category": "upper_abdomen", "symptom": None},
        {"hi": "क्या दर्द पेट के निचले हिस्से में है?", "en": "Is the pain in the lower abdomen?", "category": "lower_abdomen", "symptom": None},
        {"hi": "क्या आपको उल्टी या मिचली हो रही है?", "en": "Are you experiencing vomiting or nausea?", "category": "nausea_vomiting", "symptom": "Nausea"},
        {"hi": "क्या आपको दस्त या कब्ज है?", "en": "Do you have diarrhea or constipation?", "category": "bowel_changes", "symptom": "Diarrhea"},
        {"hi": "क्या आपको पेट फूलना महसूस हो रहा है?", "en": "Are you feeling bloated?", "category": "bloating", "symptom": "Bloating"},
        {"hi": "क्या आपको खाना खाने के बाद दर्द बढ़ जाता है?", "en": "Does the pain increase after eating?", "category": "pain_after_eating", "symptom": None},
        {"hi": "क्या आपको एसिडिटी या जलन महसूस हो रही है?", "en": "Are you experiencing acidity or burning sensation?", "category": "acidity", "symptom": "Heartburn"},
        {"hi": "क्या आपको पेशाब में कोई समस्या है?", "en": "Do you have any problems with urination?", "category": "urination_issues", "symptom": None},
    ],
    "Stomach Ache": [
        {"hi": "क्या दर्द पेट के बीच में है?", "en": "Is the pain in the middle of your stomach?", "category": "middle_abdomen", "symptom": None},
        {"hi": "क्या आपको खाना नहीं पच रहा है?", "en": "Are you experiencing indigestion?", "category": "indigestion", "symptom": "Indigestion"},
        {"hi": "क्या आपको बुखार के साथ पेट दर्द है?", "en": "Do you have fever along with stomach ache?", "category": "fever", "symptom": "Fever"},
        {"hi": "क्या आपको पेट में ऐंठन हो रही है?", "en": "Are you experiencing cramps?", "category": "cramps", "symptom": "Cramps"},
        # Add more questions as needed
    ],
    # Add more symptom categories as needed
}

# Additional general follow-up questions
additional_followup_questions = [
    {"hi": "आपकी उम्र क्या है?", "en": "What is your age?", "category": "age", "symptom": None},
    {"hi": "आपका लिंग क्या है?", "en": "What is your gender?", "category": "gender", "symptom": None},
    {"hi": "आप वर्तमान में कहां स्थित हैं?", "en": "Where are you currently located?", "category": "location", "symptom": None},
    {"hi": "लक्षण कब से हैं?", "en": "How long have you had these symptoms?", "category": "duration", "symptom": None},
    {"hi": "क्या आप कोई अन्य लक्षण महसूस कर रहे हैं?", "en": "Are you experiencing any other symptoms?", "category": "other_symptoms", "symptom": None}
]

# -------------------- Core Functions -------------------- #

def generate_audio(text: str, lang: str = 'en') -> bytes:
    """
    Generate speech audio from text using gTTS and return it as bytes.
    """
    try:
        tts = gTTS(text=text, lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_bytes = fp.read()
        logger.info("Audio generated successfully.")
        return audio_bytes
    except Exception as e:
        logger.error(f"Failed to generate audio: {e}")
        return None

def save_audio_file(audio_bytes, file_extension):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"audio_{timestamp}_{uuid.uuid4().hex}.{file_extension}"
    file_path = os.path.join('static', 'audio', file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        with open(file_path, "wb") as f:
            f.write(audio_bytes)
        logger.info(f"Audio saved as {file_name}")
        return file_path
    except Exception as e:
        logger.error(f"Failed to save audio file: {e}")
        return None

def transcribe_audio(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            transcript = openai.Audio.translate("whisper-1", audio_file)
            transcribed_text = transcript.get("text", "").strip()
            logger.info(f"Audio transcription successful: {transcribed_text}")
            return transcribed_text
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        return None
    finally:
        # Optionally delete the file
        pass

def extract_symptoms(text):
    try:
        # Use BioBERT NER model to extract symptoms
        ner_results = ner_pipeline(text)
        extracted_symptoms = set()
        for entity in ner_results:
            if entity['entity_group'] == 'SYMPTOM':
                symptom = entity['word'].strip()
                extracted_symptoms.add(symptom.title())
        logger.info(f"Extracted Symptoms using BioBERT: {extracted_symptoms}")

        # Also match against symptom list for any missed symptoms
        text_lower = text.lower()
        for symptom in symptom_list:
            symptom_lower = symptom.lower()
            if re.search(r'\b' + re.escape(symptom_lower) + r'\b', text_lower):
                extracted_symptoms.add(symptom.title())

        logger.info(f"Final Extracted Symptoms: {extracted_symptoms}")
        return extracted_symptoms
    except Exception as e:
        logger.error(f"Symptom extraction error: {e}")
        return set()

def extract_additional_entities(text):
    doc = nlp(text)
    age = None
    gender = None
    location = None
    duration = None
    medications = []

    # Medications list
    tokens = [token.text.lower() for token in doc]
    for med in medications_list:
        if med.lower() in tokens:
            medications.append(med.title())
    medications = list(set(medications))  # remove duplicates

    # Extract age
    age_patterns = [
        r'(?i)\b(?:i am|i\'m|my age is|age)\s*(\d{1,3})\b',
        r'\b(\d{1,3})\s*(?:years old|year old|y/o|yo|yrs old|yrs|years)\b',
        r'\b(\d{1,3})\s*(?:male|female|man|woman|boy|girl)\b'
    ]
    for pattern in age_patterns:
        match = re.search(pattern, text)
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
        r'(?i)\b(?:for|since|from|past)\s+(?:the\s+)?(?:past\s+)?(\w+\s+(?:day|days|week|weeks|month|months|year|years))\b',
        r'\b(\w+\s+(?:day|days|week|weeks|month|months|year|years))\s+(?:ago|back)\b'
    ]
    for pattern in duration_patterns:
        match = re.search(pattern, text)
        if match:
            duration_candidate = match.group(1)
            duration = duration_candidate.strip()
            break
    if not duration:
        # Try to extract DATE entities
        for ent in doc.ents:
            if ent.label_ == 'DATE':
                duration = ent.text
                break

    # Ensure that duration is not misassigned from age
    if age and duration and str(age) in duration:
        duration = None

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

    # Collect all possible questions for matched symptoms
    all_possible_questions = []
    for symptom in matched_symptoms:
        if symptom in symptom_followup_questions:
            symptom_questions = symptom_followup_questions[symptom]
            all_possible_questions.extend(symptom_questions)

    # Add additional follow-up questions
    all_possible_questions.extend(additional_followup_questions)

    # Remove duplicate questions based on 'category'
    unique_questions = {}
    for q in all_possible_questions:
        category = q.get('category')
        if category not in unique_questions and category not in asked_categories:
            unique_questions[category] = q

    all_possible_questions = list(unique_questions.values())

    # Randomly select up to 5 questions
    num_questions_to_ask = min(len(all_possible_questions), 5)
    selected_questions = random.sample(all_possible_questions, num_questions_to_ask)

    # Build the follow-up questions list
    for q in selected_questions:
        category = q.get('category')
        if category not in asked_categories:
            # Skip questions if the information is already provided
            if category in additional_info and additional_info.get(category):
                continue
            followup_questions.append(q)
            asked_categories.add(category)
        if len(followup_questions) >= 5:
            break

    logger.info(f"Determined Follow-Up Questions: {followup_questions}")
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

    affirmative_responses = {'yes', 'yeah', 'yep', 'yup', 'sure', 'of course', 'definitely', 'haan', 'ha'}
    negative_responses = {'no', 'nah', 'nope', 'not really', 'don\'t', 'nahi'}

    for entry in conversation_history:
        if 'user' in entry:
            user_text = entry['user']
            symptoms = extract_symptoms(user_text)
            matched_symptoms.update(symptoms)
            info = extract_additional_entities(user_text)
            for key in additional_info:
                if key in info and info[key]:
                    if isinstance(info[key], list):
                        additional_info[key].extend(info[key])
                        additional_info[key] = list(set(additional_info[key]))
                    else:
                        additional_info[key] = info[key]
        if 'followup_question_en' in entry:
            response_text = entry['response']
            symptoms = extract_symptoms(response_text)
            matched_symptoms.update(symptoms)
            info = extract_additional_entities(response_text)
            for key in additional_info:
                if key in info and info[key]:
                    if isinstance(info[key], list):
                        additional_info[key].extend(info[key])
                        additional_info[key] = list(set(additional_info[key]))
                    else:
                        additional_info[key] = info[key]

            # Infer symptoms from Yes/No answers to symptom-related questions
            question_entry = entry
            question_text = question_entry['followup_question_en']
            response_text_lower = response_text.strip().lower()

            # Check if response is affirmative
            is_affirmative = response_text_lower in affirmative_responses

            # Get the 'symptom' associated with the question
            symptom = None
            for symptom_category in symptom_followup_questions.values():
                for q in symptom_category:
                    if q['en'] == question_text:
                        symptom = q.get('symptom')
                        break
                if symptom:
                    break

            if symptom and is_affirmative:
                matched_symptoms.add(symptom)
            elif symptom and response_text_lower in negative_responses:
                # Optionally, you can handle negative responses if needed
                pass

    logger.info(f"Final Matched Symptoms: {matched_symptoms}")
    logger.info(f"Additional Information: {additional_info}")
    return matched_symptoms, additional_info

def map_symptoms_to_diseases(matched_symptoms, additional_info):
    """
    Map the matched symptoms to probable diseases based on the disease-symptom mapping.

    Args:
        matched_symptoms (set): A set of matched symptoms.
        additional_info (dict): A dictionary containing additional extracted information.

    Returns:
        dict: A dictionary of probable diseases with their respective probabilities.
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
            if disease == 'Altitude Sickness' and 'mountain' in additional_info['location'].lower():
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
            return sorted_diseases
    else:
        return {}

def generate_report(conversation_history):
    matched_symptoms, additional_info = extract_all_symptoms(conversation_history)
    report = {}
    report['symptoms'] = ', '.join(matched_symptoms) if matched_symptoms else 'Not specified'
    report['age'] = f"{additional_info['age']} years old" if additional_info['age'] else None
    report['gender'] = additional_info['gender'].title() if additional_info['gender'] else None
    report['location'] = additional_info['location'] if additional_info['location'] else None
    report['duration'] = additional_info['duration'] if additional_info['duration'] else None
    report['medications'] = ', '.join(additional_info['medications']) if additional_info['medications'] else None

    # Map symptoms to diseases
    probable_diseases = map_symptoms_to_diseases(matched_symptoms, additional_info)
    report['probable_diseases'] = probable_diseases

    # Generate plot if diseases are found
    plot_url = None
    if probable_diseases:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=list(probable_diseases.keys()), y=list(probable_diseases.values()), ax=ax)
        ax.set_xlabel("Disease")
        ax.set_ylabel("Probability (%)")
        ax.set_title("Probable Diseases")
        plt.xticks(rotation=45, ha='right')
        # Save plot to static directory
        plot_filename = f"plot_{uuid.uuid4().hex}.png"
        plot_path = os.path.join('static', 'plots', plot_filename)
        os.makedirs(os.path.dirname(plot_path), exist_ok=True)
        plt.savefig(plot_path)
        plot_url = url_for('static', filename=f'plots/{plot_filename}')
        plt.close(fig)

    report['plot_url'] = plot_url

    return report

# -------------------- Flask Routes -------------------- #

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'conversation_history' not in session:
        session['conversation_history'] = []
        session['current_step'] = 1  # 1: Initial Symptom Input, 2: Follow-Up, 3: Report
        session['symptoms_processed'] = False
        session['followup_questions'] = []
        session['current_followup'] = 0

    if request.method == 'POST':
        # Handle symptom input
        user_input = request.form.get('symptoms_text')
        if user_input:
            session['conversation_history'].append({'user': user_input})
            matched_symptoms, additional_info = extract_all_symptoms(session['conversation_history'])
            session['followup_questions'] = determine_followup_questions(matched_symptoms, additional_info)
            session['current_step'] = 2
            return redirect(url_for('followup'))
        else:
            flash("Please enter your symptoms.")
            return redirect(url_for('index'))

    # Generate welcome audio
    welcome_text = "ओ-हेल्थ में आपका स्वागत है। कृपया अपने लक्षण टाइप करें।"
    audio_bytes = generate_audio(welcome_text, lang='hi')
    if audio_bytes:
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    else:
        audio_base64 = None

    return render_template('index.html', audio_base64=audio_base64)

@app.route('/followup', methods=['GET', 'POST'])
def followup():
    if 'conversation_history' not in session or session.get('current_step') != 2:
        return redirect(url_for('index'))

    total_questions = len(session['followup_questions'])
    current_followup = session.get('current_followup', 0)

    if request.method == 'POST':
        # Handle follow-up answer
        answer = request.form.get('answer')
        if answer:
            current_question = session['followup_questions'][current_followup]
            session['conversation_history'].append({
                'followup_question_en': current_question['en'],
                'response': answer
            })
            session['current_followup'] = current_followup + 1
            if session['current_followup'] >= total_questions:
                session['current_step'] = 3
                return redirect(url_for('report'))
            else:
                return redirect(url_for('followup'))
        else:
            flash("Please provide an answer.")
            return redirect(url_for('followup'))

    if current_followup < total_questions:
        current_question = session['followup_questions'][current_followup]
        # Generate question audio
        question_audio = generate_audio(current_question['hi'], lang='hi')
        if question_audio:
            audio_base64 = base64.b64encode(question_audio).decode('utf-8')
        else:
            audio_base64 = None

        return render_template('followup.html', question=current_question, audio_base64=audio_base64, question_number=current_followup + 1, total_questions=total_questions)
    else:
        session['current_step'] = 3
        return redirect(url_for('report'))

@app.route('/report')
def report():
    if 'conversation_history' not in session or session.get('current_step') != 3:
        return redirect(url_for('index'))

    report_data = generate_report(session['conversation_history'])

    return render_template('report.html', report=report_data, conversation_history=session['conversation_history'])

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
