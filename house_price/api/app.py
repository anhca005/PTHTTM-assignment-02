"""
House Price Prediction API
---------------------------
Loads the persisted preprocessing+model pipeline (joblib) and exposes a
POST /predict endpoint. This is the SAME pipeline object used during
training, so preprocessing at inference time is guaranteed identical to
preprocessing at training time (no data leakage / no re-fitting).

Run:
    uvicorn app:app --host 0.0.0.0 --port 8001 --reload

Docs (Swagger UI):
    http://localhost:8001/docs
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
with open(os.path.join(MODEL_DIR, "meta.json"), "r", encoding="utf-8") as f:
    META = json.load(f)

app = FastAPI(
    title="House Price Prediction API",
    description="Assignment 02 - Intelligent System Development (PTIT)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class HouseInput(BaseModel):
    Area: float = Field(..., gt=0, example=60)
    Frontage: float = Field(5, gt=0, example=4.5)
    Access_Road: float = Field(6, gt=0, alias="Access Road", example=6)
    Floors: float = Field(3, gt=0, example=3)
    Bedrooms: float = Field(3, gt=0, example=3)
    Bathrooms: float = Field(2, gt=0, example=2)
    Legal_status: str = Field("Have certificate", alias="Legal status", example="Have certificate")
    Furniture_state: str = Field("Full", alias="Furniture state", example="Full")
    House_direction: str = Field("Unknown", alias="House direction", example="Đông - Nam")
    Balcony_direction: str = Field("Unknown", alias="Balcony direction", example="Đông - Nam")
    ProvinceGroup: str = Field("Hà Nội", example="Hà Nội")

    class Config:
        populate_by_name = True


class PredictionOutput(BaseModel):
    predicted_price: float
    predicted_price_unit: str
    model_used: str


@app.get("/")
def root():
    return {
        "service": "House Price Prediction API",
        "model": META["best_model_name"],
        "test_metrics": META["test_metrics"],
        "endpoints": {"predict": "POST /predict", "docs": "/docs"},
    }


@app.get("/meta")
def get_meta():
    """Expose feature schema so web/mobile clients can build their forms dynamically."""
    return META


@app.post("/predict", response_model=PredictionOutput)
def predict(house: HouseInput):
    try:
        row = pd.DataFrame([house.dict(by_alias=True)])[META["feature_cols"]]
        pred = float(pipeline.predict(row)[0])
        return PredictionOutput(
            predicted_price=round(pred, 3),
            predicted_price_unit=META["target_unit"],
            model_used=META["best_model_name"],
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
