from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import uvicorn

from news_fetcher import get_company_news
from text_preprocessing import preprocess_text
from sentiment_analyzer import analyze_sentiment
from aggregate_sentiments import aggregate_sentiments

app = FastAPI(
    title="Financial Sentiment Analysis API",
    description="Retrieves financial news, processes it, and returns aggregated sentiment analysis.",
    version="1.0.0"
)

@app.get("/sentiment")
async def get_sentiment(company: str = Query(..., description="Company ticker or name to analyze")):
    try:
        # Retrieve news articles for the given company
        articles = get_company_news(company)
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found for the given company")
        
        sentiments = []
        processed_articles = []
        for article in articles:
            # Prefer using the article's summary; fallback to title if necessary
            raw_text = article.get("summary") or article.get("title")
            if not raw_text:
                continue

            # Preprocess the text (e.g., remove HTML tags, punctuation, and convert to lowercase)
            cleaned_text = preprocess_text(raw_text)
            # Analyze the sentiment using your FinBERT-based analyzer
            sentiment_result = analyze_sentiment(cleaned_text)
            
            sentiments.append(sentiment_result)
            processed_articles.append({
                "title": article.get("title", ""),
                "cleaned_text": cleaned_text,
                "sentiment": sentiment_result
            })
        
        # Aggregate the individual sentiments into an overall sentiment
        overall_sentiment = aggregate_sentiments(sentiments)
        
        return JSONResponse(content={
            "company": company,
            "overall_sentiment": overall_sentiment,
            "articles": processed_articles
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
