import os
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file so that sensitive information like API keys can be stored securely.
load_dotenv()

# Retrieve the API key from the environment variables. This key is used to authenticate requests to the Alpha Vantage API.
FMP_API_KEY = os.getenv("FMP_API_KEY") 


def search_ticker(company_name: str) -> str:
    """
    Find the stock ticker symbol for a given company name using Alpha Vantage's SYMBOL_SEARCH API.
    
    Parameters:
        company_name (str): The full name of the company to search for.
        
    Returns:
        str: The ticker symbol if found, otherwise an empty string or None.
    
    Process:
        1. Strip any extra whitespace from the company name.
        2. Construct the API URL with the company name as a query keyword.
        3. Send a GET request to the API.
        4. If the response is successful (status code 200), parse the JSON data.
        5. Extract the best match from the "bestMatches" list.
        6. Return the ticker symbol from the best match, which is stored under the key "1. symbol".
    """
    # Remove any leading/trailing whitespace from the input
    query = company_name.strip()
    
    # Build the API URL using the provided company name and the API key
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={FMP_API_KEY}"
    
    # Send the HTTP GET request to the API endpoint
    resp = requests.get(url)
    
    # Check if the request was successful
    if resp.status_code == 200:
        # Parse the response JSON data
        data = resp.json()
        # Retrieve the list of best matching ticker symbols
        best_matches = data.get("bestMatches", [])
        if best_matches:
            # Return the ticker symbol from the first match; it is stored under the key "1. symbol"
            return best_matches[0].get("1. symbol", "")
    
    # Return None if no ticker symbol was found or if the API call was unsuccessful
    return None


def get_company_news(query: str, limit: int = 5):
    """
    Retrieve recent news for a given company ticker or company name using Alpha Vantage's NEWS_SENTIMENT API.
    
    Parameters:
        query (str): The company ticker symbol or company name.
        limit (int, optional): The maximum number of news articles to retrieve. Defaults to 5.
        
    Returns:
        list of dict: A list where each dictionary contains the 'title' and 'summary' of a news article.
    
    Process:
        1. Convert the input query to uppercase, assuming it is a ticker symbol.
        2. If the query does not consist solely of alphabetic characters, treat it as a company name
           and use the `search_ticker` function to obtain the ticker symbol.
        3. Construct the API URL with the ticker symbol.
        4. Send a GET request to the NEWS_SENTIMENT API endpoint.
        5. If the response is unsuccessful, raise an exception with the corresponding status code.
        6. Parse the JSON response to extract the news feed.
        7. For each news item (up to the specified limit), extract the title and summary (or content if summary is missing).
        8. Return a list of dictionaries containing the news articles.
    """
    # Convert the input query to uppercase, assuming it is a ticker symbol
    ticker = query.upper()
    
    # If the ticker contains non-alphabetic characters, it might not be a valid ticker,
    # so attempt to retrieve the correct ticker symbol using the search_ticker function.
    if not ticker.isalpha():
        ticker = search_ticker(query) or query

    # Construct the API URL for retrieving news, including the ticker and API key
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={FMP_API_KEY}"
    
    # Send the HTTP GET request to the API endpoint
    resp = requests.get(url)
    
    # Raise an exception if the API request was not successful
    if resp.status_code != 200:
        raise Exception(f"News API request failed with status {resp.status_code}")
    
    # Parse the JSON response data
    news_data = resp.json()
    articles = []
    
    # Alpha Vantage returns a "feed" key containing the list of news items
    feed = news_data.get("feed", [])
    
    # Process each news item up to the specified limit
    for item in feed[:limit]:
        # Extract the title of the news item; default to an empty string if not present
        title = item.get("title", "")
        # Extract the summary, or if it's not available, use the content of the article
        summary = item.get("summary", "") or item.get("content", "")
        articles.append({"title": title, "summary": summary})
    
    # Return the list of news articles
    return articles
