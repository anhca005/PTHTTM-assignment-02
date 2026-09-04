"""
E-commerce Customer Behavior — Recommendation Prediction API
---------------------------------------------------------------
Loads the persisted preprocessing+model pipeline (joblib) and exposes:
  - POST /predict       tabular prediction (deployed model, e.g. SVM)
  - POST /analyze_text   secondary TF-IDF + Logistic Regression text model,
                          used to analyze a raw review's sentiment directly.
Both pipelines are the SAME objects fit during training, so preprocessing
at inference time is guaranteed identical to preprocessing at training
time (no data leakage / no re-fitting).

Run:
    uvicorn app:app --host 0.0.0.0 --port 8002 --reload

Docs (Swagger UI):
    http://localhost:8002/docs
"""
import json
import os

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "model")

pipeline = joblib.load(os.path.join(MODEL_DIR, "model_pipeline.joblib"))
text_pipeline = joblib.load(os.path.join(MODEL_DIR, "text_model_pipeline.joblib"))
with open(os.path.join(MODEL_DIR, "meta.json"), "r", encoding="utf-8") as f:
    META = json.load(f)

app = FastAPI(
    title="E-commerce Recommendation Prediction API",
    description="Assignment 02 - Intelligent System Development (PTIT)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReviewInput(BaseModel):
    Age: float = Field(..., ge=0, le=110, example=35)
    Rating: int = Field(..., ge=1, le=5, example=5)
    Positive_Feedback_Count: int = Field(0, ge=0, alias="Positive Feedback Count", example=2)
    Review_Text: str = Field("", alias="Review Text", example="Absolutely love this dress!")
    Title: str = Field("", example="Great fit")
    Division_Name: str = Field(..., alias="Division Name", example="General")
    Department_Name: str = Field(..., alias="Department Name", example="Dresses")
    Class_Name: str = Field(..., alias="Class Name", example="Dresses")

    class Config:
        populate_by_name = True


class PredictionOutput(BaseModel):
    prediction: str
    prediction_label: int
    probability_recommended: float
    model_used: str


class TextInput(BaseModel):
    text: str = Field(..., example="This dress runs small and the fabric feels cheap.")


class TextAnalysisOutput(BaseModel):
    prediction: str
    probability_recommended: float
    model_used: str


@app.get("/")
def root():
    return {
        "service": "E-commerce Recommendation Prediction API",
        "model": META["best_model_name"],
        "test_metrics": META["test_metrics"],
        "endpoints": {
            "predict": "POST /predict (structured review -> recommend?)",
            "analyze_text": "POST /analyze_text (free-text review -> recommend?)",
            "docs": "/docs",
        },
    }


@app.get("/meta")
def get_meta():
    """Expose feature schema so web/mobile clients can build their forms dynamically."""
    return META


def _build_row(review: ReviewInput) -> pd.DataFrame:
    review_text = review.Review_Text or ""
    title = review.Title or ""
    row = {
        "Age": review.Age,
        "Rating": review.Rating,
        "Positive Feedback Count": review.Positive_Feedback_Count,
        "Review Length": len(review_text),
        "Title Length": len(title),
        "Has Review": int(len(review_text) > 0),
        "Has Title": int(len(title) > 0),
        "Division Name": review.Division_Name,
        "Department Name": review.Department_Name,
        "Class Name": review.Class_Name,
    }
    return pd.DataFrame([row])[META["feature_cols"]]


@app.post("/predict", response_model=PredictionOutput)
def predict(review: ReviewInput):
    try:
        row = _build_row(review)
        proba = pipeline.predict_proba(row)[0]
        pred_label = int(proba[1] >= 0.5)
        return PredictionOutput(
            prediction=META["class_labels"][str(pred_label)],
            prediction_label=pred_label,
            probability_recommended=round(float(proba[1]), 4),
            model_used=META["best_model_name"],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/analyze_text", response_model=TextAnalysisOutput)
def analyze_text(payload: TextInput):
    """Secondary model: TF-IDF + Logistic Regression, predicting recommendation
    directly from free review text (no structured fields required)."""
    try:
        proba = text_pipeline.predict_proba([payload.text])[0]
        pred_label = int(proba[1] >= 0.5)
        return TextAnalysisOutput(
            prediction=META["class_labels"][str(pred_label)],
            probability_recommended=round(float(proba[1]), 4),
            model_used="Text Logistic Regression (TF-IDF)",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
