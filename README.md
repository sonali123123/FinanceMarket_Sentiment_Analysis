# Finance News Agent

## Overview
This project is an end-to-end solution for financial sentiment analysis. It retrieves financial news data from an API (e.g., Alpha Vantage), processes and cleans the news text, performs sentiment analysis using a pre-trained model, aggregates the results, and exposes the outcome via a REST API built with FastAPI.

## Project Structure
- **news_fetcher.py**: Retrieves financial news data using a news API.
- **text_preprocessing.py**: Cleans and preprocesses the news text.
- **sentiment_analyzer.py**: Uses a pre-trained sentiment analysis model (e.g., FinBERT) from Hugging Face to analyze sentiment.
- **aggregate_sentiments.py**: Aggregates individual sentiment results to produce an overall sentiment.
- **main.py**: Implements a REST API endpoint `/sentiment` to return sentiment analysis results.
- **requirements.txt**: Lists Python dependencies.
- **Dockerfile**: Containerizes the application.
- **README.md**: Project documentation and setup instructions.

## Setup and Installation

### Prerequisites
- Python 3.x
- Required Python packages (listed in requirements.txt)

### Installation Steps
1. Clone the repository
```bash
git clone  https://github.com/sonali123123/FinanceMarket_Sentiment_Analysis.git

```

2. Navigate to the project directory
```bash
cd FinanceMarket_Sentiment_Analysis
```

3. Create and activate a virtual environment (recommended)
```bash
python -m venv venv
```

4. Activate the virtual environment
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

5. Install dependencies
```bash
pip install -r requirements.txt
```

6. Set up environment variables
   - Create a `.env` file in the root directory
   - Add necessary API keys 

7. Run the API locally:
    ```bash
    fastapi run main.py --port 8000
    ```
    - Once the server is running, open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
    - In the Swagger UI, find the GET `/sentiment` endpoint, click on **Try it out**, and input a company ticker or name (for example, `AAPL`) in the required field.

## Docker Containerization
Build the Docker Image:
```bash
docker build -t financial-sentiment .
```

## Run the Docker Container:
```bash
docker run -d -p 8000:8000 financial-sentiment
```
The API will be available at http://localhost:8000/sentiment?company=AAPL.

## Testing the API

You can test the API endpoint using:

Browser: Navigate to http://localhost:8000/sentiment?company=AAPL

cURL:
```bash
curl "http://localhost:8000/sentiment?company=AAPL"
```

Postman: Create a GET request to the same URL.

## Assumptions & Design

Modular Design: Each component (news fetching, preprocessing, sentiment analysis, aggregation) is independent for easy updates.

API Key Management: Uses a .env file for secure configuration.

Text & Sentiment Processing: Basic cleaning and FinBERT-based sentiment analysis, extendable for more advanced NLP.

FastAPI: Provides high performance and interactive documentation.

This concise setup allows for future enhancements like advanced NLP, improved aggregation, and scalability.
