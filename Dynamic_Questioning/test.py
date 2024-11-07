import re
import argparse
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Load the fine-tuned model and tokenizer
model_dir = "./fine_tuned_question_generatorlarge"
tokenizer = T5Tokenizer.from_pretrained(model_dir)
model = T5ForConditionalGeneration.from_pretrained(model_dir)

def extract_parameters(input_text):
    # Extract common parameters: duration, age, gender, medications taken, location
    duration = re.search(r"\b(\d+ (day|days|week|weeks|month|months|year|years))\b", input_text)
    age = re.search(r"\b(\d{1,3})-year-old\b", input_text)
    gender = re.search(r"\b(male|female|other)\b", input_text, re.IGNORECASE)
    medication = re.search(r"\btaking ([a-zA-Z0-9\s]+)\b", input_text)
    location = re.search(r"\blocated in ([a-zA-Z\s]+)\b", input_text)

    extracted_info = {
        "duration": bool(duration),
        "age": bool(age),
        "gender": bool(gender),
        "medication": bool(medication),
        "location": bool(location)
    }

    return extracted_info

def generate_questions(input_text, model, tokenizer, min_questions=5, max_questions=7):
    # Extract parameters from input
    extracted_info = extract_parameters(input_text)

    # Prepare prompt for missing parameters only
    prompt = "Generate follow-up questions based on the symptom description: " + input_text + ". "
    missing_info = [key for key, value in extracted_info.items() if not value]
    if missing_info:
        prompt += f"Ensure that you inquire about the following details if they are not already provided: {', '.join(missing_info)}. "

    prompt += "Use diverse phrasings and question types to gather comprehensive information."

    # Prepare the input for the model
    inputs = tokenizer.encode(prompt, return_tensors="pt", truncation=True)

    # Generate output with sampling for variability
    outputs = model.generate(
        inputs,
        max_length=200,
        num_return_sequences=1,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.9
    )

    # Decode and split questions
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    questions = [q.strip() for q in generated_text.split("<sep>") if q.strip()]

    # Relaxed validation for valid questions
    valid_questions = []
    for question in questions:
        # Ensure the question ends with a "?" and has a reasonable length
        if question.endswith('?') and len(question) > 5:
            valid_questions.append(question)

    # Limit to a maximum of 7 valid questions
    return valid_questions[:max_questions] if len(valid_questions) >= min_questions else valid_questions

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Generate follow-up questions based on symptom description.')
    parser.add_argument('--input', type=str, required=True, help='Symptom description input text.')
    args = parser.parse_args()

    # Use the provided input symptom description
    input_symptom = args.input

    # Generate questions
    generated_questions = generate_questions(input_symptom, model, tokenizer)
    print("Generated Questions:")
    if generated_questions:
        for idx, question in enumerate(generated_questions, 1):
            print(f"{idx}. {question}")
    else:
        print("No valid questions were generated.")
