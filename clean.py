'''
Cleans up unnecessary text from Fox News articles that were scraped by BeautifulSoup.
'''
import re
import sys
import json
junk_phrases = [
    "Fox News Flash headlines",
    "Get the Fox News app",
    "This material may not be published",
    "© 20",  # catches things like "© 2020 Fox News"
]

def remove_junk_lines(text):
    lines = text.splitlines()
    clean_lines = [
        line for line in lines
        if not any(phrase.lower() in line.lower() for phrase in junk_phrases)
    ]
    return "\n".join(clean_lines).strip()

def clean_article(text):
    # Remove everything before the main body (Main body begins after "Check out what's clicking on Foxnews.com")
    text = re.sub(r"^.*?(Check out what's clicking on Foxnews.com\s+[\w\d ,:]+)?", "", text, flags=re.DOTALL)

    # Remove footers/copyrights/menu junk
    text = re.sub(r"(©|\(c\)|Copyright).*", "", text, flags=re.IGNORECASE)

    return text.strip()

def fully_clean(text):
    text = clean_article(text)
    text = remove_junk_lines(text)
    return text

with open(sys.argv[1], 'r', encoding='utf-8', errors='ignore') as f:
    data = json.load(f)
cleaned = [fully_clean(article["text"]) for article in data if "text" in article]
json_cleaned = json.dumps(cleaned, indent=4)
with open(sys.argv[1][:-5] + "_cleaned.json", 'w') as f:
    f.write(json_cleaned)
print(f"Cleaned {len(data)} articles and saved to {sys.argv[1][:-5]}_cleaned.json")
