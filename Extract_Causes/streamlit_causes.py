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
    
    'acne' : [
    #{"hi": "आपको कितने समय से एक्ने है?", "en": "How long have you had acne?", "category": "acne", "symptom": "acne duration"},
    {"hi": "आपके पास आमतौर पर एक्ने कहाँ होते हैं?", "en": "Where do you typically get acne?", "category": "acne", "symptom": "acne location"},
    {"hi": "आपके पास किस प्रकार का एक्ने है?", "en": "What type of acne do you have?", "category": "acne", "symptom": "acne type"},
    {"hi": "आपके एक्ने कितने गंभीर हैं?", "en": "How severe is your acne?", "category": "acne", "symptom": "acne severity"},
    #{"hi": "क्या आपने अपने एक्ने के लिए कोई उपचार किया है?", "en": "Have you tried any treatments for your acne?", "category": "acne treatments", "symptom": "acne treatment"},
    {"hi": "क्या आप वर्तमान में कोई स्किनकेयर या मेकअप उत्पाद उपयोग कर रहे हैं?", "en": "Are you currently using any skincare or makeup products?", "category": "skincare", "symptom": "skincare use"},
    {"hi": "आप कौन सी दवाइयाँ ले रहे हैं?", "en": "What medications are you currently taking?", "category": "medication", "symptom": "medication"},
    {"hi": "क्या आपके परिवार में किसी को एक्ने है?", "en": "Do you have a family history of acne?", "category": "family history", "symptom": "family history"},
    {"hi": "क्या आपने अपने एक्ने के लिए किसी विशेष कारण का अनुभव किया है?", "en": "Have you noticed any specific triggers for your acne?", "category": "acne triggers", "symptom": "acne triggers"},
    {"hi": "क्या आप अत्यधिक तनाव में हैं?", "en": "Are you under a lot of stress?", "category": "stress", "symptom": "stress"}
],

'insomnia' : [
    #{"hi": "आपको कितने समय से अनिद्रा हो रही है?", "en": "How long have you been experiencing insomnia?", "category": "insomnia", "symptom": "insomnia duration"},
    {"hi": "आप आमतौर पर किस समय सोने जाते हैं और किस समय उठते हैं?", "en": "What time do you usually go to bed and wake up?", "category": "insomnia", "symptom": "sleep schedule"},
    {"hi": "आपको सोने में सामान्यतः कितना समय लगता है?", "en": "How long does it typically take you to fall asleep?", "category": "insomnia", "symptom": "time to fall asleep"},
    {"hi": "क्या आप रात में उठते हैं? अगर हां, तो कितनी बार?", "en": "Do you wake up during the night? If so, how often?", "category": "insomnia", "symptom": "night waking"},
    {"hi": "क्या आप जब उठते हैं तो आराम महसूस करते हैं?", "en": "Do you feel rested when you wake up?", "category": "insomnia", "symptom": "restfulness"},
    {"hi": "क्या आपने हाल ही में अपनी जीवनशैली में कोई बदलाव अनुभव किया है (जैसे तनाव, आहार, यात्रा)?", 
     "en": "Have you experienced any changes in your lifestyle recently (e.g., stress, diet, travel)?", 
     "category": "lifestyle", "symptom": "lifestyle changes"},
    {"hi": "क्या आप कैफीन, निकोटीन, या शराब का सेवन करते हैं, और अगर हां, तो कब?", "en": "Do you consume caffeine, nicotine, or alcohol, and if so, when?", "category": "substance use", "symptom": "substance use"},
    {"hi": "क्या आप कोई दवाइयाँ ले रहे हैं (प्रिस्क्रिप्शन, ओवर-द-काउंटर, या हर्बल)?", 
     "en": "Are you taking any medications (prescription, over-the-counter, or herbal)?", 
     "category": "medication", "symptom": "medication"},
    {"hi": "क्या आपको कोई अन्य चिकित्सा समस्याएँ हैं (जैसे दर्द, सांस लेने में समस्या, मानसिक स्वास्थ्य समस्याएँ)?", 
     "en": "Do you have any other medical conditions (e.g., pain, breathing problems, mental health conditions)?", 
     "category": "medical conditions", "symptom": "medical conditions"},
    {"hi": "क्या आप सोने से पहले कोई गतिविधियाँ या दिनचर्या करते हैं (जैसे स्क्रीन टाइम, व्यायाम, विश्राम)?", 
     "en": "Do you engage in any activities or routines before bed (e.g., screen time, exercise, relaxation)?", 
     "category": "bedtime routines", "symptom": "bedtime routine"}
],

'memory loss' : [
    #{"hi": "आपको कितने समय से याददाश्त की कमी हो रही है?", "en": "How long have you been experiencing memory loss?", "category": "memory loss", "symptom": "memory loss duration"},
    {"hi": "आप किस प्रकार की याददाश्त की समस्याओं का सामना कर रहे हैं?", "en": "What type of memory problems are you experiencing?", "category": "memory loss", "symptom": "memory problem type"},
    {"hi": "क्या याददाश्त की कमी समय के साथ बढ़ रही है?", "en": "Is the memory loss getting worse over time?", "category": "memory loss", "symptom": "memory loss progression"},
    {"hi": "क्या आपको हाल ही में कोई सिर की चोट या आघात हुआ है?", "en": "Have you had any recent head injuries or trauma?", "category": "head injury", "symptom": "head injury"},
    {"hi": "क्या आपको विशिष्ट विवरण याद करने में परेशानी हो रही है, या यह सामान्य याददाश्त की कमी है?", 
     "en": "Do you have trouble recalling specific details, or is it more about general memory loss?", 
     "category": "memory loss", "symptom": "specific vs general memory loss"},
    {"hi": "क्या आप किसी अन्य संज्ञानात्मक समस्या का अनुभव कर रहे हैं, जैसे भ्रम या ध्यान केंद्रित करने में कठिनाई?", 
     "en": "Are you experiencing any other cognitive problems, such as confusion or difficulty concentrating?", 
     "category": "cognitive problems", "symptom": "cognitive problems"},
    {"hi": "क्या आपके परिवार में किसी को याददाश्त की समस्याएँ या तंत्रिका तंत्र की बीमारियाँ हैं (जैसे अल्जाइमर, डिमेंशिया)?", 
     "en": "Do you have any family history of memory problems or neurological conditions (e.g., Alzheimer’s, dementia)?", 
     "category": "family history", "symptom": "family history"},
    {"hi": "क्या आपको हाल ही में किसी मूड परिवर्तन का अनुभव हो रहा है, जैसे अवसाद या चिंता?", 
     "en": "Have you been experiencing any mood changes, such as depression or anxiety?", 
     "category": "mood changes", "symptom": "mood changes"},
    {"hi": "क्या आप कोई दवाइयाँ या सप्लीमेंट्स ले रहे हैं?", "en": "Are you taking any medications or supplements?", "category": "medications", "symptom": "medication use"},
    {"hi": "क्या आपको कोई अन्य चिकित्सा समस्याएँ हैं, जैसे उच्च रक्तचाप, मधुमेह, या थायरॉयड की समस्याएँ?", 
     "en": "Do you have any other medical conditions, such as high blood pressure, diabetes, or thyroid problems?", 
     "category": "medical conditions", "symptom": "medical conditions"}
],

'urinary frequency' : [
    {"hi": "आपको कितनी बार पेशाब करने की आवश्यकता महसूस होती है?", "en": "How often do you feel the need to urinate?", "category": "urinary frequency", "symptom": "urination frequency"},
    {"hi": "क्या आप रात में पेशाब करने के लिए उठते हैं (नोक्टुरिया)?", "en": "Do you wake up during the night to urinate (nocturia)?", "category": "urinary frequency", "symptom": "nocturia"},
    {"hi": "क्या आप हर बार कितनी मात्रा में पेशाब करते हैं?", "en": "How much urine do you pass each time?", "category": "urinary frequency", "symptom": "urine amount"},
    {"hi": "क्या आपको पेशाब करते समय कोई दर्द या असुविधा महसूस हो रही है?", "en": "Are you experiencing any pain or discomfort while urinating?", "category": "urinary frequency", "symptom": "pain during urination"},
    {"hi": "क्या आपने अपने मूत्र के रंग या गंध में कोई बदलाव देखा है?", "en": "Have you noticed any changes in the color or odor of your urine?", "category": "urinary frequency", "symptom": "urine color/odor changes"},
    {"hi": "क्या आपको पेशाब करने की तीव्र आवश्यकता महसूस होती है लेकिन इसे रोकने में कठिनाई होती है?", 
     "en": "Do you have a strong urge to urinate but find it difficult to hold it in?", 
     "category": "urinary frequency", "symptom": "urgency/difficulty holding urine"},
    {"hi": "क्या आपको हाल ही में कोई मूत्राशय संक्रमण (UTI) या अन्य मूत्र संबंधी समस्याएँ हुई हैं?", 
     "en": "Have you recently had any urinary tract infections (UTIs) or other urinary problems?", 
     "category": "urinary frequency", "symptom": "UTI or urinary issues"},
    {"hi": "क्या आप बहुत अधिक तरल पदार्थ पीते हैं, खासकर कैफीन, शराब या शर्करा वाले पेय?", 
     "en": "Do you drink a lot of fluids, especially caffeine, alcohol, or sugary drinks?", 
     "category": "urinary frequency", "symptom": "fluid intake habits"},
    {"hi": "क्या आप अन्य कोई लक्षण अनुभव कर रहे हैं, जैसे तीव्रता, रिसाव, या पेशाब में खून?", 
     "en": "Are you experiencing any other symptoms, such as urgency, leakage, or blood in your urine?", 
     "category": "urinary frequency", "symptom": "other urinary symptoms"},
    {"hi": "क्या आपको हाल ही में अपने स्वास्थ्य में कोई बदलाव महसूस हुआ है, जैसे वजन बढ़ना, मधुमेह, या गर्भावस्था?", 
     "en": "Have you had any recent changes in your health, such as weight gain, diabetes, or pregnancy?", 
     "category": "urinary frequency", "symptom": "health changes"}
],

'ear pain' : [
    #{"hi": "आपको कितने समय से कान में दर्द हो रहा है?", "en": "How long have you been experiencing ear pain?", "category": "ear pain", "symptom": "ear pain duration"},
    {"hi": "क्या दर्द लगातार है, या यह आता-जाता है?", "en": "Is the pain constant, or does it come and go?", "category": "ear pain", "symptom": "pain pattern"},
    {"hi": "क्या आपको एक कान में दर्द हो रहा है या दोनों कानों में?", "en": "Do you have pain in one ear or both ears?", "category": "ear pain", "symptom": "ear affected"},
    {"hi": "क्या आप अन्य लक्षण अनुभव कर रहे हैं, जैसे सुनाई में कमी, कान में घंटी बजने की आवाज (टिनिटस), या चक्कर आना?", 
     "en": "Are you experiencing any other symptoms, such as hearing loss, ringing in the ear (tinnitus), or dizziness?", 
     "category": "ear pain", "symptom": "other symptoms"},
    {"hi": "क्या दर्द सर्दी, साइनस संक्रमण, या ऊपरी श्वसन संक्रमण के बाद शुरू हुआ था?", 
     "en": "Did the pain start after a cold, sinus infection, or upper respiratory infection?", 
     "category": "ear pain", "symptom": "infection history"},
    {"hi": "क्या आपको हाल ही में कान में कोई चोट या आघात हुआ है?", 
     "en": "Have you had any recent injuries or trauma to the ear?", 
     "category": "ear pain", "symptom": "ear injury"},
    {"hi": "क्या आपके कान से कोई रिसाव या डिस्चार्ज हो रहा है?", 
     "en": "Do you have drainage or discharge coming from your ear?", 
     "category": "ear pain", "symptom": "ear discharge"},
    {"hi": "क्या आप हाल ही में जोरदार शोर या पानी (जैसे तैराकी या स्नान) के संपर्क में आए हैं?", 
     "en": "Have you recently been exposed to loud noises or water (e.g., swimming or bathing)?", 
     "category": "ear pain", "symptom": "noise or water exposure"},
    {"hi": "क्या आपको बाहरी कान या कान के आस-पास के क्षेत्र को छूने या खींचने पर दर्द हो रहा है?", 
     "en": "Are you experiencing any pain when touching or pulling on the outer ear or around the ear area?", 
     "category": "ear pain", "symptom": "touch pain"},
    {"hi": "क्या आपको कान में संक्रमण या अन्य कान संबंधित समस्याओं का इतिहास है?", 
     "en": "Do you have a history of ear infections or other ear-related issues?", 
     "category": "ear pain", "symptom": "ear infection history"}
],

'hypertension' : [
    #{"hi": "आपको उच्च रक्तचाप के बारे में कितने समय से पता है?", "en": "How long have you been aware of your high blood pressure?", "category": "hypertension", "symptom": "awareness of hypertension"},
    {"hi": "क्या आपके परिवार में उच्च रक्तचाप या हृदय रोग का इतिहास है?", "en": "Do you have a family history of high blood pressure or heart disease?", "category": "hypertension", "symptom": "family history"},
    {"hi": "क्या आपको किसी अन्य चिकित्सा समस्याओं का निदान हुआ है (जैसे, मधुमेह, गुर्दे की बीमारी)?", 
     "en": "Have you been diagnosed with any other medical conditions (e.g., diabetes, kidney disease)?", 
     "category": "hypertension", "symptom": "other medical conditions"},
    {"hi": "क्या आप वर्तमान में कोई दवाइयाँ, ओवर-द-काउंटर दवाइयाँ या सप्लीमेंट्स ले रहे हैं?", 
     "en": "Are you currently taking any medications, including over-the-counter drugs or supplements?", 
     "category": "hypertension", "symptom": "medication use"},
    {"hi": "क्या आपको धूम्रपान करने का इतिहास है या अत्यधिक शराब का सेवन करते हैं?", 
     "en": "Do you have a history of smoking or excessive alcohol consumption?", 
     "category": "hypertension", "symptom": "smoking or alcohol use"},
    {"hi": "आप अपनी आहार को कैसे वर्णित करेंगे (जैसे, नमक, प्रसंस्कृत खाद्य पदार्थों में अधिक)?", 
     "en": "How would you describe your diet (e.g., high in salt, processed foods)?", 
     "category": "hypertension", "symptom": "diet habits"},
    {"hi": "क्या आप नियमित रूप से शारीरिक गतिविधि या व्यायाम करते हैं?", 
     "en": "Do you engage in regular physical activity or exercise?", 
     "category": "hypertension", "symptom": "physical activity"},
    {"hi": "क्या आप सिरदर्द, चक्कर आना, या सीने में दर्द जैसे लक्षण अनुभव कर रहे हैं?", 
     "en": "Are you experiencing any symptoms like headaches, dizziness, or chest pain?", 
     "category": "hypertension", "symptom": "hypertension symptoms"},
    {"hi": "आप अपने दैनिक जीवन में कितना तनाव महसूस कर रहे हैं?", 
     "en": "How much stress are you experiencing in your daily life?", 
     "category": "hypertension", "symptom": "stress levels"},
    {"hi": "क्या आप नियमित रूप से अपने रक्तचाप की निगरानी करते हैं? यदि हाँ, तो आपके सामान्य रक्तचाप के पठन क्या हैं?", 
     "en": "Do you monitor your blood pressure regularly? If so, what are your typical readings?", 
     "category": "hypertension", "symptom": "blood pressure monitoring"}
],

'tremors' : [
    #{"hi": "आपको कितने समय से कंपन महसूस हो रहे हैं?", "en": "How long have you been experiencing tremors?", "category": "tremors", "symptom": "duration of tremors"},
    {"hi": "क्या कंपन हमेशा होते हैं या यह आते-जाते हैं?", "en": "Are the tremors present all the time or do they come and go?", "category": "tremors", "symptom": "tremor frequency"},
    {"hi": "क्या कंपन आपके शरीर के किसी विशेष हिस्से में होते हैं (जैसे, हाथ, सिर, आवाज)?", 
     "en": "Do the tremors occur in specific parts of your body (e.g., hands, head, voice)?", 
     "category": "tremors", "symptom": "affected body parts"},
    {"hi": "क्या कंपन किसी विशेष गतिविधि के साथ और अधिक बढ़ जाते हैं, जैसे कुछ पकड़ने या हिलाने के दौरान?", 
     "en": "Do the tremors get worse with certain activities, like holding something or moving?", 
     "category": "tremors", "symptom": "activity-related worsening"},
    {"hi": "क्या आप कोई अन्य लक्षण अनुभव कर रहे हैं, जैसे कमजोरी, कठोरता, या समन्वय में समस्या?", 
     "en": "Are you experiencing any other symptoms, such as weakness, stiffness, or difficulty with coordination?", 
     "category": "tremors", "symptom": "associated symptoms"},
    {"hi": "क्या आपके परिवार में कंपन या न्यूरोलॉजिकल स्थितियों का इतिहास है (जैसे, पार्किंसंस रोग)?", 
     "en": "Do you have a family history of tremors or neurological conditions (e.g., Parkinson’s disease)?", 
     "category": "tremors", "symptom": "family history of neurological conditions"},
    {"hi": "क्या आपने हाल ही में कोई तनाव, चिंता, या मानसिक परिवर्तन अनुभव किए हैं?", 
     "en": "Have you recently experienced any stress, anxiety, or emotional changes?", 
     "category": "tremors", "symptom": "emotional or stress-related changes"},
    {"hi": "क्या आप कोई दवाइयाँ ले रहे हैं, जिसमें पर्ची वाली, ओवर-द-काउंटर दवाइयाँ, या सप्लीमेंट्स शामिल हैं?", 
     "en": "Are you taking any medications, including prescription, over-the-counter, or supplements?", 
     "category": "tremors", "symptom": "medication use"},
    {"hi": "क्या आपको हाल ही में कोई चोट, संक्रमण, या बीमारी हुई है जो आपके तंत्रिका तंत्र को प्रभावित कर सकती है?", 
     "en": "Have you had any recent injuries, infections, or illnesses that might affect your nervous system?", 
     "category": "tremors", "symptom": "nervous system impact"},
    {"hi": "क्या आप शराब पीते हैं या कैफीन का सेवन करते हैं, और यदि हां, तो कितनी मात्रा में और कितनी बार?", 
     "en": "Do you drink alcohol or consume caffeine, and if so, how much and how often?", 
     "category": "tremors", "symptom": "alcohol or caffeine consumption"}
],

'panic attack' : [
    #{"hi": "आपको कितने समय से पैनिक अटैक का अनुभव हो रहा है?", "en": "How long have you been experiencing panic attacks?", "category": "panic_attack", "symptom": "duration of panic attacks"},
    {"hi": "आपको कितनी बार पैनिक अटैक होते हैं?", "en": "How often do you have panic attacks?", "category": "panic_attack", "symptom": "frequency of panic attacks"},
    {"hi": "आप पैनिक अटैक के दौरान कौन-कौन से लक्षण अनुभव करते हैं (जैसे, तेज़ दिल की धड़कन, पसीना, छाती में दर्द, सांस लेने में कठिनाई)?", 
     "en": "What symptoms do you experience during a panic attack (e.g., rapid heartbeat, sweating, chest pain, shortness of breath)?", 
     "category": "panic_attack", "symptom": "symptoms during panic attack"},
    {"hi": "क्या पैनिक अटैक अचानक होते हैं, या आपको कुछ विशेष उत्तेजक (जैसे, तनावपूर्ण स्थिति, भीड़) का पता चलता है?", 
     "en": "Do the panic attacks occur unexpectedly, or do you notice specific triggers (e.g., stressful situations, crowds)?", 
     "category": "panic_attack", "symptom": "triggers of panic attacks"},
    {"hi": "क्या आपको पैनिक अटैक के अलावा भी चिंता या घबराहट महसूस होती है?", 
     "en": "Do you feel anxious or nervous even when you're not having a panic attack?", 
     "category": "panic_attack", "symptom": "general anxiety"},
    {"hi": "क्या आपने हाल ही में कोई बड़ा जीवन परिवर्तन या आघातक घटना अनुभव की है?", 
     "en": "Have you experienced any major life stressors or traumatic events recently?", 
     "category": "panic_attack", "symptom": "recent stressors or trauma"},
    {"hi": "क्या आप पैनिक अटैक के डर से कुछ स्थानों या स्थितियों से बचते हैं?", 
     "en": "Do you avoid certain situations or places because of the fear of having a panic attack?", 
     "category": "panic_attack", "symptom": "avoidance behaviors"},
    {"hi": "क्या आपको किसी अन्य मानसिक स्वास्थ्य समस्याओं का निदान हुआ है, जैसे चिंता, अवसाद, या PTSD?", 
     "en": "Have you been diagnosed with any other mental health conditions, such as anxiety, depression, or PTSD?", 
     "category": "panic_attack", "symptom": "co-occurring mental health conditions"},
    {"hi": "क्या आप कोई दवाइयाँ ले रहे हैं, जिसमें ओवर-द-काउंटर या हर्बल सप्लीमेंट्स भी शामिल हैं?", 
     "en": "Are you taking any medications, including over-the-counter or herbal supplements?", 
     "category": "panic_attack", "symptom": "medication use"},
    {"hi": "क्या आपने पैनिक अटैक के दौरान के अलावा कोई शारीरिक परिवर्तन महसूस किए हैं, जैसे सांस लेने में कठिनाई या छाती में दर्द?", 
     "en": "Have you noticed any physical changes, such as difficulty breathing or chest pain, when you are not having a panic attack?", 
     "category": "panic_attack", "symptom": "physical changes outside of panic attacks"}
],

'mood swings' : [
    #{"hi": "आपको कितने समय से मूड स्विंग्स का अनुभव हो रहा है?", "en": "How long have you been experiencing mood swings?", "category": "mood_swings", "symptom": "duration of mood swings"},
    {"hi": "आपके मूड स्विंग्स कितनी बार होते हैं?", "en": "How often do your mood swings occur?", "category": "mood_swings", "symptom": "frequency of mood swings"},
    {"hi": "आप किस प्रकार के मूड परिवर्तनों का अनुभव करते हैं (जैसे, बहुत खुश या बहुत उदास महसूस करना)?", 
     "en": "What types of mood changes do you experience (e.g., feeling very happy or very sad)?", 
     "category": "mood_swings", "symptom": "types of mood changes"},
    {"hi": "क्या आपके मूड स्विंग्स कुछ विशेष घटनाओं या परिस्थितियों द्वारा प्रेरित होते हैं?", 
     "en": "Do your mood swings seem to be triggered by specific events or situations?", 
     "category": "mood_swings", "symptom": "triggers of mood swings"},
    {"hi": "क्या आप मूड स्विंग्स के बीच चिड़चिड़े, चिंतित, या अवसादित महसूस करते हैं?", 
     "en": "Do you feel irritable, anxious, or depressed between mood swings?", 
     "category": "mood_swings", "symptom": "mood between swings"},
    {"hi": "क्या आपने अपने मूड परिवर्तनों में कोई पैटर्न देखा है, जैसे दिन के कुछ विशेष समयों या सप्ताह के दिनों में?", 
     "en": "Have you noticed any patterns in your mood changes, such as certain times of the day or during the week?", 
     "category": "mood_swings", "symptom": "patterns of mood changes"},
    {"hi": "क्या आप शारीरिक लक्षणों का अनुभव कर रहे हैं, जैसे नींद, भूख, या ऊर्जा स्तर में बदलाव?", 
     "en": "Are you experiencing any physical symptoms, such as changes in sleep, appetite, or energy levels?", 
     "category": "mood_swings", "symptom": "physical symptoms during mood swings"},
    {"hi": "क्या आपने हाल ही में कोई बड़ा जीवन परिवर्तन, तनावपूर्ण घटना या आघातक अनुभव किया है?", 
     "en": "Have you experienced any major life stressors, changes, or traumatic events recently?", 
     "category": "mood_swings", "symptom": "recent life stressors or trauma"},
    {"hi": "क्या आपके परिवार में मूड विकारों, जैसे बाइपोलर डिसऑर्डर या अवसाद का इतिहास है?", 
     "en": "Do you have a family history of mood disorders, such as bipolar disorder or depression?", 
     "category": "mood_swings", "symptom": "family history of mood disorders"},
    {"hi": "क्या आप कोई दवाइयाँ ले रहे हैं, जिसमें ओवर-द-काउंटर दवाइयाँ या हर्बल सप्लीमेंट्स शामिल हैं, जो आपके मूड को प्रभावित कर सकते हैं?", 
     "en": "Are you taking any medications, including over-the-counter or herbal supplements, that could affect your mood?", 
     "category": "mood_swings", "symptom": "medication use affecting mood"}
],

'memory loss' : [
    {"hi": "आपको कितने समय से याददाश्त की समस्या हो रही है?", "en": "How long have you been experiencing memory loss?", "category": "memory_loss", "symptom": "duration of memory loss"},
    {"hi": "क्या याददाश्त की समस्या धीरे-धीरे बढ़ी है या अचानक हुई है?", "en": "Is the memory loss gradual or sudden?", "category": "memory_loss", "symptom": "gradual or sudden memory loss"},
    {"hi": "आप किस प्रकार की याददाश्त की समस्याओं का सामना कर रहे हैं (जैसे नाम, नियुक्तियां, या हाल की घटनाओं को भूलना)?", 
     "en": "What type of memory problems are you experiencing (e.g., forgetting names, appointments, or recent events)?", 
     "category": "memory_loss", "symptom": "types of memory problems"},
    {"hi": "क्या आपको पुरानी घटनाओं को याद करने में कठिनाई हो रही है, या मुख्य रूप से हाल की याददाश्त प्रभावित हो रही है?", 
     "en": "Do you have difficulty recalling past events, or is it mainly recent memory that's affected?", 
     "category": "memory_loss", "symptom": "recent vs past memory"},
    {"hi": "क्या आप भ्रम या दिशाहीनता महसूस करते हैं (जैसे, परिचित स्थानों में खो जाना)?", 
     "en": "Do you experience confusion or disorientation (e.g., getting lost in familiar places)?", 
     "category": "memory_loss", "symptom": "confusion or disorientation"},
    {"hi": "क्या आपको कार्यों पर ध्यान केंद्रित करने में समस्या हो रही है?", 
     "en": "Are you having trouble concentrating or focusing on tasks?", 
     "category": "memory_loss", "symptom": "trouble concentrating"},
    {"hi": "क्या आपको हाल ही में कोई सिर की चोट, संक्रमण, या बीमारी हुई है?", 
     "en": "Have you had any recent head injuries, infections, or illnesses?", 
     "category": "memory_loss", "symptom": "recent head injuries or illnesses"},
    {"hi": "क्या आपके परिवार में याददाश्त की समस्याओं या अल्जाइमर रोग या डिमेंशिया जैसी स्थितियों का इतिहास है?", 
     "en": "Do you have a family history of memory problems or conditions like Alzheimer's disease or dementia?", 
     "category": "memory_loss", "symptom": "family history of memory problems"},
    {"hi": "क्या आपने अपनी मानसिक स्थिति में कोई परिवर्तन महसूस किया है, जैसे अवसाद, चिंता, या चिड़चिड़ापन?", 
     "en": "Have you noticed any changes in your mood, such as depression, anxiety, or irritability?", 
     "category": "memory_loss", "symptom": "mood changes"},
    {"hi": "क्या आप कोई दवाइयाँ या सप्लीमेंट्स ले रहे हैं जो आपकी याददाश्त को प्रभावित कर सकते हैं (जैसे, सोदीन, दर्द निवारक, या एंटीडिप्रेसेंट)?", 
     "en": "Are you taking any medications or supplements that could affect your memory (e.g., sedatives, pain relievers, or antidepressants)?", 
     "category": "memory_loss", "symptom": "medication affecting memory"}
],

'difficulty concentrating' : [
    {"hi": "आपको कितने समय से एकाग्रता में कठिनाई हो रही है?", "en": "How long have you been experiencing difficulty concentrating?", "category": "difficulty_concentrating", "symptom": "duration of concentration difficulty"},
    {"hi": "क्या एकाग्रता में कठिनाई स्थायी है या कभी-कभी होती है?", "en": "Is the difficulty with concentration constant or does it come and go?", "category": "difficulty_concentrating", "symptom": "constant vs intermittent concentration difficulty"},
    {"hi": "क्या आपको विशिष्ट कार्यों पर ध्यान केंद्रित करने में कठिनाई हो रही है, या यह अधिक सामान्य है?", 
     "en": "Do you find it hard to focus on specific tasks, or is it more general?", 
     "category": "difficulty_concentrating", "symptom": "focus on tasks"},
    {"hi": "क्या आपको चीज़ों को याद करने या कार्यों को पूरा करने में समस्या हो रही है?", 
     "en": "Do you have trouble remembering things or following through with tasks?", 
     "category": "difficulty_concentrating", "symptom": "memory and task completion"},
    {"hi": "क्या आप अन्य लक्षणों का अनुभव कर रहे हैं, जैसे थकावट, चिड़चिड़ापन, या नींद की समस्याएं?", 
     "en": "Are you experiencing any other symptoms, such as fatigue, irritability, or sleep problems?", 
     "category": "difficulty_concentrating", "symptom": "associated symptoms (fatigue, irritability, sleep problems)"},
    {"hi": "क्या आपने हाल ही में कोई महत्वपूर्ण तनाव, चिंता, या भावनात्मक समस्याएं अनुभव की हैं?", 
     "en": "Have you recently experienced significant stress, anxiety, or emotional challenges?", 
     "category": "difficulty_concentrating", "symptom": "stress, anxiety, or emotional challenges"},
    {"hi": "क्या आपको मानसिक स्वास्थ्य स्थितियों का कोई इतिहास है, जैसे ADHD, अवसाद, या चिंता?", 
     "en": "Do you have a history of mental health conditions, such as ADHD, depression, or anxiety?", 
     "category": "difficulty_concentrating", "symptom": "mental health history"},
    {"hi": "क्या आप वर्तमान में कोई दवाइयाँ या सप्लीमेंट्स ले रहे हैं जो आपके ध्यान को प्रभावित कर सकते हैं?", 
     "en": "Are you currently taking any medications or supplements that could affect your focus?", 
     "category": "difficulty_concentrating", "symptom": "medications affecting concentration"},
    {"hi": "क्या आपको कोई मेडिकल स्थितियां हैं, जैसे थायरॉयड समस्या, मधुमेह, या स्लीप एपनिया, जो आपकी एकाग्रता को प्रभावित कर सकती हैं?", 
     "en": "Do you have any medical conditions, such as thyroid problems, diabetes, or sleep apnea, that could affect your concentration?", 
     "category": "difficulty_concentrating", "symptom": "medical conditions affecting concentration"},
    {"hi": "क्या आपने अपनी जीवनशैली में कोई परिवर्तन महसूस किया है, जैसे नींद की खराब आदतें, आहार, या व्यायाम स्तर, जो एकाग्रता में कठिनाई का कारण हो सकते हैं?", 
     "en": "Have you had any changes in your lifestyle, such as poor sleep habits, diet, or exercise levels, that might be contributing to the difficulty concentrating?", 
     "category": "difficulty_concentrating", "symptom": "lifestyle changes affecting concentration"}
],

'hallucinations' : [
    {"hi": "आपको कितने समय से भ्रांतियाँ हो रही हैं?", "en": "How long have you been experiencing hallucinations?", "category": "hallucinations", "symptom": "duration of hallucinations"},
    {"hi": "आप किस प्रकार की भ्रांतियाँ अनुभव कर रहे हैं (जैसे, आवाजें सुनना, चीज़ें देखना, गंध महसूस करना)?", 
     "en": "What type of hallucinations are you experiencing (e.g., hearing voices, seeing things, smelling odors)?", 
     "category": "hallucinations", "symptom": "type of hallucinations"},
    {"hi": "क्या भ्रांतियाँ दिन में, रात में, या दोनों समय होती हैं?", 
     "en": "Are the hallucinations occurring during the day, at night, or both?", 
     "category": "hallucinations", "symptom": "time of hallucinations"},
    {"hi": "क्या भ्रांतियाँ आपको वास्तविक लगती हैं, या आप उन्हें झूठी पहचानते हैं?", 
     "en": "Do the hallucinations seem real to you, or do you recognize them as being false?", 
     "category": "hallucinations", "symptom": "real or false perception"},
    {"hi": "क्या भ्रांतियाँ किसी विशिष्ट उत्तेजक से जुड़ी हुई हैं, जैसे तनाव, नींद की कमी, या कुछ परिस्थितियाँ?", 
     "en": "Are the hallucinations associated with any specific triggers, such as stress, sleep deprivation, or certain situations?", 
     "category": "hallucinations", "symptom": "triggers for hallucinations"},
    {"hi": "क्या आपने अपनी मानसिक स्थिति में कोई परिवर्तन महसूस किया है, जैसे मूड स्विंग्स, चिंता, या अवसाद?", 
     "en": "Have you experienced any changes in your mental health, such as mood swings, anxiety, or depression?", 
     "category": "hallucinations", "symptom": "mental health changes"},
    {"hi": "क्या आप कोई दवाइयाँ, ओवर-द-काउंटर दवाइयाँ, या अवैध नशीली दवाएँ ले रहे हैं?", 
     "en": "Are you taking any medications, including prescription, over-the-counter, or recreational drugs?", 
     "category": "hallucinations", "symptom": "medications or drugs"},
    {"hi": "क्या आपके पास मानसिक स्वास्थ्य स्थितियों का कोई इतिहास है, जैसे स्किजोफ्रेनिया, बाइपोलर डिसऑर्डर, या प्रमुख अवसाद?", 
     "en": "Do you have any history of mental health conditions, such as schizophrenia, bipolar disorder, or major depression?", 
     "category": "hallucinations", "symptom": "mental health history"},
    {"hi": "क्या आपको हाल ही में सिर की चोट, संक्रमण, या तंत्रिका तंत्र से संबंधित कोई समस्या हुई है, जो आपके मस्तिष्क को प्रभावित कर सकती है?", 
     "en": "Have you had any recent head injuries, infections, or neurological conditions that might affect your brain?", 
     "category": "hallucinations", "symptom": "head injuries or neurological conditions"},
    {"hi": "क्या आपके परिवार में मानसिक स्वास्थ्य विकारों का कोई इतिहास है, जैसे मानसिक विकृति या मादक पदार्थों का दुरुपयोग?", 
     "en": "Do you have a family history of mental health disorders, such as psychosis or substance abuse?", 
     "category": "hallucinations", "symptom": "family history of mental health disorders"}
],

'delusions' : [
    {"hi": "आपको कितने समय से भ्रांतियाँ हो रही हैं?", "en": "How long have you been experiencing delusions?", "category": "delusions", "symptom": "duration of delusions"},
    {"hi": "आप किस प्रकार की भ्रांतियाँ अनुभव कर रहे हैं (जैसे, संदेहवादी, महानता, विचित्र)?", 
     "en": "What kind of delusions are you experiencing (e.g., paranoid, grandiose, bizarre)?", 
     "category": "delusions", "symptom": "type of delusions"},
    {"hi": "क्या आपको लगता है कि दूसरे लोग आपको नुकसान पहुँचाने की कोशिश कर रहे हैं, या कि आपके पास विशेष शक्तियाँ या क्षमताएँ हैं?", 
     "en": "Do you believe that others are out to harm you, or that you have special powers or abilities?", 
     "category": "delusions", "symptom": "paranoia or grandiosity"},
    {"hi": "क्या भ्रांतियाँ आपके दैनिक जीवन या रिश्तों को प्रभावित कर रही हैं?", 
     "en": "Are the delusions affecting your daily life or relationships?", 
     "category": "delusions", "symptom": "impact on daily life or relationships"},
    {"hi": "क्या आप मानते हैं कि आपके विश्वास वास्तविक नहीं हो सकते, या क्या आप वास्तव में उन्हें सत्य मानते हैं?", 
     "en": "Do you recognize that your beliefs may not be real, or do you truly believe them to be true?", 
     "category": "delusions", "symptom": "recognition of false beliefs"},
    {"hi": "क्या आपने हाल ही में कोई महत्वपूर्ण तनाव, जीवन परिवर्तन, या आघातपूर्ण घटनाएँ अनुभव की हैं?", 
     "en": "Have you experienced any major stressors, life changes, or traumatic events recently?", 
     "category": "delusions", "symptom": "recent stressors or trauma"},
    {"hi": "क्या आप कोई दवाइयाँ, ओवर-द-काउंटर दवाइयाँ, या अवैध नशीली दवाएँ ले रहे हैं?", 
     "en": "Are you currently taking any medications, including prescription, over-the-counter, or recreational drugs?", 
     "category": "delusions", "symptom": "medications or drugs"},
    {"hi": "क्या आपके पास मानसिक स्वास्थ्य स्थितियों का कोई इतिहास है, जैसे स्किजोफ्रेनिया, बाइपोलर डिसऑर्डर, या अवसाद?", 
     "en": "Do you have a history of mental health conditions, such as schizophrenia, bipolar disorder, or depression?", 
     "category": "delusions", "symptom": "mental health history"},
    {"hi": "क्या आपको हाल ही में सिर की चोट, संक्रमण, या तंत्रिका तंत्र से संबंधित कोई समस्या हुई है, जो आपके सोचने की क्षमता को प्रभावित कर सकती है?", 
     "en": "Have you had any recent head injuries, infections, or neurological conditions that might affect your thinking?", 
     "category": "delusions", "symptom": "head injuries or neurological conditions"},
    {"hi": "क्या आपके परिवार में मानसिक स्वास्थ्य विकारों का कोई इतिहास है, जैसे मानसिक विकृति, स्किजोफ्रेनिया, या बाइपोलर डिसऑर्डर?", 
     "en": "Do you have a family history of mental health disorders, such as psychosis, schizophrenia, or bipolar disorder?", 
     "category": "delusions", "symptom": "family history of mental health disorders"}
],

'paranoia' : [
    {"hi": "आपको कितने समय से दूसरों के प्रति संदेह या भय महसूस हो रहा है?", 
     "en": "How long have you been feeling paranoid or suspicious of others?", 
     "category": "paranoia", 
     "symptom": "duration of paranoia"},
    {"hi": "आपके पास लोगों के बारे में क्या विशिष्ट डर या चिंता हैं (जैसे, यह मानना कि लोग आपके खिलाफ साजिश कर रहे हैं या आपकी जासूसी कर रहे हैं)?", 
     "en": "What specific fears or concerns do you have about people (e.g., believing others are plotting against you or spying on you)?", 
     "category": "paranoia", 
     "symptom": "specific fears or concerns"},
    {"hi": "क्या आपको लगता है कि लोग जानबूझकर आपको नुकसान पहुँचाने या धोखा देने की कोशिश कर रहे हैं?", 
     "en": "Do you feel that people are intentionally trying to harm or deceive you?", 
     "category": "paranoia", 
     "symptom": "belief of harm or deception"},
    {"hi": "क्या यह विचार स्थिर हैं, या क्या वे आते-जाते रहते हैं?", 
     "en": "Are these thoughts persistent, or do they come and go?", 
     "category": "paranoia", 
     "symptom": "persistence of thoughts"},
    {"hi": "क्या आपने अपने संदेहपूर्ण विचारों के लिए कोई उत्तेजक देखा है (जैसे, कुछ लोग, परिस्थितियाँ, या स्थान)?", 
     "en": "Have you noticed any triggers for your paranoid thoughts (e.g., certain people, situations, or places)?", 
     "category": "paranoia", 
     "symptom": "triggers for paranoid thoughts"},
    {"hi": "क्या आपको दोस्तों, परिवार, या सहकर्मियों पर विश्वास करने में कठिनाई होती है?", 
     "en": "Do you have difficulty trusting friends, family, or coworkers?", 
     "category": "paranoia", 
     "symptom": "difficulty trusting others"},
    {"hi": "क्या आप अन्य कोई लक्षण अनुभव कर रहे हैं, जैसे चिंता, मूड स्विंग्स, या नींद में कठिनाई?", 
     "en": "Are you experiencing any other symptoms, such as anxiety, mood swings, or difficulty sleeping?", 
     "category": "paranoia", 
     "symptom": "other symptoms (e.g., anxiety, sleep problems)"},
    {"hi": "क्या आपने हाल ही में कोई महत्वपूर्ण तनाव, आघातपूर्ण घटनाएँ, या जीवन में कोई बड़ा परिवर्तन अनुभव किया है?", 
     "en": "Have you experienced any major stressors, traumatic events, or significant life changes recently?", 
     "category": "paranoia", 
     "symptom": "recent stressors or life changes"},
    {"hi": "क्या आप कोई दवाइयाँ, ओवर-द-काउंटर दवाइयाँ, या अवैध नशीली दवाएँ ले रहे हैं?", 
     "en": "Are you taking any medications, including prescription, over-the-counter, or recreational drugs?", 
     "category": "paranoia", 
     "symptom": "medications or drugs"},
    {"hi": "क्या आपके परिवार में मानसिक स्वास्थ्य विकारों का कोई इतिहास है, जैसे स्किजोफ्रेनिया, बाइपोलर डिसऑर्डर, या चिंता विकार?", 
     "en": "Do you have a family history of mental health conditions, such as schizophrenia, bipolar disorder, or anxiety disorders?", 
     "category": "paranoia", 
     "symptom": "family history of mental health conditions"}
],

'euphoria' : [
    {"hi": "आपको कितने समय से उत्साह (अत्यधिक खुशी या खुशी का अनुभव) हो रहा है?", 
     "en": "How long have you been experiencing euphoria (feeling unusually happy or elated)?", 
     "category": "euphoria", 
     "symptom": "duration of euphoria"},
    {"hi": "इन उत्साही भावनाओं की तीव्रता कितनी है?", 
     "en": "How intense are these feelings of euphoria?", 
     "category": "euphoria", 
     "symptom": "intensity of euphoria"},
    {"hi": "क्या आपको लगता है कि यह उत्साह आपके चारों ओर की स्थिति या घटनाओं के मुकाबले अत्यधिक है?", 
     "en": "Do you feel that the euphoria is out of proportion to the situation or events around you?", 
     "category": "euphoria", 
     "symptom": "disproportionate euphoria"},
    {"hi": "क्या आप अन्य कोई लक्षण अनुभव कर रहे हैं, जैसे दौड़ते विचार, अत्यधिक ऊर्जा, या आवेगी व्यवहार?", 
     "en": "Are you experiencing any other symptoms, such as racing thoughts, excessive energy, or impulsive behavior?", 
     "category": "euphoria", 
     "symptom": "associated symptoms (e.g., racing thoughts, impulsivity)"},
    {"hi": "क्या आपको असामान्य रूप से आत्मविश्वासी, ऊर्जावान, या 'दुनिया के शीर्ष पर' जैसा महसूस हो रहा है?", 
     "en": "Do you feel unusually confident, energetic, or 'on top of the world'?", 
     "category": "euphoria", 
     "symptom": "feeling of being 'on top of the world'"},
    {"hi": "क्या आपने अपने उत्साह के लिए कोई पैटर्न या उत्तेजक देखा है (जैसे, कुछ स्थितियाँ, समय का हिस्सा, या गतिविधियाँ)?", 
     "en": "Have you noticed any patterns or triggers for your euphoria (e.g., certain situations, times of day, or activities)?", 
     "category": "euphoria", 
     "symptom": "triggers for euphoria"},
    {"hi": "क्या आप कोई दवाइयाँ, ओवर-द-काउंटर दवाइयाँ, या अवैध नशीली दवाएँ ले रहे हैं (जैसे, उत्तेजक या शराब)?", 
     "en": "Are you taking any medications, including prescription, over-the-counter, or recreational drugs (e.g., stimulants or alcohol)?", 
     "category": "euphoria", 
     "symptom": "medications or drugs"},
    {"hi": "क्या आपके मानसिक स्वास्थ्य में कोई महत्वपूर्ण परिवर्तन हुए हैं, जैसे अवसाद, चिंता, या चिड़चिड़ापन?", 
     "en": "Have you had any significant changes in your mental health, such as periods of depression, anxiety, or irritability?", 
     "category": "euphoria", 
     "symptom": "changes in mental health (e.g., depression, anxiety)"},
    {"hi": "क्या आपके पास मानसिक स्वास्थ्य विकारों का इतिहास है, जैसे बाइपोलर डिसऑर्डर, उन्माद, या नशीली दवाओं का दुरुपयोग?", 
     "en": "Do you have a history of mental health conditions, such as bipolar disorder, mania, or substance abuse?", 
     "category": "euphoria", 
     "symptom": "history of mental health conditions"},
    {"hi": "क्या आपके परिवार में मानसिक स्वास्थ्य विकारों का इतिहास है, विशेष रूप से मूड विकारों जैसे बाइपोलर डिसऑर्डर या स्किजोफ्रेनिया?", 
     "en": "Do you have a family history of mental health disorders, particularly mood disorders like bipolar disorder or schizophrenia?", 
     "category": "euphoria", 
     "symptom": "family history of mood disorders"}
],

'lack of motivation' : [
    {"hi": "आपको कितने समय से प्रेरणा की कमी महसूस हो रही है?", "en": "How long have you been feeling a lack of motivation?", "category": "lack_of_motivation", "symptom": "duration of lack of motivation"},
    {"hi": "क्या प्रेरणा की कमी लगातार है, या यह आती-जाती रहती है?", "en": "Is the lack of motivation constant, or does it come and go?", "category": "lack_of_motivation", "symptom": "consistency of lack of motivation"},
    {"hi": "क्या कुछ विशेष गतिविधियाँ या कार्य हैं जिन्हें करने के लिए आपको प्रेरणा की कमी महसूस होती है (जैसे काम, शौक, सामाजिक गतिविधियाँ)?", "en": "Are there specific activities or tasks you feel unmotivated to do (e.g., work, hobbies, socializing)?", "category": "lack_of_motivation", "symptom": "specific activities affected by lack of motivation"},
    {"hi": "क्या आपने अपनी ऊर्जा स्तर या ध्यान केंद्रित करने की क्षमता में कोई बदलाव महसूस किया है?", "en": "Have you noticed any changes in your energy levels or ability to focus?", "category": "lack_of_motivation", "symptom": "changes in energy and focus"},
    {"hi": "क्या आप अन्य कोई लक्षण अनुभव कर रहे हैं, जैसे उदासी, चिंता, या चिड़चिड़ापन?", "en": "Are you experiencing any other symptoms, such as sadness, anxiety, or irritability?", "category": "lack_of_motivation", "symptom": "associated symptoms (e.g., sadness, anxiety, irritability)"},
    {"hi": "क्या आपको ऐसा महसूस हो रहा है कि आप कार्य शुरू करने में असमर्थ हैं, यहां तक कि वे कार्य जिन्हें आप पहले पसंद करते थे?", "en": "Do you feel overwhelmed or unable to start tasks, even ones you used to enjoy?", "category": "lack_of_motivation", "symptom": "difficulty starting tasks"},
    {"hi": "क्या हाल ही में कोई महत्वपूर्ण जीवन परिवर्तन, तनाव, या मानसिक चुनौतियाँ आई हैं?", "en": "Have there been any significant life changes, stressors, or emotional challenges recently?", "category": "lack_of_motivation", "symptom": "life changes or stressors"},
    {"hi": "क्या आप अच्छे से सो रहे हैं, या आपकी नींद के पैटर्न में कोई बदलाव आया है (जैसे, अनिद्रा या अत्यधिक सोना)?", "en": "Are you sleeping well, or have you experienced any changes in your sleep patterns (e.g., insomnia or excessive sleeping)?", "category": "lack_of_motivation", "symptom": "changes in sleep patterns"},
    {"hi": "क्या आपके पास मानसिक स्वास्थ्य की कोई पूर्ववर्ती स्थिति है, जैसे अवसाद, चिंता, या ADHD?", "en": "Do you have a history of mental health conditions, such as depression, anxiety, or ADHD?", "category": "lack_of_motivation", "symptom": "history of mental health conditions"},
    {"hi": "क्या आप कोई दवाइयाँ ले रहे हैं, जिसमें प्रेसक्रिप्शन, ओवर-द-काउंटर, या अवैध नशीली दवाएँ शामिल हैं?", "en": "Are you currently taking any medications, including prescription, over-the-counter, or recreational drugs?", "category": "lack_of_motivation", "symptom": "medications or drugs"}
],

'bone fracture' : [
    {"hi": "फ्रैक्चर कैसे हुआ (जैसे गिरना, दुर्घटना, खेलों की चोट)?", "en": "How did the fracture occur (e.g., fall, accident, sports injury)?", "category": "bone_fracture", "symptom": "cause of fracture"},
    {"hi": "कौन सा हड्डी फ्रैक्चर हुई है, और दर्द कहाँ है?", "en": "Which bone is fractured, and where is the pain located?", "category": "bone_fracture", "symptom": "location and type of fracture"},
    {"hi": "चोट कब लगी थी?", "en": "When did the injury happen?", "category": "bone_fracture", "symptom": "timing of injury"},
    {"hi": "क्या आपको चोट लगते समय कोई पॉपिंग या क्रैकिंग की आवाज़ सुनाई दी थी?", "en": "Did you hear a popping or cracking sound when the injury occurred?", "category": "bone_fracture", "symptom": "sound during injury"},
    {"hi": "क्या आपको घायल क्षेत्र के आसपास सूजन, चोट, या विकृति का अनुभव हो रहा है?", "en": "Are you experiencing any swelling, bruising, or deformity around the injured area?", "category": "bone_fracture", "symptom": "swelling, bruising, or deformity"},
    {"hi": "क्या आपको प्रभावित अंग या जोड़ों को हिलाने में कठिनाई हो रही है?", "en": "Do you have difficulty moving the affected limb or joint?", "category": "bone_fracture", "symptom": "difficulty moving affected limb"},
    {"hi": "क्या आपके पास पहले कोई फ्रैक्चर या हड्डी की चोटें रही हैं?", "en": "Have you had any previous fractures or bone injuries?", "category": "bone_fracture", "symptom": "history of fractures or bone injuries"},
    {"hi": "क्या आपके पास कोई मेडिकल स्थितियाँ हैं जो हड्डी स्वास्थ्य को प्रभावित करती हैं (जैसे, ऑस्टियोपोरोसिस, हड्डी का कैंसर)?", "en": "Do you have any medical conditions that affect bone health (e.g., osteoporosis, bone cancer)?", "category": "bone_fracture", "symptom": "underlying medical conditions affecting bone health"},
    {"hi": "क्या आप कोई दवाइयाँ ले रहे हैं, जिसमें कैल्शियम या विटामिन D जैसे सप्लीमेंट शामिल हैं?", "en": "Are you currently taking any medications, including supplements like calcium or vitamin D?", "category": "bone_fracture", "symptom": "current medications or supplements"},
    {"hi": "क्या आपके परिवार में हड्डी संबंधित समस्याएँ या हड्डी की मजबूती को प्रभावित करने वाली स्थितियाँ हैं?", "en": "Do you have a family history of bone problems or conditions that affect bone strength?", "category": "bone_fracture", "symptom": "family history of bone problems"}
],

'bone pain' : [
    {"hi": "हड्डी का दर्द कहाँ स्थित है?", "en": "Where exactly is the bone pain located?", "category": "bone_pain", "symptom": "location of bone pain"},
    {"hi": "आपको यह दर्द कब से हो रहा है?", "en": "How long have you been experiencing the pain?", "category": "bone_pain", "symptom": "duration of bone pain"},
    {"hi": "क्या यह दर्द लगातार है, या यह आता-जाता रहता है?", "en": "Is the pain constant, or does it come and go?", "category": "bone_pain", "symptom": "nature of bone pain"},
    {"hi": "क्या दर्द तीव्र, कुहनी, धड़कता हुआ, या दुखने वाला है?", "en": "Is the pain sharp, dull, throbbing, or aching?", "category": "bone_pain", "symptom": "type of bone pain"},
    {"hi": "क्या दर्द हलचल, दबाव, या कुछ गतिविधियों के साथ बढ़ता है?", "en": "Does the pain get worse with movement, pressure, or certain activities?", "category": "bone_pain", "symptom": "pain exacerbation"},
    {"hi": "क्या आपको हाल ही में कोई चोटें, गिरना या दुर्घटनाएं हुई हैं?", "en": "Have you had any recent injuries, falls, or accidents?", "category": "bone_pain", "symptom": "recent injuries or accidents"},
    {"hi": "क्या आपको प्रभावित क्षेत्र के आसपास सूजन, चोट, या लाली महसूस हो रही है?", "en": "Are you experiencing any swelling, bruising, or redness around the affected area?", "category": "bone_pain", "symptom": "swelling, bruising, or redness"},
    {"hi": "क्या आपने प्रभावित अंग या जोड़ों में कमजोरी, सुन्नता, या आंदोलन में कठिनाई महसूस की है?", "en": "Have you noticed any weakness, numbness, or difficulty moving the affected limb or joint?", "category": "bone_pain", "symptom": "weakness or difficulty moving"},
    {"hi": "क्या आपके पास कोई ऐसी मेडिकल स्थितियाँ हैं जो आपकी हड्डियों को प्रभावित करती हैं, जैसे कि ऑस्टियोपोरोसिस, आर्थ्राइटिस या कैंसर?", "en": "Do you have any medical conditions that might affect your bones, such as osteoporosis, arthritis, or cancer?", "category": "bone_pain", "symptom": "underlying conditions affecting bones"},
    {"hi": "क्या आप कोई दवाइयाँ या सप्लीमेंट्स ले रहे हैं, जैसे कि कैल्शियम या विटामिन D?", "en": "Are you taking any medications or supplements, including calcium or vitamin D?", "category": "bone_pain", "symptom": "medications or supplements"}
],

'sprain' : [
    {"hi": "स्ट्रेन कैसे हुआ (जैसे, गिरना, खेल की चोट, दुर्घटना)?", "en": "How did the sprain occur (e.g., fall, sports injury, accident)?", "category": "sprain", "symptom": "mechanism of injury"},
    {"hi": "कौन सा जोड़ा या लिगामेंट घायल हुआ है?", "en": "Which joint or ligament is injured?", "category": "sprain", "symptom": "injured joint or ligament"},
    {"hi": "चोट कब लगी थी?", "en": "When did the injury happen?", "category": "sprain", "symptom": "time of injury"},
    {"hi": "क्या दर्द लगातार है, या यह हलचल या दबाव से बदलता है?", "en": "Is the pain constant, or does it vary with movement or pressure?", "category": "sprain", "symptom": "pain variation"},
    {"hi": "क्या घायल क्षेत्र के आसपास सूजन, चोट या लाली है?", "en": "Is there swelling, bruising, or redness around the injured area?", "category": "sprain", "symptom": "swelling, bruising, or redness"},
    {"hi": "क्या आप प्रभावित जोड़े को हिला सकते हैं, या यह हिलाने में बहुत दर्द होता है?", "en": "Can you move the affected joint, or is it too painful to move?", "category": "sprain", "symptom": "joint movement"},
    {"hi": "क्या चोट के बाद प्रभावित जोड़े में कमजोरी या अस्थिरता महसूस हो रही है?", "en": "Have you experienced any weakness or instability in the affected joint since the injury?", "category": "sprain", "symptom": "weakness or instability"},
    {"hi": "क्या चोट लगने के समय कोई पॉपिंग या स्नैपिंग की आवाज आई थी?", "en": "Did you hear any popping or snapping sounds when the injury occurred?", "category": "sprain", "symptom": "popping or snapping sounds"},
    {"hi": "क्या आपने उसी जोड़े में पहले कभी कोई स्ट्रेन या चोट लगाई है?", "en": "Have you had any previous sprains or injuries to the same joint?", "category": "sprain", "symptom": "previous injuries"},
    {"hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं, या आपने चोट पर बर्फ, गर्मी, या अन्य उपचार का उपयोग किया है?", "en": "Are you currently taking any medications, or have you used ice, heat, or other treatments on the injury?", "category": "sprain", "symptom": "treatment used"}
],

'ligament injury' : [
    {"hi": "लिगामेंट की चोट कैसे हुई (जैसे, खेल, दुर्घटना, गिरना, मुड़ने की गति)?", "en": "How did the ligament injury occur (e.g., sports, accident, fall, twisting movement)?", "category": "ligament injury", "symptom": "mechanism of injury"},
    {"hi": "कौन सा जोड़ा या क्षेत्र घायल हुआ है (जैसे, घुटना, टखना, कोहनी)?", "en": "Which joint or area is injured (e.g., knee, ankle, elbow)?", "category": "ligament injury", "symptom": "injured joint or area"},
    {"hi": "चोट कब लगी थी, और क्या उस समय तुरंत दर्द या सूजन हुई थी?", "en": "When did the injury happen, and was there any immediate pain or swelling?", "category": "ligament injury", "symptom": "pain and swelling onset"},
    {"hi": "क्या चोट के समय कोई पॉपिंग या स्नैपिंग की आवाज आई थी?", "en": "Did you hear a popping or snapping sound when the injury occurred?", "category": "ligament injury", "symptom": "popping or snapping sounds"},
    {"hi": "क्या दर्द लगातार है, या यह हलचल या विशिष्ट गतिविधियों से बढ़ता है?", "en": "Is the pain constant, or does it worsen with movement or specific activities?", "category": "ligament injury", "symptom": "pain variation with movement"},
    {"hi": "क्या घायल जोड़े के आसपास सूजन, चोट या लाली है?", "en": "Are you experiencing swelling, bruising, or redness around the injured joint?", "category": "ligament injury", "symptom": "swelling, bruising, or redness"},
    {"hi": "क्या आप प्रभावित जोड़े को हिला सकते हैं, या यह हिलाने में बहुत दर्दनाक या अस्थिर है?", "en": "Can you move the affected joint, or is it too painful or unstable to do so?", "category": "ligament injury", "symptom": "joint movement"},
    {"hi": "क्या आपने कमजोर, अस्थिरता या वजन उठाने में कठिनाई महसूस की है?", "en": "Have you noticed any weakness, instability, or difficulty bearing weight on the injured limb?", "category": "ligament injury", "symptom": "weakness or instability"},
    {"hi": "क्या आपने पहले कभी लिगामेंट की चोट या उसी जोड़े में बार-बार समस्याएँ महसूस की हैं?", "en": "Have you had any previous ligament injuries or recurring problems with the same joint?", "category": "ligament injury", "symptom": "previous injuries"},
    {"hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं, या आपने बर्फ, संपीड़न, या ऊँचाई जैसे उपचार का उपयोग किया है?", "en": "Are you currently taking any medications, or have you used any treatments like ice, compression, or elevation?", "category": "ligament injury", "symptom": "treatment used"}
],

'gout' : [
    {"hi": "आपको गाउट के लक्षणों का अनुभव कितने समय से हो रहा है?", "en": "How long have you been experiencing symptoms of gout?", "category": "gout", "symptom": "duration of symptoms"},
    {"hi": "कौन सा जोड़ा प्रभावित है, और क्या वह सूजा हुआ, लाल, या छूने पर गर्म है?", "en": "Which joint is affected, and is it swollen, red, or warm to the touch?", "category": "gout", "symptom": "affected joint and signs"},
    {"hi": "आपने पहले कब दर्द महसूस किया था, और क्या यह अचानक था या धीरे-धीरे बढ़ा?", "en": "When did you first notice the pain, and was it sudden or gradual?", "category": "gout", "symptom": "onset of pain"},
    {"hi": "क्या आपको पहले कभी इसी तरह के लक्षण हुए थे, या यह गाउट का पहला दौरा है?", "en": "Have you had similar symptoms in the past, or is this your first episode of gout?", "category": "gout", "symptom": "previous episodes"},
    {"hi": "क्या आपको प्रभावित जोड़े में विशेष रूप से रात के समय तीव्र दर्द हो रहा है?", "en": "Are you experiencing severe pain in the affected joint, especially at night?", "category": "gout", "symptom": "pain severity and timing"},
    {"hi": "क्या आपको उच्च यूरिक एसिड स्तर का इतिहास है, या क्या आपको पहले गाउट का निदान किया गया था?", "en": "Do you have a history of high uric acid levels, or have you been diagnosed with gout before?", "category": "gout", "symptom": "history of uric acid or gout"},
    {"hi": "क्या आपने प्यूरीन से भरपूर खाद्य पदार्थों या पेय पदार्थों का सेवन किया है, जैसे लाल मांस, शंख, या शराब, विशेष रूप से बीयर या शराब?", "en": "Have you been consuming foods or drinks high in purines, such as red meat, shellfish, or alcohol, especially beer or liquor?", "category": "gout", "symptom": "dietary triggers"},
    {"hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं, विशेष रूप से मूत्रवर्धक, एस्पिरिन, या उच्च रक्तचाप या अन्य स्थितियों के लिए दवाइयाँ?", "en": "Are you currently taking any medications, particularly diuretics, aspirin, or medications for blood pressure or other conditions?", "category": "gout", "symptom": "medications"},
    {"hi": "क्या आपको कोई अन्य स्वास्थ्य समस्याएँ हैं, जैसे मोटापा, मधुमेह, या गुर्दे की बीमारी?", "en": "Do you have any other health conditions, such as obesity, diabetes, or kidney disease?", "category": "gout", "symptom": "underlying health conditions"},
    {"hi": "क्या आपको जोड़ों के दर्द के साथ बुखार या ठंड लगने जैसे लक्षण हो रहे हैं?", "en": "Are you experiencing any symptoms like fever or chills along with the joint pain?", "category": "gout", "symptom": "associated symptoms"}
],

'sciatica' : [
    {"hi": "आपको साइटिका के लक्षणों (जैसे दर्द, सुन्नता, या झुनझुनी) का अनुभव कितने समय से हो रहा है?", "en": "How long have you been experiencing sciatica symptoms (e.g., pain, numbness, or tingling)?", "category": "sciatica", "symptom": "duration of symptoms"},
    {"hi": "दर्द कहाँ स्थित है (जैसे निचला पीठ, कूल्हे, पैर, पैरों के अंगूठे)?", "en": "Where is the pain located (e.g., lower back, buttocks, legs, feet)?", "category": "sciatica", "symptom": "location of pain"},
    {"hi": "क्या दर्द लगातार है, या यह आता-जाता रहता है?", "en": "Is the pain constant, or does it come and go?", "category": "sciatica", "symptom": "pain pattern"},
    {"hi": "क्या आपको एक पैर में या दोनों पैरों में दर्द, सुन्नता, या झुनझुनी महसूस होती है?", "en": "Do you experience pain, numbness, or tingling down one leg or both legs?", "category": "sciatica", "symptom": "unilateral or bilateral symptoms"},
    {"hi": "दर्द तेज, जलन वाला, या हलका चुभता हुआ है?", "en": "Is the pain sharp, burning, or more of a dull ache?", "category": "sciatica", "symptom": "pain type"},
    {"hi": "क्या कुछ विशेष गतिविधियाँ या स्थितियाँ जैसे बैठना, खड़ा होना, खांसी या छींकने से दर्द बढ़ता है?", "en": "Does anything trigger or worsen the pain, such as sitting, standing, coughing, or sneezing?", "category": "sciatica", "symptom": "pain triggers"},
    {"hi": "क्या आपको प्रभावित पैर में कमजोरी महसूस होती है या पैर उठाने या हिलाने में कठिनाई हो रही है?", "en": "Do you have any weakness in the affected leg or difficulty moving or lifting your foot?", "category": "sciatica", "symptom": "leg weakness or mobility issues"},
    {"hi": "क्या आपको हाल ही में कोई चोट, गिरावट, या दुर्घटना हुई है जो आपकी निचली पीठ या रीढ़ को प्रभावित कर सकती है?", "en": "Have you had any recent injuries, falls, or accidents that might have affected your lower back or spine?", "category": "sciatica", "symptom": "recent injuries"},
    {"hi": "क्या आपको कोई अन्य चिकित्सीय स्थिति है, जैसे हर्नियेटेड डिस्क, डीजनरेटिव डिस्क रोग, या स्पाइनल स्टेनोसिस?", "en": "Do you have any other medical conditions, such as herniated discs, degenerative disc disease, or spinal stenosis?", "category": "sciatica", "symptom": "underlying medical conditions"},
    {"hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं, और क्या आपने साइटिका के दर्द के लिए किसी उपचार (जैसे फिजिकल थेरेपी, विश्राम, दर्द निवारण) की कोशिश की है?", "en": "Are you currently taking any medications, and have you tried any treatments (e.g., physical therapy, rest, pain relief) for the sciatica pain?", "category": "sciatica", "symptom": "medications and treatments"}
],

'herniated disc' : [
    {"hi": "आपको अपनी पीठ या गर्दन से संबंधित लक्षणों का अनुभव कितने समय से हो रहा है?", "en": "How long have you been experiencing symptoms related to your back or neck?", "category": "herniated_disc", "symptom": "duration of symptoms"},
    {"hi": "दर्द कहाँ स्थित है (जैसे निचला पीठ, गर्दन, हाथ, पैर)?", "en": "Where is the pain located (e.g., lower back, neck, arms, legs)?", "category": "herniated_disc", "symptom": "location of pain"},
    {"hi": "क्या आपको अपने हाथों या पैरों में दर्द महसूस होता है (जैसे साइटिका प्रकार का दर्द)?", "en": "Do you have pain radiating down your arms or legs (e.g., sciatica-type pain)?", "category": "herniated_disc", "symptom": "radiating pain"},
    {"hi": "क्या दर्द लगातार है, या यह आता-जाता रहता है?", "en": "Is the pain constant, or does it come and go?", "category": "herniated_disc", "symptom": "pain pattern"},
    {"hi": "क्या दर्द तेज, जलन वाला, या हलका चुभता हुआ है? क्या यह कुछ विशेष गति या स्थिति में बढ़ता है?", "en": "Is the pain sharp, burning, or dull? Does it worsen with certain movements or positions?", "category": "herniated_disc", "symptom": "pain type and triggers"},
    {"hi": "क्या आपको हाल ही में कोई चोट, भारी वजन उठाना, या ऐसी गतिविधियाँ हुई हैं जिन्होंने आपकी पीठ या गर्दन को दबाव डाला हो?", "en": "Have you had any recent injuries, heavy lifting, or activities that might have strained your back or neck?", "category": "herniated_disc", "symptom": "recent injuries or strain"},
    {"hi": "क्या आपको अपने हाथों, पैरों, हाथों या पैरों में सुन्नता, झुनझुनी या कमजोरी महसूस हो रही है?", "en": "Are you experiencing numbness, tingling, or weakness in your arms, legs, hands, or feet?", "category": "herniated_disc", "symptom": "numbness, tingling, or weakness"},
    {"hi": "क्या आपको खड़ा होने, चलने, या कुछ स्थितियों (जैसे झुकना, लंबे समय तक बैठना) में कठिनाई हो रही है?", "en": "Do you have difficulty standing, walking, or maintaining certain positions (e.g., bending, sitting for long periods)?", "category": "herniated_disc", "symptom": "mobility difficulties"},
    {"hi": "क्या आपको पीठ से संबंधित कोई पिछला इतिहास है, जैसे पिछले हर्नियेटेड डिस्क, स्पाइनल स्टेनोसिस, या डीजनरेटिव डिस्क रोग?", "en": "Do you have a history of back problems, such as previous herniated discs, spinal stenosis, or degenerative disc disease?", "category": "herniated_disc", "symptom": "history of back problems"},
    {"hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं, और क्या आपने फिजिकल थेरेपी, विश्राम, या दर्द निवारण जैसे उपचार किए हैं?", "en": "Are you currently taking any medications, and have you tried treatments like physical therapy, rest, or pain relief?", "category": "herniated_disc", "symptom": "medications and treatments"}
],

'back spasms' : [
    {"hi": "आपको पीठ में ऐंठन का अनुभव कितने समय से हो रहा है?", "en": "How long have you been experiencing back spasms?", "category": "back_spasms", "symptom": "duration of spasms"},
    {"hi": "ऐंठन कहाँ स्थित है (जैसे निचली पीठ, ऊपरी पीठ, या गर्दन)?", "en": "Where is the spasm located (e.g., lower back, upper back, or neck)?", "category": "back_spasms", "symptom": "location of spasm"},
    {"hi": "क्या ऐंठन लगातार है, या यह आता-जाता रहता है?", "en": "Are the spasms constant, or do they come and go?", "category": "back_spasms", "symptom": "spasm pattern"},
    {"hi": "जब ऐंठन होती है, तो दर्द कितना तीव्र होता है? क्या यह तेज, हल्का या ऐंठन जैसा है?", "en": "How severe is the pain during the spasms? Is it sharp, dull, or cramping?", "category": "back_spasms", "symptom": "pain severity and type"},
    {"hi": "क्या ऐंठन कुछ विशेष गतिविधियों के बाद होती है, जैसे उठाना, झुकना, या शारीरिक श्रम?", "en": "Do the spasms occur after certain activities, such as lifting, bending, or physical exertion?", "category": "back_spasms", "symptom": "activity-related spasms"},
    {"hi": "क्या आपको हाल ही में कोई चोट, गिरना, या खिंचाव हुआ है जिसने ऐंठन को उत्तेजित किया हो?", "en": "Have you had any recent injuries, falls, or strains that might have triggered the spasms?", "category": "back_spasms", "symptom": "recent injury or strain"},
    {"hi": "क्या आपको किसी अन्य लक्षण का अनुभव हो रहा है, जैसे सुन्नता, झुनझुनी, या पैरों या हाथों में कमजोरी?", "en": "Do you experience any other symptoms, such as numbness, tingling, or weakness in your legs or arms?", "category": "back_spasms", "symptom": "numbness, tingling, or weakness"},
    {"hi": "क्या ऐंठन के बाद आपको कोई कठोरता या चलने में कठिनाई हो रही है?", "en": "Are you experiencing any stiffness or difficulty moving after the spasms?", "category": "back_spasms", "symptom": "stiffness or movement difficulty"},
    {"hi": "क्या आपको पीठ से संबंधित कोई पिछला इतिहास है, जैसे हर्नियेटेड डिस्क, गठिया, या डीजनरेटिव डिस्क रोग?", "en": "Do you have a history of back problems, such as herniated discs, arthritis, or degenerative disc disease?", "category": "back_spasms", "symptom": "history of back problems"},
    {"hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं या ऐंठन के लिए उपचार (जैसे हीट, बर्फ, फिजिकल थेरेपी) कर रहे हैं?", "en": "Are you currently taking any medications or using treatments (e.g., heat, ice, physical therapy) for the spasms?", "category": "back_spasms", "symptom": "medications and treatments"}
],

'whiplash' : [
    {"hi": "चोट कब हुई थी, और क्या कारण था (जैसे कार दुर्घटना, गिरना, खेल की चोट)?", "en": "How long ago did the injury occur, and what caused the whiplash (e.g., car accident, fall, sports injury)?", "category": "whiplash", "symptom": "cause and timing of injury"},
    {"hi": "आपको कहाँ दर्द महसूस हो रहा है (जैसे गर्दन, कंधे, ऊपरी पीठ)?", "en": "Where exactly do you feel pain (e.g., neck, shoulders, upper back)?", "category": "whiplash", "symptom": "location of pain"},
    {"hi": "क्या दर्द लगातार है, या यह आता-जाता रहता है?", "en": "Is the pain constant, or does it come and go?", "category": "whiplash", "symptom": "pain pattern"},
    {"hi": "क्या आपको गर्दन या सिर में कठोरता या सीमित गति महसूस हो रही है?", "en": "Do you experience stiffness or limited movement in your neck or head?", "category": "whiplash", "symptom": "stiffness or movement limitation"},
    {"hi": "क्या आपको चोट के बाद सिरदर्द, चक्कर, या कानों में घंटी बजने (टिनिटस) का अनुभव हो रहा है?", "en": "Have you noticed any headaches, dizziness, or ringing in your ears (tinnitus) since the injury?", "category": "whiplash", "symptom": "headaches, dizziness, or tinnitus"},
    {"hi": "क्या आपको हाथों या बाहों में सुन्नता, झुनझुनी, या कमजोरी महसूस हो रही है?", "en": "Are you experiencing numbness, tingling, or weakness in your arms or hands?", "category": "whiplash", "symptom": "numbness, tingling, or weakness"},
    {"hi": "क्या आपने अन्य कोई चोटें खाई हैं, जैसे मस्तिष्क concussion या पीठ की चोटें, साथ में whiplash के?", "en": "Have you had any other injuries, such as a concussion or back injuries, along with the whiplash?", "category": "whiplash", "symptom": "other injuries"},
    {"hi": "क्या आपको दर्द या असहजता के कारण सोने में कठिनाई हो रही है?", "en": "Are you experiencing any difficulty sleeping due to the pain or discomfort?", "category": "whiplash", "symptom": "sleep disturbances"},
    {"hi": "क्या आपने किसी उपचार का प्रयास किया है (जैसे आराम, बर्फ, हीट, दर्द निवारक), और क्या उससे राहत मिली?", "en": "Have you tried any treatments (e.g., rest, ice, heat, pain relievers) to relieve the symptoms, and did they help?", "category": "whiplash", "symptom": "treatment attempts"},
    {"hi": "क्या आपको गर्दन या पीठ से संबंधित कोई इतिहास है, जैसे पिछले whiplash, हर्नियेटेड डिस्क, या गठिया?", "en": "Do you have a history of neck or back problems, such as previous whiplash, herniated discs, or arthritis?", "category": "whiplash", "symptom": "history of neck or back issues"}
],

'fibromyalgia' : [
    {"hi": "आपको अपने मांसपेशियों और जोड़ो में व्यापक दर्द या कोमलता का अनुभव कब से हो रहा है?", "en": "How long have you been experiencing widespread pain or tenderness in your muscles and joints?", "category": "fibromyalgia", "symptom": "pain and tenderness"},
    {"hi": "आपको कहाँ दर्द महसूस हो रहा है, और क्या यह शरीर के दोनों तरफ समान रूप से प्रभावित होता है?", "en": "Where do you feel the pain, and does it affect both sides of your body equally?", "category": "fibromyalgia", "symptom": "location and symmetry of pain"},
    {"hi": "क्या दर्द लगातार है, या यह आता-जाता रहता है?", "en": "Is the pain constant, or does it come and go?", "category": "fibromyalgia", "symptom": "pain pattern"},
    {"hi": "क्या आपको अन्य लक्षण महसूस हो रहे हैं, जैसे थकान, नींद में गड़बड़ी, सिरदर्द, या याददाश्त की समस्याएँ (जो अक्सर 'फाइब्रो फॉग' के नाम से जानी जाती हैं)?", "en": "Do you experience other symptoms, such as fatigue, sleep disturbances, headaches, or memory problems (often called 'fibro fog')?", "category": "fibromyalgia", "symptom": "other symptoms"},
    {"hi": "क्या आपको कोई आघात, बीमारी, या संक्रमण हुआ है जो आपके लक्षणों को उत्तेजित कर सकता है?", "en": "Do you have any history of trauma, illness, or infections that might have triggered your symptoms?", "category": "fibromyalgia", "symptom": "history of trauma or illness"},
    {"hi": "क्या आपको ध्यान केंद्रित करने, सतर्क रहने, या चीजों को याद रखने में कोई कठिनाई हो रही है?", "en": "Are you experiencing any difficulty concentrating, staying alert, or remembering things?", "category": "fibromyalgia", "symptom": "concentration and memory problems"},
    {"hi": "क्या आपके लक्षण किसी विशेष समय पर बढ़ जाते हैं (जैसे तनाव के दौरान, शारीरिक गतिविधि के बाद, या मौसम में बदलाव के साथ)?", "en": "Do your symptoms worsen at certain times (e.g., during stress, after physical activity, or with changes in the weather)?", "category": "fibromyalgia", "symptom": "symptom triggers"},
    {"hi": "क्या आपकी नींद की आदतों में कोई महत्वपूर्ण परिवर्तन हुआ है, जैसे सोने में कठिनाई, या नींद से उठने के बाद थका हुआ महसूस करना?", "en": "Have you had any significant changes in your sleep patterns, such as trouble falling or staying asleep, or waking up feeling unrefreshed?", "category": "fibromyalgia", "symptom": "sleep disturbances"},
    {"hi": "क्या आपके परिवार में फाइब्रोमायल्गिया या अन्य पुरानी दर्द की स्थितियाँ, जैसे रुमेटोइड आर्थराइटिस या ल्यूपस का इतिहास है?", "en": "Do you have a family history of fibromyalgia or other chronic pain conditions, such as rheumatoid arthritis or lupus?", "category": "fibromyalgia", "symptom": "family history"},
    {"hi": "क्या आपने अपने लक्षणों के लिए कोई उपचार (जैसे दवाइयाँ, शारीरिक चिकित्सा, तनाव प्रबंधन) किया है, और यदि किया है, तो क्या वे मददगार रहे हैं?", "en": "Have you tried any treatments (e.g., medications, physical therapy, stress management) for your symptoms, and if so, did they help?", "category": "fibromyalgia", "symptom": "treatment history"}
],

'arthritis' : [
    {"hi": "आपको जोड़ों में दर्द या जकड़न कब से हो रही है?", "en": "How long have you been experiencing joint pain or stiffness?", "category": "arthritis", "symptom": "joint pain and stiffness"},
    {"hi": "कौन से जोड़ों में समस्या है (जैसे घुटने, हाथ, कूल्हे, उंगलियाँ)?", "en": "Which joints are affected (e.g., knees, hands, hips, fingers)?", "category": "arthritis", "symptom": "location of pain"},
    {"hi": "क्या दर्द लगातार है, या यह आता-जाता रहता है?", "en": "Is the pain constant, or does it come and go?", "category": "arthritis", "symptom": "pain pattern"},
    {"hi": "क्या आपको सुबह के समय जकड़न महसूस होती है, और यदि होती है, तो यह कितनी देर तक रहती है?", "en": "Do you experience morning stiffness, and if so, how long does it last?", "category": "arthritis", "symptom": "morning stiffness"},
    {"hi": "क्या आपने प्रभावित जोड़ों में सूजन, लाली, या गर्मी महसूस की है?", "en": "Have you noticed any swelling, redness, or warmth in the affected joints?", "category": "arthritis", "symptom": "joint swelling and inflammation"},
    {"hi": "क्या दर्द कुछ गतिविधियों के साथ बेहतर या खराब होता है (जैसे विश्राम, व्यायाम, मौसम में बदलाव)?", "en": "Does the pain improve or worsen with certain activities (e.g., rest, exercise, weather changes)?", "category": "arthritis", "symptom": "activity-related pain changes"},
    {"hi": "क्या आपको प्रभावित जोड़ों में हाल ही में कोई चोट या आघात हुआ है?", "en": "Have you had any recent injuries or trauma to the affected joints?", "category": "arthritis", "symptom": "recent injury or trauma"},
    {"hi": "क्या आपको दैनिक गतिविधियाँ करने में कठिनाई हो रही है, जैसे चलना, टाइप करना, या जार खोलना?", "en": "Do you have difficulty performing daily activities, such as walking, typing, or opening jars?", "category": "arthritis", "symptom": "difficulty with daily activities"},
    {"hi": "क्या आपके परिवार में आर्थ्राइटिस या अन्य ऑटोइम्यून बीमारियों का इतिहास है, जैसे रुमेटोइड आर्थ्राइटिस या ल्यूपस?", "en": "Do you have a family history of arthritis or other autoimmune conditions, such as rheumatoid arthritis or lupus?", "category": "arthritis", "symptom": "family history of arthritis"},
    {"hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं, जिसमें दर्द निवारक, या आपने कोई उपचार (जैसे शारीरिक चिकित्सा, जीवनशैली में बदलाव) किया है?", "en": "Are you currently taking any medications, including pain relievers, or have you tried any treatments (e.g., physical therapy, lifestyle changes)?", "category": "arthritis", "symptom": "medication and treatment history"}
],

'anhedonia' : [
    {"hi": "आपको जो गतिविधियाँ पहले आनंददायक लगती थीं, उन्हें अब रुचि या खुशी क्यों नहीं हो रही है?", "en": "How long have you been experiencing a lack of interest or pleasure in activities you used to enjoy?", "category": "anhedonia", "symptom": "loss of interest in enjoyable activities"},
    {"hi": "कौन सी गतिविधियाँ या शौक अब आपको आनंददायक नहीं लगते (जैसे सामाजिक मेलजोल, शौक, भोजन, या काम)?", "en": "Which activities or hobbies do you no longer find enjoyable (e.g., socializing, hobbies, eating, or work)?", "category": "anhedonia", "symptom": "specific activities no longer enjoyable"},
    {"hi": "क्या आपको उन चीजों के प्रति उदासीनता या भावनात्मक 'न्यूम्नेस' महसूस हो रही है, जो पहले आपको खुशी देती थीं?", "en": "Do you feel indifferent or emotionally 'numb' toward things that once brought you happiness?", "category": "anhedonia", "symptom": "emotional numbness"},
    {"hi": "क्या आपने दैनिक गतिविधियों में भाग लेने की प्रेरणा, ऊर्जा, या इच्छा में कमी महसूस की है?", "en": "Have you noticed a decline in motivation, energy, or desire to engage in daily activities?", "category": "anhedonia", "symptom": "decline in motivation and energy"},
    {"hi": "क्या आप कोई मूड में बदलाव महसूस कर रहे हैं, जैसे उदासी, निराशा, या चिड़चिड़ापन?", "en": "Are you experiencing any changes in mood, such as feelings of sadness, hopelessness, or irritability?", "category": "anhedonia", "symptom": "mood changes"},
    {"hi": "क्या आपने अपनी भूख, नींद, या समग्र ऊर्जा स्तरों में कोई बदलाव महसूस किया है?", "en": "Have you noticed any changes in your appetite, sleep, or overall energy levels?", "category": "anhedonia", "symptom": "changes in appetite, sleep, or energy"},
    {"hi": "क्या आप शारीरिक लक्षणों, जैसे थकान, दर्द, या सिरदर्द, का अनुभव कर रहे हैं, जो आपके आनंद लेने की क्षमता को प्रभावित कर सकते हैं?", "en": "Are you experiencing any physical symptoms, such as fatigue, pain, or headaches, that could be contributing to your lack of enjoyment?", "category": "anhedonia", "symptom": "physical symptoms affecting enjoyment"},
    {"hi": "क्या आपने हाल ही में जीवन में कोई बदलाव, तनाव, या आघात महसूस किया है, जो आपके मानसिक स्वास्थ्य को प्रभावित कर सकता है?", "en": "Have you experienced any recent life changes, stressors, or trauma that might be affecting your mental health?", "category": "anhedonia", "symptom": "life changes or stressors"},
    {"hi": "क्या आपके पास मानसिक स्वास्थ्य स्थितियों, जैसे अवसाद, चिंता, या द्विध्रुवीय विकार, का इतिहास है?", "en": "Do you have a history of mental health conditions, such as depression, anxiety, or bipolar disorder?", "category": "anhedonia", "symptom": "history of mental health conditions"},
    {"hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं, जैसे एंटीडिप्रेसेंट्स या अन्य उपचार, और क्या उन्होंने आपके आनंद लेने की क्षमता को प्रभावित किया है?", "en": "Are you currently taking any medications, including antidepressants or other treatments, and have they affected your ability to enjoy things?", "category": "anhedonia", "symptom": "effect of medications on enjoyment"}
],

'agitation' : [
    {"hi": "आप कब से बेचैनी या उत्तेजना महसूस कर रहे हैं?", "en": "How long have you been feeling agitated or restless?", "category": "agitation", "symptom": "feeling restless or agitated"},
    {"hi": "आप किस प्रकार की भावनाओं या व्यवहारों का अनुभव कर रहे हैं (जैसे चिड़चिड़ापन, चहलकदमी, तेज बोलना, या शांत रहने में कठिनाई)?", "en": "What specific feelings or behaviors are you experiencing (e.g., irritability, pacing, rapid speech, difficulty staying still)?", "category": "agitation", "symptom": "specific behaviors or feelings of agitation"},
    {"hi": "क्या आप अत्यधिक चिंतित, घबराए हुए या तनावपूर्ण महसूस कर रहे हैं?", "en": "Do you feel excessively anxious, nervous, or on edge?", "category": "agitation", "symptom": "excessive anxiety or nervousness"},
    {"hi": "क्या उत्तेजना किसी विशेष घटना, स्थिति या विचारों से प्रेरित होती है?", "en": "Is the agitation triggered by specific events, situations, or thoughts?", "category": "agitation", "symptom": "triggers of agitation"},
    {"hi": "क्या आपको अपनी भावनाओं को नियंत्रित करने में कठिनाई हो रही है, या क्या आप पहले से ज्यादा जल्दी गुस्सा या परेशान हो जाते हैं?", "en": "Do you have difficulty controlling your emotions, or are you more easily frustrated or upset than usual?", "category": "agitation", "symptom": "difficulty controlling emotions or frustration"},
    {"hi": "क्या आप हाल ही में किसी महत्वपूर्ण तनाव या जीवन में बड़े बदलावों का सामना कर रहे हैं?", "en": "Have you been under significant stress, facing major life changes, or dealing with emotional challenges recently?", "category": "agitation", "symptom": "stress or life changes"},
    {"hi": "क्या आपको उत्तेजना के साथ कोई शारीरिक लक्षण जैसे बढ़ी हुई हृदय गति, पसीना, कांपना, या सांस लेने में कठिनाई हो रही है?", "en": "Are you experiencing any physical symptoms along with the agitation, such as increased heart rate, sweating, trembling, or difficulty breathing?", "category": "agitation", "symptom": "physical symptoms associated with agitation"},
    {"hi": "क्या आपको मानसिक स्वास्थ्य स्थितियों, जैसे चिंता, अवसाद, द्विध्रुवीय विकार, या PTSD का इतिहास है?", "en": "Do you have a history of mental health conditions, such as anxiety, depression, bipolar disorder, or PTSD?", "category": "agitation", "symptom": "history of mental health conditions"},
    {"hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं, जैसे प्रिस्क्रिप्शन, ओवर-द-काउंटर, या रिक्रिएशनल ड्रग्स?", "en": "Are you currently taking any medications, including prescription, over-the-counter, or recreational drugs?", "category": "agitation", "symptom": "medications or substance use"},
    {"hi": "क्या आपको हाल ही में नींद में कोई विघटन, थकान, या भूख में बदलाव महसूस हुआ है?", "en": "Have you experienced any recent sleep disturbances, fatigue, or changes in appetite?", "category": "agitation", "symptom": "sleep disturbances, fatigue, or appetite changes"}
],

'convulsions' : [
    {"hi": "आप कब से दौरे (माथे के झटके) का अनुभव कर रहे हैं?", "en": "How long have you been experiencing convulsions or seizures?", "category": "convulsions", "symptom": "duration of seizures"},
    {"hi": "पहला दौरा कब हुआ था, और वे कितनी बार होते हैं?", "en": "When did the first seizure occur, and how often do they happen?", "category": "convulsions", "symptom": "frequency of seizures"},
    {"hi": "दौरे के दौरान क्या दिखाई देता है (जैसे झटका, मरोड़, होश का चले जाना)?", "en": "What does the seizure look like (e.g., shaking, jerking movements, loss of consciousness)?", "category": "convulsions", "symptom": "type of seizure"},
    {"hi": "क्या आपको दौरे के शुरू होने से पहले कोई चेतावनी संकेत या आभास होता है (जैसे चक्कर आना, अजीब महसूस होना, दृष्टि में बदलाव)?", "en": "Do you experience any warning signs or aura before the convulsions start (e.g., dizziness, strange sensations, visual disturbances)?", "category": "convulsions", "symptom": "warning signs or aura before seizure"},
    {"hi": "क्या आपने कभी दौरे के दौरान या बाद में होश खो दिया है या याददाश्त में कमी अनुभव की है?", "en": "Have you ever lost consciousness or memory during or after a seizure?", "category": "convulsions", "symptom": "loss of consciousness or memory"},
    {"hi": "क्या दौरे के बाद कोई अन्य लक्षण जैसे भ्रम, सिरदर्द या मांसपेशियों में दर्द महसूस हो रहा है?", "en": "Are you experiencing any other symptoms, such as confusion, headache, or muscle soreness, after the seizure?", "category": "convulsions", "symptom": "post-seizure symptoms"},
    {"hi": "क्या आपको कोई ज्ञात चिकित्सा स्थिति है, जैसे मिर्गी, मस्तिष्क की चोट, या तंत्रिका संबंधी विकार?", "en": "Do you have any known medical conditions, such as epilepsy, brain injury, or neurological disorders?", "category": "convulsions", "symptom": "medical history (epilepsy, brain injury)"},
    {"hi": "क्या आप वर्तमान में कोई दवाइयाँ ले रहे हैं, जैसे प्रिस्क्रिप्शन, ओवर-द-काउंटर, या रिक्रिएशनल ड्रग्स?", "en": "Are you taking any medications, including prescription, over-the-counter, or recreational drugs?", "category": "convulsions", "symptom": "medications and substance use"},
    {"hi": "क्या आपको हाल ही में कोई सिर की चोट, संक्रमण, या बुखार हुआ है?", "en": "Have you had any recent head injuries, infections, or fevers?", "category": "convulsions", "symptom": "recent head injuries, infections, or fevers"},
    {"hi": "क्या आपके परिवार में मिर्गी, दौरे, या अन्य तंत्रिका संबंधी विकारों का इतिहास है?", "en": "Is there a family history of epilepsy, seizures, or other neurological disorders?", "category": "convulsions", "symptom": "family history of seizures or neurological disorders"}
],

'hives' : [
    {"hi": "आप कब से शरीर पर फफोले (उठे हुए, लाल, खुजलीदार धब्बे) का अनुभव कर रहे हैं?", "en": "How long have you been experiencing hives (raised, red, itchy welts on your skin)?", "category": "hives", "symptom": "duration of hives"},
    {"hi": "फफोले पहले कब दिखाई दिए थे, और क्या वे बढ़ते जा रहे हैं?", "en": "When did the hives first appear, and have they been getting worse?", "category": "hives", "symptom": "onset and progression of hives"},
    {"hi": "क्या फफोले किसी विशेष स्थान पर हैं, या वे आपके शरीर के विभिन्न हिस्सों में फैल रहे हैं?", "en": "Are the hives localized to a specific area, or do they spread to different parts of your body?", "category": "hives", "symptom": "location and spread of hives"},
    {"hi": "क्या फफोले आते-जाते हैं, या यह लगातार बने रहते हैं?", "en": "Do the hives come and go, or are they persistent?", "category": "hives", "symptom": "frequency and persistence of hives"},
    {"hi": "क्या आपने फफोले होने के कारण किसी विशेष पदार्थ, दवाओं, तनाव, गर्मी, या ठंड का अनुभव किया है?", "en": "Have you noticed any triggers for the hives, such as certain foods, medications, stress, heat, or cold?", "category": "hives", "symptom": "triggers for hives"},
    {"hi": "क्या फफोले के साथ कोई अन्य लक्षण हैं, जैसे सांस लेने में कठिनाई, होंठों या गले में सूजन, या चक्कर आना?", "en": "Have you experienced any other symptoms along with the hives, such as difficulty breathing, swelling in your lips or throat, or dizziness?", "category": "hives", "symptom": "associated symptoms with hives"},
    {"hi": "क्या आपको एलर्जी, अस्थमा, या अन्य त्वचा की समस्याओं (जैसे एक्जिमा, एलर्जिक रिएक्शन) का इतिहास है?", "en": "Do you have a history of allergies, asthma, or other skin conditions (e.g., eczema, allergic reactions)?", "category": "hives", "symptom": "medical history of allergies or skin conditions"},
    {"hi": "क्या आपने हाल ही में कोई नई दवाएं, खाद्य पदार्थ, या स्किनकेयर उत्पाद शुरू किए हैं?", "en": "Have you recently started any new medications, foods, or skincare products?", "category": "hives", "symptom": "recent changes in medications or products"},
    {"hi": "क्या आप हाल ही में किसी बड़े तनाव से गुजर रहे हैं या किसी संक्रमण का सामना कर रहे हैं?", "en": "Have you been under significant stress or experienced any infections recently?", "category": "hives", "symptom": "stress or infections as potential triggers"},
    {"hi": "क्या आपके परिवार में एलर्जी, फफोले, या अन्य एलर्जी संबंधित बीमारियों का इतिहास है?", "en": "Do you have a family history of allergies, hives, or other allergic conditions?", "category": "hives", "symptom": "family history of allergies or hives"}
],

'contact dermatitis' : [
    {"hi": "आप कब से चकत्ते या त्वचा में जलन महसूस कर रहे हैं?", "en": "How long have you been experiencing the rash or skin irritation?", "category": "contact_dermatitis", "symptom": "duration of rash/irritation"},
    {"hi": "चकत्ता पहले आपके शरीर के किस हिस्से पर दिखाई दिया?", "en": "Where on your body did the rash first appear?", "category": "contact_dermatitis", "symptom": "location of rash"},
    {"hi": "क्या आपने किसी नए पदार्थ, जैसे लोशन, साबुन, डिटर्जेंट, या पौधों (जैसे पोइज़न आइवी) के संपर्क में आए हैं?", "en": "Have you been in contact with any new substances, such as lotions, soaps, detergents, or plants (e.g., poison ivy)?", "category": "contact_dermatitis", "symptom": "new substance exposure"},
    {"hi": "क्या आप नोटिस करते हैं कि चकत्ता कुछ विशेष सामग्री (जैसे कुछ कपड़े, धातु, या रसायन) से संपर्क करने के बाद बढ़ जाता है?", "en": "Do you notice that the rash worsens after touching or being exposed to specific materials (e.g., certain fabrics, metals, or chemicals)?", "category": "contact_dermatitis", "symptom": "rash triggers"},
    {"hi": "क्या चकत्ता खुजलीदार, दर्दनाक, या दोनों है? क्या इसमें जलन या चुभन महसूस होती है?", "en": "Is the rash itchy, painful, or both? Does it burn or sting?", "category": "contact_dermatitis", "symptom": "pain or irritation level"},
    {"hi": "क्या आपने प्रभावित क्षेत्र में सूजन, फफोले, या रिसाव देखा है?", "en": "Have you noticed any swelling, blistering, or oozing in the affected area?", "category": "contact_dermatitis", "symptom": "swelling or blistering"},
    {"hi": "क्या आपको एलर्जी या त्वचा की समस्याओं, जैसे एक्जिमा या सोरायसिस, का इतिहास है?", "en": "Do you have a history of allergies or skin conditions, such as eczema or psoriasis?", "category": "contact_dermatitis", "symptom": "medical history of skin conditions"},
    {"hi": "क्या आपने उस समय के आसपास कोई नई दवाइयाँ, चाहे वो त्वचा पर लगाई गई हों या मुँह से ली गई हों, उपयोग की हैं?", "en": "Have you used any new medications, either topically or orally, around the time the rash started?", "category": "contact_dermatitis", "symptom": "new medication use"},
    {"hi": "क्या आपने चकत्ते के साथ कोई अन्य लक्षण महसूस किए हैं, जैसे बुखार, ठंड लगना, या थकान?", "en": "Have you experienced any other symptoms, such as fever, chills, or fatigue, along with the rash?", "category": "contact_dermatitis", "symptom": "associated symptoms"},
    {"hi": "क्या आपके परिवार में त्वचा की एलर्जी या समस्याओं, जैसे एक्जिमा, अस्थमा, या हे फीवर, का इतिहास है?", "en": "Is there a family history of skin allergies or conditions like eczema, asthma, or hay fever?", "category": "contact_dermatitis", "symptom": "family history of allergies"}
],

'atopic dermatitis' : [
    {"hi": "आप कब से एटोपिक डर्मेटाइटिस (जैसे खुजली, सूखी, लाल या सूजन वाली त्वचा) के लक्षण महसूस कर रहे हैं?", "en": "How long have you been experiencing symptoms of atopic dermatitis (e.g., itchy, dry, red, or inflamed skin)?", "category": "atopic_dermatitis", "symptom": "duration of symptoms"},
    {"hi": "आपके शरीर के किस हिस्से में सामान्य रूप से फ्लेयर-अप होते हैं (जैसे कोहनी, घुटने, चेहरा, हाथ)?", "en": "Where on your body do you typically have flare-ups (e.g., elbows, knees, face, hands)?", "category": "atopic_dermatitis", "symptom": "location of flare-ups"},
    {"hi": "क्या खुजली निरंतर रहती है, या यह आनी-जानी होती है?", "en": "Is the itching constant, or does it come and go?", "category": "atopic_dermatitis", "symptom": "itching pattern"},
    {"hi": "क्या आपने कोई ऐसे ट्रिगर या पैटर्न नोटिस किए हैं, जैसे कुछ खास खाद्य पदार्थ, कपड़े, मौसम, या तनाव, जो आपके लक्षणों को बढ़ाते हैं?", "en": "Have you noticed any triggers or patterns, such as specific foods, fabrics, weather, or stress, that make your symptoms worse?", "category": "atopic_dermatitis", "symptom": "triggers"},
    {"hi": "क्या आपको अन्य एलर्जी स्थितियों का इतिहास है, जैसे अस्थमा, हे फीवर, या खाद्य एलर्जी?", "en": "Do you have a history of other allergic conditions, such as asthma, hay fever, or food allergies?", "category": "atopic_dermatitis", "symptom": "history of allergic conditions"},
    {"hi": "क्या आपने बचपन या किशोरावस्था में कभी इसी प्रकार की त्वचा की समस्याएं अनुभव की हैं?", "en": "Have you ever had similar skin problems in childhood or as a teenager?", "category": "atopic_dermatitis", "symptom": "childhood or teenage history"},
    {"hi": "क्या आप किसी प्रकार के टॉपिकल उपचार (जैसे क्रीम या मलहम) का उपयोग कर रहे हैं, और क्या वे लक्षणों को राहत देने में मदद कर रहे हैं?", "en": "Are you using any topical treatments (e.g., creams or ointments), and have they helped relieve the symptoms?", "category": "atopic_dermatitis", "symptom": "topical treatments"},
    {"hi": "क्या आपके परिवार में एक्जिमा या अन्य त्वचा की समस्याओं (जैसे सोरायसिस, एलर्जी प्रतिक्रियाएं) का इतिहास है?", "en": "Do you have a family history of eczema or other skin conditions (e.g., psoriasis, allergic reactions)?", "category": "atopic_dermatitis", "symptom": "family history of eczema or skin conditions"},
    {"hi": "क्या आपने अपनी त्वचा में कोई परिवर्तन देखा है, जैसे खुजलाने के कारण मोटाई, दरारें, या दाग-धब्बे?", "en": "Have you noticed any changes in your skin, such as thickening, cracking, or scarring due to scratching?", "category": "atopic_dermatitis", "symptom": "skin changes due to scratching"},
    {"hi": "क्या आप इस समय कोई दवाइयाँ ले रहे हैं, और क्या आपको कोई अन्य स्वास्थ्य समस्याएं हैं (जैसे प्रतिरक्षा विकार या संक्रमण)?", "en": "Are you currently using any medications, and do you have any other health conditions (e.g., immune disorders or infections)?", "category": "atopic_dermatitis", "symptom": "current medications and other health conditions"}
],

'seborrheic dermatitis' : [
    {"hi": "आप कब से सेबोरेइक डर्मेटाइटिस (जैसे लाल, सफेद या चिकनी त्वचा) के लक्षण महसूस कर रहे हैं?", "en": "How long have you been experiencing symptoms of seborrheic dermatitis (e.g., red, flaky, or greasy skin)?", "category": "seborrheic_dermatitis", "symptom": "duration of symptoms"},
    {"hi": "आपके शरीर के किस हिस्से में सबसे ज्यादा लक्षण दिखाई दे रहे हैं (जैसे सिर की त्वचा, चेहरा, भौहें, छाती, या पीठ)?", "en": "Where on your body do you have the most noticeable symptoms (e.g., scalp, face, eyebrows, chest, or back)?", "category": "seborrheic_dermatitis", "symptom": "location of symptoms"},
    {"hi": "क्या आपको रूसी या खुजलीदार, उबड़-खाबड़ सिर की त्वचा का अनुभव होता है?", "en": "Do you experience dandruff or an itchy, flaky scalp?", "category": "seborrheic_dermatitis", "symptom": "scalp irritation"},
    {"hi": "क्या त्वचा की जलन स्थिर रहती है, या यह बीच-बीच में बढ़ जाती है?", "en": "Is the skin irritation persistent, or does it flare up intermittently?", "category": "seborrheic_dermatitis", "symptom": "irritation pattern"},
    {"hi": "क्या आपने कोई ऐसे ट्रिगर नोटिस किए हैं जो आपके लक्षणों को बढ़ाते हैं, जैसे तनाव, मौसम परिवर्तन, या कुछ खास स्किनकेयर उत्पाद?", "en": "Have you noticed any triggers that make your symptoms worse, such as stress, weather changes, or certain skincare products?", "category": "seborrheic_dermatitis", "symptom": "triggers"},
    {"hi": "क्या आपको कोई अन्य लक्षण महसूस हो रहे हैं, जैसे त्वचा पर लालिमा, परतें, या पीले रंग की पपड़ी?", "en": "Are you experiencing any other symptoms, such as redness, scaling, or yellowish crusts on your skin?", "category": "seborrheic_dermatitis", "symptom": "other symptoms"},
    {"hi": "क्या आपको कोई अन्य स्थितियाँ हैं, जैसे तैलीय त्वचा, फंगल संक्रमण, या अन्य पुरानी त्वचा स्थितियाँ (जैसे सोरायसिस, एक्जिमा)?", "en": "Do you have any underlying conditions like oily skin, fungal infections, or other chronic skin conditions (e.g., psoriasis, eczema)?", "category": "seborrheic_dermatitis", "symptom": "underlying conditions"},
    {"hi": "क्या आपको सेबोरेइक डर्मेटाइटिस से जुड़ी कोई अन्य स्थिति, जैसे पार्किंसंस रोग या एचआईवी, का इतिहास है?", "en": "Do you have a history of other conditions, such as Parkinson’s disease or HIV, which are associated with seborrheic dermatitis?", "category": "seborrheic_dermatitis", "symptom": "history of associated conditions"},
    {"hi": "क्या आपने सेबोरेइक डर्मेटाइटिस के लिए कोई उपचार किया है, जैसे मेडिकेटेड शैंपू, टॉपिकल क्रीम, या कोर्टिकोस्टेरॉइड्स?", "en": "Have you tried any treatments for seborrheic dermatitis, such as medicated shampoos, topical creams, or corticosteroids?", "category": "seborrheic_dermatitis", "symptom": "treatments tried"},
    {"hi": "क्या आपके परिवार में सेबोरेइक डर्मेटाइटिस या अन्य त्वचा विकारों का इतिहास है?", "en": "Do you have a family history of seborrheic dermatitis or other skin disorders?", "category": "seborrheic_dermatitis", "symptom": "family history of seborrheic dermatitis"}
],

'cellulitis' : [
    {"hi": "आप कब से सेल्यूलाइटिस के लक्षण महसूस कर रहे हैं (जैसे त्वचा में लालिमा, सूजन, गर्मी, या दर्द)?", "en": "How long have you been experiencing symptoms of cellulitis (e.g., redness, swelling, warmth, or pain in the skin)?", "category": "cellulitis", "symptom": "duration of symptoms"},
    {"hi": "सेल्यूलाइटिस सबसे पहले आपके शरीर के किस हिस्से में दिखा (जैसे पैरों, हाथों, चेहरे)?", "en": "Where on your body did the cellulitis first appear (e.g., legs, arms, face)?", "category": "cellulitis", "symptom": "location of cellulitis"},
    {"hi": "क्या आपको हाल ही में कट, कीड़े के काटने, या त्वचा में कोई अन्य दरारें हुई हैं जहाँ संक्रमण घुस सकता था?", "en": "Have you had any recent cuts, insect bites, or other breaks in the skin where the infection could have entered?", "category": "cellulitis", "symptom": "skin injury or break"},
    {"hi": "क्या संक्रमण का क्षेत्र समय के साथ अधिक सूजा, लाल हुआ, या दर्दनाक हो गया है?", "en": "Is the area of infection becoming more swollen, red, or painful over time?", "category": "cellulitis", "symptom": "infection progression"},
    {"hi": "क्या आपको त्वचा के संक्रमण के साथ बुखार, ठंड लगना, या फ्लू जैसे लक्षण महसूस हुए हैं?", "en": "Have you noticed any fever, chills, or flu-like symptoms along with the skin infection?", "category": "cellulitis", "symptom": "systemic symptoms"},
    {"hi": "क्या आपको कोई अन्य स्वास्थ्य समस्याएँ हैं, जैसे डायबिटीज, कमजोर इम्यून सिस्टम, या परिसंचरण संबंधी समस्याएँ, जो संक्रमण के जोखिम को बढ़ा सकती हैं?", "en": "Do you have any underlying health conditions, such as diabetes, weakened immune system, or circulatory problems, that could increase your risk of infection?", "category": "cellulitis", "symptom": "underlying health conditions"},
    {"hi": "क्या आपको पहले कभी सेल्यूलाइटिस या बार-बार होने वाले त्वचा संक्रमण का सामना हुआ है?", "en": "Have you had a history of cellulitis or recurrent skin infections in the past?", "category": "cellulitis", "symptom": "history of cellulitis"},
    {"hi": "क्या आप किसी दवा का सेवन कर रहे हैं, विशेष रूप से स्टेरॉयड या इम्यूनोसप्रेसिव दवाएँ?", "en": "Are you currently taking any medications, particularly steroids or immunosuppressive drugs?", "category": "cellulitis", "symptom": "current medications"},
    {"hi": "क्या आसपास के लिम्फ नोड्स में सूजन है, या संक्रमित क्षेत्र के आस-पास की गति सीमा में कोई बदलाव हुआ है?", "en": "Do you have any swelling in nearby lymph nodes, or have you noticed any changes in your range of motion around the infected area?", "category": "cellulitis", "symptom": "swelling or motion limitation"},
    {"hi": "क्या आपने किसी ऐसे व्यक्ति से संपर्क किया है जो त्वचा संक्रमण से पीड़ित हो, या क्या आपने किसी ऐसी स्थिति (जैसे असंक्रमित पानी में तैरना) का अनुभव किया है जिससे बैक्टीरिया के संपर्क का जोखिम बढ़ सकता हो?", "en": "Have you been in contact with anyone who has a skin infection, or have you been in situations (e.g., swimming in untreated water) that might increase exposure to bacteria?", "category": "cellulitis", "symptom": "exposure to infection"}
],

'impetigo' : [
    {"hi": "आपको दाने या घाव कब से हैं, और ये पहले कब दिखाई दिए?", "en": "How long have you had the rash or sores, and when did they first appear?", "category": "impetigo", "symptom": "duration of symptoms"},
    {"hi": "घाव आपके शरीर के किस हिस्से पर हैं (जैसे चेहरा, हाथ, पैर, या नाक और मुँह के आस-पास)?", "en": "Where on your body are the sores located (e.g., face, arms, legs, or around the nose and mouth)?", "category": "impetigo", "symptom": "location of sores"},
    {"hi": "क्या घाव फफोले के रूप में शुरू होते हैं, और क्या ये फटते हैं या स्कैब बनते हैं?", "en": "Do the sores start as blisters, and do they rupture or form scabs?", "category": "impetigo", "symptom": "type and progression of sores"},
    {"hi": "क्या घाव आपके शरीर के अन्य हिस्सों में फैल गए हैं या आपके आसपास के किसी और व्यक्ति में भी हुए हैं?", "en": "Have the sores spread to other areas of your skin or to anyone else around you?", "category": "impetigo", "symptom": "spread of infection"},
    {"hi": "क्या घाव दर्दनाक, खुजलीदार, या छूने पर कोमल हैं?", "en": "Are the sores painful, itchy, or tender to the touch?", "category": "impetigo", "symptom": "pain or discomfort"},
    {"hi": "क्या आपको हाल ही में किसी कट, कीड़े के काटने, या त्वचा की जलन का सामना हुआ है, जो आपको संक्रमण के लिए अधिक संवेदनशील बना सकता है?", "en": "Have you had any recent cuts, insect bites, or skin irritation that may have made you more prone to infection?", "category": "impetigo", "symptom": "skin injury or irritation"},
    {"hi": "क्या आपको बुखार, सूजे हुए लिम्फ नोड्स, या संक्रमण के अन्य लक्षण महसूस हुए हैं?", "en": "Do you have any fever, swollen lymph nodes, or other signs of infection?", "category": "impetigo", "symptom": "systemic infection signs"},
    {"hi": "क्या आपको या आपके आसपास के किसी व्यक्ति को इम्पेटिगो या अन्य त्वचा संक्रमणों का इतिहास रहा है?", "en": "Have you or anyone close to you had a history of impetigo or other skin infections?", "category": "impetigo", "symptom": "history of skin infections"},
    {"hi": "क्या आप कोई दवा ले रहे हैं, जैसे एंटीबायोटिक्स या स्टेरॉयड, जो आपके इम्यून सिस्टम को प्रभावित कर सकते हैं?", "en": "Are you currently taking any medications, such as antibiotics or steroids, that could affect your immune system?", "category": "impetigo", "symptom": "current medications"},
    {"hi": "क्या आपने किसी ऐसे व्यक्ति से निकट संपर्क किया है जो इम्पेटिगो या किसी अन्य त्वचा संक्रमण से पीड़ित हो?", "en": "Have you been in close contact with someone who has impetigo or another skin infection?", "category": "impetigo", "symptom": "exposure to infection"}
],

'eczema' : [
    {"hi": "आपको एक्जिमा (जैसे खुजली, सूखी, या जलन वाली त्वचा) के लक्षण कब से हैं?", "en": "How long have you been experiencing symptoms of eczema (e.g., itchy, dry, or inflamed skin)?", "category": "eczema", "symptom": "duration of symptoms"},
    {"hi": "एक्जिमा आपके शरीर के किस हिस्से पर सबसे ज्यादा दिखाई देता है (जैसे चेहरा, कोहनी, घुटने, हाथ, या पैर)?", "en": "Where on your body is the eczema most noticeable (e.g., face, elbows, knees, hands, or feet)?", "category": "eczema", "symptom": "location of eczema"},
    {"hi": "क्या आपके एक्जिमा के लक्षण बढ़ते रहते हैं या यह एक स्थायी समस्या है?", "en": "Do you experience flare-ups of your eczema, or is it a chronic issue?", "category": "eczema", "symptom": "flare-ups vs chronic issue"},
    {"hi": "क्या खुजली लगातार होती है, या यह आती जाती है, और क्या खुजली से स्थिति और खराब होती है?", "en": "Is the itching constant, or does it come and go, and does scratching worsen the condition?", "category": "eczema", "symptom": "itching patterns"},
    {"hi": "क्या आपने किसी विशेष चीज़ या पैटर्न को देखा है जो आपके एक्जिमा को और बढ़ा देता है (जैसे कुछ साबुन, डिटर्जेंट, मौसम, तनाव, या खाद्य पदार्थ)?", "en": "Have you noticed any specific triggers or patterns that worsen your eczema (e.g., certain soaps, detergents, weather changes, stress, or foods)?", "category": "eczema", "symptom": "triggers"},
    {"hi": "क्या आपको अन्य एलर्जी स्थितियाँ हैं, जैसे अस्थमा, हे फीवर, या खाद्य एलर्जी?", "en": "Do you have any other allergic conditions, such as asthma, hay fever, or food allergies?", "category": "eczema", "symptom": "allergic conditions"},
    {"hi": "क्या आपको बचपन में ऐसी ही त्वचा की समस्याएँ हुई थीं, या यह आपके लिए एक नई समस्या है?", "en": "Have you had similar skin problems as a child, or is this a new issue for you?", "category": "eczema", "symptom": "history of eczema"},
    {"hi": "क्या आप कोई स्थानीय उपचार (जैसे मॉइस्चराइज़र, कॉर्टिकोस्टेरॉयड) उपयोग करते हैं, और क्या वे प्रभावी रहे हैं?", "en": "Do you use any topical treatments (e.g., moisturizers, corticosteroids), and have they been effective?", "category": "eczema", "symptom": "treatment effectiveness"},
    {"hi": "क्या आपको कोई जटिलताएँ हुई हैं, जैसे त्वचा के संक्रमण (जैसे खुजली या टूटे हुए त्वचा के कारण)?", "en": "Have you had any complications, such as skin infections (e.g., due to scratching or broken skin)?", "category": "eczema", "symptom": "complications"},
    {"hi": "क्या आपके परिवार में एक्जिमा, एलर्जी, अस्थमा, या अन्य त्वचा संबंधी समस्याओं का इतिहास है?", "en": "Is there a family history of eczema, allergies, asthma, or other skin conditions?", "category": "eczema", "symptom": "family history"}
],

'ulcer' : [
    {"hi": "आपके शरीर पर अल्सर कहां स्थित हैं (जैसे पेट, मुँह, पैर, या पैर के तलवे)?", "en": "Where on your body are the ulcers located (e.g., stomach, mouth, legs, or feet)?", "category": "ulcer", "symptom": "location of ulcer"},
    {"hi": "आपको अल्सर कब से हो रहे हैं, और यह कब पहली बार दिखाई दिया?", "en": "How long have you been experiencing the ulcer, and when did it first appear?", "category": "ulcer", "symptom": "duration and onset"},
    {"hi": "क्या अल्सर से आपको दर्द होता है, और यदि हां, तो दर्द की तीव्रता कितनी है?", "en": "Do the ulcers cause you pain, and if so, how severe is the pain?", "category": "ulcer", "symptom": "pain severity"},
    {"hi": "क्या अल्सर खुले हुए हैं और बहाव कर रहे हैं, या क्या उन पर कोई क्रस्ट या स्कैब है?", "en": "Are the ulcers open and draining, or do they have a scab or crust over them?", "category": "ulcer", "symptom": "ulcer appearance"},
    {"hi": "क्या आपने अल्सर से रक्तस्राव देखा है, या क्या आपको कोई असामान्य स्राव हुआ है?", "en": "Have you noticed any bleeding from the ulcer, or have you had any unusual discharge?", "category": "ulcer", "symptom": "bleeding or discharge"},
    {"hi": "क्या आपको गैस्ट्राइटिस, एसिड रिफ्लक्स, क्रोहन रोग, या वैरिकोज वेन जैसी बीमारियों का इतिहास है?", "en": "Do you have a history of conditions like gastritis, acid reflux, Crohn's disease, or varicose veins?", "category": "ulcer", "symptom": "underlying conditions"},
    {"hi": "क्या आप अन्य लक्षणों का अनुभव कर रहे हैं, जैसे वजन घटना, मिचली, बुखार, या भूख में बदलाव?", "en": "Are you experiencing any other symptoms, such as weight loss, nausea, fever, or changes in appetite?", "category": "ulcer", "symptom": "other symptoms"},
    {"hi": "क्या आपने हाल ही में कोई चोट, संक्रमण, या दवाइयां (जैसे NSAIDs या स्टेरॉयड) ली हैं, जो अल्सर को बढ़ा सकती हैं?", "en": "Have you recently had any injuries, infections, or medications (such as NSAIDs or steroids) that could trigger the ulcer?", "category": "ulcer", "symptom": "triggers"},
    {"hi": "क्या आपको धूम्रपान, अत्यधिक शराब सेवन, या ऐसी आहार आदतें हैं जो अल्सर बनने में योगदान कर सकती हैं?", "en": "Do you have a history of smoking, excessive alcohol use, or a diet that could contribute to ulcer formation?", "category": "ulcer", "symptom": "lifestyle factors"},
    {"hi": "क्या आप वर्तमान में अल्सर, उच्च रक्तचाप, मधुमेह, या ऑटोइम्यून रोगों के लिए कोई दवाइयां ले रहे हैं?", "en": "Are you currently taking any medications for conditions like ulcers, high blood pressure, diabetes, or autoimmune disorders?", "category": "ulcer", "symptom": "medication history"}
],

'loss of appetite' : [
    {"hi": "आपको भूख न लगने की समस्या कब से हो रही है?", "en": "How long have you been experiencing a loss of appetite?", "category": "loss_of_appetite", "symptom": "duration"},
    {"hi": "क्या भूख न लगने की समस्या निरंतर है, या यह आती-जाती रहती है?", "en": "Is the loss of appetite constant, or does it come and go?", "category": "loss_of_appetite", "symptom": "pattern"},
    {"hi": "क्या आपने अपनी खाने की आदतों में कोई और बदलाव महसूस किया है, जैसे थोड़ी मात्रा में खाने के बाद भी पेट भर जाना या कुछ खास प्रकार के खाद्य पदार्थों से बचना?", "en": "Have you noticed any other changes in your eating habits, such as feeling full after eating small amounts or avoiding certain types of food?", "category": "loss_of_appetite", "symptom": "eating habits"},
    {"hi": "क्या आपको अन्य लक्षण महसूस हो रहे हैं, जैसे वजन कम होना, मिचली, उल्टी, या मल त्याग में बदलाव?", "en": "Do you have any associated symptoms, such as weight loss, nausea, vomiting, or changes in bowel movements?", "category": "loss_of_appetite", "symptom": "associated symptoms"},
    {"hi": "क्या आपने हाल ही में कोई तनाव, चिंता, या मानसिक बदलाव महसूस किए हैं जो आपकी भूख को प्रभावित कर सकते हैं?", "en": "Have you experienced any recent stress, anxiety, or emotional changes that could affect your appetite?", "category": "loss_of_appetite", "symptom": "emotional factors"},
    {"hi": "क्या आप कोई दवाइयां ले रहे हैं, और क्या वे आपकी भूख पर प्रभाव डाल सकती हैं (जैसे दर्द निवारक, एंटीडिप्रेसेंट्स, या कीमोथेरेपी)?", "en": "Are you currently taking any medications, and could they be affecting your appetite (e.g., painkillers, antidepressants, or chemotherapy)?", "category": "loss_of_appetite", "symptom": "medications"},
    {"hi": "क्या आपको कोई शारीरिक स्वास्थ्य समस्याएं हैं, जैसे गैस्ट्रोइंटेस्टाइनल विकार, संक्रमण, थायरॉयड समस्या, या मानसिक स्वास्थ्य समस्याएं (जैसे अवसाद या खाने से संबंधित विकार)?", "en": "Do you have any underlying health conditions, such as gastrointestinal disorders, infections, thyroid problems, or mental health conditions (e.g., depression or eating disorders)?", "category": "loss_of_appetite", "symptom": "underlying health conditions"},
    {"hi": "क्या आपने हाल ही में कोई संक्रमण, बुखार, या अन्य बीमारियां अनुभव की हैं जो भूख कम होने का कारण बन सकती हैं?", "en": "Have you had any recent infections, fevers, or other illnesses that could be contributing to the loss of appetite?", "category": "loss_of_appetite", "symptom": "recent illnesses"},
    {"hi": "क्या आपको अपनी स्वाद या गंध की भावना में कोई बदलाव महसूस हुआ है, या खाने में कठिनाई हो रही है?", "en": "Have you noticed any changes in your sense of taste or smell, or difficulty swallowing food?", "category": "loss_of_appetite", "symptom": "taste/smell or swallowing"},
    {"hi": "क्या आपको खाने से संबंधित कोई एलर्जी, पाचन समस्याएं, या पुरानी बीमारियां हैं जो भूख को प्रभावित कर सकती हैं?", "en": "Do you have a history of food allergies, digestive issues, or chronic conditions that might affect your appetite?", "category": "loss_of_appetite", "symptom": "history of digestive or food-related issues"}
],

'tinnitus' : [
    {"hi": "आपको टिनिटस (कान में घंटी बजने, बजने, या अन्य ध्वनियां) कब से हो रही हैं?", "en": "How long have you been experiencing tinnitus (ringing, buzzing, or other sounds in your ears)?", "category": "tinnitus", "symptom": "duration"},
    {"hi": "क्या टिनिटस लगातार है, या यह आती-जाती रहती है?", "en": "Is the tinnitus constant, or does it come and go?", "category": "tinnitus", "symptom": "pattern"},
    {"hi": "कान में सुनाई देने वाली ध्वनि कैसी है (जैसे घंटी बजने, बजने, सीटी बजने या झींकने)?", "en": "What does the sound in your ears sound like (e.g., ringing, buzzing, hissing, or whistling)?", "category": "tinnitus", "symptom": "sound description"},
    {"hi": "क्या टिनिटस एक कान में है या दोनों कानों में?", "en": "Is the tinnitus in one ear or both ears?", "category": "tinnitus", "symptom": "laterality"},
    {"hi": "क्या आपने हाल ही में तेज शोर, जैसे संगीत, मशीनरी, या हेडफ़ोन, के संपर्क में आए हैं?", "en": "Have you been exposed to loud noises, such as concerts, machinery, or headphones, recently?", "category": "tinnitus", "symptom": "noise exposure"},
    {"hi": "क्या आपको टिनिटस के साथ सुनने में कठिनाई या सुनवाई हानि हो रही है?", "en": "Do you have any hearing loss or difficulty hearing along with the tinnitus?", "category": "tinnitus", "symptom": "hearing loss"},
    {"hi": "क्या आपको कान के स्वास्थ्य में कोई बदलाव महसूस हुआ है, जैसे दर्द, भरी हुई अनुभूति, स्राव, या संक्रमण?", "en": "Have you experienced any changes in your ear health, such as pain, fullness, drainage, or infections?", "category": "tinnitus", "symptom": "ear health changes"},
    {"hi": "क्या आप अन्य लक्षणों का अनुभव कर रहे हैं, जैसे चक्कर, संतुलन संबंधी समस्याएं, या सिरदर्द?", "en": "Are you experiencing any other symptoms, such as dizziness, balance issues, or headaches?", "category": "tinnitus", "symptom": "associated symptoms"},
    {"hi": "क्या आपको कान से संबंधित किसी समस्या का इतिहास है, जैसे कान में संक्रमण, कान में मोम जमा होना, या टेम्पोरोमैंडिबुलर जॉइंट (TMJ) समस्याएं?", "en": "Do you have a history of ear problems, like ear infections, earwax buildup, or temporomandibular joint (TMJ) issues?", "category": "tinnitus", "symptom": "ear problems history"},
    {"hi": "क्या आप कोई दवाइयां ले रहे हैं, विशेष रूप से उन दवाओं के बारे में जो सुनवाई को प्रभावित कर सकती हैं (जैसे एस्पिरिन, एंटीबायोटिक्स, या मूत्रवर्धक)?", "en": "Are you currently taking any medications, particularly those known to affect hearing (e.g., aspirin, antibiotics, or diuretics)?", "category": "tinnitus", "symptom": "medications"}
],

'chest tightness' : [
    {"hi": "आपको छाती में संकुचन कब से महसूस हो रहा है?", "en": "How long have you been experiencing chest tightness?", "category": "chest tightness", "symptom": "duration"},
    {"hi": "क्या छाती में संकुचन लगातार है, या यह आती-जाती रहती है?", "en": "Is the chest tightness constant, or does it come and go?", "category": "chest tightness", "symptom": "pattern"},
    {"hi": "क्या आपको संकुचन विश्राम की स्थिति में महसूस होता है, या यह शारीरिक गतिविधि, तनाव, या खाने के बाद होता है?", "en": "Do you experience the tightness at rest, or does it occur during physical activity, stress, or after eating?", "category": "chest tightness", "symptom": "triggers"},
    {"hi": "1 से 10 के पैमाने पर, संकुचन की गंभीरता कितनी है?", "en": "On a scale of 1-10, how severe is the tightness?", "category": "chest tightness", "symptom": "severity"},
    {"hi": "क्या आपको संकुचन के साथ कोई अन्य लक्षण महसूस हो रहे हैं, जैसे सांस की कमी, दर्द, चक्कर, या मितली?", "en": "Do you have any associated symptoms, such as shortness of breath, pain, dizziness, or nausea?", "category": "chest tightness", "symptom": "associated symptoms"},
    {"hi": "क्या आपको हाल ही में छाती क्षेत्र में कोई चोट या आघात लगा है?", "en": "Have you had any recent injuries or trauma to the chest area?", "category": "chest tightness", "symptom": "injury/trauma"},
    {"hi": "क्या आपको दिल की बीमारी, उच्च रक्तचाप, अस्थमा, या एसिड रिफ्लक्स का इतिहास है?", "en": "Do you have a history of heart disease, high blood pressure, asthma, or acid reflux?", "category": "chest tightness", "symptom": "medical history"},
    {"hi": "क्या आपको संकुचन के साथ खांसी, घरघराहट, या सांस लेने में कठिनाई हो रही है?", "en": "Have you experienced any coughing, wheezing, or difficulty breathing in conjunction with the chest tightness?", "category": "chest tightness", "symptom": "respiratory symptoms"},
    {"hi": "क्या आप वर्तमान में अत्यधिक तनाव, चिंता, या भावनात्मक दबाव में हैं?", "en": "Are you currently under a lot of stress, anxiety, or emotional strain?", "category": "chest tightness", "symptom": "emotional factors"},
    {"hi": "क्या आप धूम्रपान करते हैं, या क्या आपने प्रदूषण या एलर्जीजनक तत्वों से संपर्क किया है?", "en": "Do you smoke, or have you been exposed to environmental factors like pollutants or allergens?", "category": "chest tightness", "symptom": "environmental factors"}
],

'nail splitting': [
    {"hi": "क्या आपको नाखूनों में दरारें या फटने की समस्या हो रही है?", "en": "Are you experiencing nail splitting or cracking?", "category": "nail_splitting", "symptom": "nail splitting"},
    {"hi": "कौन से नाखून प्रभावित हैं (जैसे उंगलियां, पैर, या कोई विशेष नाखून)?", "en": "Which nails are affected (e.g., fingers, toes, specific nails)?", "category": "nail_splitting", "symptom": "affected nails"},
    {"hi": "क्या नाखूनों में फटने से दर्द होता है या कोई असुविधा महसूस होती है?", "en": "Is the splitting painful, or does it cause any discomfort?", "category": "nail_splitting", "symptom": "pain or discomfort"},
    {"hi": "क्या आपने नाखूनों के रंग, बनावट, या मोटाई में कोई बदलाव महसूस किया है, जैसे कि रंग का बदलना या नाखूनों का कमजोर होना?", "en": "Have you noticed any changes in the color, texture, or thickness of your nails, such as discoloration or brittleness?", "category": "nail_condition", "symptom": "nail discoloration or brittleness"},
    {"hi": "क्या आपको नाखूनों को किसी प्रकार का आघात, अधिक हाथ धोने या कठोर रसायनों के संपर्क में आने का इतिहास है (जैसे सफाई उत्पाद, नेल पॉलिश रिमूवर)?", "en": "Do you have a history of nail trauma, frequent hand washing, or exposure to harsh chemicals (e.g., cleaning products, nail polish removers)?", "category": "external_factors", "symptom": "trauma or chemical exposure"},
    {"hi": "क्या आपके नाखूनों या त्वचा में कोई अन्य परिवर्तन जैसे कि सूखापन, छीलना, या नाखूनों पर रेखाएँ दिखाई दे रही हैं?", "en": "Have you been experiencing any other skin or nail changes, such as dryness, peeling, or ridges on your nails?", "category": "skin_or_nail_changes", "symptom": "dryness, peeling, or ridges"},
    {"hi": "क्या आपको कोई ऐसी स्वास्थ्य स्थिति है जैसे थायरॉयड विकार, सोरायसिस, या मधुमेह, जो आपके नाखूनों को प्रभावित कर सकती है?", "en": "Do you have any underlying health conditions, such as thyroid disorders, psoriasis, or diabetes, that may affect your nails?", "category": "health_conditions", "symptom": "underlying health conditions"},
    {"hi": "क्या आप कोई ऐसी दवाइयाँ या सप्लीमेंट ले रहे हैं, जो आपके नाखूनों को प्रभावित कर सकते हैं (जैसे कि कीमोथेरेपी, बायोटिन, या अन्य विटामिन की कमी)?", "en": "Are you taking any medications or supplements that might be affecting your nails (e.g., chemotherapy, biotin, or other vitamin deficiencies)?", "category": "medications", "symptom": "medications or supplements"},
    {"hi": "क्या आपके परिवार में नाखूनों या त्वचा की बीमारियों का इतिहास है, जैसे एक्जिमा या फंगल संक्रमण?", "en": "Do you have a family history of nail or skin conditions, such as eczema or fungal infections?", "category": "family_history", "symptom": "family history of skin or nail conditions"},
    {"hi": "क्या नाखूनों के प्रभावित हिस्सों में संक्रमण के लक्षण जैसे लालिमा, सूजन, या पस का स्राव हो रहा है?", "en": "Have you experienced any symptoms of infection, such as redness, swelling, or pus around the affected nails?", "category": "infection", "symptom": "infection symptoms"}
],

    # Add more canonical symptoms and their follow-up questions as needed
}

# Additional general follow-up questions
additional_followup_questions : [
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
