'''
Cleans up unnecessary text from Fox News articles that were scraped by BeautifulSoup.
'''
import re
import sys
import json
junk_phrases = [
    "Legal Statement. Mutual Fund and ETF data provided by"
]

# Remove lines that contain junk phrases
def remove_junk_lines(text):
    lines = text.splitlines()
    clean_lines = [
        line for line in lines
        if not any(phrase.lower() in line.lower() for phrase in junk_phrases)
    ]
    return "\n".join(clean_lines).strip()

# Remove duplicate paragraphs
def remove_duplicate_paragraphs(text):
    paragraphs = text.split("\n")
    seen = set()
    unique_paragraphs = []
    for para in paragraphs:
        stripped = para.strip()
        if stripped and stripped not in seen:
            unique_paragraphs.append(stripped)
            seen.add(stripped)
    return "\n".join(unique_paragraphs)

# clean function
def fully_clean(text):
    text = remove_junk_lines(text)
    text = remove_duplicate_paragraphs(text)
    return text

# open JSON
with open(sys.argv[1], 'r', encoding='utf-8', errors='ignore') as f:
    data = json.load(f)

# clean each text field
for article in data:
    if "text" in article:
        article["text"] = fully_clean(article["text"])
# save as json
with open(sys.argv[1][:-5] + "_cleaned.json", 'w') as f:
    json.dump(data, f, indent=4)
print(f"Cleaned {len(data)} articles and saved to {sys.argv[1][:-5]}_cleaned.json")
