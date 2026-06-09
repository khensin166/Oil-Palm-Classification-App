import io
import numpy as np
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from .model_loader import model_manager
from .utils import get_description

def process_image(image_bytes: bytes) -> np.ndarray:
    # Open image using PIL
    image = Image.open(io.BytesIO(image_bytes))
    
    # Convert to RGB if needed (e.g. PNG with alpha)
    if image.mode != "RGB":
        image = image.convert("RGB")
        
    # Resize to 224x224
    image = image.resize((224, 224))
    
    # Convert to numpy array
    img_array = np.array(image)
    
    # Expand dimensions to (1, 224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Preprocess using mobilenet_v2 preprocess_input
    img_array = preprocess_input(img_array)
    
    return img_array

def interpret_prediction(prediction_scores, class_names):
    # Buat all_predictions sesuai urutan class_names
    all_predictions = []
    for i, score in enumerate(prediction_scores):
        conf = float(score)
        all_predictions.append({
            "label": class_names[i],
            "confidence": conf,
            "confidence_percent": f"{conf * 100:.2f}%"
        })
        
    # Urutkan score dari tertinggi ke terendah
    sorted_indices = prediction_scores.argsort()[::-1]
    
    top_index = sorted_indices[0]
    top_label = class_names[top_index]
    top_confidence = float(prediction_scores[top_index])
    top_confidence_percent = f"{top_confidence * 100:.2f}%"
    description = None if top_label.lower() == "unknown" else get_description(top_label)

    # Jika model prediksi unknown
    if top_label.lower() == "unknown":
        return {
            "success": True,
            "is_valid": False,
            "prediction": "unknown",
            "confidence": top_confidence,
            "confidence_percent": top_confidence_percent,
            "message": "Gambar tidak dikenali sebagai buah sawit Dura, Pisifera, atau Tenera.",
            "description": None,
            "all_predictions": all_predictions
        }
        
    # Prediksi berhasil
    return {
        "success": True,
        "is_valid": True,
        "prediction": top_label,
        "confidence": top_confidence,
        "confidence_percent": top_confidence_percent,
        "message": "Prediksi berhasil.",
        "description": description,
        "all_predictions": all_predictions
    }

def predict_image(image_bytes: bytes):
    if not model_manager.is_loaded():
        raise Exception("Model is not loaded")
        
    # Preprocess image
    processed_img = process_image(image_bytes)
    
    # Predict
    predictions = model_manager.model.predict(processed_img)
    scores = predictions[0]
    
    # Interpret
    result = interpret_prediction(scores, model_manager.class_names)
    
    return result
