import requests
import pandas as pd
import nltk
import torch

from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Read URLs from file
with open("fox_news_articles/covid_fox_links.txt", "r") as f:
    urls = [line.strip() for line in f.readlines()]

data = []

for url in urls:
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        # Load the emotion analysis model
        emotion_analyzer = pipeline("text-classification", model="joeddav/distilbert-base-uncased-go-emotions-student", top_k=None)
        # Extract article text
        paragraphs = soup.find_all("p")
        headers = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        text = " ".join([p.get_text() for p in paragraphs]).join([h.get_text() for h in headers])
        date = soup.find("time")
        if not text:
            print(f"No text found for URL: {url}")
            continue  # Skip if no text is found
        
        # Perform sentiment analysis
        sentiment = analyzer.polarity_scores(text)
        # Perform emotion classification
        emotions = emotion_analyzer(text[:512])  # Truncate to 512 tokens

        # Convert emotions into a dictionary
        emotion_dict = {emo['label']: emo['score'] for emo in emotions[0]}

        # Store relevant emotions
        data.append({
            "URL": url,
            "Text": text[:500],  # Store a snippet
            "Sentiment Score": sentiment["compound"],
            "Date": date,
            **emotion_dict  # Expands emotion labels as separate columns
        })
    
    except Exception as e:
        print(f"Error processing {url}: {e}")

# Save results
df = pd.DataFrame(data)
df.to_csv("covid_sentanal.csv", index=False)
