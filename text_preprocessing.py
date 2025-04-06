import re
import string

def preprocess_text(text: str) -> str:
    """
    Clean and preprocess text:
      - Remove HTML tags
      - Convert to lowercase
      - Remove punctuation
      - Remove extra whitespace
    """
    # Remove HTML tags using a simple regex
    no_html = re.sub(r'<[^>]+>', '', text)
    # Convert to lowercase
    lower_text = no_html.lower()
    # Remove punctuation using str.translate
    clean_text = lower_text.translate(str.maketrans('', '', string.punctuation))
    # Remove extra whitespace
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text

def tokenize_text(text: str) -> list:
    """
    Tokenize text by splitting on whitespace.
    """
    return text.split()

def process_articles(articles: list):
    """
    For each article (a dict with keys 'title' and 'summary'),
    clean the text and print the cleaned text and tokens.
    """
    for idx, article in enumerate(articles, start=1):
        raw_title = article.get("title", "")
        raw_summary = article.get("summary", "")
        
        cleaned_title = preprocess_text(raw_title)
        cleaned_summary = preprocess_text(raw_summary)
        
        tokens_title = tokenize_text(cleaned_title)
        tokens_summary = tokenize_text(cleaned_summary)
        
        print(f"Article {idx}:")
        print("Cleaned Title:", cleaned_title)
        print("Title Tokens:", tokens_title)
        print("Cleaned Summary:", cleaned_summary)
        print("Summary Tokens:", tokens_summary)
        print("\n")

if __name__ == "__main__":
    # Example usage with sample articles
    articles = [
        {
            "title": "Example Title One <b>HTML</b>",
            "summary": "This is the first example summary! It includes punctuation, HTML, and more."
        },
        {
            "title": "Example Title Two",
            "summary": "Another example summary; testing text preprocessing: remove, clean and tokenize."
        }
    ]
    
    process_articles(articles)
