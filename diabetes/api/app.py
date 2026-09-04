"""
Diabetes Prediction API
------------------------
Loads the persisted preprocessing+model pipeline (joblib) and exposes
a POST /predict endpoint. This is the SAME pipeline object used during
training, so preprocessing at inference time is guaranteed identical
to preprocessing at training time (no data leakage / no re-fitting).

Run:
    uvicorn app:app --host 0.0.0.0 --port 8000 --reload

Docs (Swagger UI):
    http://localhost:8000/docs
"""
import json
import os
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "model")

pipeline = joblib.load(os.path.join(MODEL_DIR, "model_pipeline.joblib"))
with open(os.path.join(MODEL_DIR, "meta.json"), "r", encoding="utf-8") as f:
    META = json.load(f)

app = FastAPI(
    title="Diabetes Prediction API",
    description="Assignment 02 - Intelligent System Development (PTIT)",
    version="1.0.0",
)

# Allow the web/mobile static clients (served from file:// or another port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PatientInput(BaseModel):
    gender: Literal["Female", "Male", "Other"] = Field(..., example="Female")
    age: float = Field(..., ge=0, le=120, example=45)
    hypertension: Literal[0, 1] = Field(..., example=0)
    heart_disease: Literal[0, 1] = Field(..., example=0)
    smoking_history: str = Field(..., example="never")
    bmi: float = Field(..., ge=10, le=80, example=24.5)
    HbA1c_level: float = Field(..., ge=3, le=15, example=5.7)
    blood_glucose_level: float = Field(..., ge=50, le=400, example=120)


class PredictionOutput(BaseModel):
    prediction: str
    prediction_label: int
    confidence: float
    model_used: str


@app.get("/")
def root():
    return {
        "service": "Diabetes Prediction API",
        "model": META["best_model_name"],
        "test_metrics": META["test_metrics"],
        "endpoints": {"predict": "POST /predict", "docs": "/docs"},
    }


@app.get("/meta")
def get_meta():
    """Expose feature schema so web/mobile clients can build their forms dynamically."""
    return META


@app.post("/predict", response_model=PredictionOutput)
def predict(patient: PatientInput):
    try:
        row = pd.DataFrame([patient.dict()])[META["feature_cols"]]
        proba = pipeline.predict_proba(row)[0]
        pred_label = int(proba[1] >= 0.5)
        confidence = float(proba[pred_label])
        return PredictionOutput(
            prediction=META["class_labels"][str(pred_label)],
            prediction_label=pred_label,
            confidence=round(confidence, 4),
            model_used=META["best_model_name"],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
