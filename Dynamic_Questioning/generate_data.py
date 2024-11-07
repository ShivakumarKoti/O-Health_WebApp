import openai
import pandas as pd
import random
import time
from tqdm import tqdm
import os

# Initialize OpenAI API
openai.api_key = "OPEN-API-KEY"

if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

# Load symptoms from 'symptoms.csv'
def load_symptoms(filename="symptoms.csv"):
    df = pd.read_csv(filename)
    return df['SymptomName'].tolist()  # Load symptoms from the 'SymptomName' column

indian_cities = [
    "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Ahmedabad",
    "Chennai", "Kolkata", "Pune", "Jaipur", "Surat", "Lucknow",
    "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam",
    "Pimpri-Chinchwad", "Patna", "Vadodara", "Bangalore", "Bengaluru", "Mysore",
    "Goa","Sagar","Honavar","Karwar","Jammu", "Kashmir", "Shivamogga","Kerala",
    "Thiruvanathapuram","Gulbarga"
]

# Static list of common medications
medications = [
    "Ibuprofen", "Dolo 650", "Paracetamol", "Amoxicillin",
    "Vitamin C", "Antihistamines", "Aspirin", "Antacids", "Cough syrup"
]

# Gender options
genders = ["male", "female","boy","girl","man","woman"]

def generate_symptom_description(symptoms):
    symptom = random.choice(symptoms)
    description = f"I have {symptom}"
    included_info = []

    # Randomly decide to include optional info
    if random.choice([True, False]):
        duration_days = random.randint(1, 30)
        description += f" for {duration_days} days"
        included_info.append("duration")

    if random.choice([True, False]):
        age = random.randint(1, 100)
        gender = random.choice(genders)
        description += f", I am a {age}-year-old {gender}"
        included_info.append("age_gender")

    if random.choice([True, False]):
        medication = random.choice(medications)
        description += f", taking {medication}"
        included_info.append("medications")

    if random.choice([True, False]):
        location = random.choice(indian_cities)
        description += f", located in {location}"
        included_info.append("location")

    description += "."
    return description, included_info

def construct_prompt(input_text, included_info):
    prompt = (
        f"You are a compassionate and thorough medical professional. A patient has provided the following symptom description:\n\n"
        f"\"{input_text}\"\n\n"
        f"Based on this information, generate between 5 and 7 follow-up questions to ask the patient. "
    )

    # Instruct to ask about missing optional info
    optional_info_keys = ["duration", "age_gender", "medications", "location"]
    missing_info = [key for key in optional_info_keys if key not in included_info]
    if missing_info:
        prompt += (
            f"Ensure that you inquire about the following details if they are not already provided: "
            f"{', '.join(missing_info)}. "
        )

    prompt += (
        "Use diverse phrasings and question types to gather comprehensive information.\n\n"
        "Provide the questions separated by <sep>."
    )
    return prompt

def generate_followup_questions(input_text, included_info):
    prompt = construct_prompt(input_text, included_info)
    max_retries = 5
    backoff_factor = 2
    for attempt in range(max_retries):
        try:
            # Use the chat-based API call for gpt-3.5-turbo or gpt-4 models
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
                messages=[
                    {"role": "system", "content": "You are a helpful and compassionate medical professional."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200,  # Increased to allow space for 5-7 questions
                n=1,
                stop=None,
            )
            answer = response.choices[0].message['content'].strip()
            # Clean and format the answer
            questions = [q.strip() for q in answer.split("<sep>") if q.strip()]
            # Ensure there are between 5 and 7 questions
            if len(questions) < 5:
                print("Insufficient questions generated. Retrying...")
                continue
            return "<sep>".join(questions[:7])  # Return up to 7 questions
        except openai.error.RateLimitError:
            print(f"Rate limit exceeded. Retrying in {backoff_factor ** attempt} seconds...")
            time.sleep(backoff_factor ** attempt)
        except openai.error.APIError as e:
            print(f"OpenAI API error: {e}. Retrying in {backoff_factor ** attempt} seconds...")
            time.sleep(backoff_factor ** attempt)
        except Exception as e:
            print(f"Unexpected error: {e}. Retrying in {backoff_factor ** attempt} seconds...")
            time.sleep(backoff_factor ** attempt)
    print("Failed to generate follow-up questions after multiple attempts.")
    return ""

def main():
    # Load symptoms from CSV file
    symptoms = load_symptoms("symptoms.csv")

    num_entries = 1000
    data = []
    existing_inputs = set()

    print("Generating dataset...")

    for _ in tqdm(range(num_entries)):
        # Ensure unique inputs to increase diversity
        while True:
            input_text, included_info = generate_symptom_description(symptoms)
            if input_text not in existing_inputs:
                existing_inputs.add(input_text)
                break

        target = generate_followup_questions(input_text, included_info)
        data.append({"input": input_text, "target": target})

        # To respect rate limits and avoid hitting API limits
        time.sleep(1)

    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv("medical_followup_datasetnew.csv", index=False)
    print("Dataset 'medical_followup_dataset.csv' with 1,000 entries has been created successfully.")

if __name__ == "__main__":
    main()
