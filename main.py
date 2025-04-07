from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import uvicorn

# Import utility functions for retrieving news, preprocessing text, analyzing sentiment, and aggregating sentiments.
from news_fetcher import get_company_news
from text_preprocessing import preprocess_text
from sentiment_analyzer import analyze_sentiment
from aggregate_sentiments import aggregate_sentiments

# Create and configure the FastAPI application with descriptive metadata.
app = FastAPI(
    title="Financial Sentiment Analysis API",
    description="Retrieves financial news, processes it, and returns aggregated sentiment analysis.",
    version="1.0.0"
)

@app.get("/sentiment")
async def get_sentiment(company: str = Query(..., description="Company ticker or name to analyze")):
    """
    Analyze the overall financial sentiment for a specified company.
    
    This endpoint performs the following steps:
      1. Retrieves news articles related to the provided company (ticker or name).
      2. For each article, it selects the summary (or title if the summary is missing), cleans the text,
         and analyzes its sentiment using a FinBERT-based model.
      3. Aggregates the sentiments from all articles to compute an overall sentiment.
    
    Query Parameters:
        company (str): The company ticker or name to analyze.
    
    Returns:
        JSONResponse: A JSON object containing:
            - "company": The provided company ticker or name.
            - "overall_sentiment": The aggregated sentiment result (label and confidence).
            - "articles": A list of processed articles with their original title, cleaned text, and sentiment result.
    
    Raises:
        HTTPException: 404 error if no articles are found for the specified company.
        HTTPException: 500 error if any exception occurs during processing.
    """
    try:
        # Retrieve news articles for the given company using the get_company_news function.
        articles = get_company_news(company)
        if not articles:
            # If no articles are found, raise a 404 error.
            raise HTTPException(status_code=404, detail="No articles found for the given company")
        
        sentiments = []          # List to store individual sentiment analysis results.
        processed_articles = []  # List to store processed article details.
        
        # Process each article from the retrieved articles.
        for article in articles:
            # Use the article's summary if available; otherwise, fallback to the title.
            raw_text = article.get("summary") or article.get("title")
            # If there is no text available, skip this article.
            if not raw_text:
                continue

            # Preprocess the text: remove HTML tags, punctuation, extra whitespace, and convert to lowercase.
            cleaned_text = preprocess_text(raw_text)
            # Analyze the sentiment of the cleaned text using the FinBERT-based sentiment analyzer.
            sentiment_result = analyze_sentiment(cleaned_text)
            
            # Append the sentiment result for aggregation.
            sentiments.append(sentiment_result)
            # Save the processed article details.
            processed_articles.append({
                "title": article.get("title", ""),
                "cleaned_text": cleaned_text,
                "sentiment": sentiment_result
            })
        
        # Aggregate individual sentiment results to derive an overall sentiment.
        overall_sentiment = aggregate_sentiments(sentiments)
        
        # Return the aggregated results in a JSON response.
        return JSONResponse(content={
            "company": company,
            "overall_sentiment": overall_sentiment,
            "articles": processed_articles
        })
    except Exception as e:
        # If any error occurs during processing, return a 500 error with the error message.
        raise HTTPException(status_code=500, detail=str(e))

# Entry point: Run the FastAPI application using uvicorn when executed as the main module.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
