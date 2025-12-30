"""
FastAPI Backend for Smart Garbage Segregation System
Final Assignment - Academic Project

This application provides a web-based interface for waste classification
using a pre-trained deep learning model. It simulates servo motor behavior
to determine which bin (Recyclable/Other) the waste should go to.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import io
import os
from utils import load_model, preprocess, LABELS, classify_recyclable

# Initialize FastAPI app
app = FastAPI(
    title="Smart Garbage Segregation System",
    description="AI-powered waste classification with servo motor simulation",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global model variable (loaded once at startup)
model = None


@app.on_event("startup")
async def load_model_on_startup():
    """
    Load the trained model once when the application starts.
    This avoids reloading the model on every request.
    """
    global model
    try:
        # Get absolute path to model file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, 'weights', 'modelnew.h5')
        model_path = os.path.abspath(model_path)
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")
        
        print(f"Loading model from: {model_path}")
        model = load_model(model_path)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Serve the main HTML page.
    """
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Error: index.html not found</h1>",
            status_code=404
        )


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict waste class from uploaded image.
    
    Args:
        file: Uploaded image file
        
    Returns:
        JSON response with prediction results:
        {
            "predicted_class": str,
            "confidence": float,
            "bin": str,
            "servo_angle": int
        }
    """
    # Check if model is loaded
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Read uploaded file
        contents = await file.read()
        
        # Open image with PIL
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if necessary (handle RGBA, L, etc.)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Preprocess image
        processed_image = preprocess(image)
        
        # Add batch dimension
        image_batch = np.expand_dims(processed_image, axis=0)
        
        # Make prediction
        predictions = model.predict(image_batch, verbose=0)
        
        # Get predicted class index
        predicted_index = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))
        
        # Get class name from hardcoded labels
        predicted_class = LABELS[predicted_index]
        
        # Determine bin type and servo angle
        bin_type, servo_angle = classify_recyclable(predicted_class)
        
        # Return JSON response
        return JSONResponse(content={
            "predicted_class": predicted_class,
            "confidence": confidence,
            "bin": bin_type,
            "servo_angle": servo_angle
        })
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

