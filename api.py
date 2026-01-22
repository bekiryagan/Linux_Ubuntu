from fastapi import FastAPI, HTTPException, Query
from textblob import TextBlob
import uvicorn
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sentiment Analysis API", version="1.0.0")

# User database with permissions
users = {
    "alice": {"password": "wonderland", "permissions": ["v1", "v2"]},
    "bob": {"password": "builder", "permissions": ["v1"]}
}

def authenticate(username: str, password: str) -> bool:
    """Authenticate a user"""
    if username in users and users[username]["password"] == password:
        return True
    return False

def authorize(username: str, version: str) -> bool:
    """Check if user has permission for the given API version"""
    if username in users:
        return version in users[username]["permissions"]
    return False

def analyze_sentiment(sentence: str) -> dict:
    """Analyze the sentiment of a sentence"""
    blob = TextBlob(sentence)
    polarity = blob.sentiment.polarity
    
    if polarity > 0:
        sentiment = "positive"
    elif polarity < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return {
        "sentence": sentence,
        "sentiment": sentiment,
        "polarity": polarity
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {"status": "healthy"}

@app.get("/permissions")
def get_permissions(username: str = Query(...), password: str = Query(...)):
    """Get user permissions"""
    if not authenticate(username, password):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    
    return {
        "username": username,
        "permissions": users[username]["permissions"]
    }

@app.get("/v1/sentiment")
def sentiment_v1(
    username: str = Query(...),
    password: str = Query(...),
    sentence: str = Query(...)
):
    """Sentiment analysis API v1"""
    if not authenticate(username, password):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    
    if not authorize(username, "v1"):
        raise HTTPException(status_code=403, detail="Not authorized for v1")
    
    return analyze_sentiment(sentence)

@app.get("/v2/sentiment")
def sentiment_v2(
    username: str = Query(...),
    password: str = Query(...),
    sentence: str = Query(...)
):
    """Sentiment analysis API v2 (premium)"""
    if not authenticate(username, password):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    
    if not authorize(username, "v2"):
        raise HTTPException(status_code=403, detail="Not authorized for v2")
    
    return analyze_sentiment(sentence)

if __name__ == "__main__":
    logger.info("Starting the Sentiment Analysis API")
    uvicorn.run(app, host="0.0.0.0", port=8000)
