from transformers import T5ForConditionalGeneration, T5Tokenizer, Trainer, TrainingArguments
import torch
from sklearn.model_selection import train_test_split
import pandas as pd

# Load and prepare the data
data = pd.read_csv("medical_followup_dataset.csv")
data = data[['input', 'target']]
data['input'] = "Generate follow-up questions: " + data['input']
data['target'] = data['target'].str.replace("<br>", "<sep>", regex=False)

# Split the data
train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)

# Load T5 model and tokenizer
model_name = "t5-large"  # Use 't5-base' for a small model, 't5-small' smaller model
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Tokenize data
def preprocess_data(data, tokenizer, max_input_length=128, max_target_length=128):
    inputs = data["input"].tolist()
    targets = data["target"].tolist()

    model_inputs = tokenizer(inputs, max_length=max_input_length, padding="max_length", truncation=True, return_tensors="pt")
    labels = tokenizer(targets, max_length=max_target_length, padding="max_length", truncation=True, return_tensors="pt").input_ids
    labels[labels == tokenizer.pad_token_id] = -100
    model_inputs["labels"] = labels

    return model_inputs

train_encodings = preprocess_data(train_data, tokenizer)
val_encodings = preprocess_data(val_data, tokenizer)

# Dataset class
class FollowUpDataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

    def __len__(self):
        return len(self.encodings["input_ids"])

train_dataset = FollowUpDataset(train_encodings)
val_dataset = FollowUpDataset(val_encodings)

# Training arguments
training_args = TrainingArguments(
    output_dir="./question_generator_modellarge",
    evaluation_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=5,  # Increase the number of epochs for better learning
    weight_decay=0.01,
    save_total_limit=1,
    logging_dir="./logs"
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

# Train the model
trainer.train()

# Save the model and tokenizer
model.save_pretrained("./fine_tuned_question_generatorlarge")
tokenizer.save_pretrained("./fine_tuned_question_generatorlarge")
