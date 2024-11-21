# corrected_input is uncommented and disabled
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
import streamlit as st
import streamlit.components.v1 as components
from audio_recorder_streamlit import audio_recorder
import random
import json

API_KEY="AIzaSyASUfCPNIKGs4tvsMkStfeW8wpCKqJmZzY"

# -------------------- Environment Setup -------------------- #

# Securely access the OpenAI API key from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

if not openai.api_key:
    st.error("OpenAI API key not found. Please set it in the Streamlit Secrets.")
    st.stop()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- Load BioBERT NER Model -------------------- #

# URL to your BioBERT NER model zip file hosted externally
BIOBERT_MODEL_URL = "https://www.dropbox.com/scl/fi/odjgcsy5i8ktmpbag6p33/medical-bert-symptom-ner.zip?rlkey=j4ekri3mp92341o0wq2plnro6&st=0ucut9k7&dl=1"

# Path to the BioBERT model directory
BIOBERT_MODEL_DIR = 'medical-bert-symptom-ner'  # Path where the model will be extracted

def download_and_unzip_biobert_model(model_url, model_dir):
    if not os.path.exists(model_dir):
        st.info("Downloading the BioBERT NER model. Please wait...")
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
            # Remove the zip file if it exists
            if os.path.exists('biobert_model.zip'):
                try:
                    os.remove('biobert_model.zip')
                    logger.info("biobert_model.zip removed successfully.")
                except Exception as e:
                    st.warning(f"Could not remove biobert_model.zip: {e}")
                    logger.warning(f"Could not remove biobert_model.zip: {e}")

# Download and unzip the BioBERT model if it doesn't exist
download_and_unzip_biobert_model(BIOBERT_MODEL_URL, BIOBERT_MODEL_DIR)

# Check if the BioBERT model directory exists after extraction
if not os.path.exists(BIOBERT_MODEL_DIR):
    st.error(f"BioBERT model directory '{BIOBERT_MODEL_DIR}' not found after extraction.")
    logger.error(f"BioBERT model directory '{BIOBERT_MODEL_DIR}' not found after extraction.")
    st.stop()

# Load the tokenizer and model using caching
@st.cache_resource
def load_biobert_ner_pipeline():
    try:
        tokenizer = AutoTokenizer.from_pretrained(BIOBERT_MODEL_DIR, add_prefix_space=True)
        model = AutoModelForTokenClassification.from_pretrained(BIOBERT_MODEL_DIR)
        device = 0 if torch.cuda.is_available() else -1
        ner_pipeline_model = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple", device=device)
        logger.info("BioBERT NER pipeline loaded successfully.")
        return ner_pipeline_model
    except Exception as e:
        st.error(f"Failed to load BioBERT NER pipeline: {e}")
        logger.error(f"Failed to load BioBERT NER pipeline: {e}")
        st.stop()

ner_pipeline = load_biobert_ner_pipeline()
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

@st.cache_resource
def load_disease_symptom_mapping():
    """
    Load the disease-symptom mapping from a CSV file.
    """
    if not os.path.exists("disease_symptom_mapping.csv"):
        st.error("'disease_symptom_mapping.csv' not found in the current directory.")
        logger.error("'disease_symptom_mapping.csv' not found.")
        st.stop()
    try:
        df = pd.read_csv("disease_symptom_mapping.csv")
        logger.info("'disease_symptom_mapping.csv' loaded successfully.")
        return df
    except Exception as e:
        st.error(f"Failed to load 'disease_symptom_mapping.csv': {e}")
        logger.error(f"Failed to load 'disease_symptom_mapping.csv': {e}")
        st.stop()

df_disease_symptom = load_disease_symptom_mapping()

# Prepare a list of known symptoms
known_symptoms = df_disease_symptom['SymptomName'].unique()

# -------------------- Define Symptom and Medication Lists -------------------- #


# Load the expanded symptom list from a CSV file
def load_symptom_list(csv_file_path='Extract_Causes/symptom_list_2.csv'):
    """
    Load symptoms from a CSV file into a Python list and mapping.

    Args:
        csv_file_path (str): Path to the CSV file containing symptoms.

    Returns:
        tuple: A tuple containing:
            - symptom_list (list): A list of symptom variants.
            - symptom_to_canonical (dict): A mapping from variant to canonical symptom.
    """
    try:
        df_symptoms = pd.read_csv(csv_file_path)
        # Validate required columns
        if 'SymptomName' not in df_symptoms.columns or 'CanonicalSymptom' not in df_symptoms.columns:
            st.error("CSV file must contain 'SymptomName' and 'CanonicalSymptom' columns.")
            return [], {}
        # Drop rows with missing values
        df_symptoms = df_symptoms.dropna(subset=['SymptomName', 'CanonicalSymptom'])
        # Create the mapping
        symptom_to_canonical = {}
        for _, row in df_symptoms.iterrows():
            variant = row['SymptomName'].strip().lower()
            canonical = row['CanonicalSymptom'].strip().lower()
            symptom_to_canonical[variant] = canonical
        # Create a list of unique variants
        symptom_list = list(symptom_to_canonical.keys())
        st.success(f"Loaded {len(symptom_list)} symptom variants from '{csv_file_path}'.")
        return symptom_list, symptom_to_canonical
    except FileNotFoundError:
        st.error(f"Error: The file '{csv_file_path}' was not found.")
        return [], {}
    except pd.errors.EmptyDataError:
        st.error(f"Error: The file '{csv_file_path}' is empty.")
        return [], {}
    except Exception as e:
        st.error(f"An error occurred while loading symptoms: {e}")
        return [], {}

# Expanded medications list
medications_list = [
    "ibuprofen", "dolo650", "paracetamol", "aspirin", "acetaminophen","Dolo 650",
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
        if detection.lang != 'en':
            translated = translator.translate(text, dest='en')
            logger.info(f"Translated '{text}' from {LANGUAGES.get(detection.lang, 'unknown')} to English: '{translated.text}'")
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
        translated = translator.translate(text, src='en', dest='hi')
        translated_text = translated.text
        logger.info(f"Translated to Hindi: '{translated_text}'")
        return translated_text
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return text

def correct_spelling(text):
    """
    Corrects the spelling of the given text using TextBlob while preserving medical terms.

    Args:
        text (str): The input text to correct.

    Returns:
        str: The spell-corrected text.
    """
    try:
        blob = TextBlob(text)
        corrected_blob = blob.correct()
        corrected_text = str(corrected_blob)

        # Restore medical terms and critical words
        for term in medications_list:
            if term.lower() in corrected_text.lower():
                # Use regex to replace all case-insensitive occurrences with the correct case
                pattern = re.compile(re.escape(term), re.IGNORECASE)
                corrected_text = pattern.sub(term, corrected_text)

        logger.info(f"Spelling corrected: '{text}' -> '{corrected_text}'")
        return corrected_text
    except Exception as e:
        logger.error(f"Spell correction failed: {e}")
        return text  # Return original text if correction fails

# -------------------- Symptom Follow-Up Questions -------------------- #

# Define a mapping from canonical symptoms to their variants
canonical_symptom_mapping = {
    'pain': ['pain', 'back pain', 'abdominal pain', 'chest pain', 'joint pain','stomach pain','stomach ache','stomach pain', 'stomachache', 'abdominal discomfort','stomachache','stomachpain','knee pain'],
    #'stomach pain': ['stomach ache', 'stomach pain', 'stomachache', 'abdominal discomfort'],
    'headache': ['headache', 'migraine', 'cephalalgia'],
    'nausea': ['nausea', 'queasiness', 'sickness', 'upset stomach'],
    'fever': ['fever', 'pyrexia','high temperature'],
    'cough' : ['cough'],
    'dizziness': ['dizziness', 'dizzy', 'lightheadedness', 'vertigo'],
    'yellow eyes': ['yellow eyes', 'jaundice', 'scleral icterus'],
    'acidity' : ['acidity','gastritis'],
    'weakness' : ['weakness','dehydration','dehydrated'],
    'skin rash' : ['skin rash', 'skin rashes'],
    # Add more canonical symptoms and their variants as needed
}

# Generate a reverse mapping: any variant symptom maps to its canonical term
symptom_to_canonical = {}
for canonical, variants in canonical_symptom_mapping.items():
    for variant in variants:
        symptom_to_canonical[variant.lower()] = canonical.lower()

# Define follow-up questions for each canonical symptom
canonical_symptom_followup_questions = {
    'pain': [
        #{"hi": "क्या आपको पेट में दर्द हो रहा है?", "en": "Are you experiencing abdominal pain?", "category": "abdominal_pain", "symptom": "Abdominal pain"},
        {"hi": "पेट दर्द कहाँ महसूस हो रहा है?", "en": "Where exactly are you feeling the pain?", "category": "pain_location", "symptom": None},
        {"hi": "क्या पेट दर्द के साथ मतली है?", "en": "Do you have nausea along with the pain?", "category": "nausea", "symptom": "Nausea"},
        {"hi": "क्या आपको उल्टी भी हो रही है?", "en": "Are you also vomiting?", "category": "vomiting", "symptom": "Vomiting"},
        {"hi": "क्या आपके पेट में सूजन है?", "en": "Is there any swelling?", "category": "swelling", "symptom": "Abdominal swelling"},
        {"hi": "क्या आपको कब्ज है या दस्त हो रहे हैं?", "en": "Are you experiencing constipation or diarrhea?", "category": "bowel_changes", "symptom": "Constipation or diarrhea"},
        {"hi": "क्या पेट दर्द अचानक शुरू हुआ था या धीरे-धीरे?", "en": "Did the pain start suddenly or gradually?", "category": "pain_onset", "symptom": None},
        {"hi": "क्या पेट दर्द खाने के बाद बढ़ता है?", "en": "Does the pain increase after eating?", "category": "postprandial_pain", "symptom": "Postprandial pain"},
        {"hi": "क्या आपको पसीना आ रहा है पेट दर्द के साथ?", "en": "Are you sweating with the pain?", "category": "sweating", "symptom": "Sweating"},
        {"hi": "क्या आपके पेट में कोई हार्टबिटिंग महसूस हो रहा है?", "en": "Do you feel any heartburn in your abdomen?", "category": "heartburn", "symptom": "Heartburn"},
        {"hi": "क्या आप घायल हुए हैं?", "en": "Have you been injured?", "category": "injury", "symptom": "Injury"},
    ],
    'stomach ache': [
        {"hi": "आपने हाल ही में कौन से खाद्य पदार्थ खाए?", "en": "What foods did you recently eat?",  "category": "pain_location", "symptom": "stomach ache"},
        {"hi": "सीने में दर्द की तीव्रता क्या है?", "en": "What is the intensity of your stomach ache?", "category": "stomach ache", "symptom": "stomach ache"},
        {"hi": "क्या दर्द का स्थान स्पष्ट है?", "en": "Is the location of the pain specific?", "category": "pain_location", "symptom": "Specific pain location"},
        {"hi": "क्या दर्द के साथ सांस लेने में कठिनाई है?", "en": "Are you having difficulty breathing along with the pain?", "category": "breathing_difficulty", "symptom": "Difficulty breathing"},
        {"hi": "क्या आप अत्यधिक तनाव में हैं साथ ही सीने में दर्द?", "en": "Are you under extreme stress along with chest pain?", "category": "stress_chest_pain", "symptom": "Stress-related chest pain"},
        {"hi": "क्या आपको छाती में भारीपन महसूस हो रहा है?", "en": "Do you feel a heaviness in your chest?", "category": "chest_heaviness", "symptom": "Chest heaviness"},
    ],
    'acidity': [
        {"hi": "आपने हाल ही में कौन से खाद्य पदार्थ खाए?", "en": "What foods did you recently eat?",  "category": "stomach ache", "symptom": "stomach ache"},
        {"hi": "दर्द कितना तीव्र है?", "en": "How intense is the pain?", "category": "stomach ache", "symptom": "stomach ache"},
        {"hi": "क्या दर्द के साथ सांस लेने में कठिनाई है?", "en": "Are you having difficulty breathing along with the pain?", "category": "breathing_difficulty", "symptom": "Difficulty breathing"},
        {"hi": "क्या आप अत्यधिक तनाव में हैं साथ ही सीने में दर्द?", "en": "Are you under extreme stress along with chest pain?", "category": "stress_chest_pain", "symptom": "Stress-related chest pain"},
        {"hi": "क्या आपको छाती में भारीपन महसूस हो रहा है?", "en": "Do you feel a heaviness in your chest?", "category": "chest_heaviness", "symptom": "Chest heaviness"},
    ],

     'weakness': [
        {"hi": "क्या आपको थकान महसूस होती है?", "en": "Do you feel fatigue? ", "category": "weakness",  "symptom": "weakness"},
        {"hi": "क्या आपको नींद की कमी का सामना करना पड़ता है?", "en": "Do you face lack of sleep?", "category": "lack of sleep", "symptom": "sleep deprivation"},
        {"hi": "क्या आप खुद को हाइड्रेटेड रखते हैं?", "en": "Do you keep yourself hydrated??", "category": "dehydration", "symptom": "dehydration"},
        {"hi": "क्या आपको मांसपेशियों में कमजोरी है?", "en": "Do you have muscle weakness?", "category": "weakness", "symptom": "Weakness"},
        {"hi": "क्या आप पौष्टिक भोजन खाते हैं?", "en": "Do you eat nutritious food?", "category": "weakness", "symptom": "Weakness"},
         {"hi": "क्या आप प्रतिदिन व्यायाम करते हैं?", "en": "Do you exercise daily?", "category": "weakness", "symptom": "Weakness"},
        {"hi": "क्या आप शारीरिक रूप से विकलांग व्यक्ति हैं?", "en": "Are you physically challenged person?", "category": "weakness", "symptom": "Weakness"},
    ],
    
    'headache': [
        {"hi": "क्या आपका सिरदर्द लगातार है या बीच-बीच में आता है?", "en": "Is your headache constant or intermittent?", "category": "headache_type", "symptom": None},
        {"hi": "क्या सिरदर्द की तीव्रता बढ़ रही है?", "en": "Is the intensity of your headache increasing?", "category": "intensity_increase", "symptom": None},
        {"hi": "क्या सिरदर्द के साथ दृष्टि में परिवर्तन है?", "en": "Are you experiencing any changes in vision along with headache?", "category": "vision_changes", "symptom": "Vision changes"},
        {"hi": "क्या सिरदर्द की शुरुआत अचानक हुई थी या धीरे-धीरे?", "en": "Did the headache start suddenly or gradually?", "category": "onset", "symptom": None},
        {"hi": "क्या सिरदर्द का कोई विशिष्ट स्थान है?", "en": "Is there a specific location where you feel the headache?", "category": "location_specific", "symptom": "Location-specific headache"},
        {"hi": "क्या आपको मिचली हो रही है साथ ही सिरदर्द?", "en": "Are you feeling nauseous along with headache?", "category": "nausea_headache", "symptom": "Nausea"},
        {"hi": "क्या आपको ध्वनि या रोशनी से संवेदनशीलता है साथ ही सिरदर्द?", "en": "Do you have sensitivity to sound or light along with headache?", "category": "sensory_sensitivity", "symptom": "Sensitivity to sound or light"},
        {"hi": "क्या आपने कोई नया स्टाइलिश हैडबैग या चश्मा पहनना शुरू किया है?", "en": "Have you started wearing a new stylish hat or glasses?", "category": "external_factors", "symptom": None},
        {"hi": "क्या आपको तनाव है साथ ही सिरदर्द?", "en": "Are you under stress along with headache?", "category": "stress_headache", "symptom": "Stress-related headache"},
        {"hi": "क्या आपकी नींद में कोई कमी है साथ ही सिरदर्द?", "en": "Are you lacking sleep along with headache?", "category": "sleep_deprivation", "symptom": "Sleep deprivation"},
        ],
    'nausea': [
        {"hi": "क्या आपको उल्टी हो रही है?", "en": "Are you vomiting?", "category": "vomiting", "symptom": "Vomiting"},
        {"hi": "क्या आपको लगातार मतली महसूस हो रही है?", "en": "Are you experiencing constant nausea?", "category": "constant_nausea", "symptom": "Constant nausea"},
        {"hi": "क्या मतली के साथ कोई अन्य लक्षण हैं?", "en": "Are there any other symptoms along with nausea?", "category": "other_symptoms", "symptom": None},
        {"hi": "क्या आपको खाने के बाद मतली होती है?", "en": "Do you feel nauseous after eating?", "category": "postprandial_nausea", "symptom": "Postprandial nausea"},
        {"hi": "क्या आपको पेट में दर्द हो रहा है साथ ही मतली?", "en": "Are you experiencing abdominal pain along with nausea?", "category": "abdominal_pain_nausea", "symptom": "Abdominal pain"},
        {"hi": "क्या आपको सिरदर्द है साथ ही मतली?", "en": "Do you have headaches along with nausea?", "category": "headache_nausea", "symptom": "Headache"},
        {"hi": "क्या आपके मूत्र में कोई परिवर्तन आया है?", "en": "Have you noticed any changes in your urine?", "category": "urinary_changes", "symptom": None},
        {"hi": "क्या आपको कोई चक्कर आ रहे हैं साथ ही मतली?", "en": "Are you feeling dizzy along with nausea?", "category": "dizziness_nausea", "symptom": "Dizziness"},
        {"hi": "क्या आपको नींद नहीं आ रही है साथ ही मतली?", "en": "Are you having trouble sleeping along with nausea?", "category": "sleep_disturbance", "symptom": "Sleep disturbance"},
        {"hi": "क्या आपकी त्वचा पीलिया हो रही है साथ ही मतली?", "en": "Is your skin turning yellow along with nausea?", "category": "jaundice_nausea", "symptom": "Jaundice"},
    ],
    'dizziness': [
        {"hi": "क्या आप चक्कर आ रहे हैं?", "en": "Are you feeling dizzy?", "category": "dizziness_type", "symptom": None},
        {"hi": "क्या चक्कर आना अचानक शुरू हुआ था या धीरे-धीरे?", "en": "Did the dizziness start suddenly or gradually?", "category": "dizziness_onset", "symptom": None},
        {"hi": "क्या चक्कर आने के साथ मतली या उल्टी हो रही है?", "en": "Are you experiencing nausea or vomiting along with dizziness?", "category": "dizziness_nausea_vomiting", "symptom": "Nausea or vomiting"},
        {"hi": "क्या चक्कर आना चलने या खड़े होने पर बढ़ता है?", "en": "Does the dizziness increase when walking or standing?", "category": "position_related_dizziness", "symptom": "Position-related dizziness"},
        {"hi": "क्या आपको सिरदर्द हो रहा है साथ में चक्कर आना?", "en": "Are you having headaches along with dizziness?", "category": "headache_dizziness", "symptom": "Headache"},
        {"hi": "क्या आपके आसपास की चीजें घूमती हुई दिख रही हैं?", "en": "Are objects around you spinning?", "category": "visual_dizziness", "symptom": "Visual dizziness"},
        {"hi": "क्या आपको संतुलन बिगड़ रहा है?", "en": "Are you losing your balance?", "category": "balance_issues", "symptom": "Balance issues"},
    ],
    'yellow eyes': [
        {"hi": "क्या आपके आंखों का रंग पीला हो गया है?", "en": "Have your eyes turned yellow?", "category": "jaundice_eye", "symptom": "Jaundice in eyes"},
        {"hi": "क्या आपकी त्वचा भी पीली हो गई है?", "en": "Has your skin also turned yellow?", "category": "jaundice_skin", "symptom": "Jaundice in skin"},
        {"hi": "क्या आपको थकान महसूस हो रही है साथ में पीली आँखें?", "en": "Are you feeling fatigued along with yellow eyes?", "category": "fatigue_jaundice", "symptom": "Fatigue with jaundice"},
        {"hi": "क्या आपके मूत्र का रंग गहरा हो गया है?", "en": "Has the color of your urine become darker?", "category": "dark_urine", "symptom": "Dark urine"},
        {"hi": "क्या आपके बवासीर या पेट में दर्द है साथ में पीली आँखें?", "en": "Do you have hemorrhoids or abdominal pain along with yellow eyes?", "category": "hemorrhoids_abdominal_pain", "symptom": "Hemorrhoids or abdominal pain"},
        {"hi": "क्या आपकी आँखों में जलन हो रही है?", "en": "Are your eyes feeling itchy along with yellowing?", "category": "itchy_eyes", "symptom": "Itchy eyes"},
        {"hi": "क्या आपके मुँह से पीली लार निकल रही है?", "en": "Is yellow saliva coming from your mouth?", "category": "yellow_saliva", "symptom": "Yellow saliva"},
    ],
    'fever': [
        {"hi": "क्या आपका बुखार लगातार है या बीच-बीच में आता है?", "en": "Is your fever constant or intermittent?", "category": "fever_type", "symptom": None},
        {"hi": "क्या आपको ठंड लग रही है?", "en": "Are you experiencing any chills?", "category": "chills", "symptom": "Chills"},
        {"hi": "क्या आपने कोई दवा ली है?", "en": "Have you taken any medication?", "category": "medications", "symptom": None},
        {"hi": "क्या आपको सिरदर्द है?", "en": "Are you experiencing headaches?", "category": "headache", "symptom": "Headache"},
        {"hi": "क्या आपको उल्टी जैसा महसूस हो रहा है?", "en": "Are you feeling nauseous?", "category": "nausea", "symptom": "Nausea"},
        {"hi": "क्या आपका तापमान सामान्य से अधिक है?", "en": "Is your temperature higher than normal?", "category": "high_temperature", "symptom": "High temperature"},
        {"hi": "क्या आपको रात में पसीना आता है?", "en": "Do you experience night sweats?", "category": "night_sweats", "symptom": "Night sweats"},
        {"hi": "क्या आपको भूख कम लग रही है?", "en": "Are you experiencing loss of appetite?", "category": "loss_of_appetite", "symptom": "Loss of appetite"},
        {"hi": "क्या आपको सांस लेने में कठिनाई हो रही है?", "en": "Are you having difficulty breathing?", "category": "breathing_difficulty", "symptom": "Difficulty breathing"},
        {"hi": "क्या आपके शरीर में कोई अन्य दर्द महसूस हो रहा है?", "en": "Are you experiencing any other pains in your body?", "category": "other_pains", "symptom": None},
    ],
    'cough': [
        {"hi": "क्या आपकी खांसी सूखी है या बलगम के साथ?", "en": "Is your cough dry or with phlegm?", "category": "cough_type", "symptom": None},
        {"hi": "क्या आपके खांसी के साथ बुखार है?", "en": "Do you have a fever along with your cough?", "category": "fever", "symptom": "Fever"},
        {"hi": "क्या आपको सांस लेने में कठिनाई हो रही है?", "en": "Are you experiencing difficulty breathing?", "category": "breathing", "symptom": "Shortness of breath"},
        {"hi": "क्या आपकी खांसी रात में बढ़ जाती है?", "en": "Does your cough worsen at night?", "category": "time", "symptom": None},
        {"hi": "क्या आपको सीने में दर्द है?", "en": "Are you experiencing chest pain?", "category": "chest_pain", "symptom": "Chest pain"},
        {"hi": "क्या आपको गले में खराश है?", "en": "Do you have a sore throat?", "category": "sore_throat", "symptom": "Sore throat"},
        {"hi": "क्या आपकी आवाज़ बदल गई है?", "en": "Has your voice changed?", "category": "voice_change", "symptom": "Hoarseness"},
        {"hi": "क्या आपको सांस लेने में सीटी जैसी आवाज़ आती है?", "en": "Do you experience wheezing?", "category": "wheezing", "symptom": "Wheezing"},
        {"hi": "क्या आपके खांसी के साथ बलगम में खून है?", "en": "Is there blood in your phlegm with your cough?", "category": "hemoptysis", "symptom": "Hemoptysis"},
        {"hi": "क्या आपकी खांसी के साथ तेज सांस लेना शामिल है?", "en": "Does your cough include rapid breathing?", "category": "rapid_breathing", "symptom": "Rapid breathing"},
        ],

'muscle pain': [
        {"hi": "क्या आपके मांसपेशियों में दर्द लगातार है या आता-जाता है?", "en": "Is your muscle pain constant or does it come and go?", "category": "intermittent_pain", "symptom": None},
        {"hi": "क्या मांसपेशियों में दर्द किसी विशेष गतिविधि के दौरान बढ़ता है?", "en": "Does your muscle pain increase during any specific activity?", "category": "activity_related_pain", "symptom": None},
        {"hi": "क्या आपके मांसपेशियों में दर्द के साथ सूजन भी है?", "en": "Is there any swelling along with your muscle pain?", "category": "swelling", "symptom": "swelling"},
        {"hi": "क्या आपको मांसपेशियों में खिंचाव महसूस हो रहा है?", "en": "Are you feeling any muscle cramps?", "category": "cramps", "symptom": "cramps"},
        {"hi": "क्या मांसपेशियों में दर्द के साथ कमजोरी भी महसूस हो रही है?", "en": "Are you experiencing any weakness along with muscle pain?", "category": "weakness", "symptom": "weakness"}
    ],

    'joint pain': [
        {"hi": "क्या आपके जोड़ों में दर्द लगातार है या आता-जाता है?", "en": "Is your joint pain constant or does it come and go?", "category": "intermittent_pain", "symptom": None},
        {"hi": "क्या किसी विशेष गतिविधि के दौरान जोड़ों में दर्द बढ़ता है?", "en": "Does your joint pain increase during any specific activity?", "category": "activity_related_pain", "symptom": None},
        {"hi": "क्या आपके जोड़ों में सूजन भी है?", "en": "Is there any swelling in your joints?", "category": "swelling", "symptom": "swelling"},
        {"hi": "क्या आपको जोड़ों में कठोरता महसूस हो रही है?", "en": "Are you experiencing stiffness in your joints?", "category": "stiffness", "symptom": "stiffness"},
        {"hi": "क्या जोड़ों में दर्द के साथ कोई आवाज़ भी सुनाई देती है?", "en": "Do you hear any clicking or popping sounds in your joints along with pain?", "category": "sounds_with_pain", "symptom": None}
    ],

    'chest pain': [
        {"hi": "क्या आपका छाती में दर्द तेज है या स्थिर है?", "en": "Is your chest pain sharp or dull?", "category": "pain_intensity", "symptom": None},
        {"hi": "क्या छाती का दर्द अचानक शुरू हुआ था या धीरे-धीरे?", "en": "Did the chest pain start suddenly or gradually?", "category": "onset", "symptom": None},
        {"hi": "क्या छाती में दर्द के साथ सांस लेने में कठिनाई हो रही है?", "en": "Are you experiencing difficulty breathing along with chest pain?", "category": "breathing_difficulty", "symptom": "shortness of breath"},
        {"hi": "क्या छाती का दर्द किसी विशेष गतिविधि के दौरान बढ़ता है?", "en": "Does your chest pain increase during any specific activity?", "category": "activity_related_pain", "symptom": None},
        {"hi": "क्या छाती का दर्द आपके हाथ, गर्दन या कमर में फैल रहा है?", "en": "Is your chest pain radiating to your arms, neck, or back?", "category": "radiating_pain", "symptom": None},
        {"hi": "क्या छाती में दर्द के साथ पसीना आना शुरू हुआ है?", "en": "Have you started sweating along with chest pain?", "category": "sweating_with_pain", "symptom": "sweating"}
    ],

    'back pain': [
        {"hi": "क्या आपका पीठ दर्द निचले हिस्से में है या ऊपर?", "en": "Is your back pain in the lower or upper back?", "category": "pain_location", "symptom": None},
        {"hi": "क्या पीठ दर्द लगातार है या आता-जाता है?", "en": "Is your back pain constant or does it come and go?", "category": "intermittent_pain", "symptom": None},
        {"hi": "क्या किसी विशेष गतिविधि के दौरान पीठ दर्द बढ़ता है?", "en": "Does your back pain increase during any specific activity?", "category": "activity_related_pain", "symptom": None},
        {"hi": "क्या पीठ दर्द के साथ सूजन है?", "en": "Is there any swelling along with your back pain?", "category": "swelling", "symptom": "swelling"},
        {"hi": "क्या आपको पीठ दर्द के साथ किसी अन्य प्रकार का दर्द भी महसूस हो रहा है?", "en": "Are you experiencing any other type of pain along with your back pain?", "category": "other_pain", "symptom": "Other pain"},
        {"hi": "क्या पीठ दर्द के साथ कमजोरी महसूस हो रही है?", "en": "Are you experiencing any weakness along with back pain?", "category": "weakness", "symptom": "weakness"}
    ],

    'constipation': [
        {"hi": "क्या आपको कब्ज की समस्या कितने दिनों से है?", "en": "How many days have you been experiencing constipation?", "category": "duration", "symptom": None},
        {"hi": "क्या कब्ज के साथ पेट में दर्द है?", "en": "Are you experiencing abdominal pain along with constipation?", "category": "abdominal_pain", "symptom": "abdominal pain"},
        {"hi": "क्या आप नियमित रूप से पानी पीते हैं?", "en": "Are you drinking enough water regularly?", "category": "hydration", "symptom": None},
        {"hi": "क्या आपकी डाइट में पर्याप्त फाइबर है?", "en": "Does your diet include sufficient fiber?", "category": "diet_fiber", "symptom": None},
        {"hi": "क्या कब्ज की समस्या के साथ कोई अन्य लक्षण हैं?", "en": "Are there any other symptoms associated with your constipation?", "category": "other_symptoms", "symptom": None},
        {"hi": "क्या आप नियमित रूप से व्यायाम करते हैं?", "en": "Do you exercise regularly?", "category": "exercise", "symptom": None}
    ],

    'sore throat': [
        {"hi": "क्या आपकी गले में दर्द लगातार है या आता-जाता है?", "en": "Is your sore throat constant or does it come and go?", "category": "intermittent_pain", "symptom": None},
        {"hi": "क्या आपको निगलने में कठिनाई हो रही है?", "en": "Are you having difficulty swallowing?", "category": "difficulty_swallowing", "symptom": "difficulty swallowing"},
        {"hi": "क्या गले में दर्द के साथ सूजन भी है?", "en": "Is there any swelling along with your sore throat?", "category": "swelling", "symptom": "swelling"},
        {"hi": "क्या आपकी आवाज़ में परिवर्तन आया है?", "en": "Has there been any change in your voice?", "category": "voice_changes", "symptom": "voice changes"},
        {"hi": "क्या आपको गले में जलन महसूस हो रही है?", "en": "Are you experiencing any burning sensation in your throat?", "category": "burning_sensation", "symptom": "burning"},
        {"hi": "क्या आपके गले में कोई गड़गड़ाहट है?", "en": "Do you have any tickling sensation in your throat?", "category": "tickling_sensation", "symptom": None}
    ],

    'diarrhea': [
        {"hi": "क्या आपको दस्त लगातार हो रहे हैं या कभी-कभी?", "en": "Are you experiencing diarrhea continuously or intermittently?", "category": "intermittent_diarrea", "symptom": None},
        {"hi": "क्या दस्त के साथ पेट में दर्द है?", "en": "Do you have abdominal pain along with diarrhea?", "category": "abdominal_pain", "symptom": "abdominal pain"},
        {"hi": "क्या आपको दस्त के साथ उल्टी भी हो रही है?", "en": "Are you also experiencing vomiting along with diarrhea?", "category": "vomiting", "symptom": "vomiting"},
        {"hi": "क्या आप अपने शरीर से अधिक पानी खो रहे हैं?", "en": "Are you losing more water from your body?", "category": "dehydration", "symptom": "dehydration"},
        {"hi": "क्या दस्त के साथ बुखार भी है?", "en": "Is there a fever along with diarrhea?", "category": "fever", "symptom": "fever"},
        {"hi": "क्या आपको दस्त के साथ कोई अन्य लक्षण महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with diarrhea?", "category": "other_symptoms", "symptom": None}
    ],

    'vomiting': [
        {"hi": "क्या उल्टी लगातार हो रही है या कभी-कभी?", "en": "Are you vomiting continuously or intermittently?", "category": "intermittent_vomiting", "symptom": None},
        {"hi": "क्या उल्टी के साथ पेट में दर्द है?", "en": "Do you have abdominal pain along with vomiting?", "category": "abdominal_pain", "symptom": "abdominal pain"},
        {"hi": "क्या आपको उल्टी के साथ दस्त भी हो रहे हैं?", "en": "Are you also experiencing diarrhea along with vomiting?", "category": "diarrhea", "symptom": "diarrhea"},
        {"hi": "क्या उल्टी के कारण आपको शरीर से पानी की कमी हो रही है?", "en": "Are you losing water from your body due to vomiting?", "category": "dehydration", "symptom": "dehydration"},
        {"hi": "क्या उल्टी के साथ बुखार भी है?", "en": "Is there a fever along with vomiting?", "category": "fever", "symptom": "fever"},
        {"hi": "क्या आपको उल्टी के साथ कोई अन्य लक्षण महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with vomiting?", "category": "other_symptoms", "symptom": None}
    ],

    'chills': [
        {"hi": "क्या आपके ठंडक के साथ बुखार भी है?", "en": "Do you have a fever along with chills?", "category": "fever", "symptom": "fever"},
        {"hi": "क्या ठंडक की अनुभूति लगातार है या आता-जाता है?", "en": "Is your feeling of chills constant or intermittent?", "category": "intermittent_chills", "symptom": None},
        {"hi": "क्या ठंडक के साथ पसीना आना भी शुरू हो गया है?", "en": "Have you started sweating along with chills?", "category": "sweating_with_chills", "symptom": "sweating"},
        {"hi": "क्या ठंडक के साथ कमजोरी महसूस हो रही है?", "en": "Are you experiencing any weakness along with chills?", "category": "weakness", "symptom": "weakness"},
        {"hi": "क्या आपको ठंडक के साथ कोई अन्य लक्षण भी महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with chills?", "category": "other_symptoms", "symptom": None},
        {"hi": "क्या ठंडक की अनुभूति किसी विशेष समय पर अधिक होती है?", "en": "Do you feel chills more at any specific time?", "category": "time_related_chills", "symptom": None}
    ],

    'shortness of breath': [
        {"hi": "क्या आपको सांस लेने में कठिनाई हो रही है?", "en": "Are you having difficulty breathing?", "category": "breathing_difficulty", "symptom": None},
        {"hi": "क्या सांस लेने में कठिनाई स्थिर है या बढ़ती जा रही है?", "en": "Is your difficulty in breathing constant or worsening?", "category": "intermittent_difficulty", "symptom": None},
        {"hi": "क्या सांस लेने में कठिनाई के साथ दिल की धड़कन तेज हो रही है?", "en": "Is your heart rate increasing along with difficulty breathing?", "category": "heart_rate_increase", "symptom": None},
        {"hi": "क्या सांस लेने में कठिनाई किसी विशेष गतिविधि के दौरान बढ़ती है?", "en": "Does your difficulty in breathing increase during any specific activity?", "category": "activity_related_difficulty", "symptom": None},
        {"hi": "क्या आपको सांस लेने में दर्द भी हो रहा है?", "en": "Are you experiencing pain while breathing?", "category": "breathing_pain", "symptom": None},
        {"hi": "क्या सांस लेने में कठिनाई के साथ कोई अन्य लक्षण भी हैं?", "en": "Are there any other symptoms along with difficulty breathing?", "category": "other_symptoms", "symptom": None}
    ],

    'swelling': [
        {"hi": "क्या सूजन किसी विशेष हिस्से में है?", "en": "Is the swelling in any specific area?", "category": "swelling_location", "symptom": None},
        {"hi": "क्या सूजन के साथ दर्द भी है?", "en": "Is there any pain along with swelling?", "category": "pain_with_swelling", "symptom": None},
        {"hi": "क्या सूजन लगातार है या आता-जाता है?", "en": "Is the swelling constant or does it come and go?", "category": "intermittent_swelling", "symptom": None},
        {"hi": "क्या सूजन के कारण त्वचा में कोई परिवर्तन हो रहा है?", "en": "Is there any change in the skin due to swelling?", "category": "skin_changes_with_swelling", "symptom": None},
        {"hi": "क्या सूजन के साथ त्वचा की लालिमा भी है?", "en": "Is there redness of the skin along with swelling?", "category": "redness_with_swelling", "symptom": "redness"},
        {"hi": "क्या सूजन के कारण आपको बेचैनी हो रही है?", "en": "Are you feeling restless due to swelling?", "category": "restlessness_with_swelling", "symptom": None}
    ],

    'infection': [
        {"hi": "क्या आपको बुखार है?", "en": "Do you have a fever?", "category": "fever", "symptom": "fever"},
        {"hi": "क्या संक्रमण के कारण आपको किसी विशेष हिस्से में दर्द हो रहा है?", "en": "Are you experiencing pain in any specific area due to the infection?", "category": "localized_pain", "symptom": None},
        {"hi": "क्या संक्रमण के साथ सूजन भी है?", "en": "Is there any swelling along with the infection?", "category": "swelling", "symptom": "swelling"},
        {"hi": "क्या संक्रमण के कारण आपको कमजोरी महसूस हो रही है?", "en": "Are you feeling weak due to the infection?", "category": "weakness", "symptom": "weakness"},
        {"hi": "क्या संक्रमण के साथ कोई अन्य लक्षण भी हैं?", "en": "Are there any other symptoms along with the infection?", "category": "other_symptoms", "symptom": None},
        {"hi": "क्या संक्रमण के कारण आपको त्वचा में लालिमा आ रही है?", "en": "Is there any redness in your skin due to the infection?", "category": "skin_redness", "symptom": "redness"}
    ],

    'depression': [
        {"hi": "क्या आपको उदासी या निराशा महसूस हो रही है?", "en": "Are you feeling sad or hopeless?", "category": "sadness", "symptom": None},
        {"hi": "क्या आपकी रुचियों में कमी आई है?", "en": "Have you lost interest in your usual activities?", "category": "loss_of_interest", "symptom": None},
        {"hi": "क्या आपको खुद को नीचा महसूस होता है?", "en": "Do you feel worthless?", "category": "worthlessness", "symptom": None},
        {"hi": "क्या आपको निर्णय लेने में कठिनाई हो रही है?", "en": "Are you having difficulty making decisions?", "category": "decision_difficulty", "symptom": None},
        {"hi": "क्या आपकी नींद में कोई समस्या है?", "en": "Are you having any problems with your sleep?", "category": "sleep_problems", "symptom": "insomnia"},
        {"hi": "क्या आपको खुद को चोट पहुँचाने का विचार आता है?", "en": "Are you having thoughts of harming yourself?", "category": "self_harm_thoughts", "symptom": None},
        {"hi": "क्या आपको ऊर्जा की कमी महसूस हो रही है?", "en": "Are you feeling a lack of energy?", "category": "energy_deficit", "symptom": "fatigue"}
    ],

    'diabetes': [
        {"hi": "क्या आपको बार-बार पेशाब आ रहा है?", "en": "Are you urinating frequently?", "category": "frequent_urination", "symptom": "urinary frequency"},
        {"hi": "क्या आपको अत्यधिक प्यास लग रही है?", "en": "Are you feeling excessively thirsty?", "category": "excessive_thirst", "symptom": "excessive thirst"},
        {"hi": "क्या आपको बहुत भूख लग रही है?", "en": "Are you feeling very hungry?", "category": "increased_appetite", "symptom": "increased appetite"},
        {"hi": "क्या आपके वजन में अचानक कमी आई है?", "en": "Have you experienced sudden weight loss?", "category": "sudden_weight_loss", "symptom": "weight loss"},
        {"hi": "क्या आपको धुंधली दृष्टि हो रही है?", "en": "Are you experiencing blurred vision?", "category": "blurred_vision", "symptom": "blurred vision"},
        {"hi": "क्या आपको ऊँची या नीची रक्तचाप की समस्या है?", "en": "Do you have high or low blood pressure?", "category": "blood_pressure", "symptom": None},
        {"hi": "क्या आपके घुटनों या पैरों में सुन्नता है?", "en": "Are you experiencing numbness in your knees or feet?", "category": "numbness", "symptom": "numbness"}
    ],

    'allergies': [
        {"hi": "क्या आपको किसी विशेष चीज़ से एलर्जी है?", "en": "Do you have allergies to any specific substance?", "category": "specific_allergy", "symptom": None},
        {"hi": "क्या आपकी त्वचा में खुजली या लालिमा है?", "en": "Do you have itching or redness on your skin?", "category": "skin_allergy_symptoms", "symptom": "itching"},
        {"hi": "क्या आपको सांस लेने में कठिनाई हो रही है?", "en": "Are you experiencing difficulty breathing?", "category": "breathing_difficulty", "symptom": "shortness of breath"},
        {"hi": "क्या आपके आंखों में सूजन या जलन है?", "en": "Do you have swelling or irritation in your eyes?", "category": "eye_allergy_symptoms", "symptom": "itchy eyes"},
        {"hi": "क्या आपको गले में खुजली या सूजन महसूस हो रही है?", "en": "Are you feeling itchiness or swelling in your throat?", "category": "throat_allergy_symptoms", "symptom": "swelling"},
        {"hi": "क्या आपके लक्षण किसी खास मौसम या वातावरण में अधिक होते हैं?", "en": "Do your symptoms worsen in certain seasons or environments?", "category": "environmental_allergy_triggers", "symptom": None}
    ],

    'high blood pressure': [
        {"hi": "क्या आपको सिरदर्द होता है खासकर सुबह में?", "en": "Do you experience headaches, especially in the morning?", "category": "morning_headaches", "symptom": "headache"},
        {"hi": "क्या आपको धड़कन तेज या अनियमित महसूस होती है?", "en": "Do you feel your heartbeat is fast or irregular?", "category": "irregular_heartbeat", "symptom": "irregular heartbeat"},
        {"hi": "क्या आपको चक्कर आना या चक्कर आना महसूस होता है?", "en": "Do you feel dizzy or lightheaded?", "category": "dizziness", "symptom": "dizziness"},
        {"hi": "क्या आपको सांस लेने में कठिनाई हो रही है?", "en": "Are you having difficulty breathing?", "category": "breathing_difficulty", "symptom": "shortness of breath"},
        {"hi": "क्या आपकी आँखों में धुंधलापन है?", "en": "Do you experience blurred vision?", "category": "blurred_vision", "symptom": "blurred vision"},
        {"hi": "क्या आपको थकान महसूस हो रही है?", "en": "Are you feeling fatigued?", "category": "fatigue", "symptom": "fatigue"},
        {"hi": "क्या आपको छाती में दर्द महसूस हो रहा है?", "en": "Are you feeling chest pain?", "category": "chest_pain", "symptom": "chest pain"}
    ],

    'low blood pressure': [
        {"hi": "क्या आपको चक्कर आ रहे हैं या आप चकरा रहे हैं?", "en": "Are you feeling dizzy or faint?", "category": "dizziness_fainting", "symptom": "dizziness"},
        {"hi": "क्या आपको कमजोरी महसूस हो रही है?", "en": "Are you feeling weak?", "category": "weakness", "symptom": "weakness"},
        {"hi": "क्या आपको धुंधली दृष्टि हो रही है?", "en": "Are you experiencing blurred vision?", "category": "blurred_vision", "symptom": "blurred vision"},
        {"hi": "क्या आपको सांस लेने में कठिनाई हो रही है?", "en": "Are you having difficulty breathing?", "category": "breathing_difficulty", "symptom": "shortness of breath"},
        {"hi": "क्या आपको थकान हो रही है?", "en": "Are you feeling fatigued?", "category": "fatigue", "symptom": "fatigue"},
        {"hi": "क्या आपको पेट में दर्द हो रहा है?", "en": "Are you experiencing abdominal pain?", "category": "abdominal_pain", "symptom": "abdominal pain"},
        {"hi": "क्या आपकी त्वचा ठंडी और पसीनी है?", "en": "Is your skin cold and clammy?", "category": "skin_cold_clammy", "symptom": "sweating"}
    ],
    'cramps': [
        {"hi": "क्या आपको क्रैम्प्स लगातार हो रहे हैं या कभी-कभी?", "en": "Are you experiencing cramps continuously or intermittently?", "category": "intermittent_cramps", "symptom": None},
        {"hi": "क्या क्रैम्प्स किसी विशेष समय पर अधिक होते हैं?", "en": "Do your cramps occur more frequently at any specific time?", "category": "time_related_cramps", "symptom": None},
        {"hi": "क्या क्रैम्प्स के साथ दर्द की तीव्रता बढ़ रही है?", "en": "Is the intensity of your cramps increasing?", "category": "intensity_increase", "symptom": None},
        {"hi": "क्या क्रैम्प्स के साथ सूजन भी है?", "en": "Is there any swelling along with your cramps?", "category": "swelling_with_cramps", "symptom": "swelling"},
        {"hi": "क्या क्रैम्प्स के कारण आपको थकान महसूस हो रही है?", "en": "Are you feeling fatigued due to cramps?", "category": "fatigue_with_cramps", "symptom": "fatigue"},
        {"hi": "क्या क्रैम्प्स किसी विशेष गतिविधि के दौरान बढ़ते हैं?", "en": "Do your cramps increase during any specific activity?", "category": "activity_related_cramps", "symptom": None},
        {"hi": "क्या आपको क्रैम्प्स के साथ दर्द में कोई बदलाव महसूस हो रहा है?", "en": "Are you noticing any changes in the pain associated with your cramps?", "category": "pain_changes", "symptom": None}
    ],

    'irritation': [
        {"hi": "क्या आपको त्वचा पर खुजली या जलन महसूस हो रही है?", "en": "Are you experiencing itching or burning sensations on your skin?", "category": "skin_itching_burning", "symptom": "itching"},
        {"hi": "क्या आपको आंखों, नाक या गले में जलन हो रही है?", "en": "Are you feeling irritation in your eyes, nose, or throat?", "category": "localized_irritation", "symptom": None},
        {"hi": "क्या आपके शरीर के किसी विशेष हिस्से में जलन महसूस हो रही है?", "en": "Are you feeling burning sensations in any specific part of your body?", "category": "specific_irritation", "symptom": None},
        {"hi": "क्या जलन के साथ सूजन भी है?", "en": "Is there any swelling along with the irritation?", "category": "swelling_with_irritation", "symptom": "swelling"},
        {"hi": "क्या आपको किसी विशेष पदार्थ से जलन हो रही है?", "en": "Are you experiencing irritation due to any specific substance?", "category": "triggered_irritation", "symptom": None},
        {"hi": "क्या जलन के कारण आपकी त्वचा लाल हो गई है?", "en": "Has the irritation caused any redness on your skin?", "category": "redness_with_irritation", "symptom": "redness"},
        {"hi": "क्या जलन के साथ कोई अन्य लक्षण भी हैं?", "en": "Are there any other symptoms along with the irritation?", "category": "other_symptoms", "symptom": None}
    ],

    'inflammation': [
        {"hi": "क्या सूजन किसी विशेष हिस्से में है?", "en": "Is the inflammation localized to any specific area?", "category": "localized_inflammation", "symptom": None},
        {"hi": "क्या सूजन के साथ दर्द भी है?", "en": "Is there any pain along with the inflammation?", "category": "pain_with_inflammation", "symptom": None},
        {"hi": "क्या सूजन लगातार है या आता-जाता है?", "en": "Is the inflammation constant or does it come and go?", "category": "intermittent_inflammation", "symptom": None},
        {"hi": "क्या सूजन के कारण त्वचा में लालिमा या गर्मी महसूस हो रही है?", "en": "Is there any redness or warmth in the skin due to inflammation?", "category": "skin_changes_with_inflammation", "symptom": "redness"},
        {"hi": "क्या सूजन के साथ कोई अन्य लक्षण भी हैं?", "en": "Are there any other symptoms along with the inflammation?", "category": "other_symptoms", "symptom": None},
        {"hi": "क्या सूजन किसी विशेष समय पर अधिक होती है?", "en": "Does the inflammation occur more frequently at any specific time?", "category": "time_related_inflammation", "symptom": None},
        {"hi": "क्या सूजन के कारण आपको चलने-फिरने में कठिनाई हो रही है?", "en": "Are you having difficulty moving due to the inflammation?", "category": "movement_difficulty_with_inflammation", "symptom": None}
    ],

    'weight gain': [
        {"hi": "क्या आपको वजन तेजी से बढ़ रहा है?", "en": "Are you gaining weight rapidly?", "category": "rapid_weight_gain", "symptom": "weight gain"},
        {"hi": "क्या वजन बढ़ने के साथ आपके कपड़ों में कसाव आ रहा है?", "en": "Is your clothing feeling tighter due to weight gain?", "category": "clothing_tightness", "symptom": None},
        {"hi": "क्या वजन बढ़ने के कारण आपको थकान महसूस हो रही है?", "en": "Are you feeling fatigued due to weight gain?", "category": "fatigue_with_weight_gain", "symptom": "fatigue"},
        {"hi": "क्या वजन बढ़ने के साथ आपको सांस लेने में कठिनाई हो रही है?", "en": "Are you experiencing difficulty breathing due to weight gain?", "category": "breathing_difficulty_with_weight_gain", "symptom": "shortness of breath"},
        {"hi": "क्या वजन बढ़ने के साथ आपकी त्वचा पर कोई परिवर्तन आ रहा है?", "en": "Are there any changes in your skin due to weight gain?", "category": "skin_changes_with_weight_gain", "symptom": "skin changes"},
        {"hi": "क्या वजन बढ़ने के साथ आपको किसी विशेष हिस्से में दर्द हो रहा है?", "en": "Are you experiencing pain in any specific area due to weight gain?", "category": "localized_pain_with_weight_gain", "symptom": None},
        {"hi": "क्या वजन बढ़ने के साथ आपका मूड भी प्रभावित हो रहा है?", "en": "Is your mood being affected along with weight gain?", "category": "mood_changes_with_weight_gain", "symptom": "depression"}
    ],

    'hair loss': [
        {"hi": "क्या आपको बालों का झड़ना तेजी से हो रहा है?", "en": "Are you experiencing rapid hair loss?", "category": "rapid_hair_loss", "symptom": "hair loss"},
        {"hi": "क्या बालों का झड़ना किसी विशेष समय पर अधिक होता है?", "en": "Does hair loss occur more frequently at any specific time?", "category": "time_related_hair_loss", "symptom": None},
        {"hi": "क्या बालों का झड़ना किसी विशेष हिस्से में ज्यादा हो रहा है?", "en": "Is hair loss more prominent in any specific area?", "category": "localized_hair_loss", "symptom": None},
        {"hi": "क्या बालों का झड़ना के साथ स्कैल्प में खुजली या जलन है?", "en": "Is there itching or burning in the scalp along with hair loss?", "category": "scalp_itching_burning", "symptom": "itching"},
        {"hi": "क्या आपके बालों की ग्रोथ धीमी हो गई है?", "en": "Has your hair growth slowed down?", "category": "slowed_hair_growth", "symptom": None},
        {"hi": "क्या बालों का झड़ना के कारण आपकी आत्म-सम्मान प्रभावित हो रहा है?", "en": "Is your self-esteem being affected due to hair loss?", "category": "self_esteem_impact", "symptom": None},
        {"hi": "क्या आपके बालों का रंग बदल रहा है?", "en": "Are you noticing any changes in your hair color?", "category": "hair_color_changes", "symptom": "hair color changes"}
    ],

    'numbness': [
        {"hi": "क्या आपको किसी विशेष हिस्से में सुन्नता महसूस हो रही है?", "en": "Are you feeling numbness in any specific area?", "category": "localized_numbness", "symptom": None},
        {"hi": "क्या सुन्नता लगातार है या आती-जाती है?", "en": "Is the numbness constant or does it come and go?", "category": "intermittent_numbness", "symptom": None},
        {"hi": "क्या सुन्नता किसी विशेष गतिविधि के दौरान बढ़ती है?", "en": "Does your numbness increase during any specific activity?", "category": "activity_related_numbness", "symptom": None},
        {"hi": "क्या सुन्नता के साथ झुनझुनी भी हो रही है?", "en": "Are you experiencing tingling sensations along with numbness?", "category": "tingling_with_numbness", "symptom": "tingling"},
        {"hi": "क्या सुन्नता किसी विशेष समय पर अधिक होती है?", "en": "Does the numbness occur more frequently at any specific time?", "category": "time_related_numbness", "symptom": None},
        {"hi": "क्या आपको सुन्नता के साथ कमजोरी भी महसूस हो रही है?", "en": "Are you feeling any weakness along with numbness?", "category": "weakness_with_numbness", "symptom": "weakness"},
        {"hi": "क्या सुन्नता के साथ त्वचा में कोई परिवर्तन आ रहा है?", "en": "Are there any changes in your skin due to numbness?", "category": "skin_changes_with_numbness", "symptom": "skin changes"}
    ],

    'itchy eyes': [
        {"hi": "क्या आपकी आँखों में खुजली लगातार है या आती-जाती है?", "en": "Is the itchiness in your eyes constant or does it come and go?", "category": "intermittent_itchiness", "symptom": None},
        {"hi": "क्या आपकी आँखों में लालिमा भी है?", "en": "Is there any redness in your eyes along with itchiness?", "category": "redness_with_itchy_eyes", "symptom": "redness"},
        {"hi": "क्या आपकी आँखों में जलन या दर्द है?", "en": "Are you experiencing any burning or pain in your eyes?", "category": "burning_pain_with_itchy_eyes", "symptom": "burning"},
        {"hi": "क्या आपकी आँखों से पानी आ रहा है?", "en": "Are your eyes watering?", "category": "watery_eyes", "symptom": "watery eyes"},
        {"hi": "क्या आपकी आँखों की खुजली किसी विशेष पदार्थ से संबंधित है?", "en": "Is the itchiness in your eyes related to any specific substance?", "category": "triggered_itchy_eyes", "symptom": None},
        {"hi": "क्या आपकी आँखों में सूजन है?", "en": "Is there any swelling in your eyes?", "category": "swelling_with_itchy_eyes", "symptom": "swelling"},
        {"hi": "क्या आपकी आँखों में कोई धुंधलापन है?", "en": "Are you experiencing any blurriness in your vision along with itchy eyes?", "category": "blurred_vision_with_itchy_eyes", "symptom": "blurred vision"}
    ],

'bloating': [
        {"hi": "क्या आपको पेट में सूजन महसूस हो रही है?", "en": "Are you feeling bloated in your abdomen?", "category": "abdominal_bloating", "symptom": None},
        {"hi": "क्या सूजन के साथ पेट में दर्द भी हो रहा है?", "en": "Are you experiencing abdominal pain along with bloating?", "category": "abdominal_pain_with_bloating", "symptom": "abdominal pain"},
        {"hi": "क्या सूजन के कारण आपको सांस लेने में कठिनाई हो रही है?", "en": "Is bloating causing difficulty in breathing?", "category": "breathing_difficulty_with_bloating", "symptom": "shortness of breath"},
        {"hi": "क्या आपको सूजन के साथ मतली या उल्टी हो रही है?", "en": "Are you experiencing nausea or vomiting along with bloating?", "category": "nausea_vomiting_with_bloating", "symptom": "nausea"},
        {"hi": "क्या सूजन के कारण आपको थकान महसूस हो रही है?", "en": "Are you feeling fatigued due to bloating?", "category": "fatigue_with_bloating", "symptom": "fatigue"}
    ],

    'gas': [
        {"hi": "क्या आपको पेट में गैस की अधिकता महसूस हो रही है?", "en": "Are you feeling excessive gas in your abdomen?", "category": "excessive_gas", "symptom": "gas"},
        {"hi": "क्या गैस के साथ पेट में दर्द भी हो रहा है?", "en": "Are you experiencing abdominal pain along with gas?", "category": "abdominal_pain_with_gas", "symptom": "abdominal pain"},
        {"hi": "क्या गैस के कारण आपको पेट फूलने का अनुभव हो रहा है?", "en": "Are you experiencing bloating due to gas?", "category": "bloating_with_gas", "symptom": "bloating"},
        {"hi": "क्या गैस के साथ आपका मूड भी प्रभावित हो रहा है?", "en": "Is your mood being affected along with gas?", "category": "mood_changes_with_gas", "symptom": "depression"},
        {"hi": "क्या गैस के कारण आपकी नींद प्रभावित हो रही है?", "en": "Is gas affecting your sleep?", "category": "sleep_disturbance_with_gas", "symptom": "insomnia"}
    ],

    'hiccups': [
        {"hi": "क्या आपके सिकुड़न लगातार हो रही है या आती-जाती हैं?", "en": "Are your hiccups continuous or intermittent?", "category": "intermittent_hiccups", "symptom": None},
        {"hi": "क्या सिकुड़न के साथ आपको दर्द भी हो रहा है?", "en": "Are you experiencing pain along with hiccups?", "category": "pain_with_hiccups", "symptom": "chest pain"},
        {"hi": "क्या आपको सिकुड़न के दौरान सांस लेने में कठिनाई हो रही है?", "en": "Are you having difficulty breathing during hiccups?", "category": "breathing_difficulty_with_hiccups", "symptom": "shortness of breath"},
        {"hi": "क्या सिकुड़न के कारण आपका खाना निगलने में कठिनाई हो रही है?", "en": "Are hiccups causing difficulty in swallowing your food?", "category": "swallowing_difficulty_with_hiccups", "symptom": "difficulty swallowing"},
        {"hi": "क्या सिकुड़न के साथ आपके पेट में दर्द हो रहा है?", "en": "Are you experiencing abdominal pain along with hiccups?", "category": "abdominal_pain_with_hiccups", "symptom": "abdominal pain"},
        {"hi": "क्या आपके सिकुड़न के कारण आपकी नींद प्रभावित हो रही है?", "en": "Are your hiccups affecting your sleep?", "category": "sleep_disturbance_with_hiccups", "symptom": "insomnia"}
    ],

    'indigestion': [
        {"hi": "क्या आपको भोजन के बाद पेट में दर्द हो रहा है?", "en": "Are you experiencing abdominal pain after eating?", "category": "post_meal_abdominal_pain", "symptom": "abdominal pain"},
        {"hi": "क्या आपको गैस या सूजन महसूस हो रही है?", "en": "Are you feeling gas or bloating?", "category": "gas_bloating_with_indigestion", "symptom": "gas"},
        {"hi": "क्या indigestion के साथ आपको उल्टी या दस्त भी हो रहे हैं?", "en": "Are you also experiencing vomiting or diarrhea along with indigestion?", "category": "vomiting_diarrhea_with_indigestion", "symptom": "vomiting"},
        {"hi": "क्या indigestion के कारण आपको भोजन निगलने में कठिनाई हो रही है?", "en": "Is indigestion causing difficulty in swallowing your food?", "category": "swallowing_difficulty_with_indigestion", "symptom": "difficulty swallowing"},
        {"hi": "क्या indigestion के साथ आपको पेट में भारीपन महसूस हो रहा है?", "en": "Are you feeling a heaviness in your abdomen along with indigestion?", "category": "heaviness_with_indigestion", "symptom": None},
        {"hi": "क्या indigestion के कारण आपकी नींद प्रभावित हो रही है?", "en": "Is indigestion affecting your sleep?", "category": "sleep_disturbance_with_indigestion", "symptom": "insomnia"}
    ],

    'heartburn': [
        {"hi": "क्या आपको पेट में जलन या जलती हुई अनुभूति हो रही है?", "en": "Are you experiencing burning sensations in your stomach?", "category": "burning_sensation_with_heartburn", "symptom": "burning"},
        {"hi": "क्या जलन आपके छाती के क्षेत्र में हो रही है?", "en": "Is the burning sensation occurring in your chest area?", "category": "chest_burning", "symptom": "chest burning"},
        {"hi": "क्या आपको यह जलन खाने के बाद ज्यादा होती है?", "en": "Does the burning sensation increase after eating?", "category": "post_meal_heartburn", "symptom": "heartburn"},
        {"hi": "क्या जलन के साथ आपको सांस लेने में कठिनाई हो रही है?", "en": "Are you having difficulty breathing along with the burning sensation?", "category": "breathing_difficulty_with_heartburn", "symptom": "shortness of breath"},
        {"hi": "क्या आपको जलन के साथ पेट में दर्द भी हो रहा है?", "en": "Are you experiencing abdominal pain along with the burning sensation?", "category": "abdominal_pain_with_heartburn", "symptom": "abdominal pain"},
        {"hi": "क्या यह जलन रात में ज्यादा होती है?", "en": "Does the burning sensation occur more at night?", "category": "night_time_heartburn", "symptom": None},
        {"hi": "क्या आपको पेट में भारीपन महसूस हो रहा है?", "en": "Are you feeling a heaviness in your stomach?", "category": "heaviness_with_heartburn", "symptom": None}
    ],

    'mouth sores': [
        {"hi": "क्या आपके मुंह में घाव तेजी से बढ़ रहे हैं?", "en": "Are your mouth sores spreading rapidly?", "category": "rapid_spread_mouth_sores", "symptom": "mouth sores"},
        {"hi": "क्या मुंह के घावों के साथ सूजन भी है?", "en": "Is there any swelling along with your mouth sores?", "category": "swelling_with_mouth_sores", "symptom": "swelling"},
        {"hi": "क्या मुंह के घाव खाने या पीने में दर्द पैदा करते हैं?", "en": "Do your mouth sores cause pain while eating or drinking?", "category": "pain_with_mouth_sores", "symptom": "pain"},
        {"hi": "क्या आपको मुंह के घावों से रक्तस्राव हो रहा है?", "en": "Are your mouth sores bleeding?", "category": "bleeding_mouth_sores", "symptom": "bleeding"},
        {"hi": "क्या मुंह के घावों के साथ आपके दांतों में दर्द है?", "en": "Are you experiencing tooth pain along with mouth sores?", "category": "tooth_pain_with_mouth_sores", "symptom": "tooth pain"},
        {"hi": "क्या मुंह के घावों के कारण आपकी बोलने में कठिनाई हो रही है?", "en": "Are your mouth sores causing difficulty in speaking?", "category": "speech_difficulty_with_mouth_sores", "symptom": "difficulty speaking"},
        {"hi": "क्या मुंह के घावों के साथ आपको कोई अन्य लक्षण भी हैं?", "en": "Are there any other symptoms along with mouth sores?", "category": "other_symptoms", "symptom": None}
    ],

    'nosebleeds': [
        {"hi": "क्या नाक से खून बहना बार-बार हो रहा है?", "en": "Are you experiencing frequent nosebleeds?", "category": "frequent_nosebleeds", "symptom": "nosebleeds"},
        {"hi": "क्या नाक से खून बहने के साथ दर्द भी हो रहा है?", "en": "Are you experiencing pain along with nosebleeds?", "category": "pain_with_nosebleeds", "symptom": "chest pain"},
        {"hi": "क्या नाक से खून बहने का कोई विशेष कारण है?", "en": "Is there any specific cause for your nosebleeds?", "category": "specific_cause_nosebleeds", "symptom": None},
        {"hi": "क्या नाक से खून बहने के साथ आपको सूजन भी हो रही है?", "en": "Is there any swelling along with your nosebleeds?", "category": "swelling_with_nosebleeds", "symptom": "swelling"},
        {"hi": "क्या आपको नाक से खून बहने के बाद कमजोरी महसूस हो रही है?", "en": "Are you feeling weak after nosebleeds?", "category": "weakness_with_nosebleeds", "symptom": "weakness"},
        {"hi": "क्या नाक से खून बहने के कारण आपके आँखों में भी कोई समस्या हो रही है?", "en": "Are you experiencing any issues with your eyes due to nosebleeds?", "category": "eye_issues_with_nosebleeds", "symptom": None},
        {"hi": "क्या नाक से खून बहने के साथ आपको सिरदर्द भी हो रहा है?", "en": "Are you experiencing headaches along with nosebleeds?", "category": "headache_with_nosebleeds", "symptom": "headache"}
    ],

    'ear ringing': [
        {"hi": "क्या कानों में बजने वाली आवाजें लगातार हैं या कभी-कभी आती हैं?", "en": "Are the ringing sounds in your ears constant or intermittent?", "category": "intermittent_ringing", "symptom": None},
        {"hi": "क्या कानों में बजने वाली आवाजें तेज हो रही हैं?", "en": "Are the ringing sounds in your ears becoming louder?", "category": "intensity_increase_ringing", "symptom": None},
        {"hi": "क्या कानों में बजने वाली आवाजें आपके सुनने में कठिनाई पैदा कर रही हैं?", "en": "Are the ringing sounds in your ears causing difficulty in hearing?", "category": "hearing_difficulty_with_ringing", "symptom": "hearing loss"},
        {"hi": "क्या कानों में बजने वाली आवाजें किसी विशेष समय पर अधिक होती हैं?", "en": "Do the ringing sounds in your ears occur more frequently at any specific time?", "category": "time_related_ringing", "symptom": None},
        {"hi": "क्या कानों में बजने वाली आवाजें किसी विशेष गतिविधि के दौरान बढ़ती हैं?", "en": "Do the ringing sounds in your ears increase during any specific activity?", "category": "activity_related_ringing", "symptom": None},
        {"hi": "क्या आपको कानों में बजने वाली आवाजें सुनने के साथ साथ सूजन या दर्द भी महसूस हो रहा है?", "en": "Are you experiencing swelling or pain in your ears along with ringing sounds?", "category": "swelling_pain_with_ringing", "symptom": "swelling"},
        {"hi": "क्या कानों में बजने वाली आवाजें किसी विशेष दवा के सेवन के कारण हो रही हैं?", "en": "Are the ringing sounds in your ears caused by taking any specific medication?", "category": "medication_related_ringing", "symptom": None}
    ],

    'decreased appetite': [
        {"hi": "क्या आपकी भूख कम हो गई है?", "en": "Has your appetite decreased?", "category": "appetite_decrease", "symptom": "decreased appetite"},
        {"hi": "क्या भूख में कमी के साथ वजन घट रहा है?", "en": "Are you losing weight along with decreased appetite?", "category": "weight_loss_with_decreased_appetite", "symptom": "weight loss"},
        {"hi": "क्या भूख में कमी के कारण आपकी ऊर्जा स्तर प्रभावित हो रहा है?", "en": "Is your energy level being affected due to decreased appetite?", "category": "energy_deficit_with_decreased_appetite", "symptom": "fatigue"},
        {"hi": "क्या भूख में कमी के साथ पेट में दर्द हो रहा है?", "en": "Are you experiencing abdominal pain along with decreased appetite?", "category": "abdominal_pain_with_decreased_appetite", "symptom": "abdominal pain"},
        {"hi": "क्या आपको भूख में कमी के साथ कोई अन्य लक्षण भी महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with decreased appetite?", "category": "other_symptoms", "symptom": None},
        {"hi": "क्या भूख में कमी के कारण आपको थकान महसूस हो रही है?", "en": "Are you feeling fatigued due to decreased appetite?", "category": "fatigue_with_decreased_appetite", "symptom": "fatigue"},
        {"hi": "क्या आपकी डाइट में कोई विशेष परिवर्तन हुआ है?", "en": "Has there been any specific change in your diet?", "category": "diet_changes", "symptom": None}
    ],

    'increased appetite': [
        {"hi": "क्या आपकी भूख में अचानक बढ़ोतरी हो गई है?", "en": "Has there been a sudden increase in your appetite?", "category": "sudden_increase_appetite", "symptom": "increased appetite"},
        {"hi": "क्या वजन बढ़ने के साथ आपकी भूख में भी वृद्धि हुई है?", "en": "Has your appetite increased along with weight gain?", "category": "appetite_increase_with_weight_gain", "symptom": "weight gain"},
        {"hi": "क्या आपकी भूख में वृद्धि के कारण आपकी डाइट में कोई विशेष बदलाव हुआ है?", "en": "Has there been any specific change in your diet due to increased appetite?", "category": "diet_changes_with_increased_appetite", "symptom": None},
        {"hi": "क्या भूख में वृद्धि के साथ आपको थकान भी महसूस हो रही है?", "en": "Are you feeling fatigued along with increased appetite?", "category": "fatigue_with_increased_appetite", "symptom": "fatigue"},
        {"hi": "क्या आपको भूख में वृद्धि के साथ कोई अन्य लक्षण भी महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with increased appetite?", "category": "other_symptoms", "symptom": None},
        {"hi": "क्या आपकी भूख में वृद्धि के कारण आपकी नींद प्रभावित हो रही है?", "en": "Is your sleep being affected due to increased appetite?", "category": "sleep_disturbance_with_increased_appetite", "symptom": "insomnia"},
        {"hi": "क्या भूख में वृद्धि के साथ आपका मूड भी प्रभावित हो रहा है?", "en": "Is your mood being affected along with increased appetite?", "category": "mood_changes_with_increased_appetite", "symptom": "depression"}
    ],

    'feeling full quickly': [
        {"hi": "क्या आपको खाने के तुरंत बाद भरा हुआ महसूस होता है?", "en": "Do you feel full immediately after eating?", "category": "early_satiety", "symptom": "feeling full quickly"},
        {"hi": "क्या भरा हुआ महसूस होने के साथ पेट में दर्द भी हो रहा है?", "en": "Are you experiencing abdominal pain along with feeling full quickly?", "category": "abdominal_pain_with_satiety", "symptom": "abdominal pain"},
        {"hi": "क्या आपको खाने में कठिनाई हो रही है?", "en": "Are you having difficulty eating?", "category": "eating_difficulty", "symptom": "difficulty swallowing"},
        {"hi": "क्या आपके खाने के साथ किसी विशेष प्रकार का दर्द होता है?", "en": "Do you experience any specific type of pain while eating?", "category": "pain_with_eating", "symptom": "pain"},
        {"hi": "क्या आपको खाने के बाद वजन बढ़ने की समस्या हो रही है?", "en": "Are you having issues with weight gain after eating?", "category": "weight_gain_after_eating", "symptom": "weight gain"},
        {"hi": "क्या आपको खाने के बाद सूजन महसूस हो रही है?", "en": "Are you feeling bloated after eating?", "category": "bloating_after_eating", "symptom": "bloating"},
        {"hi": "क्या आपको खाने के बाद थकान महसूस हो रही है?", "en": "Are you feeling fatigued after eating?", "category": "fatigue_after_eating", "symptom": "fatigue"}
    ],

    'unusual sweating': [
        {"hi": "क्या आपको असामान्य रूप से पसीना आ रहा है?", "en": "Are you experiencing unusual sweating?", "category": "unusual_sweating", "symptom": "sweating"},
        {"hi": "क्या पसीना आना किसी विशेष समय या गतिविधि के दौरान बढ़ता है?", "en": "Does sweating increase during any specific time or activity?", "category": "activity_related_sweating", "symptom": None},
        {"hi": "क्या आपको रात में अधिक पसीना आता है?", "en": "Are you sweating excessively at night?", "category": "night_time_sweating", "symptom": "night sweats"},
        {"hi": "क्या पसीना आना आपको किसी विशेष अंग या शरीर के हिस्से में हो रहा है?", "en": "Is the sweating occurring in any specific part or area of your body?", "category": "localized_sweating", "symptom": None},
        {"hi": "क्या पसीना आना के साथ आपको कोई अन्य लक्षण भी हैं?", "en": "Are there any other symptoms along with sweating?", "category": "other_symptoms", "symptom": None},
        {"hi": "क्या पसीना आना किसी विशेष दवा के सेवन के कारण हो रहा है?", "en": "Is the sweating caused by taking any specific medication?", "category": "medication_related_sweating", "symptom": None},
        {"hi": "क्या आपको पसीना आना के कारण कोई अन्य स्वास्थ्य समस्याएँ हो रही हैं?", "en": "Are you experiencing any other health issues due to sweating?", "category": "health_issues_with_sweating", "symptom": None}
    ],

    'dark urine': [
        {"hi": "क्या आपका पेशाब गहरा रंग का हो गया है?", "en": "Has your urine become dark-colored?", "category": "dark_urine", "symptom": "dark urine"},
        {"hi": "क्या गहरे पेशाब के साथ आपको कोई अन्य लक्षण भी महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with dark urine?", "category": "other_symptoms_with_dark_urine", "symptom": None},
        {"hi": "क्या आपका पेशाब सामान्य से अधिक है?", "en": "Is your urine output more than usual?", "category": "increased_urine_output", "symptom": "frequent urination"},
        {"hi": "क्या आपको पेशाब के साथ कोई दर्द भी हो रहा है?", "en": "Are you experiencing any pain while urinating?", "category": "pain_with_dark_urine", "symptom": "urinary pain"},
        {"hi": "क्या आपके पेशाब में खून की लकीरें आ रही हैं?", "en": "Are you noticing blood streaks in your urine?", "category": "blood_streaks_in_urine", "symptom": "blood in urine"},
        {"hi": "क्या गहरे पेशाब के कारण आपकी त्वचा में कोई परिवर्तन आ रहा है?", "en": "Is there any change in your skin due to dark urine?", "category": "skin_changes_with_dark_urine", "symptom": "skin discoloration"},
        {"hi": "क्या आपका पेशाब गहरा रंग होने के कारण आपको थकान महसूस हो रही है?", "en": "Are you feeling fatigued due to dark-colored urine?", "category": "fatigue_with_dark_urine", "symptom": "fatigue"}
    ],

    'light-colored stools': [
        {"hi": "क्या आपके मल का रंग हल्का हो गया है?", "en": "Has your stool become light-colored?", "category": "light_colored_stools", "symptom": "light-colored stools"},
        {"hi": "क्या हल्के रंग के मल के साथ आपको पेट में दर्द भी हो रहा है?", "en": "Are you experiencing abdominal pain along with light-colored stools?", "category": "abdominal_pain_with_light_stools", "symptom": "abdominal pain"},
        {"hi": "क्या आपके मल में कोई अन्य परिवर्तन आ रहा है?", "en": "Are you noticing any other changes in your stool?", "category": "other_changes_with_light_stools", "symptom": None},
        {"hi": "क्या आपके मल में कोई रक्त है?", "en": "Is there any blood in your stool?", "category": "blood_in_stool", "symptom": "blood in stool"},
        {"hi": "क्या आपको मल त्यागने में कठिनाई हो रही है?", "en": "Are you having difficulty in passing stool?", "category": "difficulty_passing_stool", "symptom": "constipation"},
        {"hi": "क्या हल्के रंग के मल के साथ आपको उल्टी भी हो रही है?", "en": "Are you experiencing vomiting along with light-colored stools?", "category": "vomiting_with_light_stools", "symptom": "vomiting"},
        {"hi": "क्या आपके मल त्यागने के साथ आपको पसीना आ रहा है?", "en": "Are you sweating while passing stool?", "category": "sweating_with_light_stools", "symptom": "sweating"}
    ],

    'blood in urine': [
        {"hi": "क्या आपको पेशाब में खून दिखाई दे रहा है?", "en": "Are you noticing blood in your urine?", "category": "blood_in_urine", "symptom": "blood in urine"},
        {"hi": "क्या खून की मात्रा बढ़ रही है?", "en": "Is the amount of blood in your urine increasing?", "category": "increasing_blood_in_urine", "symptom": None},
        {"hi": "क्या खून आने के साथ आपको पेशाब में दर्द हो रहा है?", "en": "Are you experiencing pain while urinating along with blood in urine?", "category": "pain_with_blood_in_urine", "symptom": "urinary pain"},
        {"hi": "क्या खून आने के साथ आपको कमजोरी भी महसूस हो रही है?", "en": "Are you feeling weak along with blood in your urine?", "category": "weakness_with_blood_in_urine", "symptom": "weakness"},
        {"hi": "क्या खून आने के कारण आपकी त्वचा में कोई परिवर्तन आ रहा है?", "en": "Is there any change in your skin due to blood in urine?", "category": "skin_changes_with_blood_in_urine", "symptom": "skin discoloration"},
        {"hi": "क्या खून आने के साथ आपको बुखार भी है?", "en": "Do you have a fever along with blood in urine?", "category": "fever_with_blood_in_urine", "symptom": "fever"},
        {"hi": "क्या खून आने के साथ आपको पसीना भी आ रहा है?", "en": "Are you sweating along with blood in urine?", "category": "sweating_with_blood_in_urine", "symptom": "sweating"}
    ],

    'blood in stool': [
        {"hi": "क्या आपके मल में खून दिखाई दे रहा है?", "en": "Are you noticing blood in your stool?", "category": "blood_in_stool", "symptom": "blood in stool"},
        {"hi": "क्या खून का रंग गहरा है या हल्का?", "en": "Is the blood in your stool dark or light-colored?", "category": "blood_color_in_stool", "symptom": None},
        {"hi": "क्या खून आने के साथ आपको पेट में दर्द हो रहा है?", "en": "Are you experiencing abdominal pain along with blood in stool?", "category": "abdominal_pain_with_blood_in_stool", "symptom": "abdominal pain"},
        {"hi": "क्या खून आने के कारण आपको कमजोरी महसूस हो रही है?", "en": "Are you feeling weak due to blood in your stool?", "category": "weakness_with_blood_in_stool", "symptom": "weakness"},
        {"hi": "क्या खून आने के साथ आपके मल त्यागने की आदत बदल गई है?", "en": "Has your bowel movement pattern changed along with blood in stool?", "category": "bowel_movement_changes_with_blood_in_stool", "symptom": "constipation"},
        {"hi": "क्या खून आने के साथ आपको बुखार भी है?", "en": "Do you have a fever along with blood in stool?", "category": "fever_with_blood_in_stool", "symptom": "fever"},
        {"hi": "क्या खून आने के कारण आपकी त्वचा में कोई परिवर्तन आ रहा है?", "en": "Is there any change in your skin due to blood in stool?", "category": "skin_changes_with_blood_in_stool", "symptom": "skin discoloration"}
    ],

    'frequent infections': [
        {"hi": "क्या आपको बार-बार संक्रमण हो रहे हैं?", "en": "Are you experiencing frequent infections?", "category": "frequent_infections", "symptom": "frequent infections"},
        {"hi": "क्या बार-बार होने वाले संक्रमणों के साथ आपको कोई अन्य लक्षण भी महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with frequent infections?", "category": "other_symptoms_with_frequent_infections", "symptom": None},
        {"hi": "क्या आपको संक्रमण होने के बाद तेजी से ठीक होने में कठिनाई हो रही है?", "en": "Are you having difficulty recovering quickly after infections?", "category": "delayed_recovery_with_infections", "symptom": "delayed healing"},
        {"hi": "क्या संक्रमण के प्रकार में कोई विशेष बदलाव आया है?", "en": "Has there been any specific change in the types of infections you are getting?", "category": "change_in_infection_types", "symptom": None},
        {"hi": "क्या आपको बार-बार होने वाले संक्रमणों के कारण थकान महसूस हो रही है?", "en": "Are you feeling fatigued due to frequent infections?", "category": "fatigue_with_frequent_infections", "symptom": "fatigue"},
        {"hi": "क्या आपको संक्रमण के साथ सूजन भी हो रही है?", "en": "Are you experiencing any swelling along with infections?", "category": "swelling_with_infections", "symptom": "swelling"},
        {"hi": "क्या आपको संक्रमण के कारण त्वचा में कोई परिवर्तन आ रहा है?", "en": "Are there any changes in your skin due to infections?", "category": "skin_changes_with_infections", "symptom": "skin discoloration"}
    ],

    'delayed healing': [
        {"hi": "क्या आपके घाव या चोटों का ठीक होने में समय अधिक लग रहा है?", "en": "Are your wounds or injuries taking longer to heal?", "category": "delayed_healing", "symptom": "delayed healing"},
        {"hi": "क्या ठीक होने में देरी के साथ आपको दर्द भी हो रहा है?", "en": "Are you experiencing pain along with delayed healing?", "category": "pain_with_delayed_healing", "symptom": "pain"},
        {"hi": "क्या आपके घावों में कोई संक्रमण भी हो रही है?", "en": "Are your wounds getting infected while healing?", "category": "infection_with_delayed_healing", "symptom": "infection"},
        {"hi": "क्या ठीक होने में देरी के कारण आपकी त्वचा में कोई परिवर्तन आ रहा है?", "en": "Is there any change in your skin due to delayed healing?", "category": "skin_changes_with_delayed_healing", "symptom": "skin discoloration"},
        {"hi": "क्या आपको घावों के ठीक होने में किसी विशेष दवा का सेवन करना पड़ रहा है?", "en": "Are you taking any specific medication for delayed healing of wounds?", "category": "medication_with_delayed_healing", "symptom": None},
        {"hi": "क्या आपके घाव या चोटों के ठीक होने में कोई विशेष कारण है?", "en": "Is there any specific reason for the delayed healing of your wounds or injuries?", "category": "specific_cause_delayed_healing", "symptom": None},
        {"hi": "क्या आपको घावों के ठीक होने के दौरान कमजोरी महसूस हो रही है?", "en": "Are you feeling weak during the healing of your wounds?", "category": "weakness_with_delayed_healing", "symptom": "weakness"}
    ],

    'excessive thirst': [
        {"hi": "क्या आपको अत्यधिक प्यास लग रही है?", "en": "Are you feeling excessively thirsty?", "category": "excessive_thirst", "symptom": "excessive thirst"},
        {"hi": "क्या अत्यधिक प्यास के साथ आपको बार-बार पेशाब आ रहा है?", "en": "Are you urinating frequently along with excessive thirst?", "category": "frequent_urination_with_thirst", "symptom": "frequent urination"},
        {"hi": "क्या अत्यधिक प्यास के कारण आप पर्याप्त पानी पी रहे हैं?", "en": "Are you drinking enough water due to excessive thirst?", "category": "hydration_with_thirst", "symptom": "dehydration"},
        {"hi": "क्या अत्यधिक प्यास के साथ आपको कमजोरी भी महसूस हो रही है?", "en": "Are you feeling weak along with excessive thirst?", "category": "weakness_with_thirst", "symptom": "weakness"},
        {"hi": "क्या अत्यधिक प्यास के साथ आपके शरीर में कोई अन्य परिवर्तन हो रहा है?", "en": "Are there any other changes in your body along with excessive thirst?", "category": "other_changes_with_thirst", "symptom": None},
        {"hi": "क्या आपकी डाइट में कोई विशेष बदलाव हुआ है जिससे आपको अत्यधिक प्यास लग रही है?", "en": "Has there been any specific change in your diet causing excessive thirst?", "category": "diet_changes_with_thirst", "symptom": None},
        {"hi": "क्या आपको अत्यधिक प्यास के साथ वजन कम हो रहा है?", "en": "Are you losing weight along with excessive thirst?", "category": "weight_loss_with_thirst", "symptom": "weight loss"}
    ],

    'dehydration': [
        {"hi": "क्या आपको शरीर से पानी की कमी महसूस हो रही है?", "en": "Are you feeling dehydrated?", "category": "dehydration", "symptom": "dehydration"},
        {"hi": "क्या आपको प्यास लगी हुई है?", "en": "Are you feeling thirsty?", "category": "thirst", "symptom": "thirst"},
        {"hi": "क्या आपका पेशाब कम आ रहा है और रंग गहरा हो गया है?", "en": "Is your urine output reduced and dark-colored?", "category": "reduced_dark_urine", "symptom": "dark urine"},
        {"hi": "क्या आपको सिरदर्द या चक्कर आ रहे हैं?", "en": "Are you experiencing headaches or dizziness?", "category": "headache_dizziness_with_dehydration", "symptom": "headache"},
        {"hi": "क्या आपको शरीर में सूजन महसूस हो रही है?", "en": "Are you feeling swelling in your body?", "category": "swelling_with_dehydration", "symptom": "swelling"},
        {"hi": "क्या आपको पसीना आ रहा है या त्वचा सूखी हो गई है?", "en": "Are you sweating or is your skin dry?", "category": "sweating_dry_skin_with_dehydration", "symptom": "sweating"},
        {"hi": "क्या आपको थकान महसूस हो रही है?", "en": "Are you feeling fatigued?", "category": "fatigue_with_dehydration", "symptom": "fatigue"}
    ],

    'skin burn': [
        {"hi": "क्या आपको त्वचा पर जलन या दर्द महसूस हो रहा है?", "en": "Are you feeling burning or pain on your skin?", "category": "burning_pain_with_skin_burn", "symptom": "burning"},
        {"hi": "क्या त्वचा पर जलने के कारण सूजन हो रही है?", "en": "Is there any swelling due to the skin burn?", "category": "swelling_with_skin_burn", "symptom": "swelling"},
        {"hi": "क्या आपको त्वचा पर दाने या फफोले हो रहे हैं?", "en": "Are you developing blisters or bumps on your skin?", "category": "blisters_bumps_with_skin_burn", "symptom": "skin lesions"},
        {"hi": "क्या त्वचा पर जलने के बाद त्वचा लाल हो गई है?", "en": "Has your skin turned red after the burn?", "category": "redness_with_skin_burn", "symptom": "redness"},
        {"hi": "क्या त्वचा पर जलने के साथ कोई अन्य लक्षण भी हैं?", "en": "Are there any other symptoms along with the skin burn?", "category": "other_symptoms_with_skin_burn", "symptom": None},
        {"hi": "क्या त्वचा पर जलने के कारण आपको दर्द में वृद्धि हो रही है?", "en": "Is the pain increasing due to the skin burn?", "category": "pain_increase_with_skin_burn", "symptom": "pain"},
        {"hi": "क्या त्वचा पर जलने के कारण कोई संक्रमण हो गया है?", "en": "Has the skin burn led to any infection?", "category": "infection_with_skin_burn", "symptom": "infection"}
    ],

    'sweating': [
        {"hi": "क्या आपको पसीना आना सामान्य से अधिक हो रहा है?", "en": "Are you sweating more than usual?", "category": "excessive_sweating", "symptom": "sweating"},
        {"hi": "क्या पसीना आना किसी विशेष समय पर अधिक होता है?", "en": "Does sweating occur more frequently at any specific time?", "category": "time_related_sweating", "symptom": None},
        {"hi": "क्या पसीना आना के साथ कोई अन्य लक्षण भी हैं?", "en": "Are there any other symptoms along with sweating?", "category": "other_symptoms_with_sweating", "symptom": None},
        {"hi": "क्या आपको पसीना आना के कारण किसी विशेष गतिविधि के दौरान कठिनाई हो रही है?", "en": "Are you experiencing difficulty during any specific activity due to sweating?", "category": "activity_related_sweating", "symptom": None},
        {"hi": "क्या पसीना आना के साथ आपको त्वचा में कोई परिवर्तन हो रहा है?", "en": "Are you noticing any changes in your skin due to sweating?", "category": "skin_changes_with_sweating", "symptom": "skin changes"},
        {"hi": "क्या पसीना आना के कारण आपकी त्वचा सूखी हो गई है?", "en": "Has sweating caused your skin to become dry?", "category": "dry_skin_with_sweating", "symptom": "dry skin"},
        {"hi": "क्या पसीना आना के साथ आपको कोई अन्य स्वास्थ्य समस्याएँ हो रही हैं?", "en": "Are you experiencing any other health issues due to sweating?", "category": "health_issues_with_sweating", "symptom": None}
    ],

    'feeling cold': [
        {"hi": "क्या आपको ठंड लगना सामान्य से अधिक हो रहा है?", "en": "Are you feeling cold more than usual?", "category": "excessive_cold", "symptom": "feeling cold"},
        {"hi": "क्या ठंड महसूस होने के साथ आपको दर्द भी हो रहा है?", "en": "Are you experiencing pain along with feeling cold?", "category": "pain_with_feeling_cold", "symptom": "pain"},
        {"hi": "क्या ठंड महसूस होने के कारण आपको थकान हो रही है?", "en": "Are you feeling fatigued due to feeling cold?", "category": "fatigue_with_feeling_cold", "symptom": "fatigue"},
        {"hi": "क्या आपको ठंड महसूस होने के साथ त्वचा में कोई परिवर्तन हो रहा है?", "en": "Are you noticing any changes in your skin due to feeling cold?", "category": "skin_changes_with_feeling_cold", "symptom": "skin discoloration"},
        {"hi": "क्या ठंड महसूस होने के कारण आपकी नींद प्रभावित हो रही है?", "en": "Is feeling cold affecting your sleep?", "category": "sleep_disturbance_with_feeling_cold", "symptom": "insomnia"},
        {"hi": "क्या ठंड महसूस होने के साथ आपको कोई अन्य लक्षण भी महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with feeling cold?", "category": "other_symptoms_with_feeling_cold", "symptom": None},
        {"hi": "क्या ठंड महसूस होने के कारण आपके शरीर में कोई कमजोरी आ रही है?", "en": "Is feeling cold causing any weakness in your body?", "category": "weakness_with_feeling_cold", "symptom": "weakness"}
    ],

    'double vision': [
        {"hi": "क्या आपकी दृष्टि दोहरी हो रही है लगातार या कभी-कभी?", "en": "Is your vision double continuously or intermittently?", "category": "intermittent_double_vision", "symptom": None},
        {"hi": "क्या दोहरी दृष्टि के साथ आपको सिरदर्द भी हो रहा है?", "en": "Are you experiencing headaches along with double vision?", "category": "headache_with_double_vision", "symptom": "headache"},
        {"hi": "क्या दोहरी दृष्टि किसी विशेष समय या गतिविधि के दौरान बढ़ती है?", "en": "Does your double vision increase during any specific time or activity?", "category": "activity_related_double_vision", "symptom": None},
        {"hi": "क्या आपकी दृष्टि में कोई अन्य परिवर्तन हो रहा है?", "en": "Are there any other changes in your vision?", "category": "other_vision_changes_with_double_vision", "symptom": None},
        {"hi": "क्या दोहरी दृष्टि के साथ आपके आँखों में दर्द भी हो रहा है?", "en": "Are you experiencing eye pain along with double vision?", "category": "eye_pain_with_double_vision", "symptom": "eye pain"},
        {"hi": "क्या दोहरी दृष्टि के कारण आपको चलने-फिरने में कठिनाई हो रही है?", "en": "Are you having difficulty walking due to double vision?", "category": "walking_difficulty_with_double_vision", "symptom": None},
        {"hi": "क्या दोहरी दृष्टि अचानक शुरू हुई है या धीरे-धीरे?", "en": "Did your double vision start suddenly or gradually?", "category": "sudden_graduate_double_vision", "symptom": None}
    ],

    'eye redness': [
        {"hi": "क्या आपकी आँखें लाल हो रही हैं लगातार या कभी-कभी?", "en": "Are your eyes becoming red continuously or intermittently?", "category": "intermittent_eye_redness", "symptom": "eye redness"},
        {"hi": "क्या आँखों में लालिमा के साथ सूजन भी हो रही है?", "en": "Is there any swelling along with redness in your eyes?", "category": "swelling_with_eye_redness", "symptom": "swelling"},
        {"hi": "क्या आँखों में लालिमा के साथ दर्द भी हो रहा है?", "en": "Are you experiencing pain along with redness in your eyes?", "category": "pain_with_eye_redness", "symptom": "eye pain"},
        {"hi": "क्या लालिमा किसी विशेष गतिविधि या समय पर बढ़ती है?", "en": "Does redness in your eyes increase during any specific activity or time?", "category": "activity_time_related_eye_redness", "symptom": None},
        {"hi": "क्या लालिमा के कारण आपकी दृष्टि प्रभावित हो रही है?", "en": "Is the redness in your eyes affecting your vision?", "category": "vision_impact_with_eye_redness", "symptom": "blurred vision"},
        {"hi": "क्या आँखों में लालिमा के साथ पानी आना शुरू हो गया है?", "en": "Have you started experiencing watering of the eyes along with redness?", "category": "watering_with_eye_redness", "symptom": "eye tearing"},
        {"hi": "क्या लालिमा के साथ आपकी आँखों में खुजली या जलन हो रही है?", "en": "Are you experiencing itching or burning sensations in your eyes along with redness?", "category": "itching_burning_with_eye_redness", "symptom": "itching"}
    ],

    'eye discharge': [
        {"hi": "क्या आपकी आँखों से अधिक मात्रा में स्राव आ रहा है?", "en": "Are you experiencing excessive discharge from your eyes?", "category": "excessive_eye_discharge", "symptom": "eye discharge"},
        {"hi": "क्या आँखों में स्राव के साथ सूजन भी है?", "en": "Is there any swelling along with discharge in your eyes?", "category": "swelling_with_eye_discharge", "symptom": "swelling"},
        {"hi": "क्या आँखों में स्राव के साथ खुजली या जलन हो रही है?", "en": "Are you experiencing itching or burning sensations in your eyes along with discharge?", "category": "itching_burning_with_eye_discharge", "symptom": "itching"},
        {"hi": "क्या आँखों में स्राव के कारण आपकी दृष्टि प्रभावित हो रही है?", "en": "Is the discharge in your eyes affecting your vision?", "category": "vision_impact_with_eye_discharge", "symptom": "blurred vision"},
        {"hi": "क्या स्राव में रंग में कोई परिवर्तन आया है?", "en": "Has there been any change in the color of the discharge?", "category": "discharge_color_change", "symptom": None},
        {"hi": "क्या आँखों में स्राव के साथ कोई अन्य लक्षण भी हैं?", "en": "Are there any other symptoms along with eye discharge?", "category": "other_symptoms_with_eye_discharge", "symptom": None},
        {"hi": "क्या स्राव के कारण आपकी आँखों में सूजन हो रही है?", "en": "Is there any swelling in your eyes due to discharge?", "category": "swelling_with_eye_discharge", "symptom": "swelling"}
    ],

    'ear discharge': [
        {"hi": "क्या आपके कान से स्राव आ रहा है?", "en": "Are you experiencing discharge from your ears?", "category": "ear_discharge", "symptom": "ear discharge"},
        {"hi": "क्या स्राव के साथ कान में दर्द भी हो रहा है?", "en": "Are you experiencing pain in your ears along with discharge?", "category": "pain_with_ear_discharge", "symptom": "ear pain"},
        {"hi": "क्या स्राव का रंग में कोई परिवर्तन आया है?", "en": "Has there been any change in the color of the discharge?", "category": "discharge_color_change_ear", "symptom": None},
        {"hi": "क्या स्राव के कारण कान में सूजन हो रही है?", "en": "Is there any swelling in your ears due to discharge?", "category": "swelling_with_ear_discharge", "symptom": "swelling"},
        {"hi": "क्या स्राव के साथ आपको सुनने में कठिनाई हो रही है?", "en": "Are you having difficulty hearing along with ear discharge?", "category": "hearing_difficulty_with_ear_discharge", "symptom": "hearing loss"},
        {"hi": "क्या स्राव के कारण कान में खुजली हो रही है?", "en": "Are you experiencing itching in your ears due to discharge?", "category": "itching_with_ear_discharge", "symptom": "itching"},
        {"hi": "क्या स्राव के साथ आपको कोई अन्य लक्षण भी महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with ear discharge?", "category": "other_symptoms_with_ear_discharge", "symptom": None}
    ],

    'hearing loss': [
        {"hi": "क्या आपको सुनने में कठिनाई हो रही है लगातार या कभी-कभी?", "en": "Are you experiencing difficulty hearing continuously or intermittently?", "category": "intermittent_hearing_loss", "symptom": None},
        {"hi": "क्या सुनने में कमी किसी विशेष समय या स्थिति में होती है?", "en": "Does the hearing loss occur more during any specific time or situation?", "category": "time_situation_related_hearing_loss", "symptom": None},
        {"hi": "क्या सुनने में कमी के साथ आपको कान में दर्द भी हो रहा है?", "en": "Are you experiencing ear pain along with hearing loss?", "category": "ear_pain_with_hearing_loss", "symptom": "ear pain"},
        {"hi": "क्या सुनने में कमी के कारण आपकी दैनिक गतिविधियाँ प्रभावित हो रही हैं?", "en": "Are your daily activities being affected due to hearing loss?", "category": "daily_activity_impact_with_hearing_loss", "symptom": None},
        {"hi": "क्या आपको कान में कोई स्राव या जलन महसूस हो रही है?", "en": "Are you feeling any discharge or irritation in your ears?", "category": "discharge_irritation_with_hearing_loss", "symptom": "ear discharge"},
        {"hi": "क्या सुनने में कमी के साथ आपका संतुलन भी प्रभावित हो रहा है?", "en": "Is your balance being affected along with hearing loss?", "category": "balance_impact_with_hearing_loss", "symptom": "balance problems"},
        {"hi": "क्या सुनने में कमी के कारण आपको सामाजिक स्थितियों में कठिनाई हो रही है?", "en": "Are you facing difficulties in social situations due to hearing loss?", "category": "social_difficulty_with_hearing_loss", "symptom": None}
    ],

    'balance problems': [
        {"hi": "क्या आपको संतुलन बिगड़ने की समस्या हो रही है?", "en": "Are you experiencing balance problems?", "category": "balance_problems", "symptom": "balance problems"},
        {"hi": "क्या संतुलन बिगड़ने के साथ चक्कर आना भी हो रहा है?", "en": "Are you experiencing dizziness along with balance problems?", "category": "dizziness_with_balance_problems", "symptom": "dizziness"},
        {"hi": "क्या संतुलन बिगड़ने की समस्या किसी विशेष समय या स्थिति में होती है?", "en": "Do balance problems occur more during any specific time or situation?", "category": "time_situation_related_balance_problems", "symptom": None},
        {"hi": "क्या संतुलन बिगड़ने के साथ आपको कोई अन्य लक्षण भी महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with balance problems?", "category": "other_symptoms_with_balance_problems", "symptom": None},
        {"hi": "क्या संतुलन बिगड़ने के कारण आपकी दैनिक गतिविधियाँ प्रभावित हो रही हैं?", "en": "Are your daily activities being affected due to balance problems?", "category": "daily_activity_impact_with_balance_problems", "symptom": None},
        {"hi": "क्या संतुलन बिगड़ने के साथ कान में कोई समस्या है?", "en": "Do you have any ear problems along with balance issues?", "category": "ear_problems_with_balance_problems", "symptom": "ear discharge"},
        {"hi": "क्या संतुलन बिगड़ने के कारण आपको चलने-फिरने में कठिनाई हो रही है?", "en": "Are you having difficulty walking due to balance problems?", "category": "walking_difficulty_with_balance_problems", "symptom": None}
    ],

    'taste changes': [
        {"hi": "क्या आपके स्वाद में कोई बदलाव आया है?", "en": "Have you noticed any changes in your taste?", "category": "taste_changes", "symptom": "taste changes"},
        {"hi": "क्या स्वाद में बदलाव के साथ आप कुछ खास चीज़ों का स्वाद नहीं ले पा रहे हैं?", "en": "Are you unable to taste certain specific things along with taste changes?", "category": "specific_taste_changes", "symptom": None},
        {"hi": "क्या आपको स्वाद में कमी या बढ़ोतरी महसूस हो रही है?", "en": "Are you experiencing a decrease or increase in taste?", "category": "decrease_increase_taste", "symptom": None},
        {"hi": "क्या स्वाद में बदलाव के साथ आपकी भूख प्रभावित हो रही है?", "en": "Is your appetite being affected due to taste changes?", "category": "appetite_impact_with_taste_changes", "symptom": "decreased appetite"},
        {"hi": "क्या स्वाद में बदलाव के कारण आपको खाना पसंद नहीं आता?", "en": "Are you not liking food due to taste changes?", "category": "food_dislike_with_taste_changes", "symptom": "decreased appetite"},
        {"hi": "क्या आपको स्वाद में बदलाव के साथ कोई अन्य लक्षण भी महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with taste changes?", "category": "other_symptoms_with_taste_changes", "symptom": None},
        {"hi": "क्या स्वाद में बदलाव अचानक शुरू हुआ है या धीरे-धीरे?", "en": "Did your taste changes start suddenly or gradually?", "category": "sudden_graduate_taste_changes", "symptom": None}
    ],

    'smell changes': [
        {"hi": "क्या आपकी गंध में कोई बदलाव आया है?", "en": "Have you noticed any changes in your sense of smell?", "category": "smell_changes", "symptom": "smell changes"},
        {"hi": "क्या गंध में बदलाव के साथ आपकी भूख प्रभावित हो रही है?", "en": "Is your appetite being affected due to changes in smell?", "category": "appetite_impact_with_smell_changes", "symptom": "decreased appetite"},
        {"hi": "क्या गंध में बदलाव के कारण आप कुछ खास चीजों की गंध नहीं ले पा रहे हैं?", "en": "Are you unable to detect the smell of certain specific things due to smell changes?", "category": "specific_smell_changes", "symptom": None},
        {"hi": "क्या आपको गंध में बदलाव के साथ कोई अन्य लक्षण भी महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with smell changes?", "category": "other_symptoms_with_smell_changes", "symptom": None},
        {"hi": "क्या गंध में बदलाव अचानक शुरू हुआ है या धीरे-धीरे?", "en": "Did your smell changes start suddenly or gradually?", "category": "sudden_graduate_smell_changes", "symptom": None},
        {"hi": "क्या गंध में बदलाव के साथ आपके मूड में भी कोई परिवर्तन आया है?", "en": "Has your mood changed along with smell changes?", "category": "mood_changes_with_smell_changes", "symptom": "depression"},
        {"hi": "क्या गंध में बदलाव के कारण आपको खाने में कोई समस्या हो रही है?", "en": "Are you having any issues with eating due to smell changes?", "category": "eating_issues_with_smell_changes", "symptom": "difficulty swallowing"}
    ],

    'rapid breathing': [
        {"hi": "क्या आपकी सांसें तेजी से आ रही हैं?", "en": "Are your breaths coming rapidly?", "category": "rapid_breathing", "symptom": "rapid breathing"},
        {"hi": "क्या तेजी से सांस लेने के साथ कोई अन्य लक्षण भी हैं?", "en": "Are there any other symptoms along with rapid breathing?", "category": "other_symptoms_with_rapid_breathing", "symptom": None},
        {"hi": "क्या तेजी से सांस लेने के कारण आपको सांस लेने में कठिनाई हो रही है?", "en": "Are you having difficulty breathing due to rapid breathing?", "category": "difficulty_breathing_with_rapid_breathing", "symptom": "shortness of breath"},
        {"hi": "क्या तेजी से सांस लेने के साथ आपका दिल भी तेज धड़क रहा है?", "en": "Is your heart beating faster along with rapid breathing?", "category": "heart_rate_increase_with_rapid_breathing", "symptom": "irregular heartbeat"},
        {"hi": "क्या तेजी से सांस लेने के कारण आपको चक्कर आ रहे हैं?", "en": "Are you experiencing dizziness due to rapid breathing?", "category": "dizziness_with_rapid_breathing", "symptom": "dizziness"},
        {"hi": "क्या तेजी से सांस लेने के साथ आपको पसीना आ रहा है?", "en": "Are you sweating along with rapid breathing?", "category": "sweating_with_rapid_breathing", "symptom": "sweating"},
        {"hi": "क्या तेजी से सांस लेने का कारण कोई विशेष गतिविधि है?", "en": "Is there any specific activity causing your rapid breathing?", "category": "activity_related_rapid_breathing", "symptom": None}
    ],

    'irregular heartbeat': [
        {"hi": "क्या आपके दिल की धड़कन अनियमित हो गई है?", "en": "Has your heartbeat become irregular?", "category": "irregular_heartbeat", "symptom": "irregular heartbeat"},
        {"hi": "क्या अनियमित धड़कन के साथ आपको चक्कर आ रहे हैं?", "en": "Are you experiencing dizziness along with an irregular heartbeat?", "category": "dizziness_with_irregular_heartbeat", "symptom": "dizziness"},
        {"hi": "क्या अनियमित धड़कन के साथ आपको थकान भी हो रही है?", "en": "Are you feeling fatigued along with an irregular heartbeat?", "category": "fatigue_with_irregular_heartbeat", "symptom": "fatigue"},
        {"hi": "क्या आपके दिल की धड़कन तेज हो गई है?", "en": "Has your heartbeat become faster?", "category": "fast_heartbeat_with_irregular_heartbeat", "symptom": "heart palpitations"},
        {"hi": "क्या अनियमित धड़कन के कारण आपको सांस लेने में कठिनाई हो रही है?", "en": "Are you having difficulty breathing due to an irregular heartbeat?", "category": "breathing_difficulty_with_irregular_heartbeat", "symptom": "shortness of breath"},
        {"hi": "क्या अनियमित धड़कन के साथ आपको कोई अन्य लक्षण भी महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with an irregular heartbeat?", "category": "other_symptoms_with_irregular_heartbeat", "symptom": None},
        {"hi": "क्या अनियमित धड़कन अचानक शुरू हुई है या धीरे-धीरे?", "en": "Did your irregular heartbeat start suddenly or gradually?", "category": "sudden_graduate_irregular_heartbeat", "symptom": None}
    ],

    'neck pain': [
        {"hi": "क्या आपकी गर्दन में दर्द लगातार है या आता-जाता है?", "en": "Is your neck pain constant or does it come and go?", "category": "intermittent_neck_pain", "symptom": None},
        {"hi": "क्या गर्दन का दर्द किसी विशेष गतिविधि के दौरान बढ़ता है?", "en": "Does your neck pain increase during any specific activity?", "category": "activity_related_neck_pain", "symptom": None},
        {"hi": "क्या गर्दन के दर्द के साथ सिरदर्द भी हो रहा है?", "en": "Are you experiencing headaches along with neck pain?", "category": "headache_with_neck_pain", "symptom": "headache"},
        {"hi": "क्या गर्दन में दर्द के साथ कोई सूजन भी है?", "en": "Is there any swelling along with neck pain?", "category": "swelling_with_neck_pain", "symptom": "swelling"},
        {"hi": "क्या गर्दन के दर्द के कारण आपकी गतिशीलता प्रभावित हो रही है?", "en": "Is your mobility being affected due to neck pain?", "category": "mobility_impact_with_neck_pain", "symptom": None},
        {"hi": "क्या गर्दन में दर्द के साथ किसी विशेष प्रकार का दर्द हो रहा है?", "en": "Are you experiencing any specific type of pain in your neck?", "category": "specific_pain_with_neck_pain", "symptom": "pain"},
        {"hi": "क्या गर्दन का दर्द अचानक शुरू हुआ है या धीरे-धीरे?", "en": "Did your neck pain start suddenly or gradually?", "category": "sudden_graduate_neck_pain", "symptom": None}
    ],

    'sinus pressure': [
        {"hi": "क्या आपको साइनस में दबाव महसूस हो रहा है?", "en": "Are you feeling pressure in your sinuses?", "category": "sinus_pressure", "symptom": "sinus pressure"},
        {"hi": "क्या साइनस दबाव के साथ सिरदर्द भी हो रहा है?", "en": "Are you experiencing headaches along with sinus pressure?", "category": "headache_with_sinus_pressure", "symptom": "headache"},
        {"hi": "क्या साइनस दबाव के साथ आपको नाक बंद होना भी हो रहा है?", "en": "Are you also experiencing a blocked nose along with sinus pressure?", "category": "blocked_nose_with_sinus_pressure", "symptom": "nasal congestion"},
        {"hi": "क्या साइनस दबाव के कारण आपकी आँखों में सूजन हो रही है?", "en": "Is sinus pressure causing swelling in your eyes?", "category": "eye_swelling_with_sinus_pressure", "symptom": "swelling"},
        {"hi": "क्या साइनस दबाव के साथ आपकी आवाज़ में परिवर्तन आया है?", "en": "Has your voice changed along with sinus pressure?", "category": "voice_changes_with_sinus_pressure", "symptom": "voice changes"},
        {"hi": "क्या साइनस दबाव के कारण आपको सांस लेने में कठिनाई हो रही है?", "en": "Are you having difficulty breathing due to sinus pressure?", "category": "breathing_difficulty_with_sinus_pressure", "symptom": "shortness of breath"},
        {"hi": "क्या साइनस दबाव के साथ आपको चक्कर आ रहे हैं?", "en": "Are you experiencing dizziness along with sinus pressure?", "category": "dizziness_with_sinus_pressure", "symptom": "dizziness"}
    ],

    'sinus headache': [
        {"hi": "क्या आपकी सिरदर्द साइनस से संबंधित है?", "en": "Is your headache related to your sinuses?", "category": "sinus_related_headache", "symptom": "headache"},
        {"hi": "क्या सिरदर्द के साथ साइनस में दबाव महसूस हो रहा है?", "en": "Are you feeling pressure in your sinuses along with the headache?", "category": "sinus_pressure_with_headache", "symptom": "sinus pressure"},
        {"hi": "क्या सिरदर्द के साथ नाक बंद होना भी हो रहा है?", "en": "Are you also experiencing a blocked nose along with the headache?", "category": "blocked_nose_with_headache", "symptom": "nasal congestion"},
        {"hi": "क्या सिरदर्द के साथ आंखों में सूजन हो रही है?", "en": "Is there any swelling in your eyes along with the headache?", "category": "eye_swelling_with_headache", "symptom": "swelling"},
        {"hi": "क्या सिरदर्द के साथ आपकी आवाज़ में कोई बदलाव आया है?", "en": "Has your voice changed along with the headache?", "category": "voice_changes_with_headache", "symptom": "voice changes"},
        {"hi": "क्या सिरदर्द के कारण आपकी गतिशीलता प्रभावित हो रही है?", "en": "Is your mobility being affected due to the headache?", "category": "mobility_impact_with_headache", "symptom": None},
        {"hi": "क्या सिरदर्द अचानक शुरू हुआ है या धीरे-धीरे?", "en": "Did your headache start suddenly or gradually?", "category": "sudden_graduate_headache", "symptom": None}
    ],

    'muscle spasms': [
        {"hi": "क्या आपको मांसपेशियों में अचानक स्पैसम्स महसूस हो रहे हैं?", "en": "Are you experiencing sudden muscle spasms?", "category": "sudden_muscle_spasms", "symptom": "muscle spasms"},
        {"hi": "क्या मांसपेशियों में स्पैसम्स लगातार हो रहे हैं या कभी-कभी?", "en": "Are muscle spasms occurring continuously or intermittently?", "category": "intermittent_muscle_spasms", "symptom": None},
        {"hi": "क्या स्पैसम्स के साथ दर्द भी हो रहा है?", "en": "Are you experiencing pain along with muscle spasms?", "category": "pain_with_muscle_spasms", "symptom": "pain"},
        {"hi": "क्या मांसपेशियों में स्पैसम्स किसी विशेष गतिविधि के दौरान बढ़ते हैं?", "en": "Do muscle spasms increase during any specific activity?", "category": "activity_related_muscle_spasms", "symptom": None},
        {"hi": "क्या स्पैसम्स के कारण आपकी गतिशीलता प्रभावित हो रही है?", "en": "Are your mobility being affected due to muscle spasms?", "category": "mobility_impact_with_muscle_spasms", "symptom": None},
        {"hi": "क्या मांसपेशियों में स्पैसम्स के साथ सूजन भी हो रही है?", "en": "Is there any swelling along with muscle spasms?", "category": "swelling_with_muscle_spasms", "symptom": "swelling"},
        {"hi": "क्या स्पैसम्स के साथ आपको कोई अन्य लक्षण भी महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with muscle spasms?", "category": "other_symptoms_with_muscle_spasms", "symptom": None}
    ],

    'muscle strains': [
        {"hi": "क्या आपको मांसपेशियों में खिंचाव या तनाव महसूस हो रहा है?", "en": "Are you feeling any muscle strain or tension?", "category": "muscle_strain", "symptom": "muscle strains"},
        {"hi": "क्या मांसपेशियों में तनाव के साथ दर्द भी हो रहा है?", "en": "Are you experiencing pain along with muscle strain?", "category": "pain_with_muscle_strain", "symptom": "pain"},
        {"hi": "क्या मांसपेशियों में तनाव किसी विशेष गतिविधि के दौरान बढ़ता है?", "en": "Does muscle strain increase during any specific activity?", "category": "activity_related_muscle_strain", "symptom": None},
        {"hi": "क्या मांसपेशियों में तनाव के कारण आपकी गतिशीलता प्रभावित हो रही है?", "en": "Is your mobility being affected due to muscle strain?", "category": "mobility_impact_with_muscle_strain", "symptom": None},
        {"hi": "क्या मांसपेशियों में तनाव के साथ सूजन भी हो रही है?", "en": "Is there any swelling along with muscle strain?", "category": "swelling_with_muscle_strain", "symptom": "swelling"},
        {"hi": "क्या मांसपेशियों में तनाव के साथ कोई अन्य लक्षण भी हैं?", "en": "Are there any other symptoms along with muscle strain?", "category": "other_symptoms_with_muscle_strain", "symptom": None},
        {"hi": "क्या मांसपेशियों में तनाव अचानक शुरू हुआ है या धीरे-धीरे?", "en": "Did your muscle strain start suddenly or gradually?", "category": "sudden_graduate_muscle_strain", "symptom": None}
    ],

    'muscle injuries': [
        {"hi": "क्या आपको किसी मांसपेशी में चोट लगी है?", "en": "Have you injured any muscle?", "category": "muscle_injury", "symptom": "muscle injuries"},
        {"hi": "क्या मांसपेशी में चोट के साथ दर्द भी हो रहा है?", "en": "Are you experiencing pain along with the muscle injury?", "category": "pain_with_muscle_injury", "symptom": "pain"},
        {"hi": "क्या मांसपेशी में चोट के कारण आपकी गतिशीलता प्रभावित हो रही है?", "en": "Is your mobility being affected due to the muscle injury?", "category": "mobility_impact_with_muscle_injury", "symptom": None},
        {"hi": "क्या मांसपेशी में चोट के साथ सूजन भी हो रही है?", "en": "Is there any swelling along with the muscle injury?", "category": "swelling_with_muscle_injury", "symptom": "swelling"},
        {"hi": "क्या मांसपेशी में चोट के कारण आपको कमजोरी महसूस हो रही है?", "en": "Are you feeling weak due to the muscle injury?", "category": "weakness_with_muscle_injury", "symptom": "weakness"},
        {"hi": "क्या मांसपेशी में चोट के साथ कोई अन्य लक्षण भी हैं?", "en": "Are there any other symptoms along with the muscle injury?", "category": "other_symptoms_with_muscle_injury", "symptom": None},
        {"hi": "क्या मांसपेशी में चोट अचानक हुई है या किसी दुर्घटना के बाद?", "en": "Did your muscle injury occur suddenly or after an accident?", "category": "sudden_or_accident_related_muscle_injury", "symptom": None}
    ],

    'skin rash': [
        {"hi": "क्या आपके शरीर पर कोई दाने या चकत्ते हैं?", "en": "Do you have any bumps or spots on your skin?", "category": "bumps_spots_with_skin_rash", "symptom": "skin rash"},
        {"hi": "क्या त्वचा पर लालिमा या सूजन भी है?", "en": "Is there any redness or swelling on your skin along with the rash?", "category": "redness_swelling_with_skin_rash", "symptom": "redness"},
        {"hi": "क्या रैश किसी विशेष स्थान पर ज्यादा हैं?", "en": "Are the rashes more concentrated in any specific area?", "category": "localized_skin_rash", "symptom": None},
        {"hi": "क्या रैश के साथ खुजली या जलन भी हो रही है?", "en": "Are you experiencing itching or burning sensations along with the rash?", "category": "itching_burning_with_skin_rash", "symptom": "itching"},
        {"hi": "क्या रैश समय के साथ फैल रहे हैं या स्थिर हैं?", "en": "Are the rashes spreading over time or are they static?", "category": "spreading_vs_static_skin_rash", "symptom": None},
        {"hi": "क्या आपके रैश के कारण आपकी त्वचा में कोई परिवर्तन हो रहा है?", "en": "Are there any changes in your skin due to the rash?", "category": "skin_changes_with_skin_rash", "symptom": "skin discoloration"},
        {"hi": "क्या रैश अचानक शुरू हुए हैं या धीरे-धीरे?", "en": "Did your rashes start suddenly or gradually?", "category": "sudden_graduate_skin_rash", "symptom": None}
    ],

    'herpes': [
        {"hi": "क्या आपको मुंह या होंठों पर छाले हैं?", "en": "Do you have sores on your mouth or lips?", "category": "mouth_lips_sores_with_herpes", "symptom": "mouth sores"},
        {"hi": "क्या हर्पीज़ के साथ आपके होंठों में सूजन भी है?", "en": "Is there any swelling in your lips along with herpes?", "category": "lip_swelling_with_herpes", "symptom": "swelling"},
        {"hi": "क्या हर्पीज़ के कारण आपकी त्वचा में कोई परिवर्तन हो रहा है?", "en": "Are there any changes in your skin due to herpes?", "category": "skin_changes_with_herpes", "symptom": "skin discoloration"},
        {"hi": "क्या हर्पीज़ के साथ आपको दर्द भी हो रहा है?", "en": "Are you experiencing pain along with herpes?", "category": "pain_with_herpes", "symptom": "pain"},
        {"hi": "क्या हर्पीज़ के कारण आपको किसी विशेष गतिविधि में कठिनाई हो रही है?", "en": "Are you having difficulty in any specific activity due to herpes?", "category": "activity_difficulty_with_herpes", "symptom": None},
        {"hi": "क्या हर्पीज़ के साथ आपको कोई अन्य लक्षण भी महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with herpes?", "category": "other_symptoms_with_herpes", "symptom": None},
        {"hi": "क्या हर्पीज़ अचानक शुरू हुई है या किसी संक्रमण के बाद?", "en": "Did your herpes start suddenly or after an infection?", "category": "sudden_or_infection_related_herpes", "symptom": None}
    ],

    'shingles': [
        {"hi": "क्या आपको त्वचा पर जलन या दर्द महसूस हो रही है?", "en": "Are you feeling burning sensations or pain on your skin?", "category": "burning_pain_with_shingles", "symptom": "burning"},
        {"hi": "क्या त्वचा पर पट्टियां या फफोले हो रहे हैं?", "en": "Are you developing blisters or patches on your skin?", "category": "blisters_patches_with_shingles", "symptom": "skin lesions"},
        {"hi": "क्या दर्द किसी विशेष क्षेत्र में केंद्रित है?", "en": "Is the pain concentrated in any specific area?", "category": "localized_pain_with_shingles", "symptom": None},
        {"hi": "क्या आपको कमजोरी महसूस हो रही है?", "en": "Are you feeling weak?", "category": "weakness_with_shingles", "symptom": "weakness"},
        {"hi": "क्या दर्द के साथ आपको सूजन भी हो रही है?", "en": "Is there any swelling along with the pain?", "category": "swelling_with_shingles", "symptom": "swelling"},
        {"hi": "क्या आपको सिरदर्द या बुखार हो रहा है?", "en": "Are you experiencing headaches or fever?", "category": "headache_fever_with_shingles", "symptom": "headache"},
        {"hi": "क्या दर्द से आपकी नींद प्रभावित हो रही है?", "en": "Is the pain affecting your sleep?", "category": "sleep_disturbance_with_shingles", "symptom": "insomnia"}
    ],

    'warts': [
        {"hi": "क्या आपके शरीर पर वर्ट्स हो रहे हैं?", "en": "Are you developing warts on your body?", "category": "warts", "symptom": "warts"},
        {"hi": "क्या वर्ट्स के साथ कोई दर्द या खुजली हो रही है?", "en": "Are you experiencing any pain or itching along with warts?", "category": "pain_itching_with_warts", "symptom": "itching"},
        {"hi": "क्या वर्ट्स कहीं फैल रहे हैं या स्थिर हैं?", "en": "Are the warts spreading or remaining static?", "category": "spreading_vs_static_warts", "symptom": None},
        {"hi": "क्या वर्ट्स किसी विशेष स्थान पर अधिक हो रहे हैं?", "en": "Are the warts more prevalent in any specific area?", "category": "localized_warts", "symptom": None},
        {"hi": "क्या वर्ट्स के कारण आपकी त्वचा में कोई परिवर्तन हो रहा है?", "en": "Are there any changes in your skin due to warts?", "category": "skin_changes_with_warts", "symptom": "skin discoloration"},
        {"hi": "क्या वर्ट्स के साथ आपको कोई अन्य लक्षण भी महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with warts?", "category": "other_symptoms_with_warts", "symptom": None},
        {"hi": "क्या वर्ट्स अचानक शुरू हुए हैं या किसी संक्रमण के बाद?", "en": "Did your warts start suddenly or after an infection?", "category": "sudden_or_infection_related_warts", "symptom": None}
    ],

    'moles': [
        {"hi": "क्या आपके शरीर पर मौल्स में कोई बदलाव आया है?", "en": "Have there been any changes in your moles?", "category": "mole_changes", "symptom": "moles"},
        {"hi": "क्या मौल्स का आकार, रंग या आकृति बदल गई है?", "en": "Has the size, color, or shape of your moles changed?", "category": "size_color_shape_changes_with_moles", "symptom": None},
        {"hi": "क्या मौल्स से खून आ रहा है या दर्द हो रहा है?", "en": "Are you experiencing bleeding or pain from your moles?", "category": "bleeding_pain_with_moles", "symptom": "bleeding"},
        {"hi": "क्या मौल्स किसी विशेष समय पर अधिक दिखाई देते हैं?", "en": "Do your moles become more noticeable at any specific time?", "category": "time_related_moles", "symptom": None},
        {"hi": "क्या मौल्स के कारण आपकी त्वचा में कोई अन्य परिवर्तन हो रहा है?", "en": "Are there any other changes in your skin due to moles?", "category": "skin_changes_with_moles", "symptom": "skin discoloration"},
        {"hi": "क्या मौल्स अचानक हो गए हैं या धीरे-धीरे?", "en": "Did your moles appear suddenly or gradually?", "category": "sudden_graduate_moles", "symptom": None},
        {"hi": "क्या मौल्स के साथ आपको कोई अन्य लक्षण भी महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with moles?", "category": "other_symptoms_with_moles", "symptom": None}
    ],

    'skin lesions': [
        {"hi": "क्या आपको त्वचा पर घाव या गांठें महसूस हो रही हैं?", "en": "Are you feeling sores or lumps on your skin?", "category": "sores_lumps_with_skin_lesions", "symptom": "skin lesions"},
        {"hi": "क्या त्वचा पर घावों के साथ सूजन भी है?", "en": "Is there any swelling along with sores on your skin?", "category": "swelling_with_skin_lesions", "symptom": "swelling"},
        {"hi": "क्या त्वचा पर घावों के साथ दर्द भी हो रहा है?", "en": "Are you experiencing pain along with sores on your skin?", "category": "pain_with_skin_lesions", "symptom": "pain"},
        {"hi": "क्या त्वचा पर घाव धीरे-धीरे बढ़ रहे हैं या स्थिर हैं?", "en": "Are the sores on your skin increasing gradually or remaining static?", "category": "increasing_vs_static_skin_lesions", "symptom": None},
        {"hi": "क्या त्वचा पर घावों का रंग बदल रहा है?", "en": "Are the sores on your skin changing in color?", "category": "color_changes_with_skin_lesions", "symptom": "skin discoloration"},
        {"hi": "क्या त्वचा पर घावों के साथ खुजली या जलन हो रही है?", "en": "Are you experiencing itching or burning sensations along with sores on your skin?", "category": "itching_burning_with_skin_lesions", "symptom": "itching"},
        {"hi": "क्या त्वचा पर घावों के कारण आपकी त्वचा में कोई अन्य परिवर्तन हो रहा है?", "en": "Are there any other changes in your skin due to sores?", "category": "other_skin_changes_with_skin_lesions", "symptom": None}
    ],

    'skin lumps': [
        {"hi": "क्या आपको त्वचा पर गांठें या गांठे महसूस हो रही हैं?", "en": "Are you feeling lumps or bumps on your skin?", "category": "skin_lumps", "symptom": "skin lumps"},
        {"hi": "क्या त्वचा पर गांठों के साथ सूजन भी है?", "en": "Is there any swelling along with lumps on your skin?", "category": "swelling_with_skin_lumps", "symptom": "swelling"},
        {"hi": "क्या त्वचा पर गांठों के साथ दर्द भी हो रहा है?", "en": "Are you experiencing pain along with lumps on your skin?", "category": "pain_with_skin_lumps", "symptom": "pain"},
        {"hi": "क्या त्वचा पर गांठें स्थिर हैं या बढ़ रही हैं?", "en": "Are the lumps on your skin static or increasing?", "category": "static_increasing_skin_lumps", "symptom": None},
        {"hi": "क्या त्वचा पर गांठों का रंग बदल रहा है?", "en": "Are the lumps on your skin changing in color?", "category": "color_changes_with_skin_lumps", "symptom": "skin discoloration"},
        {"hi": "क्या त्वचा पर गांठों के साथ खुजली या जलन हो रही है?", "en": "Are you experiencing itching or burning sensations along with lumps on your skin?", "category": "itching_burning_with_skin_lumps", "symptom": "itching"},
        {"hi": "क्या त्वचा पर गांठों के कारण आपकी त्वचा में कोई अन्य परिवर्तन हो रहा है?", "en": "Are there any other changes in your skin due to lumps?", "category": "other_skin_changes_with_skin_lumps", "symptom": None}
    ],

    'skin bumps': [
        {"hi": "क्या आपको त्वचा पर उभार या गांठें महसूस हो रही हैं?", "en": "Are you feeling bumps or lumps on your skin?", "category": "skin_bumps", "symptom": "skin bumps"},
        {"hi": "क्या त्वचा पर उभार के साथ सूजन भी है?", "en": "Is there any swelling along with bumps on your skin?", "category": "swelling_with_skin_bumps", "symptom": "swelling"},
        {"hi": "क्या त्वचा पर उभार के साथ दर्द भी हो रहा है?", "en": "Are you experiencing pain along with bumps on your skin?", "category": "pain_with_skin_bumps", "symptom": "pain"},
        {"hi": "क्या त्वचा पर उभार धीरे-धीरे बढ़ रहे हैं या स्थिर हैं?", "en": "Are the bumps on your skin increasing gradually or remaining static?", "category": "increasing_vs_static_skin_bumps", "symptom": None},
        {"hi": "क्या त्वचा पर उभार का रंग बदल रहा है?", "en": "Are the bumps on your skin changing in color?", "category": "color_changes_with_skin_bumps", "symptom": "skin discoloration"},
        {"hi": "क्या त्वचा पर उभार के साथ खुजली या जलन हो रही है?", "en": "Are you experiencing itching or burning sensations along with bumps on your skin?", "category": "itching_burning_with_skin_bumps", "symptom": "itching"},
        {"hi": "क्या त्वचा पर उभार के कारण आपकी त्वचा में कोई अन्य परिवर्तन हो रहा है?", "en": "Are there any other changes in your skin due to bumps?", "category": "other_skin_changes_with_skin_bumps", "symptom": None}
    ],

    'skin cracking': [
        {"hi": "क्या आपकी त्वचा दरार खा रही है?", "en": "Is your skin cracking?", "category": "skin_cracking", "symptom": "skin cracking"},
        {"hi": "क्या दरारों के साथ त्वचा में सूजन भी है?", "en": "Is there any swelling along with skin cracking?", "category": "swelling_with_skin_cracking", "symptom": "swelling"},
        {"hi": "क्या त्वचा की दरारों के साथ खुजली या जलन हो रही है?", "en": "Are you experiencing itching or burning sensations along with skin cracking?", "category": "itching_burning_with_skin_cracking", "symptom": "itching"},
        {"hi": "क्या त्वचा की दरारें किसी विशेष समय पर अधिक होती हैं?", "en": "Do your skin cracks occur more frequently at any specific time?", "category": "time_related_skin_cracking", "symptom": None},
        {"hi": "क्या त्वचा की दरारें स्थिर हैं या बढ़ रही हैं?", "en": "Are your skin cracks static or increasing?", "category": "increasing_vs_static_skin_cracking", "symptom": None},
        {"hi": "क्या त्वचा की दरारों के साथ कोई अन्य लक्षण भी हैं?", "en": "Are there any other symptoms along with skin cracking?", "category": "other_symptoms_with_skin_cracking", "symptom": None},
        {"hi": "क्या त्वचा की दरारें अचानक शुरू हुई हैं या धीरे-धीरे?", "en": "Did your skin cracks start suddenly or gradually?", "category": "sudden_graduate_skin_cracking", "symptom": None}
    ],

    'skin itching': [
        {"hi": "क्या आपकी त्वचा में खुजली लगातार है या कभी-कभी आती है?", "en": "Is the itching on your skin continuous or intermittent?", "category": "intermittent_skin_itching", "symptom": "skin itching"},
        {"hi": "क्या खुजली के साथ त्वचा में लालिमा भी है?", "en": "Is there any redness on your skin along with itching?", "category": "redness_with_skin_itching", "symptom": "redness"},
        {"hi": "क्या खुजली के कारण आपको त्वचा में सूजन हो रही है?", "en": "Is itching causing any swelling on your skin?", "category": "swelling_with_skin_itching", "symptom": "swelling"},
        {"hi": "क्या खुजली आपको सोने में परेशान कर रही है?", "en": "Is itching disturbing your sleep?", "category": "sleep_disturbance_with_skin_itching", "symptom": "insomnia"},
        {"hi": "क्या खुजली के साथ त्वचा में कोई दरार या फफोले हो रहे हैं?", "en": "Are there any cracks or blisters on your skin along with itching?", "category": "cracks_blisters_with_skin_itching", "symptom": "skin lesions"},
        {"hi": "क्या आपकी त्वचा में खुजली के कारण कोई अन्य परिवर्तन हो रहा है?", "en": "Are there any other changes in your skin due to itching?", "category": "skin_changes_with_skin_itching", "symptom": "skin discoloration"},
        {"hi": "क्या खुजली किसी विशेष समय या वातावरण में बढ़ती है?", "en": "Does itching increase during any specific time or environment?", "category": "environment_related_skin_itching", "symptom": None}
    ],

    'skin burning': [
        {"hi": "क्या आपकी त्वचा में जलन महसूस हो रही है?", "en": "Are you feeling burning sensations on your skin?", "category": "skin_burning", "symptom": "skin burning"},
        {"hi": "क्या जलन के साथ त्वचा में सूजन भी है?", "en": "Is there any swelling along with burning sensations on your skin?", "category": "swelling_with_skin_burning", "symptom": "swelling"},
        {"hi": "क्या जलन के कारण आपकी त्वचा लाल हो गई है?", "en": "Has your skin turned red due to burning sensations?", "category": "redness_with_skin_burning", "symptom": "redness"},
        {"hi": "क्या त्वचा की जलन किसी विशेष समय पर अधिक होती है?", "en": "Do the burning sensations on your skin occur more frequently at any specific time?", "category": "time_related_skin_burning", "symptom": None},
        {"hi": "क्या जलन के साथ आपको त्वचा में कोई दरार या फफोले हो रहे हैं?", "en": "Are there any cracks or blisters on your skin along with burning sensations?", "category": "cracks_blisters_with_skin_burning", "symptom": "skin lesions"},
        {"hi": "क्या जलन के साथ आपको कोई अन्य लक्षण भी महसूस हो रहे हैं?", "en": "Are you experiencing any other symptoms along with burning sensations on your skin?", "category": "other_symptoms_with_skin_burning", "symptom": None},
        {"hi": "क्या जलन अचानक शुरू हुई है या धीरे-धीरे?", "en": "Did the burning sensations on your skin start suddenly or gradually?", "category": "sudden_graduate_skin_burning", "symptom": None}
    ],

    'skin pain': [
        {"hi": "क्या आपको त्वचा पर दर्द महसूस हो रहा है?", "en": "Are you feeling pain on your skin?", "category": "skin_pain", "symptom": "skin pain"},
        {"hi": "क्या त्वचा के दर्द के साथ कोई सूजन भी है?", "en": "Is there any swelling along with skin pain?", "category": "swelling_with_skin_pain", "symptom": "swelling"},
        {"hi": "क्या त्वचा के दर्द के कारण आपको चलने-फिरने में कठिनाई हो रही है?", "en": "Are you having difficulty walking due to skin pain?", "category": "walking_difficulty_with_skin_pain", "symptom": None},
        {"hi": "क्या त्वचा के दर्द के साथ कोई दरार या फफोले हो रहे हैं?", "en": "Are there any cracks or blisters on your skin along with pain?", "category": "cracks_blisters_with_skin_pain", "symptom": "skin lesions"},
        {"hi": "क्या दर्द के साथ आपकी त्वचा में लालिमा हो गई है?", "en": "Has your skin turned red along with the pain?", "category": "redness_with_skin_pain", "symptom": "redness"},
        {"hi": "क्या त्वचा के दर्द के साथ आपको खुजली या जलन भी हो रही है?", "en": "Are you experiencing itching or burning sensations along with skin pain?", "category": "itching_burning_with_skin_pain", "symptom": "itching"},
        {"hi": "क्या त्वचा का दर्द अचानक शुरू हुआ है या धीरे-धीरे?", "en": "Did the skin pain start suddenly or gradually?", "category": "sudden_graduate_skin_pain", "symptom": None}
    ],

    'skin swelling': [
        {"hi": "क्या आपकी त्वचा में सूजन हो रही है?", "en": "Are you experiencing swelling in your skin?", "category": "skin_swelling", "symptom": "swelling"},
        {"hi": "क्या सूजन के साथ त्वचा में लालिमा भी है?", "en": "Is there any redness in your skin along with swelling?", "category": "redness_with_skin_swelling", "symptom": "redness"},
        {"hi": "क्या सूजन के कारण आपको किसी विशेष हिस्से में दर्द हो रहा है?", "en": "Is the swelling causing any pain in a specific area?", "category": "localized_pain_with_skin_swelling", "symptom": "pain"},
        {"hi": "क्या सूजन लगातार है या आता-जाता है?", "en": "Is the swelling constant or does it come and go?", "category": "intermittent_skin_swelling", "symptom": None},
        {"hi": "क्या सूजन के साथ कोई अन्य लक्षण भी हैं?", "en": "Are there any other symptoms along with swelling?", "category": "other_symptoms_with_skin_swelling", "symptom": None},
        {"hi": "क्या सूजन किसी विशेष समय पर अधिक होती है?", "en": "Does the swelling occur more frequently at any specific time?", "category": "time_related_skin_swelling", "symptom": None},
        {"hi": "क्या सूजन के कारण आपकी त्वचा में कोई परिवर्तन हो रहा है?", "en": "Are there any changes in your skin due to swelling?", "category": "skin_changes_with_skin_swelling", "symptom": "skin discoloration"}
    ],
    # Add more canonical symptoms and their follow-up questions as needed
}

# Additional general follow-up questions
additional_followup_questions = [
    {"hi": "आपकी उम्र क्या है?", "en": "What is your age?", "category": "age", "symptom": None},
    {"hi": "आपका लिंग क्या है?", "en": "What is your gender?", "category": "gender", "symptom": None},
    {"hi": "आप वर्तमान में कहां स्थित हैं?", "en": "Where are you currently located?", "category": "location", "symptom": None},
    {"hi": "लक्षण कब से हैं?", "en": "How long have you had these symptoms?", "category": "duration", "symptom": None},
    {"hi": "क्या आप कोई अन्य लक्षण महसूस कर रहे हैं?", "en": "Are you experiencing any other symptoms?", "category": "other_symptoms", "symptom": None}
]

# Normalize symptom lists
known_symptoms_lower = [symptom.lower() for symptom in known_symptoms]
#symptom_list_lower = [symptom.lower() for symptom in symptom_list]

# Convert symptom_followup_questions keys to lowercase
#symptom_followup_questions_lower = {symptom.lower(): questions for symptom, questions in symptom_followup_questions.items()}


# -------------------- Core Functions -------------------- #
# Google TTS
def generate_audio_with_api_key(text, api_key, lang='hi-IN'):
    """
    Generate audio bytes from text using Google Cloud Text-to-Speech REST API with an API key.

    Args:
        text (str): The text to convert to speech.
        api_key (str): Your Google Cloud API key.
        lang (str): The language code (default is 'hi-IN' for Hindi).

    Returns:
        bytes: Audio content in bytes, or None if failed.
    """
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"

    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }

    # Define the request payload
    data = {
        "input": {
            "text": text
        },
        "voice": {
            "languageCode": lang,
            "name": "hi-IN-Wavenet-E",  # Choose a specific voice or let Google select default
            "ssmlGender": "NEUTRAL"
        },
        "audioConfig": {
            "audioEncoding": "MP3",
            "pitch": 0,
            "speakingRate": 1.0
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an error for bad status codes
        audio_content = response.json().get('audioContent')
        if audio_content:
            return base64.b64decode(audio_content)
        else:
            st.error("No audio content received from the API.")
            return None
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
        st.error(f"Response: {response.text}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def embed_audio_autoplay_google(audio_bytes):
    """
    Embed and autoplay audio in Streamlit.

    Args:
        audio_bytes (bytes): The audio content in bytes.
    """
    if audio_bytes:
        # Convert bytes to base64 for embedding
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    else:
        st.error("No audio to play.")

# Audio Open
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
        st.error(f"Failed to generate audio: {e}")
        return None

def embed_audio_autoplay(audio_bytes: bytes):
    """
    Embed audio in Streamlit app with autoplay using HTML and JavaScript.
    Includes a fallback play button if autoplay is blocked.
    """
    if audio_bytes is None:
        return

    # Encode audio to base64
    audio_base64 = base64.b64encode(audio_bytes).decode()

    # HTML and JavaScript to autoplay the audio
    audio_html = f"""
    <audio id="audioPlayer" src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>
    <script>
        window.addEventListener('load', function() {{
            var audio = document.getElementById('audioPlayer');
            audio.play().then(() => {{
                console.log('Audio played successfully');
            }}).catch((error) => {{
                console.log('Autoplay was prevented:', error);
                // Display a play button if autoplay is blocked
                var playButton = document.createElement('button');
                playButton.innerHTML = 'Play Audio';
                playButton.style.fontSize = '16px';
                playButton.style.padding = '10px 20px';
                playButton.style.marginTop = '20px';
                playButton.onclick = function() {{
                    audio.play();
                }};
                document.body.appendChild(playButton);
            }});
        }});
    </script>
    """

    # Embed the HTML in Streamlit
    components.html(audio_html, height=0, width=0)

def save_audio_file(audio_bytes, file_extension):
    """
    Save the audio bytes to a file with a unique name.
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
    Transcribe the audio file using OpenAI's Whisper API with translation to English.
    """
    try:
        with open(file_path, "rb") as audio_file:
            transcript = openai.Audio.translate("whisper-1", audio_file)
            transcribed_text = transcript.get("text", "").strip()
            logger.info(f"Audio transcription successful: {transcribed_text}")
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

def normalize_symptom(symptom):
    """
    Normalize a symptom to its canonical form.
    """
    symptom_lower = symptom.lower()
    return symptom_to_canonical.get(symptom_lower, symptom_lower)  # Return the canonical form or the original if not found

def get_followup_questions(initial_symptoms):
    """
    Retrieve follow-up questions based on the initial canonical symptoms.
    """
    followup_questions = []
    for symptom in initial_symptoms:
        canonical_symptom = normalize_symptom(symptom)
        questions = canonical_symptom_followup_questions.get(canonical_symptom, [])
        followup_questions.extend(questions)
    return followup_questions

def extract_symptoms(text, symptom_list, symptom_to_canonical):
    """
    Extract exact symptoms from the given text using symptom list and mapping.

    Args:
        text (str): The input text to extract symptoms from.
        symptom_list (list): List of symptom variants.
        symptom_to_canonical (dict): Mapping from variant to canonical symptom.

    Returns:
        list: A list of canonical symptoms extracted from the text.
    """
    try:
        text_lower = text.lower()
        extracted_symptoms = set()

        # Use NER to extract symptoms
        ner_results = ner_pipeline(text)
        for entity in ner_results:
            if entity['entity_group'] == 'SYMPTOM':
                symptom = entity['word'].strip().lower()
                if symptom in symptom_to_canonical:
                    canonical = symptom_to_canonical[symptom]
                    extracted_symptoms.add(canonical)
        
        # Additionally, use keyword matching for any missed symptoms
        for symptom_variant in symptom_list:
            if re.search(r'\b' + re.escape(symptom_variant) + r'\b', text_lower):
                canonical = symptom_to_canonical.get(symptom_variant, symptom_variant)
                extracted_symptoms.add(canonical)
        
        # Remove generic terms
        extracted_symptoms = [sym for sym in extracted_symptoms if sym not in {'no', 'yes', 'nothing', 'nothing else'}]
        
        logger.info(f"Final Extracted Symptoms: {extracted_symptoms}")
        return list(extracted_symptoms)
    except Exception as e:
        st.error(f"An error occurred during symptom extraction: {e}")
        logger.error(f"Symptom extraction error: {e}")
        return []

def extract_possible_causes(text):
    """
    Use OpenAI API to generate a one-sentence overview of the possible cause from the transcript
    only if the input is medically related. Otherwise, return "No suitable cause determined from the transcript."
    """
    try:
        # Modify the prompt to instruct GPT to only provide causes for medical content
        prompt = (
            f"Based on the following patient transcript, determine if the content is medically related. "
            f"If it is, provide a one-sentence possible cause of the symptoms. If it is not medically related, "
            f"respond with 'No suitable cause determined from the transcript.'\n\n{text}\n\nPossible cause:"
        )

        # Make the API call
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

        # Extract and clean the response
        cause = response['choices'][0]['message']['content'].strip()
        cause = re.sub(r'^Possible cause:\s*', '', cause, flags=re.IGNORECASE)

        # Check if the cause is non-medical and return the appropriate message
        if "No suitable cause determined from the transcript" in cause:
            logger.info("Non-medical input detected. No suitable cause determined.")
            return "No suitable cause determined from the transcript."

        logger.info(f"Generated possible cause using OpenAI API: {cause}")
        return cause
    except Exception as e:
        logger.error(f"Failed to generate possible cause using OpenAI API: {e}")
        return "No possible causes determined."

def translate_and_correct(text):
    """
    Translates input text to English if necessary and corrects spelling while preserving medical terms.

    Args:
        text (str): The input text to process.

    Returns:
        str: The translated and spell-corrected text.
    """
    try:
        # Translate to English if not already in English
        translated_text = translate_to_english(text)
        logger.info(f"Translated and corrected text: '{translated_text}'")
        return translated_text
    except Exception as e:
        logger.error(f"Translation and correction failed: {e}")
        return text  # Fallback to original text if translation fails

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

    # Medications extraction: find medications in the text using regex for better accuracy
    for med in medications_list:
        pattern = re.compile(re.escape(med), re.IGNORECASE)
        if pattern.search(text):
            medications.append(med.title())

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
    gender_patterns = [
        r'\b(?:i am|i\'m)\s+(?:a\s+)?(male|female|boy|girl|man|woman)\b',
        r'\b(?:gender)\s*[:\-]?\s*(male|female|other)\b'
    ]
    for pattern in gender_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            gender_candidate = match.group(1)
            gender = gender_candidate.lower()
            break

    # Extract location
    location_patterns = [
        r'\b(?:i am|i\'m)\s+(?:in|located in|located at|from)\s+([A-Za-z\s]+)\b',
        r'\b(?:location)\s*[:\-]?\s*([A-Za-z\s]+)\b',
        r'\b(?:state)\s*[:\-]?\s*([A-Za-z\s]+)\b'
    ]
    for pattern in location_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            location_candidate = match.group(1)
            location = location_candidate.strip()
            break
    if not location:
        # Try to extract GPE entities
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
        match = re.search(pattern, text, re.IGNORECASE)
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

def determine_followup_questions(initial_symptoms, additional_info, asked_question_categories):
    """
    Determine the next set of follow-up questions based on initial symptoms and additional information.
    Ensures 3 to 7 questions, with each question from a different symptom group.
    """
    followup_questions = []
    asked_categories = set(asked_question_categories)

    # Retrieve follow-up questions based on initial symptoms
    symptom_based_questions = get_followup_questions(initial_symptoms)

    # Shuffle to randomize question selection
    random.shuffle(symptom_based_questions)

    # Select questions ensuring each is from a different symptom group
    selected_symptom_questions = []
    symptom_groups_asked = set()

    for question in symptom_based_questions:
        symptom = question['symptom']
        if symptom and symptom not in symptom_groups_asked and question['category'] not in asked_categories:
            selected_symptom_questions.append(question)
            symptom_groups_asked.add(symptom)
            asked_categories.add(question['category'])
        if len(selected_symptom_questions) >= 5:
            break  # Limit to maximum of 5 symptom-based questions

    followup_questions.extend(selected_symptom_questions)

    # Handle additional information questions only if not already provided
    additional_followup_questions = [
        {"hi": "आपकी उम्र क्या है?", "en": "What is your age?", "category": "age", "symptom": None},
        {"hi": "आपका लिंग क्या है?", "en": "What is your gender?", "category": "gender", "symptom": None},
        {"hi": "आप वर्तमान में कहाँ स्थित हैं?", "en": "Where are you currently located?", "category": "location", "symptom": None},
        {"hi": "लक्षण कितने समय से हैं?", "en": "How long have you been experiencing these symptoms?", "category": "duration", "symptom": None},
        {"hi": "क्या आप कोई दवा ले रहे हैं?", "en": "Are you taking any medications?", "category": "medications", "symptom": None},
        # Add more additional follow-up questions as needed
    ]

    # Identify missing additional information
    missing_additional_info = []
    for add_q in additional_followup_questions:
        category = add_q['category']
        if not additional_info.get(category):
            if add_q['category'] not in asked_categories:
                missing_additional_info.append(add_q)

    # Shuffle to randomize question selection
    random.shuffle(missing_additional_info)

    # Select additional questions up to 2
    selected_additional_questions = []
    for question in missing_additional_info:
        if len(selected_additional_questions) >= 2:
            break
        selected_additional_questions.append(question)
        asked_categories.add(question['category'])

    followup_questions.extend(selected_additional_questions)

    # Ensure the total number of questions is between 3 to 7
    total_questions = len(followup_questions)
    if total_questions < 3:
        needed = 3 - total_questions
        # Optionally, add "other symptoms" question if not already asked
        if 'other_symptoms' not in asked_categories:
            other_symptoms_question = {
                "hi": "क्या आप कोई अन्य लक्षण महसूस कर रहे हैं?",
                "en": "Are you experiencing any other symptoms?",
                "category": "other_symptoms",
                "symptom": None
            }
            followup_questions.append(other_symptoms_question)
            asked_categories.add('other_symptoms')
            total_questions += 1

    # Limit to maximum of 7 questions
    if total_questions > 7:
        followup_questions = followup_questions[:7]

    logger.info(f"Determined Follow-Up Questions: {[q['en'] for q in followup_questions]}")
    return followup_questions

def extract_all_symptoms(conversation_history, symptom_list, symptom_to_canonical):
    """
    Extract all exact symptoms and additional information from the conversation history.
    Collect all user inputs into a single transcript for cause analysis.

    Args:
        conversation_history (list): List of conversation entries.
        symptom_list (list): List of symptom variants.
        symptom_to_canonical (dict): Mapping from variant to canonical symptom.

    Returns:
        tuple: (matched_symptoms, additional_info, combined_transcript)
    """
    exact_symptoms = set()
    canonical_symptoms = set()
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
        if 'user' in entry:
            user_text = entry['user']
            combined_transcript += " " + user_text  # Collecting all user inputs
            symptoms = extract_symptoms(user_text, symptom_list, symptom_to_canonical)
            exact_symptoms.update(symptoms)
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
            is_affirmative = any(re.search(r'\b' + re.escape(word) + r'\b', response_text_lower) for word in affirmative_responses)
            is_negative = any(re.search(r'\b' + re.escape(word) + r'\b', response_text_lower) for word in negative_responses)

            if not is_negative:
                # Extract symptoms from the response text
                response_symptoms = extract_symptoms(response_text, symptom_list, symptom_to_canonical)
                exact_symptoms.update(response_symptoms)

            # Get the 'symptom' associated with the question using canonical mapping
            symptom = None
            for canonical_symptom, questions in canonical_symptom_followup_questions.items():
                for q in questions:
                    if q['en'].lower() == question_text.lower():
                        symptom = q.get('symptom')
                        break
                if symptom:
                    break

            if symptom and is_affirmative:
                canonical_symptoms.add(symptom.lower())  # For follow-up mapping
                combined_transcript += " " + response_text  # Include affirmative response in transcript
            elif symptom and is_negative:
                canonical_symptoms.discard(symptom.lower())  # Remove symptom if previously added
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

    # Update session_state with additional_info and exact_symptoms
    if 'additional_info' not in st.session_state:
        st.session_state.additional_info = {}
    if 'matched_symptoms' not in st.session_state:
        st.session_state.matched_symptoms = set()

    # Update existing session state with new data
    for key in additional_info:
        if additional_info[key]:
            if isinstance(additional_info[key], list):
                st.session_state.additional_info.setdefault(key, []).extend(additional_info[key])
                st.session_state.additional_info[key] = list(set(st.session_state.additional_info[key]))
            else:
                st.session_state.additional_info[key] = additional_info[key]

    # Update matched_symptoms with exact_symptoms
    st.session_state.matched_symptoms.update(exact_symptoms)

    # For follow-up questions, use canonical_symptoms
    if 'canonical_matched_symptoms' not in st.session_state:
        st.session_state.canonical_matched_symptoms = set()
    st.session_state.canonical_matched_symptoms.update(canonical_symptoms)

    logger.info(f"Final Exact Symptoms: {st.session_state.matched_symptoms}")
    logger.info(f"Canonical Symptoms for Follow-Up: {st.session_state.canonical_matched_symptoms}")
    logger.info(f"Additional Information: {st.session_state.additional_info}")
    logger.info(f"Combined Transcript for Cause Analysis: {combined_transcript}")

    return st.session_state.matched_symptoms, st.session_state.additional_info, combined_transcript

def extract_and_prepare_questions(conversation_history):
    """
    Extract symptoms and additional info from the conversation history and prepare follow-up questions.
    """
    matched_symptoms, additional_info, possible_causes = extract_all_symptoms(conversation_history)
    st.session_state.additional_info = additional_info  # Store in session state for access elsewhere
    st.session_state.possible_causes = possible_causes  # Store possible causes in session state
    followup_questions = determine_followup_questions(matched_symptoms, additional_info)
    st.session_state.matched_symptoms = matched_symptoms  # Store matched symptoms in session state
    return followup_questions

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

def generate_report(conversation_history):
    """
    Generate the final diagnostic report based on the conversation history.
    Additionally, generate and play an audio summary in Hindi.
    """
    # Access session_state variables
    exact_symptoms = st.session_state.get('matched_symptoms', set())
    additional_info = st.session_state.get('additional_info', {})

    # Combine transcript for possible cause analysis
    combined_transcript = " ".join([entry['user'] for entry in conversation_history if 'user' in entry])
    combined_transcript += " " + " ".join([entry['response'] for entry in conversation_history if 'response' in entry])

    st.subheader("📄 **Final Report:**")
    st.write("**Symptoms:**", ', '.join(sorted(exact_symptoms)) if exact_symptoms else 'Not specified')

    # Display Additional Information
    if additional_info.get('age'):
        st.write(f"**Age:** {additional_info['age']} years old")
    if additional_info.get('gender'):
        st.write(f"**Gender:** {additional_info['gender'].title()}")
    if additional_info.get('location'):
        st.write(f"**Location:** {additional_info['location']}")
    if additional_info.get('duration'):
        st.write(f"**Duration of Symptoms:** {additional_info['duration']}")
    if additional_info.get('medications'):
        st.write(f"**Medications Taken:** {', '.join(additional_info['medications'])}")

    # Generate a single possible cause using OpenAI API based on the combined transcript
    possible_cause = extract_possible_causes(combined_transcript)

    # Display Possible Cause
    if possible_cause and possible_cause != "No suitable cause determined from the transcript.":
        st.write("**Possible Cause:**")
        st.write(f"- {possible_cause}")
    else:
        st.write("**Possible Cause:** No possible causes determined.")

    # Map symptoms to diseases (optional, depending on your implementation)
    probable_diseases = map_symptoms_to_diseases(exact_symptoms, additional_info)

    st.subheader("📝 **Transcript of Questions and Answers:**")
    question_count = 1
    for entry in conversation_history:
        if 'followup_question_en' in entry and 'response' in entry:
            st.write(f"**Question {question_count} (English):** {entry['followup_question_en']}")
            st.write(f"**Your Answer:** {entry['response']}")
            st.write("---")
            question_count += 1

    # -------------------- New Functionality: Speak Causes and Symptoms in Hindi -------------------- #

    # Check if a possible cause was determined
    if possible_cause and possible_cause != "No suitable cause determined from the transcript.":
        # Translate the cause to Hindi
        translated_cause = translator.translate(possible_cause, src='en', dest='hi').text
    else:
        translated_cause = "आपके लक्षणों के आधार पर कोई संभावित कारण नहीं पाया गया।"

    # Translate exact symptoms to Hindi
    if exact_symptoms:
        translated_symptoms_list = [translate_to_hindi(symptom) for symptom in exact_symptoms]
        translated_symptoms = ', '.join(translated_symptoms_list)
    else:
        translated_symptoms = "कोई लक्षण नहीं पहचाने गए।"

    # Construct the Hindi message
    if translated_cause != "आपके लक्षणों के आधार पर कोई संभावित कारण नहीं पाया गया।":
        # Specific message including symptoms and possible causes
        message_hindi = f"आपके लक्षण: {translated_symptoms}. इन लक्षणों के कारण, संभावित कारण यह हैं: {translated_cause}. हम आपको सबसे उपयुक्त डॉक्टर से तुरंत जोड़ रहे हैं।"
    else:
        # If no possible cause, still inform the user about connecting to a doctor
        message_hindi = f"{translated_cause} हम आपकी मदद के लिए एक डॉक्टर से संपर्क कर रहे हैं।"

    # Generate the audio in Hindi
    audio_bytes = generate_audio_with_api_key(message_hindi, API_KEY, lang='hi')

    # Play the audio
    if audio_bytes:
        embed_audio_autoplay_google(audio_bytes)
    else:
        st.error("Failed to generate final report audio.")

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

    # Use regex to match whole words only
    is_affirmative = any(re.search(r'\b' + re.escape(word) + r'\b', response_lower) for word in affirmative_responses)
    is_negative = any(re.search(r'\b' + re.escape(word) + r'\b', response_lower) for word in negative_responses)

    # Initialize session_state.matched_symptoms if not already
    if 'matched_symptoms' not in st.session_state:
        st.session_state.matched_symptoms = set()

    if is_affirmative and question['symptom']:
        st.session_state.matched_symptoms.add(question['symptom'].lower())  # Ensure lowercase
        logger.info(f"Added symptom '{question['symptom']}' based on affirmative response.")
        st.success(f"Added symptom: {question['symptom']}")
    elif is_negative and question['symptom']:
        if question['symptom'].lower() in st.session_state.matched_symptoms:
            st.session_state.matched_symptoms.remove(question['symptom'].lower())
            logger.info(f"Removed symptom '{question['symptom']}' based on negative response.")
            st.warning(f"Removed symptom: {question['symptom']}")
        else:
            logger.info(f"No action taken for symptom '{question['symptom']}' as it's not present.")
    else:
        logger.info("Response not recognized as affirmative or negative.")

# -------------------- Main Streamlit Application -------------------- #

def main():
    # Initialize session state variables
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0  # Start at welcome
        st.session_state.conversation_history = []
        st.session_state.report_generated = False
        st.session_state.followup_questions = []
        st.session_state.current_followup = 0
        st.session_state.additional_info = {
            'age': None,
            'gender': None,
            'location': None,
            'duration': None,
            'medications': []
        }
        st.session_state.matched_symptoms = set()
        st.session_state.asked_question_categories = set()  # Track asked question categories

    st.title("🩺 O-Health LLM App")
    st.write("""
        Welcome to the O-Health LLM App. You can either speak your symptoms in Hindi or type them in English to receive potential disease recommendations based on your inputs.
    """)

    # Load symptoms from CSV
    symptom_list, symptom_to_canonical = load_symptom_list('Extract_Causes/symptom_list_2.csv')

    if not symptom_list:
        st.error("Symptom list is empty or failed to load. Please check the CSV file.")
        return

    # Step 0: Welcome Message
    if st.session_state.current_step == 0:
        # Generate and play the welcome audio in Hindi
        welcome_text = "ओ-हेल्थ में आपका स्वागत है। कृपया माइक्रोफ़ोन बटन दबाएं और अपने लक्षण बोलें।"
        audio_bytes = generate_audio_with_api_key(welcome_text, API_KEY, lang='hi')
        if audio_bytes:
            embed_audio_autoplay_google(audio_bytes)
        else:
            st.error("Failed to generate welcome audio.")

        # Display a welcome message
        st.write("### Hello, Welcome to O-Health")
        st.write("Please provide your symptoms to get started.")

        st.session_state.current_step = 1  # Proceed to the next step

    # Step 1: Initial Symptom Input
    if st.session_state.current_step == 1:
        st.header("🗣️ Please Press the Microphone Button and Speak Your Symptoms:")
        # Record audio
        audio_bytes = audio_recorder(key="voice_input_initial")
        if audio_bytes and not st.session_state.get('symptoms_processed'):
            st.audio(audio_bytes, format="audio/wav")
            file_name = save_audio_file(audio_bytes, "wav")
            if file_name:
                st.success("Audio recorded and saved successfully!")
                st.info("Transcribing your audio... Please wait.")
                transcribed_text = transcribe_audio(file_name)
                if transcribed_text:
                    # Detect and translate to English if necessary
                    corrected_text = translate_and_correct(transcribed_text)

                    st.subheader("📝 Transcribed Text (English):")
                    st.write(corrected_text)

                    # Assign corrected_input to corrected_text
                    corrected_input = corrected_text

                    # After processing initial input and updating conversation history
                    st.session_state.conversation_history.append({
                        'user': corrected_input
                    })

                    # Extract symptoms and additional information
                    matched_symptoms, additional_info, combined_transcript = extract_all_symptoms(
                        st.session_state.conversation_history,
                        symptom_list,
                        symptom_to_canonical
                    )

                    # Determine follow-up questions using extracted data
                    followup_questions = determine_followup_questions(
                        matched_symptoms,
                        additional_info,
                        st.session_state.asked_question_categories
                    )
                    st.session_state.followup_questions = followup_questions

                    st.session_state.current_step = 2  # Proceed to follow-up questions
                    st.session_state.symptoms_processed = True
                    st.experimental_rerun()

                else:
                    st.error("Failed to transcribe the audio.")
            else:
                st.error("Failed to save the audio file.")
        else:
            st.write("Please record your symptoms using the microphone button above.")

        # Optionally, provide a fallback text input
        st.write("**Alternatively, you can type your symptoms below:**")
        user_input = st.text_area("Enter your symptoms here...")
        if st.button("Submit Symptoms"):
            if user_input.strip() == "":
                st.warning("Please enter your symptoms.")
            else:
                # Detect and translate to English if necessary
                translated_input = translate_to_english(user_input)
                corrected_input = translated_input

                st.subheader("📝 Your Input:")
                st.write(corrected_input)
                st.session_state.conversation_history.append({
                    'user': corrected_input
                })

                # Extract symptoms and additional information
                matched_symptoms, additional_info, combined_transcript = extract_all_symptoms(
                    st.session_state.conversation_history,
                    symptom_list,
                    symptom_to_canonical
                )

                # Determine follow-up questions using extracted data
                followup_questions = determine_followup_questions(
                    matched_symptoms,
                    additional_info,
                    st.session_state.asked_question_categories
                )
                st.session_state.followup_questions = followup_questions

                st.session_state.current_step = 2  # Proceed to follow-up questions
                st.session_state.symptoms_processed = True
                st.experimental_rerun()

    # Step 2: Follow-Up Questions
    if st.session_state.current_step == 2:
        total_questions = len(st.session_state.followup_questions)
        if total_questions == 0:
            st.info("No follow-up questions required based on your inputs.")
            st.session_state.current_step = 3  # Proceed to report
            st.experimental_rerun()

        if st.session_state.current_followup < total_questions:
            current_question = st.session_state.followup_questions[st.session_state.current_followup]
            question_number = st.session_state.current_followup + 1

            # Display the question
            st.subheader(f"🔍 Follow-Up Question {question_number} of {total_questions}:")
            st.write(f"**Hindi:** {current_question['hi']}")
            st.write(f"**English:** {current_question['en']}")

            # Generate the question audio in Hindi
            if not st.session_state.get(f'question_{st.session_state.current_followup}_played'):
                question_audio = generate_audio_with_api_key(current_question['hi'], API_KEY, lang='hi')
                if question_audio:
                    embed_audio_autoplay_google(question_audio)
                    st.session_state[f'question_{st.session_state.current_followup}_played'] = True
                else:
                    st.error("Failed to generate question audio.")

            # Record the user's answer
            st.write("**Please record your answer using the microphone button below:**")
            response_audio_bytes = audio_recorder(key=f"voice_input_followup_{st.session_state.current_followup}")
            if response_audio_bytes and not st.session_state.get(f'answer_{st.session_state.current_followup}_processed'):
                st.audio(response_audio_bytes, format="audio/wav")
                response_file_name = save_audio_file(response_audio_bytes, "wav")
                if response_file_name:
                    st.success("Audio recorded and saved successfully!")
                    st.info("Transcribing your audio... Please wait.")
                    response_transcribed = transcribe_audio(response_file_name)
                    if response_transcribed:
                        # Detect and translate to English if necessary
                        corrected_response = translate_and_correct(response_transcribed)

                        st.subheader(f"📝 Response to Follow-Up Question {question_number} (English):")
                        st.write(corrected_response)
                        # Handle yes/no responses to add/remove symptoms
                        handle_yes_no_response(current_question, corrected_response)
                        # Extract any new symptoms from the response
                        st.session_state.conversation_history.append({
                            'followup_question_en': current_question['en'],
                            'response': corrected_response
                        })
                        matched_symptoms, additional_info, combined_transcript = extract_all_symptoms(
                            st.session_state.conversation_history,
                            symptom_list,
                            symptom_to_canonical
                        )

                        # Add current question category to asked categories
                        current_category = current_question.get('category')
                        if current_category:
                            st.session_state.asked_question_categories.add(current_category)

                        st.session_state[f'answer_{st.session_state.current_followup}_processed'] = True
                        st.session_state.current_followup += 1
                        st.experimental_rerun()
                    else:
                        st.error("Failed to transcribe your audio response.")
                else:
                    st.error("Failed to save the audio file.")
            else:
                st.write("Please record your answer using the microphone button above.")

            # Optionally, provide a fallback text input
            st.write("**Alternatively, you can type your answer below:**")
            answer_input = st.text_input("Enter your answer here...", key=f"answer_input_{st.session_state.current_followup}")
            if st.button("Submit Answer", key=f"submit_answer_{st.session_state.current_followup}"):
                if answer_input.strip() == "":
                    st.warning("Please enter your answer.")
                else:
                    corrected_answer = translate_to_english(answer_input)

                    st.session_state.conversation_history.append({
                        'followup_question_en': current_question['en'],
                        'response': corrected_answer
                    })
                    handle_yes_no_response(current_question, corrected_answer)
                    matched_symptoms, additional_info, combined_transcript = extract_all_symptoms(
                        st.session_state.conversation_history,
                        symptom_list,
                        symptom_to_canonical
                    )

                    # Add current question category to asked categories
                    current_category = current_question.get('category')
                    if current_category:
                        st.session_state.asked_question_categories.add(current_category)

                    st.session_state[f'answer_{st.session_state.current_followup}_processed'] = True
                    st.session_state.current_followup += 1
                    st.experimental_rerun()
        else:
            # All follow-up questions have been asked
            st.session_state.current_step = 3
            st.experimental_rerun()

    # Step 3: Generate Report
    if st.session_state.current_step == 3 and not st.session_state.report_generated:
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
        # Display extracted information
        matched_symptoms = st.session_state.get('matched_symptoms', set())
        additional_info = st.session_state.get('additional_info', {})
        st.write("**Extracted Information:**")
        st.write(f"**Symptoms:** {', '.join(matched_symptoms) if matched_symptoms else 'Not specified'}")
        if additional_info.get('age'):
            st.write(f"**Age:** {additional_info['age']} years old")
        if additional_info.get('gender'):
            st.write(f"**Gender:** {additional_info['gender'].title()}")
        if additional_info.get('location'):
            st.write(f"**Location:** {additional_info['location']}")
        if additional_info.get('duration'):
            st.write(f"**Duration:** {additional_info['duration']}")
        if additional_info.get('medications'):
            st.write(f"**Medications Taken:** {', '.join(additional_info['medications'])}")
            
if __name__ == "__main__":
    main()
