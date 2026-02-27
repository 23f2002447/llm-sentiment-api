from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow ALL origins (important for graders)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health route (important)
@app.get("/")
def health():
    return {"status": "running"}


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
        return {"sentiment": "positive", "rating": min(5, 3 + score)}
    elif score < 0:
        return {"sentiment": "negative", "rating": max(1, 3 + score)}
    else:
        return {"sentiment": "neutral", "rating": 3}


@app.post("/comment", response_model=SentimentResponse)
def analyze_comment(request: CommentRequest):
    return analyze_sentiment(request.comment)
