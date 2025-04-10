import pandas as pd
import nltk
import torch
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
import sys
from transformers import pipeline,  AutoModelForSequenceClassification, AutoTokenizer
from datasets import Dataset

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

model_path = "/home/kr5379/IW-Programming-1/go_emotions_model"
# Load the model and tokenizer offline
device = "cuda" # if torch.cuda.is_available() else "cpu"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Initialize pipeline with local model
emotion_analyzer = pipeline("text-classification",
                            model=model,
                            tokenizer=tokenizer,
                            top_k=None,
                            truncation=True,
                            batch_size=16,
                            device=0)
# Read json file
with open(sys.argv[1], "r") as f:
    articles = json.load(f)

# Step 1: Prepare data for the Dataset
emotion_inputs = [{"text": article["text"][:512]} for article in articles]
emotion_dataset = Dataset.from_list(emotion_inputs)
# Convert the dataset to a list of strings (the "text" column only)
emotion_inputs = [item['text'] for item in emotion_dataset]

# Step 2: Run emotion analysis efficiently
print(emotion_dataset[0])
emotion_results = emotion_analyzer(emotion_inputs, batch_size=16)

# Step 3: Combine results
data = []
for article, emotions in zip(articles, emotion_results):
    text = article["text"]
    sentiment = analyzer.polarity_scores(text)
    emotion_dict = {emo['label']: emo['score'] for emo in emotions}
    
    data.append({
        "URL": article['url'],
        "Text": text[100:500],  # Snippet
        "Sentiment Score": sentiment["compound"],
        "Date": article['date'],
        **emotion_dict
    })

# Save results
df = pd.DataFrame(data)
df.to_csv(sys.argv[1][:-5] + ".csv", index=False)
