import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variable
FMP_API_KEY = os.getenv("FMP_API_KEY") 

def search_ticker(company_name: str) -> str:
    """
    Find the stock ticker symbol for a given company name using Alpha Vantage's SYMBOL_SEARCH API.
    """
    query = company_name.strip()
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={FMP_API_KEY}"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        best_matches = data.get("bestMatches", [])
        if best_matches:
            # The symbol is stored under the key "1. symbol"
            return best_matches[0].get("1. symbol", "")
    return None

def get_company_news(query: str, limit: int = 5):
    """
    Retrieve recent news for a given company ticker or name using Alpha Vantage's NEWS_SENTIMENT API.
    Returns a list of dictionaries with 'title' and 'summary' keys.
    """
    # Assume the input is a ticker symbol in uppercase; if not, search for the ticker
    ticker = query.upper()
    if not ticker.isalpha():
        ticker = search_ticker(query) or query

    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={FMP_API_KEY}"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f"News API request failed with status {resp.status_code}")
    
    news_data = resp.json()
    articles = []
    # Alpha Vantage returns a "feed" key containing the list of news items
    feed = news_data.get("feed", [])
    for item in feed[:limit]:
        title = item.get("title", "")
        summary = item.get("summary", "") or item.get("content", "")
        articles.append({"title": title, "summary": summary})
    return articles

if __name__ == "__main__":
    # Demo run for the company ticker "AAPL"
    company = "AAPL"
    print(f"Fetching news for company: {company}")
    
    try:
        articles = get_company_news(company)
        if articles:
            print(f"Retrieved {len(articles)} articles for {company}:")
            for idx, article in enumerate(articles, start=1):
                print(f"\nArticle {idx}:")
                print(f"Title: {article['title']}")
                print(f"Summary: {article['summary']}")
        else:
            print("No articles found for the given company.")
    except Exception as e:
        print(f"Error occurred: {e}")
