from sklearn.feature_extraction.text import TfidfVectorizer
import json
import numpy as np
import pandas as pd

# load the covid json file
# FOR COVID
# with open('covid_articles_cleaned.json', 'r') as f:
#     data = json.load(f)
# Extract the text fields
# texts = [article["text"] for article in data if "text" in article]

# FOR WELFARE
with open('welfare-1_cleaned.json', 'r') as f:
    data1 = json.load(f)
with open('welfare-2_cleaned.json', 'r') as f:
    data2 = json.load(f)
# Extract the text fields
texts1 = [article["text"] for article in data1 if "text" in article]
texts2 = [article["text"] for article in data2 if "text" in article]
texts = texts1 + texts2

vectorizer = TfidfVectorizer(max_df=0.9, min_df=5, ngram_range=(1, 2))
X = vectorizer.fit_transform(texts)  # or stimulus_texts
feature_names = vectorizer.get_feature_names_out()

frequencies = X.toarray().sum(axis=0)  # total frequency for each term
freq_dict = dict(zip(feature_names, frequencies))
# sort + get top N
top_n = 200
sorted_terms = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)[:top_n]
df = pd.DataFrame(sorted_terms, columns=["term", "frequency"])
df.to_csv("welfare_term_frequencies.csv", index=False)