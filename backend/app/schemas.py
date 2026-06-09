from pydantic import BaseModel
from typing import List

class PredictionScore(BaseModel):
    label: str
    confidence: float
    confidence_percent: str

class PredictionResponse(BaseModel):
    success: bool
    is_valid: bool
    prediction: str | None = None
    confidence: float | None = None
    confidence_percent: str | None = None
    description: str | None = None
    all_predictions: List[PredictionScore] | None = None
    message: str | None = None

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
