# Diabetes Prediction — Reproducibility Guide

Part of Assignment 02 (Intelligent System Development, PTIT).

## Environment
- Python 3.10+
- Random seed: 42 (set in notebook and `run_pipeline.py`)
- OS tested: Linux (should also work on Windows/macOS)

## 1. Install dependencies
```bash
pip install -r requirements.txt
```

## 2. Dataset
- Source: Kaggle — [Diabetes prediction dataset](https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset)
  (Mohammed Mustafa), 100,000 rows.
- Place the CSV at `data/diabetes.csv` (already included in this submission).

## 3. Reproduce the experiment
Open and run all cells in `notebook/diabetes.ipynb` top to bottom, **or** run the equivalent
script:
```bash
cd notebook   # so relative paths ../data and ../model resolve correctly
jupyter nbconvert --to notebook --execute diabetes.ipynb
```
This regenerates `model/model_pipeline.joblib` and `model/meta.json`.

## 4. Run the REST API
```bash
cd api
pip install fastapi uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
- Interactive docs: http://localhost:8000/docs
- Health check: http://localhost:8000/
- Prediction endpoint: `POST http://localhost:8000/predict`

Example request:
```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{
  "gender": "Female", "age": 67, "hypertension": 1, "heart_disease": 1,
  "smoking_history": "former", "bmi": 32.5, "HbA1c_level": 7.2, "blood_glucose_level": 210
}'
```

## 5. Web client
Open `web/index.html` directly in a browser (double-click, or serve via
`python -m http.server` from the `web/` folder). Set the "API Base URL" field to match
where the API is running (default `http://localhost:8000`), fill the form, click Predict.

## 6. Mobile client
`mobile/index.html` is a phone-sized, single-column client for the same API — open it on a
phone's browser (serve it with `python -m http.server` from the `mobile/` folder and browse to
`http://<your-computer-IP>:<port>` from the phone, both devices on the same network). It can
also be added to the phone's home screen via the browser's "Add to Home Screen" option
(a `manifest.json` is included).

## Notes on data leakage
The same `preprocessor` (StandardScaler + OneHotEncoder) is fit **only** on the training
split and saved inside the persisted `model_pipeline.joblib`. The API and both clients never
re-fit any preprocessing step — they only call `.predict_proba()` on the already-fitted
pipeline, guaranteeing training/inference consistency.
