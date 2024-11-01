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
import streamlit.components.v1 as components

# -------------------- Environment Setup -------------------- #

# Set the OpenAI API key from environment variable
openai.api_key = st.secrets["OPENAI_API_KEY"]

if not openai.api_key:
    st.error("OpenAI API key not found. Please set it as an environment variable 'OPENAI_API_KEY'.")
    st.stop()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# -------------------- Define Symptom List -------------------- #

symptom_list = [
    'fever', 'cough', 'headache', 'nausea', 'abdominal pain', 'chills',
    'vomiting', 'diarrhea', 'fatigue', 'shortness of breath', 'sore throat',
    'runny nose', 'sneezing', 'rash', 'dizziness', 'weakness', 'loss of appetite',
    'muscle pain', 'joint pain', 'chest pain', 'back pain', 'constipation',
    'throat pain', 'cold', 'flu', 'breathlessness', 'stomach ache', 'migraine',
    'pain', 'ache', 'sore', 'burning', 'itching', 'swelling', 'infection',
    'inflammation', 'cramps', 'ulcers', 'bleeding', 'irritation', 'anxiety',
    'depression', 'insomnia', 'cancer', 'diabetes', 'hypertension',
    # Add more symptoms and their variations as needed
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

def embed_audio_autoplay(audio_bytes: bytes):
    """
    Embed audio in Streamlit app with autoplay using HTML and JavaScript.
    Includes a fallback play button if autoplay is blocked.
    """
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

def extract_symptoms(text):
    try:
        text_lower = text.lower()
        extracted_symptoms = set()
        for symptom in symptom_list:
            symptom_lower = symptom.lower()
            # Use word boundaries to avoid partial matches
            if re.search(r'\b' + re.escape(symptom_lower) + r'\b', text_lower):
                extracted_symptoms.add(symptom.title())
        logger.info(f"Extracted Symptoms: {extracted_symptoms}")
        return extracted_symptoms
    except Exception as e:
        st.error(f"An error occurred during symptom extraction: {e}")
        logger.error(f"Symptom extraction error: {e}")
        return set()

def extract_additional_entities(text):
    doc = nlp(text)
    age = None
    gender = None
    location = None
    duration = None
    medications = []

    # Medications list (extend as needed)
    medications_list = [
        "ibuprofen", "dolo650", "paracetamol", "aspirin", "acetaminophen",
        "amoxicillin", "antibiotic", "metformin", "lisinopril", "atorvastatin",
        "cetirizine", "azithromycin", "hydrochlorothiazide", "omeprazole",
        "sertraline", "naproxen", "albuterol", "simvastatin", "loratadine",
        "furosemide", "clopidogrel", "prednisone", "insulin", "levothyroxine",
        "gabapentin", "citalopram", "hydrocodone", "codeine", "tramadol",
        "doxycycline", "ciprofloxacin", "lorazepam", "diazepam", "clonazepam",
        # Add more as needed
    ]
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

    # Define symptom-specific follow-up questions
    symptom_followup_questions = {
        "Fever": [
            {"hi": "क्या आपका बुखार लगातार है या बार-बार आता है?", "en": "Is your fever constant or intermittent?", "category": "fever_type"},
            {"hi": "क्या आप ठंडक महसूस कर रहे हैं?", "en": "Are you experiencing any chills?", "category": "chills"},
            {"hi": "क्या आपने कोई दवा ली है?", "en": "Have you taken any medication?", "category": "medications"},
            {"hi": "क्या आपको सिरदर्द हो रहा है?", "en": "Are you experiencing headaches?", "category": "headache"},
            {"hi": "क्या आपको उल्टी महसूस हो रही है?", "en": "Are you feeling nauseous?", "category": "nausea"}
        ],
        "Cough": [
            {"hi": "क्या आपकी खांसी सूखी है या बलगम के साथ?", "en": "Is your cough dry or with phlegm?", "category": "cough_type"},
            {"hi": "क्या आपके खांसी के साथ बुखार है?", "en": "Do you have a fever along with your cough?", "category": "fever"},
            {"hi": "क्या आप सांस लेने में कठिनाई महसूस करते हैं?", "en": "Are you experiencing difficulty breathing?", "category": "breathing"},
            {"hi": "क्या आपकी खांसी रात में ज्यादा होती है?", "en": "Does your cough worsen at night?", "category": "time"},
            {"hi": "क्या आपको सीने में दर्द हो रहा है?", "en": "Are you experiencing chest pain?", "category": "chest_pain"}
        ],
        # Add more symptoms and their corresponding follow-up questions as needed
    }

    # Additional general follow-up questions
    additional_followup_questions = [
        {"hi": "आपकी उम्र क्या है?", "en": "What is your age?", "category": "age"},
        {"hi": "आपका लिंग क्या है?", "en": "What is your gender?", "category": "gender"},
        {"hi": "आप वर्तमान में कहां स्थित हैं?", "en": "Where are you currently located?", "category": "location"},
        {"hi": "लक्षण कब से हैं?", "en": "How long have you had these symptoms?", "category": "duration"},
        {"hi": "क्या आप कोई अन्य लक्षण महसूस कर रहे हैं?", "en": "Are you experiencing any other symptoms?", "category": "other_symptoms"}
    ]

    # Determine questions based on matched symptoms
    for symptom in matched_symptoms:
        if symptom in symptom_followup_questions:
            for q in symptom_followup_questions[symptom]:
                category = q.get('category')
                if category not in asked_categories and len(followup_questions) < 5:
                    # Skip questions if the information is already provided
                    if category in additional_info and additional_info.get(category):
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
            matched_symptoms.update(symptoms)
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
            matched_symptoms.update(symptoms)
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

def extract_and_prepare_questions(conversation_history):
    matched_symptoms, additional_info = extract_all_symptoms(conversation_history)
    st.session_state.additional_info = additional_info  # Store in session state for access elsewhere
    followup_questions = determine_followup_questions(matched_symptoms, additional_info)
    st.session_state.matched_symptoms = matched_symptoms  # Store matched symptoms in session state
    return followup_questions

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

# -------------------- Streamlit Interface -------------------- #

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

    st.title("🩺 O-Health Diagnostic Tool")
    st.write("""
        Welcome to the O-Health Diagnostic Tool. You can either speak your symptoms in Hindi or type them in English to receive potential disease recommendations based on your inputs.
    """)

    # Step 0: Welcome Message
    if st.session_state.current_step == 0:
        # Generate the welcome audio in Hindi
        welcome_text = "ओ-हेल्थ में आपका स्वागत है। कृपया माइक्रोफ़ोन बटन दबाएं और अपने लक्षण बोलें।"
        audio_bytes = generate_audio(welcome_text, lang='hi')
        if audio_bytes:
            # Attempt to embed and autoplay the audio
            embed_audio_autoplay(audio_bytes)
        else:
            st.error("Failed to generate welcome audio.")

        # Display a welcome message
        st.write("### Hello! 👋")
        st.write("We're glad to have you here.")
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
                    st.subheader("📝 Transcribed Text (English):")
                    st.write(transcribed_text)
                    st.session_state.conversation_history.append({
                        'user': transcribed_text
                    })
                    st.session_state.followup_questions = extract_and_prepare_questions(st.session_state.conversation_history)
                    st.session_state.current_step = 2  # Proceed to follow-up questions
                    st.session_state['symptoms_processed'] = True
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
                st.subheader("📝 Your Input:")
                st.write(user_input)
                st.session_state.conversation_history.append({
                    'user': user_input
                })
                st.session_state.followup_questions = extract_and_prepare_questions(st.session_state.conversation_history)
                st.session_state.current_step = 2  # Proceed to follow-up questions
                st.session_state['symptoms_processed'] = True
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
                question_audio = generate_audio(current_question['hi'], lang='hi')
                if question_audio:
                    # Attempt to embed and autoplay the audio
                    embed_audio_autoplay(question_audio)
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
                        st.subheader(f"📝 Response to Follow-Up Question {question_number} (English):")
                        st.write(response_transcribed)
                        st.session_state.conversation_history.append({
                            'followup_question_en': current_question['en'],
                            'response': response_transcribed
                        })
                        # Process the response
                        new_symptoms = extract_symptoms(response_transcribed)
                        if new_symptoms:
                            st.session_state.matched_symptoms.update(new_symptoms)
                        # Extract additional entities
                        info = extract_additional_entities(response_transcribed)
                        for key, value in info.items():
                            if value:
                                if isinstance(value, list):
                                    st.session_state.additional_info[key].extend(value)
                                    st.session_state.additional_info[key] = list(set(st.session_state.additional_info[key]))
                                else:
                                    st.session_state.additional_info[key] = value
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
                    st.session_state.conversation_history.append({
                        'followup_question_en': current_question['en'],
                        'response': answer_input
                    })
                    # Process the response
                    new_symptoms = extract_symptoms(answer_input)
                    if new_symptoms:
                        st.session_state.matched_symptoms.update(new_symptoms)
                    # Extract additional entities
                    info = extract_additional_entities(answer_input)
                    for key, value in info.items():
                        if value:
                            if isinstance(value, list):
                                st.session_state.additional_info[key].extend(value)
                                st.session_state.additional_info[key] = list(set(st.session_state.additional_info[key]))
                            else:
                                st.session_state.additional_info[key] = value
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
