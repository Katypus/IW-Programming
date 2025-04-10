from sklearn.feature_extraction.text import TfidfVectorizer
import json

# load the welfare json file
with open('welfare.json', 'r') as f:
    data = json.load(f)
# Extract the text fields
welfare_texts = []

vectorizer = TfidfVectorizer(max_df=0.9, min_df=5, ngram_range=(1, 2))
X = vectorizer.fit_transform(welfare_texts)  # or stimulus_texts
feature_names = vectorizer.get_feature_names_out()

# Get top terms
import numpy as np
top_n = 20
mean_tfidf = X.mean(axis=0).A1
top_indices = np.argsort(mean_tfidf)[-top_n:]
top_terms = [feature_names[i] for i in reversed(top_indices)]
