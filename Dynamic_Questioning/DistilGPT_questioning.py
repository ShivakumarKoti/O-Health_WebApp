# health_question_generator_with_llm.py

import spacy
import re
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Load spaCy English model
nlp = spacy.load('en_core_web_sm')

# Initialize the LLM for text generation
# Choose a model suitable for your hardware capabilities
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")  # Or use "distilgpt2" for lower resource usage
model = AutoModelForCausalLM.from_pretrained("gpt2")
text_generator = pipeline('text-generation', model=model, tokenizer=tokenizer, device=-1)  # Set device to -1 for CPU

# List of symptoms to look for
symptom_list = [
    'cough', 'fever', 'nausea', 'stomach ache', 'constipation', 'muscle pain',
    'high temperature', 'high blood pressure', 'fatigue', 'headache', 'indigestion',
    'itching', 'pain', 'swelling', 'vomiting', 'cold'
]

# Synonyms for symptoms
symptom_synonyms = {
    'high temperature': 'fever',
    'stomach ache': 'abdominal pain',
    'cold': 'common cold',
    'muscle pain': 'myalgia',
    'high blood pressure': 'hypertension',
    # Add more synonyms as needed
}

# Expanded mapping of symptoms to possible questions
symptom_questions = {
    'fever': [
        'Have you measured your temperature?',
        'Are you experiencing chills or sweating?',
        'Do you have any rash accompanying the fever?',
        'Have you taken any medication to reduce the fever?',
        'Are you experiencing night sweats?',
        'Have you traveled recently to any areas with known infections?',
        'Is the fever constant or does it come and go?',
        'Have you noticed any unusual bleeding or bruising?',
        'Are you experiencing any difficulty breathing?',
        'Do you have a sore throat or nasal congestion?',
    ],
    'nausea': [
        'Have you experienced vomiting?',
        'Does anything relieve your nausea?',
        'Have you noticed any changes in your diet?',
        'Could you be pregnant?',
        'Is the nausea worse at certain times of the day?',
        'Have you been exposed to anyone with similar symptoms?',
        'Are you experiencing dizziness along with nausea?',
        'Have you had recent exposure to toxins or spoiled food?',
        'Are you experiencing abdominal pain?',
        'Have you started any new medications?',
    ],
    'headache': [
        'Where is the headache located?',
        'Is the pain sharp, dull, or throbbing?',
        'Have you experienced any visual disturbances?',
        'Does light or sound make your headache worse?',
        'Have you had headaches like this before?',
        'Does resting improve your headache?',
        'Are you under a lot of stress recently?',
        'Have you had any head injuries?',
        'Do you feel nausea or dizziness with the headache?',
        'Have you noticed any stiffness in your neck?',
    ],
    'cough': [
        'Is your cough dry or producing mucus?',
        'What color is the mucus, if any?',
        'Are you experiencing any shortness of breath?',
        'Do you have any chest pain when coughing?',
        'Have you been exposed to dust or smoke recently?',
        'Does the cough worsen at night or after exercise?',
        'Are you experiencing a sore throat?',
        'Have you had any fever or chills?',
        'Are you wheezing or experiencing tightness in your chest?',
        'Have you recently started any new medications?',
    ],
    # Add more symptoms with additional questions
    # ...
}

# General health questions
general_questions = [
    'Have you experienced any other symptoms?',
    'Are there any factors that worsen or relieve your symptoms?',
    'Do you have any known allergies?',
    'Have you recently traveled or been exposed to new environments?',
    'Are you up to date with your vaccinations?',
    'Do you have a family history of similar symptoms?',
    'Have you recently changed any medications or supplements?',
    'Are you experiencing any stress or anxiety?',
    'How is your appetite?',
    'Are you drinking enough fluids?',
    'Have you had any recent infections or illnesses?',
    'Do you smoke or consume alcohol?',
    'Are you getting regular exercise?',
    'Have you experienced any changes in your weight?',
    'How is your sleep quality?',
]

# Functions for entity extraction remain the same as before

def normalize_symptom(symptom):
    return symptom_synonyms.get(symptom, symptom)

def extract_age(text):
    age = re.search(r'(\d{1,3})\s*(year old|years old|yo)\b', text)
    if age:
        return int(age.group(1))
    return None

def extract_gender(doc):
    genders = {'male': 'male', 'female': 'female', 'man': 'male', 'woman': 'female', 'girl': 'female', 'boy': 'male'}
    for token in doc:
        if token.text.lower() in genders:
            return genders[token.text.lower()]
    return None

def extract_duration(text):
    duration = re.search(r'(for|since)\s*(\d+)\s*(day|days|week|weeks|month|months|year|years)', text)
    if duration:
        return f"{duration.group(2)} {duration.group(3)}"
    return None

def extract_medications(doc):
    medications = []
    for ent in doc.ents:
        if ent.label_ == 'DRUG':
            medications.append(ent.text)
    return medications if medications else None

def extract_symptoms(doc):
    symptoms = []
    for token in doc:
        token_text = token.text.lower()
        if token_text in symptom_list:
            symptoms.append(normalize_symptom(token_text))
    return list(set(symptoms))  # Remove duplicates

# Function to generate dynamic questions using the LLM
def generate_llm_question(symptom, provided_params):
    prompt = f"As a medical assistant, generate a concise and relevant question to ask a patient who is experiencing {symptom}."
    # Include known parameters to avoid redundancy
    if provided_params['duration']:
        prompt += f" The symptom has been present for {provided_params['duration']}."
    if provided_params['medications']:
        prompt += f" The patient is taking {', '.join(provided_params['medications'])}."
    prompt += " Avoid repeating information already provided and focus on gathering new details."

    # Generate text using the LLM
    response = text_generator(prompt, max_length=50, num_return_sequences=1)
    generated_text = response[0]['generated_text']
    question = generated_text.strip().split('\n')[0]
    # Ensure the generated text is formatted as a question
    if not question.endswith('?'):
        question += '?'
    return question.strip()

# Main function to generate questions
def generate_questions(user_input):
    doc = nlp(user_input)

    # Extract parameters
    age = extract_age(user_input)
    gender = extract_gender(doc)
    duration = extract_duration(user_input)
    medications = extract_medications(doc)
    symptoms = extract_symptoms(doc)

    # Parameters provided in input
    provided_params = {
        'age': age,
        'gender': gender,
        'duration': duration,
        'medications': medications
    }

    # Generate questions
    questions = []

    # Avoid asking about provided parameters
    if age is None:
        questions.append('May I know your age?')
    if gender is None:
        questions.append('Can you specify your gender?')
    if duration is None:
        questions.append('How long have you been experiencing these symptoms?')
    if medications is None:
        questions.append('Are you currently taking any medications?')

    # Add symptom-specific questions
    for symptom in symptoms:
        if len(questions) >= 5:
            break
        symptom_key = normalize_symptom(symptom)
        predefined_questions = symptom_questions.get(symptom_key, [])
        for question in predefined_questions:
            if len(questions) >= 5:
                break
            if question not in questions:
                questions.append(question)

    # If more questions are needed, generate using LLMs
    if len(questions) < 5:
        for symptom in symptoms:
            if len(questions) >= 5:
                break
            llm_question = generate_llm_question(symptom, provided_params)
            if llm_question not in questions:
                questions.append(llm_question)

    # Fill up with general questions if needed
    for question in general_questions:
        if len(questions) >= 5:
            break
        if question not in questions:
            questions.append(question)

    # Limit to 5 questions
    questions = questions[:5]

    return questions

# Example usage
if __name__ == "__main__":
    user_input = input("Please describe your symptoms: ")
    questions = generate_questions(user_input)

    print("\nGenerated Questions:")
    for idx, question in enumerate(questions, 1):
        print(f"{idx}. {question}")
