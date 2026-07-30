from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from inference import InvalidImageError, get_model, predict_digit, preprocess_image
from schemas import PredictRequest, PredictResponse


@asynccontextmanager
async def lifespan(_app: FastAPI):
    get_model()  # load once at startup instead of on the first request
    yield


app = FastAPI(title="Handwritten Digit Recognition API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    try:
        image_array = preprocess_image(request.image)
    except InvalidImageError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    digit, confidence = predict_digit(image_array)
    return PredictResponse(digit=digit, confidence=confidence)
