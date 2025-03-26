import requests
import time
import os

SERPAPI_KEY = "4ceb3ea41d4b4aedc75aed5b6eabeeb7fed55bee9bec5630e287430b03d81b46"
# Function to search Fox News articles with pagination
def search_fox_news_covid_stimulus(max_results=500):
    query = 'COVID stimulus checks site:foxnews.com'
    articles = []

    for start in range(0, max_results, 100):  # Paginate in chunks of 100
        params = {
            "engine": "google",
            "q": query,
            "num": 100,  # Max results per request
            "start": start,  # Pagination offset
            "api_key": SERPAPI_KEY
        }

        response = requests.get("https://serpapi.com/search", params=params)

        if response.status_code == 200:
            news_results = response.json().get("news_results", [])
            if not news_results:
                break  # Stop if no more results

            articles.extend(news_results)
            print(f"Fetched {len(news_results)} articles from offset {start}")

        time.sleep(2)  # Pause to avoid rate limits

    return articles

# Ensure output directory exists
output_dir = "fox_news_articles"
os.makedirs(output_dir, exist_ok=True)

print("Fetching Fox News articles about COVID stimulus checks...")

articles = search_fox_news_covid_stimulus(max_results=500)

# Define file name
filename = os.path.join(output_dir, "fox_news_covid_stimulus.txt")

# Save articles to a text file
with open(filename, "w", encoding="utf-8") as f:
    for article in articles:
        link = article.get("link", "No Link")
        f.write(f"{link}\n")

print(f"Saved {len(articles)} articles to {filename}")
