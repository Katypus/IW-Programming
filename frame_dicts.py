import re
from collections import Counter
import json
import sys
import pandas as pd

frame_dict = {
    "democratic party":[
        "biden", "democrats", "democratic", "pelosi",
        "obama", "clinton", "hillary", "senate",
        "congress", "the left", "progressive","medicare"
    ],
    "republican party":[
    "trump", "republicans", "republican", "mcconnell",
    "conservative", "gop", "right-wing",
    "congress", "the right", "conservatives",
    "musk", "doge", "elon", "maga",
    "reagan", "libertarian", "libertarians",
    "liberty", "liberties", "libertarianism",
    "tesla"
    ],
    "undeserving":[
        "unemployment", "welfare", "welfare queen",
        "welfare queens", "welfare state", "welfare states",
        "welfare dependency", "welfare dependents",
        "fraud","illegal", "immigrants",
        "crime", "border", "mexico", "mexican",
        "report", "immigration", "illegals",
        "criminal", "criminals", "criminality",
        "murder","lazy", "laziness", "lazy people",
        "lazy people", "entitlement", "entitlements",
        "entitled", "entitlement programs", "moral",
        "irresponsible"
    ],
    "economics":[
        "economy", "economic", "inflation",
        "interest", "interest rates", "interest rate",
        "debt", "deficit", "taxes",
        "tax", "taxpayer", "taxpayers",
        "spending", "spend", "spending cuts",
        "spending cut", "budget", "budgets",
        "financial", "finance", "trade","money",
        "market", "markets", "stock", "check","checks",
        "stimulus", "relief", "payments", "package",
        "stimulus package", "stimulus payments",
        "stimulus check", "stimulus checks", "trillion",
        "billion", "business", "businesses",
        "corporation", "corporations", "corporate",
        "aid", "direct", "irs", "benefits"
    ],
    "security":[
        "police", "security", "ice", "border patrol",
        "national guard", "military", "army",
        "navy", "air force", "armed forces",
        "law enforcement", "law enforcement agencies",
        "law","laws", "legal", "military", "found"
    ],

}

# makes all text lowercase and removes punctuation
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

# counts the number of times each frame appears in text
def detect_frames(text, frame_dict):
    counts = Counter()
    total_words = len(text.split())
    for frame, keywords in frame_dict.items():
        for keyword in keywords:
            # You can match whole words only
            if re.search(rf'\b{re.escape(keyword)}\b', text):
                counts[frame] += len(re.findall(rf'\b{re.escape(keyword)}\b', text))/total_words
    return counts

results = []

with open(sys.argv[1], 'r', encoding='utf-8', errors='ignore') as f:
    articles = json.load(f)
for article in articles:
    text = preprocess(article['text'])
    frame_counts = detect_frames(text, frame_dict)
    results.append({
        "URL" : article['url'],
        "frame_counts": frame_counts
    })
# Convert the results to a flat structure suitable for CSV
df = pd.DataFrame([
    {
        "URL": r["URL"],
        **r["frame_counts"]
    } for r in results
])
# save to csv
df.to_csv(sys.argv[1][:-5] + "_frames.csv", index=False)