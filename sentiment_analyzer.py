from transformers import pipeline

# Initialize the sentiment analysis pipeline using FinBERT (or another suitable pre-trained model)
sentiment_model = pipeline(
    "sentiment-analysis", 
    model="ProsusAI/finbert"  # You can change this model if needed
)

def analyze_sentiment(text: str) -> dict:
    """
    Analyze the sentiment of the provided preprocessed text using FinBERT.
    Returns a dictionary with a sentiment label and a confidence score.
    """
    results = sentiment_model(text)
    if not results:
        return {"label": "NEUTRAL", "score": 0.0}
    
    sentiment = results[0]
    label = sentiment["label"].upper()  # Ensure consistency in label formatting
    score = sentiment["score"]
    return {"label": label, "score": score}

if __name__ == "__main__":
    # Example texts for sentiment analysis
    texts = [
        "this is a positive sentiment text example",
        "this is a negative sentiment example with some issues",
        "neutral tone text with neither strong sentiment"
    ]
    
    for idx, text in enumerate(texts, start=1):
        sentiment = analyze_sentiment(text)
        print(f"Text {idx} Sentiment: {sentiment}")
