import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .schemas import PredictionResponse, HealthResponse
from .model_loader import model_manager
from .predictor import predict_image

load_dotenv()

app = FastAPI(title="Palm Fruit Classification API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model on startup
@app.on_event("startup")
async def startup_event():
    model_path = os.getenv("MODEL_PATH", "models/model_mobilenetv2_sawit_inference.keras")
    class_names_path = os.getenv("CLASS_NAMES_PATH", "models/class_names.json")
    model_manager.load_model_and_classes(model_path, class_names_path)

@app.get("/")
def root():
    return {"message": "Palm Fruit Classification API is running"}

@app.get("/health", response_model=HealthResponse)
def health_check():
    return {
        "status": "ok",
        "model_loaded": model_manager.is_loaded()
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(image: UploadFile = File(...)):
    if not image.content_type.startswith("image/"):
        return JSONResponse(
            status_code=400,
            content={"success": False, "is_valid": False, "message": "Invalid image file"}
        )
        
    try:
        # Read image bytes
        image_bytes = await image.read()
        
        # Predict & validate
        result = predict_image(image_bytes)
        
        return PredictionResponse(**result)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "is_valid": False, "message": f"Error processing image: {str(e)}"}
        )
