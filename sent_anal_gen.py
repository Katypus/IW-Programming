import pandas as pd
import nltk
import torch
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
import sys
from transformers import pipeline,  AutoModelForSequenceClassification, AutoTokenizer

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

model_path = "/home/kr5379/IW-Programming-1/go_emotions_model"
# Load the model and tokenizer offline
device = "cuda" # if torch.cuda.is_available() else "cpu"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Initialize pipeline with local model
# if not torch.cuda.is_available():
#     raise RuntimeError("CUDA is not available! Check your Slurm job.")
emotion_analyzer = pipeline("text-classification", model=model, tokenizer=tokenizer, device=0, top_k=None)
# Read json file
with open(sys.argv[1], "r") as f:
    articles = json.load(f)

data = []

for article in articles:
    try:
        # Load the emotion analysis model
        emotion_analyzer = pipeline("text-classification", model="joeddav/distilbert-base-uncased-go-emotions-student", top_k=None)
        # get text from the json file
        text = article['text']
        # Perform sentiment analysis
        sentiment = analyzer.polarity_scores(text)
        # Perform emotion classification
        emotions = emotion_analyzer(text[:512])  # Truncate to 512 tokens
        # Convert emotions into a dictionary
        emotion_dict = {emo['label']: emo['score'] for emo in emotions[0]}
        # Store relevant emotions
        data.append({
            "URL": article['url'],
            "Text": text[100:500],  # Store a snippet
            "Sentiment Score": sentiment["compound"],
            "Date": article['date'],
            **emotion_dict  # Expands emotion labels as separate columns
        })
    
    except Exception as e:
        print(f"Error processing {article['url']}: {e}")

# Save results
df = pd.DataFrame(data)
df.to_csv(sys.argv[1][:-5] + ".csv", index=False)
