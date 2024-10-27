import os
import datetime
import openai
import dotenv
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from pydub import AudioSegment
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from rapidfuzz import process, fuzz  # Corrected import
import torch
import zipfile
import requests
import shutil
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import spacy
import re
import logging

# -------------------- Environment Setup -------------------- #

# Load environment variables from .env file
dotenv.load_dotenv()
#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "sk-_8i-5CjqPiA9GdeDqjfsybwgMwyXsreAzHqdYjlNxFT3BlbkFJxgU4Fd2AAV5G8z5yth53M-KKgRRQaTmR9XWLE0Da8A"
# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- Load BioBERT NER Model -------------------- #

# URL to your BioBERT NER model zip file hosted externally
BIOBERT_MODEL_URL = "https://www.dropbox.com/scl/fi/bsphlpwlt7jclb9ybiyx6/medical-bert-symptom-ner.zip?rlkey=j1066ivw1qvkp0c8urpm8pjv6&st=bk4e923j&dl=1"

# Path to the BioBERT model directory
biobert_model_dir = 'medical-bert-symptom-ner'  # Path where the model will be extracted

def download_and_unzip_biobert_model(model_url, model_dir):
    if not os.path.exists(model_dir):
        st.info("Downloading the BioBERT NER model. Please wait...")
        # Download the model zip file
        with st.spinner('Downloading BioBERT NER model...'):
            response = requests.get(model_url, stream=True)
            if response.status_code == 200:
                with open('biobert_model.zip', 'wb') as out_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            out_file.write(chunk)
            else:
                st.error("Failed to download the BioBERT NER model. Please check the URL.")
                st.stop()
        # Unzip the model
        try:
            with zipfile.ZipFile('biobert_model.zip', 'r') as zip_ref:
                zip_ref.extractall('.')
            st.success("BioBERT NER model downloaded and extracted successfully.")
        except zipfile.BadZipFile:
            st.error("Downloaded BioBERT model file is not a valid zip file.")
            st.stop()
        finally:
            os.remove('biobert_model.zip')

# Download and unzip the BioBERT model if it doesn't exist
download_and_unzip_biobert_model(BIOBERT_MODEL_URL, biobert_model_dir)

# Check if the BioBERT model directory exists after extraction
if not os.path.exists(biobert_model_dir):
    st.error(f"BioBERT model directory '{biobert_model_dir}' not found after extraction.")
    st.stop()

# Load the tokenizer and model using caching
@st.cache_resource
def load_biobert_ner_pipeline():
    tokenizer = AutoTokenizer.from_pretrained(biobert_model_dir, add_prefix_space=True)
    model = AutoModelForTokenClassification.from_pretrained(biobert_model_dir)
    device = 0 if torch.cuda.is_available() else -1
    ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple", device=device)
    return ner_pipeline

ner_pipeline = load_biobert_ner_pipeline()
st.sidebar.success("BioBERT NER model loaded successfully!")

# -------------------- Load Whisper Model -------------------- #

@st.cache_resource
def load_whisper_model():
    """
    Load the SpaCy model for additional NLP tasks.
    """
    try:
        nlp = spacy.load('en_core_web_sm')
        return nlp
    except OSError:
        st.error("SpaCy model 'en_core_web_sm' not found. Please ensure it's installed correctly.")
        logger.error("SpaCy model 'en_core_web_sm' not found.")
        st.stop()

nlp = load_whisper_model()

# -------------------- Load Disease-Symptom Mapping -------------------- #

@st.cache_resource
def load_disease_symptom_mapping():
    if not os.path.exists("disease_symptom_mapping.csv"):
        st.error("'disease_symptom_mapping.csv' not found in the current directory.")
        logger.error("'disease_symptom_mapping.csv' not found.")
        st.stop()
    df = pd.read_csv("disease_symptom_mapping.csv")
    logger.info("'disease_symptom_mapping.csv' loaded successfully.")
    return df

df_disease_symptom = load_disease_symptom_mapping()

# Prepare a list of known symptoms
known_symptoms = df_disease_symptom['SymptomName'].unique()

# -------------------- Core Functions -------------------- #

def translate(audio_file):
    """
    Translate the given audio file to English using OpenAI's Whisper API.

    Args:
        audio_file (file-like object): The audio file to translate.

    Returns:
        dict: The translation result.
    """
    try:
        translation = openai.Audio.translate("whisper-1", audio_file)
        st.info("Translation successful.")
        return translation
    except Exception as e:
        st.error(f"Translation failed: {e}")
        logger.error(f"Translation failed: {e}")
        return None

def transcribe(audio_file):
    """
    Transcribe the given audio file using OpenAI's Whisper API.

    Args:
        audio_file (file-like object): The audio file to transcribe.

    Returns:
        dict: The transcription result.
    """
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        st.info("Transcription successful.")
        return transcript
    except Exception as e:
        st.error(f"Transcription failed: {e}")
        logger.error(f"Transcription failed: {e}")
        return None

def save_audio_file(audio_bytes, file_extension):
    """
    Save audio bytes to a file with the specified extension.

    Args:
        audio_bytes (bytes): Audio data in bytes.
        file_extension (str): The extension of the output audio file.

    Returns:
        str: The name of the saved audio file.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"audio_{timestamp}.{file_extension}"

    try:
        with open(file_name, "wb") as f:
            f.write(audio_bytes)
        st.success(f"Audio saved as {file_name}")
        logger.info(f"Audio saved as {file_name}")
        return file_name
    except Exception as e:
        st.error(f"Failed to save audio file: {e}")
        logger.error(f"Failed to save audio file: {e}")
        return None

def translate_audio(file_path):
    """
    Translate the audio file at the specified path to English.

    Args:
        file_path (str): The path of the audio file to translate.

    Returns:
        str: The translated text in English.
    """
    try:
        with open(file_path, "rb") as audio_file:
            translation = translate(audio_file)
            if translation:
                return translation.get("text", "").strip()
            else:
                return ""
    except Exception as e:
        st.error(f"An error occurred while translating: {e}")
        logger.error(f"An error occurred while translating: {e}")
        return ""

def transcribe_audio(file_path):
    """
    Transcribe the audio file at the specified path.

    Args:
        file_path (str): The path of the audio file to transcribe.

    Returns:
        str: The transcribed text.
    """
    try:
        with open(file_path, "rb") as audio_file:
            transcript = transcribe(audio_file)
            if transcript:
                return transcript.get("text", "").strip()
            else:
                return ""
    except Exception as e:
        st.error(f"An error occurred while transcribing: {e}")
        logger.error(f"An error occurred while transcribing: {e}")
        return ""

def extract_symptoms(text):
    """
    Extract symptoms from the input text using BioBERT-based NER.

    Args:
        text (str): The input text containing symptoms.

    Returns:
        set: A set of extracted symptom strings.
    """
    entities = ner_pipeline(text)
    if not entities:
        return set()
    # Extract unique symptoms
    extracted_symptoms = set([entity['word'].title() for entity in entities])
    return extracted_symptoms

def match_symptoms(extracted_symptoms):
    """
    Match extracted symptoms with known symptoms using RapidFuzz.

    Args:
        extracted_symptoms (set): A set of extracted symptom strings.

    Returns:
        set: A set of matched symptoms from the known symptoms list.
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
    Extract additional entities like age, gender, location, duration, and medications from text.

    Args:
        text (str): The input text.

    Returns:
        dict: A dictionary containing extracted entities.
    """
    doc = nlp(text)
    age = None
    gender = None
    location = None
    duration = None
    medications = []

    # Extract entities using SpaCy
    for ent in doc.ents:
        if ent.label_ == 'GPE':
            location = ent.text

    # Extract age
    age_patterns = [
        r'(\b\d{1,2}\b)\s*(years old|year old|y/o|yo|yrs old)',
        r'age\s*(\b\d{1,2}\b)'
    ]
    for pattern in age_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            age = int(match.group(1))
            break

    # Extract gender
    gender_patterns = [
        r'\b(male|female|man|woman|boy|girl)\b'
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

    # Extract duration
    duration_patterns = [
        r'since\s*(\d+\s*(days?|weeks?|months?|years?))',
        r'for\s*(\d+\s*(days?|weeks?|months?|years?))',
        r'(\d+\s*(days?|weeks?|months?|years?))\s*(ago|back)'
    ]
    for pattern in duration_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            duration = match.group(1)
            break

    # Extract medications
    # For simplicity, we'll assume that medications are mentioned after phrases like 'taking' or 'taken'
    medication_patterns = [
        r'(taking|taken|take)\s+([\w\s]+)'
    ]
    for pattern in medication_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            meds = match[1].strip()
            # Remove common words that are not medications
            stopwords = ['and', 'or', 'but', 'with', 'without']
            meds = ' '.join([word for word in meds.split() if word.lower() not in stopwords])
            medications.append(meds.title())

    return {
        'age': age,
        'gender': gender,
        'location': location,
        'duration': duration,
        'medications': medications
    }

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

# -------------------- Streamlit Interface -------------------- #

def main():

    #Main function to run the integrated Whisper Transcription and BioBERT-based Symptom-to-Disease Mapper app.

    st.title("🩺 O-Health LLM Tool")
    st.write("""
        Welcome to the O-Health LLM Platform. You can either speak your symptoms in any language or type them to receive healthcare recommendations based on your inputs.
    """)

    # Create two tabs: Voice Input and Text Input
    tab1, tab2 = st.tabs(["🔊 Voice Input", "✍️ Text Input"])

    # ----------------- Voice Input Tab ----------------- #
    with tab1:
        st.header("Record Your Symptoms in Hindi")
        st.write("Click the **Record** button below, speak your symptoms in Hindi, and then click **Stop**.")

        # Record audio using audio_recorder_streamlit
        audio_bytes = audio_recorder()

        if audio_bytes:
            # Display the recorded audio
            st.audio(audio_bytes, format="audio/wav")

            # Save the recorded audio to a file
            file_name = save_audio_file(audio_bytes, "wav")

            if file_name:
                st.info("Audio recorded and saved successfully!")

                # Translate the audio to English
                translated_text = translate_audio(file_name)

                if translated_text:
                    st.subheader("📝 Transcribed and Translated Text (English):")
                    st.write(translated_text)
                    # Store the translated text in session state for diagnosis
                    st.session_state["user_input"] = translated_text
                else:
                    st.error("Failed to transcribe and translate the audio.")

    # ----------------- Text Input Tab ----------------- #
    with tab2:
        st.header("Enter Your Symptoms in English")
        st.write("Type your symptoms below and click **Submit** to receive disease recommendations.")

        # Text area for user input
        user_input = st.text_area(
            "📋 Enter your symptoms and additional information:",
            height=150,
            placeholder="e.g., I have been suffering from fever for the past two days.",
        )

        if st.button("Submit"):
            if user_input.strip() == "":
                st.warning("Please enter your symptoms for diagnosis.")
            else:
                st.session_state["user_input"] = user_input
                st.success("Input received! Click on the **Diagnose** button to proceed.")

    # ----------------- Diagnose Button ----------------- #
    if st.button("Diagnose"):
        if "user_input" not in st.session_state or st.session_state["user_input"].strip() == "":
            st.warning("Please provide your symptoms either via voice or text input first.")
        else:
            with st.spinner("Analyzing your symptoms..."):
                input_text = st.session_state["user_input"]

                # Extract symptoms using BioBERT-based NER pipeline
                extracted_symptoms = extract_symptoms(input_text)
                if not extracted_symptoms:
                    st.error("No symptoms detected. Please try again.")
                    return

                # Match extracted symptoms with known symptoms
                matched_symptoms = match_symptoms(extracted_symptoms)

                if not matched_symptoms:
                    st.error("No matching symptoms found in our database. Please try again with different symptoms.")
                    return

                # Extract additional entities (age, gender, etc.)
                additional_info = extract_additional_entities(input_text)

                # Display extracted information
                st.subheader("📝 Extracted Information:")
                st.write(f"**Symptoms:** {', '.join(matched_symptoms)}")
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

                # Map symptoms to diseases
                probable_diseases = map_symptoms_to_diseases(matched_symptoms, additional_info)

                if probable_diseases:
                    # Display results
                    st.subheader("🩺 Probable Diseases:")
                    for disease, prob in probable_diseases.items():
                        st.write(f"**{disease}**: {prob}%")

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

# -------------------- Run the App -------------------- #

if __name__ == "__main__":
    main()
