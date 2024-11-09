import os
import io
import re
import datetime
import logging
import base64
import uuid
import zipfile
import requests
import pandas as pd
import torch
import spacy
import matplotlib.pyplot as plt
import seaborn as sns
import openai
from gtts import gTTS
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from googletrans import Translator, LANGUAGES
from textblob import TextBlob
import random
import time
from flask import Flask, render_template, request, redirect, url_for, session, flash

# -------------------- Environment Setup -------------------- #

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

# Securely access the OpenAI API key
openai.api_key = "OPEN-KEY"  # Replace with your actual OpenAI API key

if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please set it in the code.")

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- Define Audio Directory -------------------- #

# Define the path for audio files
AUDIO_FOLDER = os.path.join('static', 'audio')
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

# -------------------- Load BioBERT NER Model -------------------- #

# URL to your BioBERT NER model zip file hosted externally
BIOBERT_MODEL_URL = "https://www.dropbox.com/scl/fi/odjgcsy5i8ktmpbag6p33/medical-bert-symptom-ner.zip?rlkey=j4ekri3mp92341o0wq2plnro6&st=0ucut9k7&dl=1"

# Path to the BioBERT model directory
BIOBERT_MODEL_DIR = 'medical-bert-symptom-ner'  # Path where the model will be extracted

def download_and_unzip_biobert_model(model_url, model_dir):
    if not os.path.exists(model_dir):
        print("Downloading the BioBERT NER model. Please wait...")
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
            exit()
        # Unzip the model
        try:
            with zipfile.ZipFile('biobert_model.zip', 'r') as zip_ref:
                zip_ref.extractall('.')
            print("BioBERT NER model downloaded and extracted successfully.")
            logger.info("BioBERT NER model extracted successfully.")
        except zipfile.BadZipFile as e:
            print("Downloaded BioBERT model file is not a valid zip file.")
            logger.error(f"Invalid zip file: {e}")
            exit()
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
    print(f"BioBERT model directory '{BIOBERT_MODEL_DIR}' not found after extraction.")
    logger.error(f"BioBERT model directory '{BIOBERT_MODEL_DIR}' not found after extraction.")
    exit()

# Load the tokenizer and model
def load_biobert_ner_pipeline():
    try:
        tokenizer = AutoTokenizer.from_pretrained(BIOBERT_MODEL_DIR, add_prefix_space=True)
        model = AutoModelForTokenClassification.from_pretrained(BIOBERT_MODEL_DIR)
        device = 0 if torch.cuda.is_available() else -1
        ner_pipeline_model = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple", device=device)
        logger.info("BioBERT NER pipeline loaded successfully.")
        return ner_pipeline_model
    except Exception as e:
        print(f"Failed to load BioBERT NER pipeline: {e}")
        logger.error(f"Failed to load BioBERT NER pipeline: {e}")
        exit()

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
        exit()

nlp = load_spacy_model()

# -------------------- Load Disease-Symptom Mapping -------------------- #

def load_disease_symptom_mapping():
    """
    Load the disease-symptom mapping from a CSV file.
    """
    if not os.path.exists("disease_symptom_mapping.csv"):
        print("'disease_symptom_mapping.csv' not found in the current directory.")
        logger.error("'disease_symptom_mapping.csv' not found.")
        exit()
    try:
        df = pd.read_csv("disease_symptom_mapping.csv")
        logger.info("'disease_symptom_mapping.csv' loaded successfully.")
        return df
    except Exception as e:
        print(f"Failed to load 'disease_symptom_mapping.csv': {e}")
        logger.error(f"Failed to load 'disease_symptom_mapping.csv': {e}")
        exit()

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
    'high temperature', 'high blood pressure', 'low blood pressure'
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
    "vitamin c", "vitamin d", "multivitamin", "antacid", "antidepressant"
    # Add more medications as needed
]

# Initialize the translator
translator = Translator()

def translate_to_english(text):
    """
    Translate text to English if it's not already in English.
    """
    try:
        detection = translator.detect(text)
        logger.info(f"Detected language: {LANGUAGES.get(detection.lang, 'unknown')} for text: '{text}'")
        if detection.lang != 'en':
            translated = translator.translate(text, dest='en')
            logger.info(f"Translated '{text}' to English: '{translated.text}'")
            return translated.text
        return text
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return text  # Fallback to original text if translation fails

def translate_to_hindi(text):
    """
    Translate text to Hindi.
    """
    try:
        translated = translator.translate(text, dest='hi')
        logger.info(f"Translated to Hindi: '{translated.text}'")
        return translated.text
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return text  # Fallback to original text if translation fails

def extract_symptoms(text):
    """
    Extract symptoms from the given text using BioBERT NER model and regex matching.
    """
    try:
        # Use BioBERT NER model to extract symptoms
        ner_results = ner_pipeline(text)
        extracted_symptoms = set()
        for entity in ner_results:
            if entity['entity_group'] == 'SYMPTOM':
                symptom = entity['word'].strip()
                # Ensure the symptom is in the known_symptoms list
                if symptom.title() in known_symptoms:
                    extracted_symptoms.add(symptom.title())
        logger.info(f"Extracted Symptoms using BioBERT: {extracted_symptoms}")

        # Also match against symptom list for any missed symptoms
        text_lower = text.lower()
        for symptom in symptom_list:
            symptom_lower = symptom.lower()
            if re.search(r'\b' + re.escape(symptom_lower) + r'\b', text_lower):
                extracted_symptoms.add(symptom.title())

        logger.info(f"Final Extracted Symptoms: {extracted_symptoms}")
        extracted_symptoms = [med for med in extracted_symptoms if med not in {'No', 'yes', 'no'}]
        return extracted_symptoms
    except Exception as e:
        logger.error(f"Symptom extraction error: {e}")
        return set()

def generate_tts_audio(text, filename, lang='hi'):
    """
    Generate a TTS audio file using gTTS and save it to the AUDIO_FOLDER.
    Returns the path to the audio file.
    """
    try:
        cleanup_audio_files()  # Clean old files
        tts = gTTS(text=text, lang=lang)
        filepath = os.path.join(AUDIO_FOLDER, filename)
        tts.save(filepath)
        logger.info(f"Generated TTS audio file: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Failed to generate TTS audio: {e}")
        return None

def cleanup_audio_files():
    """
    Remove audio files older than 1 hour from the AUDIO_FOLDER.
    """
    now = time.time()
    cutoff = now - 3600  # 1 hour in seconds
    for filename in os.listdir(AUDIO_FOLDER):
        filepath = os.path.join(AUDIO_FOLDER, filename)
        if os.path.isfile(filepath):
            file_modified = os.path.getmtime(filepath)
            if file_modified < cutoff:
                try:
                    os.remove(filepath)
                    logger.info(f"Deleted old audio file: {filepath}")
                except Exception as e:
                    logger.error(f"Failed to delete {filepath}: {e}")

def extract_possible_causes(text):
    """
    Use OpenAI API to generate a one-sentence overview of the possible cause from the transcript.
    """
    try:
        prompt = f"Based on the following patient transcript, provide a one-sentence possible cause of the symptoms:\n\n{text}\n\nPossible cause:"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides possible causes of medical symptoms based on patient transcripts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.7,
            n=1,
            stop=None,
        )
        cause = response['choices'][0]['message']['content'].strip()
        # Remove any leading prompts like "Possible cause:" if present
        cause = re.sub(r'^Possible cause:\s*', '', cause, flags=re.IGNORECASE)
        logger.info(f"Generated possible cause using OpenAI API: {cause}")
        return cause
    except Exception as e:
        logger.error(f"Failed to generate possible cause using OpenAI API: {e}")
        return "No possible causes determined."

def extract_additional_entities(text):
    """
    Extract additional entities like age, gender, location, duration, and medications from text.
    """
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
    medications = [med for med in medications if med not in {'Yes', 'No'}]

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
        if ent.label_ in ['GPE', 'LOC']:
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

def determine_followup_questions(conversation_history, additional_info):
    """
    Determine the next set of follow-up questions based on matched symptoms and additional information.
    """
    matched_symptoms, _, _ = extract_all_symptoms(conversation_history)
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
    if num_questions_to_ask > 0:
        selected_questions = random.sample(all_possible_questions, num_questions_to_ask)
    else:
        selected_questions = []

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
    """
    Extract all symptoms, additional information, and possible causes from the conversation history.
    Collect all user inputs into a single transcript for cause analysis.
    """
    matched_symptoms = set()
    additional_info = {
        'age': None,
        'gender': None,
        'location': None,
        'duration': None,
        'medications': []
    }
    combined_transcript = ""

    affirmative_responses = {'yes', 'yeah', 'yep', 'yup', 'sure', 'of course', 'definitely', 'haan', 'ha'}
    negative_responses = {'no', 'nah', 'nope', 'not really', "don't", 'nahi'}

    for entry in conversation_history:
        if 'user_input' in entry:
            user_text = entry['user_input']
            combined_transcript += " " + user_text  # Collecting all user inputs
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
            question_text = entry['followup_question_en']
            response_text_lower = response_text.strip().lower()

            # Check if response is affirmative or negative
            is_affirmative = any(word in response_text_lower for word in affirmative_responses)
            is_negative = any(word in response_text_lower for word in negative_responses)

            # Get the 'symptom' associated with the question
            symptom = None
            for symptom_category in symptom_followup_questions.values():
                for q in symptom_category:
                    if q['en'].lower() == question_text.lower():
                        symptom = q.get('symptom')
                        break
                if symptom:
                    break

            if symptom and is_affirmative:
                matched_symptoms.add(symptom)
                combined_transcript += " " + response_text  # Include affirmative response in transcript
            elif symptom and is_negative:
                if symptom in matched_symptoms:
                    matched_symptoms.remove(symptom)
                # Do not include negative responses in transcript for cause analysis
            else:
                combined_transcript += " " + response_text  # Include other responses

            # Extract additional entities from the response
            info = extract_additional_entities(response_text)
            for key in additional_info:
                if key in info and info[key]:
                    if isinstance(info[key], list):
                        additional_info[key].extend(info[key])
                        additional_info[key] = list(set(additional_info[key]))
                    else:
                        additional_info[key] = info[key]

    # Extract possible causes from the combined transcript
    possible_cause = extract_possible_causes(combined_transcript)

    logger.info(f"Final Matched Symptoms: {matched_symptoms}")
    logger.info(f"Additional Information: {additional_info}")
    logger.info(f"Combined Transcript for Cause Analysis: {combined_transcript}")
    logger.info(f"Possible Cause: {possible_cause}")

    return matched_symptoms, additional_info, possible_cause

def map_symptoms_to_diseases(matched_symptoms, additional_info):
    """
    Map the matched symptoms to probable diseases based on the disease-symptom mapping.
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

def handle_yes_no_response(question, response):
    """
    Handles yes/no responses to follow-up questions to add or remove symptoms.

    Args:
        question (dict): The current follow-up question being asked.
        response (str): The user's response to the follow-up question.
    """
    affirmative_responses = {'yes', 'yeah', 'yep', 'yup', 'sure', 'of course', 'definitely', 'haan', 'ha'}
    negative_responses = {'no', 'nah', 'nope', 'not really', "don't", 'nahi'}

    response_lower = response.strip().lower()
    is_affirmative = any(word in response_lower for word in affirmative_responses)
    is_negative = any(word in response_lower for word in negative_responses)

    # Initialize session['matched_symptoms'] if not already
    if 'matched_symptoms' not in session:
        session['matched_symptoms'] = []

    matched_symptoms = set(session['matched_symptoms'])

    if is_affirmative and question['symptom']:
        matched_symptoms.add(question['symptom'])
        logger.info(f"Added symptom '{question['symptom']}' based on affirmative response.")
    elif is_negative and question['symptom']:
        if question['symptom'] in matched_symptoms:
            matched_symptoms.remove(question['symptom'])
            logger.info(f"Removed symptom '{question['symptom']}' based on negative response.")
        else:
            logger.info(f"No action taken for symptom '{question['symptom']}' as it's not present.")
    else:
        logger.info("Response not recognized as yes/no or no associated symptom.")

    session['matched_symptoms'] = list(matched_symptoms)

# -------------------- Flask Routes -------------------- #

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        symptoms = request.form.get('symptoms', '').strip()
        if not symptoms:
            return render_template('home.html', error="कृपया अपने लक्षण दर्ज करें।")  # "Please enter your symptoms."

        # Translate and process input
        translated_input = translate_to_english(symptoms)
        corrected_input = translated_input  # Since 'corrected_input' is disabled

        # Initialize session variables
        session['conversation_history'] = [{'user_input': corrected_input}]
        session['current_step'] = 1
        session['symptoms_processed'] = False

        # Extract additional info
        matched_symptoms, additional_info, _ = extract_all_symptoms(session['conversation_history'])
        session['additional_info'] = additional_info
        session['matched_symptoms'] = list(matched_symptoms)

        # Determine follow-up questions
        followup_questions = determine_followup_questions(session['conversation_history'], additional_info)
        session['followup_questions'] = followup_questions
        session['current_followup'] = 0

        return redirect(url_for('followup'))
    return render_template('home.html')

@app.route('/followup', methods=['GET', 'POST'])
def followup():
    current_followup = session.get('current_followup', 0)
    followup_questions = session.get('followup_questions', [])

    if current_followup >= len(followup_questions):
        return redirect(url_for('report'))

    current_question = followup_questions[current_followup]
    question_number = current_followup + 1
    total_questions = len(followup_questions)

    if request.method == 'POST':
        answer = request.form.get('answer', '').strip()
        if not answer:
            return render_template('followup.html', current_question=current_question,
                                   question_number=question_number, total_questions=total_questions,
                                   error="कृपया अपना उत्तर दें।")  # "Please provide your answer."

        # Process answer
        translated_answer = translate_to_english(answer)
        corrected_answer = translated_answer  # Since 'corrected_input' is disabled

        # Update conversation history
        conversation_history = session.get('conversation_history', [])
        conversation_history.append({
            'followup_question_en': current_question['en'],
            'response': corrected_answer
        })
        session['conversation_history'] = conversation_history

        # Handle yes/no response
        handle_yes_no_response(current_question, corrected_answer)

        # Update matched symptoms
        extracted_symptoms = extract_symptoms(corrected_answer)
        matched_symptoms = set(session.get('matched_symptoms', []))
        matched_symptoms.update(extracted_symptoms)
        session['matched_symptoms'] = list(matched_symptoms)

        # Increment follow-up counter
        session['current_followup'] = current_followup + 1
        return redirect(url_for('followup'))

    return render_template('followup.html', current_question=current_question,
                           question_number=question_number, total_questions=total_questions)

@app.route('/report')
def report():
    conversation_history = session.get('conversation_history', [])
    matched_symptoms, additional_info, possible_cause_en = extract_all_symptoms(conversation_history)

    logger.info(f"Reporting Possible Cause: {possible_cause_en}")  # Ensure it's correctly retrieved

    # Map symptoms to diseases
    probable_diseases = map_symptoms_to_diseases(matched_symptoms, additional_info)

    # Prepare data for template
    symptoms = ', '.join(matched_symptoms) if matched_symptoms else 'Not specified'
    age = additional_info.get('age')
    gender = additional_info.get('gender')
    location = additional_info.get('location')
    duration = additional_info.get('duration')
    medications = ', '.join(additional_info.get('medications', []))

    # Generate TTS audio for possible_cause in Hindi and English
    possible_cause_audio_url_hi = None
    possible_cause_audio_url_en = None
    possible_cause_hindi = ""
    if possible_cause_en and possible_cause_en != "No possible causes determined.":
        # Translate possible_cause back to Hindi
        possible_cause_hindi = translate_to_hindi(possible_cause_en)
        # Create unique filenames
        filename_hi = f"possible_cause_hi_{uuid.uuid4().hex}.mp3"
        filename_en = f"possible_cause_en_{uuid.uuid4().hex}.mp3"
        # Generate Hindi audio
        audio_path_hi = generate_tts_audio(possible_cause_hindi, filename_hi, lang='hi')
        if audio_path_hi:
            possible_cause_audio_url_hi = url_for('static', filename=f'audio/{filename_hi}')
        # Generate English audio
        audio_path_en = generate_tts_audio(possible_cause_en, filename_en, lang='en')
        if audio_path_en:
            possible_cause_audio_url_en = url_for('static', filename=f'audio/{filename_en}')

    return render_template('report.html',
                           symptoms=symptoms,
                           age=age,
                           gender=gender,
                           location=location,
                           duration=duration,
                           medications=medications,
                           possible_cause_en=possible_cause_en,  # English version
                           possible_cause_hi=possible_cause_hindi,  # Hindi version
                           possible_cause_audio_url_hi=possible_cause_audio_url_hi,  # Hindi audio
                           possible_cause_audio_url_en=possible_cause_audio_url_en,  # English audio
                           probable_diseases=probable_diseases,
                           conversation_history=conversation_history)

if __name__ == "__main__":
    app.run(debug=True)
