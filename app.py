"""
Bug Prediction API - FastAPI REST Service
Trained model untuk prediksi bug berdasarkan code metrics
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import joblib
import numpy as np
from datetime import datetime
import os
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Bug Prediction API",
    description="REST API untuk prediksi bug berdasarkan code complexity metrics",
    version="1.0.0"
)

# CORS middleware configuration
# Ambil dari environment variable untuk production flexibility
try:
    origins_env = os.getenv("ALLOWED_ORIGINS", "*")
    origins = [origin.strip() for origin in origins_env.split(",") if origin.strip()]
except Exception:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS origins configured: {origins}")

# Load model dan feature names saat startup
model = None
feature_names = []

@app.on_event("startup")
async def load_model():
    global model, feature_names
    try:
        model_path = os.getenv("MODEL_PATH", "best_model.joblib")
        features_path = os.getenv("FEATURES_PATH", "feature_names.joblib")
        
        if os.path.exists(model_path) and os.path.exists(features_path):
            model = joblib.load(model_path)
            feature_names = joblib.load(features_path)
            logger.info(f"✅ Model loaded successfully with features: {feature_names}")
        else:
            logger.error(f"❌ Model files not found: {model_path} or {features_path}")
    except Exception as e:
        logger.error(f"❌ Error loading model: {e}")

# Pydantic models untuk validation
class CodeMetrics(BaseModel):
    """Input schema untuk single prediction"""
    radon_total_complexity: int = Field(..., ge=0, description="Total cyclomatic complexity")
    radon_num_items: int = Field(..., ge=0, description="Number of code items")
    pylint_msgs_count: int = Field(..., ge=0, description="Pylint messages count")
    pylint_rc: int = Field(..., ge=0, description="Pylint return code")
    bandit_issues_count: int = Field(..., ge=0, description="Bandit security issues count")
    bandit_rc: int = Field(..., ge=0, description="Bandit return code")
    
    class Config:
        json_schema_extra = {
            "example": {
                "radon_total_complexity": 60,
                "radon_num_items": 29,
                "pylint_msgs_count": 32,
                "pylint_rc": 30,
                "bandit_issues_count": 1,
                "bandit_rc": 1
            }
        }

class BatchCodeMetrics(BaseModel):
    """Input schema untuk batch predictions"""
    items: List[CodeMetrics]

class PredictionResponse(BaseModel):
    """Output schema untuk prediction result"""
    is_bug: bool
    confidence: float
    probabilities: dict
    metrics: dict

class BatchPredictionResponse(BaseModel):
    """Output schema untuk batch predictions"""
    predictions: List[PredictionResponse]
    total: int

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint dengan basic info"""
    return {
        "service": "Bug Prediction API",
        "status": "running",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_status = "loaded" if model is not None else "not_loaded"
    return {
        "status": "healthy" if model is not None else "unhealthy",
        "model": model_status,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/model/info")
async def model_info():
    """Get model information"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": str(type(model)),
        "features": feature_names,
        "feature_count": len(feature_names),
        "pipeline_steps": [step[0] for step in model.steps] if hasattr(model, 'steps') else []
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(metrics: CodeMetrics):
    """
    Predict bug probability untuk single code file
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Prepare input features
        X = np.array([[
            metrics.radon_total_complexity,
            metrics.radon_num_items,
            metrics.pylint_msgs_count,
            metrics.pylint_rc,
            metrics.bandit_issues_count,
            metrics.bandit_rc
        ]])
        
        # Prediction
        prediction = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0]
        
        return PredictionResponse(
            is_bug=bool(prediction),
            confidence=float(max(probabilities) * 100),
            probabilities={
                "no_bug": float(probabilities[0]),
                "bug": float(probabilities[1])
            },
            metrics=metrics.dict()
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(batch: BatchCodeMetrics):
    """
    Batch prediction untuk multiple code files
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        predictions = []
        for metrics in batch.items:
            # Prepare input
            X = np.array([[
                metrics.radon_total_complexity,
                metrics.radon_num_items,
                metrics.pylint_msgs_count,
                metrics.pylint_rc,
                metrics.bandit_issues_count,
                metrics.bandit_rc
            ]])
            
            # Prediction
            prediction = model.predict(X)[0]
            probabilities = model.predict_proba(X)[0]
            
            predictions.append(PredictionResponse(
                is_bug=bool(prediction),
                confidence=float(max(probabilities) * 100),
                probabilities={
                    "no_bug": float(probabilities[0]),
                    "bug": float(probabilities[1])
                },
                metrics=metrics.dict()
            ))
        
        return BatchPredictionResponse(
            predictions=predictions,
            total=len(predictions)
        )
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Local development
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
