from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Model name
model_name = "joeddav/distilbert-base-uncased-go-emotions-student"

# Download the model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Save to disk
model.save_pretrained("go_emotions_model")
tokenizer.save_pretrained("go_emotions_model")
