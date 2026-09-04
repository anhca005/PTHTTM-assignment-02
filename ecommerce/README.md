# E-commerce Customer Behavior & Interest Discovery — Reproducibility Guide

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
- Source: Kaggle — Women's Clothing E-Commerce Reviews (23,486 rows).
- Place the CSV at `data/ecommerce_reviews.csv` (already included in this submission).

## 3. Reproduce the experiment
Run the training script (regenerates charts, `model/model_pipeline.joblib`,
`model/text_model_pipeline.joblib` and `model/meta.json`):
```bash
cd notebook
python train.py
```
The equivalent Jupyter notebook `notebook/ecommerce.ipynb` contains the same steps with
explanations, EDA plots, and Observation/Interpretation/ML-implication notes; open and
"Run All" to reproduce it interactively.

## 4. Run the REST API
```bash
cd api
pip install fastapi uvicorn
uvicorn app:app --host 0.0.0.0 --port 8002 --reload
```
- Interactive docs: http://localhost:8002/docs
- Health check: http://localhost:8002/
- Structured prediction endpoint: `POST http://localhost:8002/predict`
- Free-text analysis endpoint: `POST http://localhost:8002/analyze_text`

Example requests:
```bash
curl -X POST http://localhost:8002/predict -H "Content-Type: application/json" -d '{
  "Age": 35, "Rating": 5, "Positive Feedback Count": 2,
  "Review Text": "Absolutely love this dress!", "Title": "Great fit",
  "Division Name": "General", "Department Name": "Dresses", "Class Name": "Dresses"
}'

curl -X POST http://localhost:8002/analyze_text -H "Content-Type: application/json" -d '{
  "text": "This dress runs small and the fabric feels cheap."
}'
```

## 5. Web client
Open `web/index.html` directly in a browser (or serve via `python -m http.server` from the
`web/` folder). Set the "API Base URL" field to match where the API is running (default
`http://localhost:8002`). The page has two sections: a structured form (calls `/predict`)
and a free-text box (calls `/analyze_text`).

## 6. Mobile client
`mobile/index.html` is a phone-sized, single-column client with both sections above — open
it on a phone's browser (serve it with `python -m http.server` from the `mobile/` folder and
browse to `http://<your-computer-IP>:<port>` from the phone, both devices on the same
network). It can also be added to the phone's home screen via the browser's "Add to Home
Screen" option (a `manifest.json` is included).

## Notes on data leakage
The tabular `preprocessor` (median-imputation + `StandardScaler` for numeric columns,
most-frequent imputation + `OneHotEncoder` for categorical columns) and the
`TfidfVectorizer` are both fit **only** on the training split and saved inside their
respective persisted `.joblib` pipelines. The API and both clients never re-fit any
preprocessing step — they only call `.predict_proba()` on the already-fitted pipelines,
guaranteeing training/inference consistency.

## Model summary
- Problem type: **binary classification** (target = `Recommended IND`).
- 6 models compared on the validation split: Logistic Regression, Decision Tree, Random
  Forest, KNN, SVM (all on the tabular representation) plus a Text Logistic Regression on
  TF-IDF features of `Review Text` (see `model/model_comparison_validation.csv`).
- Selected (deployed) model: **SVM** on the tabular representation (highest validation F1).
  The text-only model is kept as a secondary artifact (`/analyze_text`) but is not the
  primary deployed model — it needs review text, which does not exist yet at the moment a
  "will this listing be recommended" prediction is normally needed.
- Test-set performance: see `model/meta.json` → `test_metrics`
  (Accuracy ≈ 0.94, Precision ≈ 0.99, Recall ≈ 0.94, F1 ≈ 0.96, ROC-AUC ≈ 0.98).
