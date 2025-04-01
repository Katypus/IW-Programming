import requests
import json
from bs4 import BeautifulSoup

# Read URLs from a file
with open("fox_news_articles/welfare_fox_broad.txt", "r") as f:
    urls = [line.strip() for line in f.readlines()]

data = []

for url in urls:
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract article text
        paragraphs = soup.find_all("p")
        headers = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        text = " ".join([p.get_text() for p in paragraphs]).join([h.get_text() for h in headers])

                # Extract publication date
        date = None
        meta_date = soup.find("meta", {"property": "article:published_time"})
        if meta_date:
            date = meta_date["content"]
        else:
            time_tag = soup.find("time")
            if time_tag and "datetime" in time_tag.attrs:
                date = time_tag["datetime"]
            elif time_tag:
                date = time_tag.get_text(strip=True)  # Convert to string properly

        # Ensure text & date are strings
        data.append({"url": url, "text": text, "date": str(date) if date else "Unknown"})

    except Exception as e:
        print(f"Error processing {url}: {e}")

# Save to JSON
with open("welfare_articles.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print("Scraping complete. Saved as welfare_articles.json")
