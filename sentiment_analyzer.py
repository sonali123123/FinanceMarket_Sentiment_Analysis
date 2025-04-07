from transformers import pipeline

# Initialize the sentiment analysis pipeline using a pre-trained FinBERT model.
# This pipeline leverages the "ProsusAI/finbert" model to analyze text sentiment.

sentiment_model = pipeline(
    "sentiment-analysis", 
    model="ProsusAI/finbert"  # Using the pre-trained FinBERT model
)

def analyze_sentiment(text: str) -> dict:
    """
    Analyze the sentiment of the given text using a pre-trained FinBERT model.
    
    This function passes the provided text through a sentiment analysis pipeline that utilizes
    FinBERT. It returns a dictionary containing a sentiment label and a confidence score.
    The sentiment label is standardized to uppercase for consistency.
    
    Parameters:
        text (str): The input text (preprocessed if necessary) for which sentiment analysis is to be performed.
        
    Returns:
        dict: A dictionary with the following keys:
              - "label": A string representing the sentiment (e.g., 'POSITIVE', 'NEGATIVE', 'NEUTRAL').
              - "score": A float representing the confidence score of the sentiment prediction.
              
    Example:
        >>> result = analyze_sentiment("The market is bullish today!")
        >>> print(result)
        {'label': 'POSITIVE', 'score': 0.98}
    """
    # Obtain sentiment analysis results from the model.
    results = sentiment_model(text)
    
    # If no results are returned, default to a neutral sentiment with zero confidence.
    if not results:
        return {"label": "NEUTRAL", "score": 0.0}
    
    # Extract the first (and typically only) result from the list.
    sentiment = results[0]
    
    # Standardize the sentiment label to uppercase.
    label = sentiment["label"].upper()
    
    # Extract the confidence score from the result.
    score = sentiment["score"]
    
    # Return the sentiment analysis result as a dictionary.
    return {"label": label, "score": score}
