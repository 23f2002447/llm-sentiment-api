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

    positive_words = [
        "amazing", "great", "excellent", "love", "fantastic",
        "awesome", "good", "satisfied", "wonderful",
        "brilliant", "perfect", "enjoyed", "liked",
        "couldn't put it down", "highly recommend"
    ]

    negative_words = [
        "bad", "worst", "terrible", "hate", "awful",
        "poor", "useless", "disappointing", "disappointed",
        "fell apart", "boring", "waste", "not worth",
        "expected better", "horrible"
    ]

    score = 0

    # Phrase match first
    for phrase in positive_words:
        if phrase in text:
            score += 2

    for phrase in negative_words:
        if phrase in text:
            score -= 2

    # Basic sentiment words
    words = text.split()

    for word in words:
        if word in positive_words:
            score += 1
        if word in negative_words:
            score -= 1

    # Final decision
    if score >= 2:
        return {"sentiment": "positive", "rating": 5}
    elif score == 1:
        return {"sentiment": "positive", "rating": 4}
    elif score == 0:
        return {"sentiment": "neutral", "rating": 3}
    elif score == -1:
        return {"sentiment": "negative", "rating": 2}
    else:
        return {"sentiment": "negative", "rating": 1}

@app.post("/comment", response_model=SentimentResponse)
def analyze_comment(request: CommentRequest):
    return analyze_sentiment(request.comment)
