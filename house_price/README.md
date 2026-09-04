# House Price Prediction — Reproducibility Guide

Part of Assignment 02 (Intelligent System Development, PTIT).

## Environment
- Python 3.10+
- Random seed: 42 (set in `notebook/train.py` and the notebook)
- OS tested: Windows (should also work on Linux/macOS)

## 1. Install dependencies
```bash
pip install -r requirements.txt
```

## 2. Dataset
- Source: Kaggle — Vietnam Housing Dataset (real-estate listings, ~30k rows).
- Place the CSV at `data/vietnam_housing.csv` (already included in this submission;
  despite the original `.xls` extension the file is plain CSV/UTF-8).

## 3. Reproduce the experiment
Run the training script (regenerates charts, `model/model_pipeline.joblib` and
`model/meta.json`):
```bash
cd notebook
python train.py
```
The equivalent Jupyter notebook `notebook/house_price.ipynb` contains the same steps with
explanations, EDA plots, and Observation/Interpretation/ML-implication notes; open and
"Run All" to reproduce it interactively.

## 4. Run the REST API
```bash
cd api
pip install fastapi uvicorn
uvicorn app:app --host 0.0.0.0 --port 8001 --reload
```
- Interactive docs: http://localhost:8001/docs
- Health check: http://localhost:8001/
- Prediction endpoint: `POST http://localhost:8001/predict`

Example request:
```bash
curl -X POST http://localhost:8001/predict -H "Content-Type: application/json" -d '{
  "Area": 60, "Frontage": 4.5, "Access Road": 6, "Floors": 3, "Bedrooms": 3, "Bathrooms": 2,
  "Legal status": "Have certificate", "Furniture state": "Full",
  "House direction": "Unknown", "Balcony direction": "Unknown", "ProvinceGroup": "Ha Noi"
}'
```

## 5. Web client
Open `web/index.html` directly in a browser (or serve via `python -m http.server` from the
`web/` folder). Set the "API Base URL" field to match where the API is running (default
`http://localhost:8001`), fill the form, click **Predict Price**.

## 6. Mobile client
`mobile/index.html` is a phone-sized, single-column client for the same API — open it on a
phone's browser (serve it with `python -m http.server` from the `mobile/` folder and browse
to `http://<your-computer-IP>:<port>` from the phone, both devices on the same network). It
can also be added to the phone's home screen via the browser's "Add to Home Screen" option
(a `manifest.json` is included).

## Notes on data leakage
The same `preprocessor` (median-imputation + `StandardScaler` for numeric columns,
most-frequent imputation + `OneHotEncoder` for categorical columns) is fit **only** on the
training split and saved inside the persisted `model_pipeline.joblib`. The API and both
clients never re-fit any preprocessing step — they only call `.predict()` on the
already-fitted pipeline, guaranteeing training/inference consistency.

## Model summary
- Problem type: **regression** (target = `Price`, billion VND).
- 5 models compared on the validation split: Linear Regression, Ridge, Decision Tree,
  Random Forest, Gradient Boosting (see `model/model_comparison_validation.csv`).
- Selected model: **Gradient Boosting Regressor** (lowest validation RMSE).
- Test-set performance: see `model/meta.json` → `test_metrics`
  (MAE ≈ 1.25, RMSE ≈ 1.59, R² ≈ 0.47, in billion VND).
