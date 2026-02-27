from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommentRequest(BaseModel):
    comment: str

class SentimentResponse(BaseModel):
    sentiment: str
    rating: int


def analyze_sentiment(text: str):
    text = text.lower()

    positive_words = ["amazing", "great", "excellent", "love", "fantastic", "awesome", "good"]
    negative_words = ["bad", "worst", "terrible", "hate", "awful", "poor", "useless"]

    score = 0

    for word in positive_words:
        if word in text:
            score += 1

    for word in negative_words:
        if word in text:
            score -= 1

    if score > 0:
        sentiment = "positive"
        rating = min(5, 3 + score)
    elif score < 0:
        sentiment = "negative"
        rating = max(1, 3 + score)
    else:
        sentiment = "neutral"
        rating = 3

    return {"sentiment": sentiment, "rating": rating}

@app.get("/")
def health():
    return {"status": "running"}

@app.post("/comment", response_model=SentimentResponse)
async def analyze_comment(request: CommentRequest):
    try:
        return analyze_sentiment(request.comment)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
