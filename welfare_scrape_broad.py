from serpapi import GoogleSearch
import itertools

# queries serpAPI for fox news articles about 'welfare', created welfare_fox_links.txt
def google_search(query, max_results=500):
    links = []
    for start in range(0, max_results, 100):
        params = {
            "q": query,
            "num": 100,
            "start": start,
            "api_key": "4ceb3ea41d4b4aedc75aed5b6eabeeb7fed55bee9bec5630e287430b03d81b46"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        page = [r["link"] for r in results.get("organic_results", [])] #if "foxnews.com" in r["link"]]
        links.append(page)
    return links

# Run search
# edit search to find articles from foxnews
query = "site:foxnews.com inurl:news (\"Social Security\" OR \"disability benefits\" OR \"unemployment benefits\" OR \"welfare\") -inurl:video"

fox_news_links = google_search(query, max_results=500)

# Flatten the list of lists into a single list
fox_news_links = list(itertools.chain.from_iterable(fox_news_links))

print("\n".join(fox_news_links))
