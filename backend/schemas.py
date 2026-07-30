from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    image: str = Field(..., description="Base64 data URL of the drawn digit (PNG)")


class PredictResponse(BaseModel):
    digit: int
    confidence: float
