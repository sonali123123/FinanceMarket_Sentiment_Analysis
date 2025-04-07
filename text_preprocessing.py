import re
import string

def preprocess_text(text: str) -> str:
    """
    Clean and preprocess text by performing several operations:
    
    Operations:
      - Remove HTML tags using a regular expression.
      - Convert all characters to lowercase.
      - Remove punctuation using str.translate.
      - Remove extra whitespace (including newlines and tabs).
    
    Parameters:
        text (str): The raw input text that may contain HTML tags, punctuation, and extra whitespace.
        
    Returns:
        str: The cleaned text.
    """
    # Remove HTML tags using a regex that matches any content within angle brackets.
    no_html = re.sub(r'<[^>]+>', '', text)
    
    # Convert the text to lowercase to standardize the text.
    lower_text = no_html.lower()
    
    # Remove punctuation from the text.
    # Create a translation table that maps each punctuation character to None.
    clean_text = lower_text.translate(str.maketrans('', '', string.punctuation))
    
    # Replace multiple whitespace characters with a single space and strip leading/trailing whitespace.
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    return clean_text

def tokenize_text(text: str) -> list:
    """
    Tokenize text by splitting the cleaned text on whitespace.
    
    Parameters:
        text (str): The cleaned text to tokenize.
        
    Returns:
        list: A list of word tokens extracted from the text.
    """
    # Split the text by whitespace to create a list of tokens.
    return text.split()

def process_articles(articles: list):
    """
    Process a list of articles by cleaning and tokenizing their titles and summaries.
    
    Each article is expected to be a dictionary with keys 'title' and 'summary'. For each article:
      - Clean the title and summary using preprocess_text.
      - Tokenize the cleaned title and summary using tokenize_text.
      - Print the cleaned text and the list of tokens for both title and summary.
    
    Parameters:
        articles (list): A list of dictionaries where each dictionary represents an article with 'title' and 'summary' keys.
        
    Returns:
        None: The function prints the output and does not return a value.
    """
    # Enumerate through the list of articles, starting index at 1 for display purposes.
    for idx, article in enumerate(articles, start=1):
        # Retrieve the raw title and summary from the article dictionary.
        raw_title = article.get("title", "")
        raw_summary = article.get("summary", "")
        
        # Clean the title and summary by removing HTML tags, converting to lowercase, removing punctuation, and trimming whitespace.
        cleaned_title = preprocess_text(raw_title)
        cleaned_summary = preprocess_text(raw_summary)
        
        # Tokenize the cleaned title and summary by splitting on whitespace.
        tokens_title = tokenize_text(cleaned_title)
        tokens_summary = tokenize_text(cleaned_summary)
        
        # Print the article details in a formatted way.
        print(f"Article {idx}:")
        print("Cleaned Title:", cleaned_title)
        print("Title Tokens:", tokens_title)
        print("Cleaned Summary:", cleaned_summary)
        print("Summary Tokens:", tokens_summary)
        print("\n")  # Print an extra newline for separation between articles.
