"""
Application 3 - E-commerce Customer Behavior & Interest Discovery
Assignment 02 - Intelligent System Development (PTIT)

Pipeline: Raw Data -> Understand -> Clean -> Represent -> Learn -> Evaluate -> Persist

Dataset: Women's Clothing E-Commerce Reviews (Kaggle). One observation = one customer
review of one product.
Target: Recommended IND (0 = customer does NOT recommend the product,
                          1 = customer recommends the product).
This is a BINARY CLASSIFICATION problem.
"""
import json
import os
import time

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DATA_PATH = os.path.join(ROOT_DIR, "data", "ecommerce_reviews.csv")
CHART_DIR = os.path.join(ROOT_DIR, "charts")
MODEL_DIR = os.path.join(ROOT_DIR, "model")
os.makedirs(CHART_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")

# --------------------------------------------------------------------------
# 1-2. RAW DATA & UNDERSTANDING
# --------------------------------------------------------------------------
print("=" * 70)
print("STEP 1-2: RAW DATA & UNDERSTANDING")
print("=" * 70)
df = pd.read_csv(DATA_PATH)
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])
print("Dataset shape:", df.shape)
print(df.head(3).to_string())
print("\nDtypes:")
print(df.dtypes)
print("\nMissing values per column:")
print(df.isna().sum())
print("\nDuplicated rows:", df.duplicated().sum())
print("\nTarget distribution:")
print(df["Recommended IND"].value_counts())

# --------------------------------------------------------------------------
# 3. CLEAN
# --------------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 3: DATA CLEANING")
print("=" * 70)
df_clean = df.copy()

before = len(df_clean)
df_clean = df_clean.drop_duplicates()
print(f"Removed {before - len(df_clean)} exact duplicate rows.")

invalid_checks = {
    "Age <= 0": (df_clean["Age"] <= 0).sum(),
    "Rating outside 1-5": (~df_clean["Rating"].between(1, 5)).sum(),
    "Recommended IND not 0/1": (~df_clean["Recommended IND"].isin([0, 1])).sum(),
    "Positive Feedback Count < 0": (df_clean["Positive Feedback Count"] < 0).sum(),
}
print("Invalid value counts:", invalid_checks)

# Outlier analysis (IQR) - report only, kept (real customer behaviour).
outlier_summary = []
for col in ["Age", "Positive Feedback Count"]:
    q1, q3 = df_clean[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    n_out = ((df_clean[col] < lower) | (df_clean[col] > upper)).sum()
    outlier_summary.append((col, lower, upper, n_out))
print("\nOutlier summary (IQR method):")
for col, lower, upper, n_out in outlier_summary:
    print(f"  {col}: bounds=({lower:.2f}, {upper:.2f}) outliers={n_out}")

# Product-category columns are missing for only 14 rows -> drop those rows
# (dropping is safe here: 14 / 23486 = 0.06%).
before = len(df_clean)
df_clean = df_clean.dropna(subset=["Division Name", "Department Name", "Class Name"])
print(f"\nDropped {before - len(df_clean)} rows with missing product-category info.")

# Title / Review Text are free text and are frequently missing; missingness
# itself is informative (a customer who leaves no comment behaves
# differently from one who writes a long review), so instead of imputing
# text we engineer explicit numeric/binary features from it.
df_clean["Review Text"] = df_clean["Review Text"].fillna("")
df_clean["Title"] = df_clean["Title"].fillna("")
df_clean["Has Review"] = (df_clean["Review Text"].str.len() > 0).astype(int)
df_clean["Has Title"] = (df_clean["Title"].str.len() > 0).astype(int)
df_clean["Review Length"] = df_clean["Review Text"].str.len()
df_clean["Title Length"] = df_clean["Title"].str.len()

print(f"\nCleaned dataset shape: {df_clean.shape}")

# --------------------------------------------------------------------------
# 4. REPRESENT
# --------------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 4: DATA REPRESENTATION")
print("=" * 70)
numeric_features = [
    "Age", "Rating", "Positive Feedback Count",
    "Review Length", "Title Length", "Has Review", "Has Title",
]
categorical_features = ["Division Name", "Department Name", "Class Name"]
target_col = "Recommended IND"
feature_cols = numeric_features + categorical_features

X = df_clean[feature_cols].copy()
y = df_clean[target_col].copy()
review_text = df_clean["Review Text"].copy()
print(f"X shape (raw feature matrix, tabular part): {X.shape}")
print(f"y shape (target vector): {y.shape}")
print("Numeric features:", numeric_features)
print("Categorical features:", categorical_features)

# --------------------------------------------------------------------------
# 5. EDA
# --------------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 5: EXPLORATORY DATA ANALYSIS")
print("=" * 70)

plt.figure(figsize=(6, 4.5))
sns.countplot(x=y, color="#7c3aed")
plt.title("Distribution of Recommended IND")
plt.xlabel("Recommended IND (0 = not recommended, 1 = recommended)")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "01_target_distribution.png"), dpi=120)
plt.close()

plt.figure(figsize=(7, 4.5))
ct = pd.crosstab(df_clean["Rating"], y, normalize="index") * 100
ct.plot(kind="bar", stacked=True, color=["#f87171", "#34d399"])
plt.title("Recommendation Rate by Rating")
plt.ylabel("Percentage (%)")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "02_recommend_by_rating.png"), dpi=120)
plt.close()

plt.figure(figsize=(7, 4.5))
sns.histplot(df_clean["Review Length"], bins=40, color="#7c3aed")
plt.title("Distribution of Review Text Length")
plt.xlabel("Review length (characters)")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "03_review_length_distribution.png"), dpi=120)
plt.close()

plt.figure(figsize=(8, 5))
top_dept = df_clean["Department Name"].value_counts()
sns.barplot(x=top_dept.values, y=top_dept.index, color="#7c3aed")
plt.title("Number of Reviews per Department")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "04_reviews_per_department.png"), dpi=120)
plt.close()

plt.figure(figsize=(6, 5))
corr = df_clean[["Age", "Rating", "Positive Feedback Count", "Recommended IND"]].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="Purples")
plt.title("Correlation Matrix")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "05_correlation_matrix.png"), dpi=120)
plt.close()

print("Saved 5 EDA charts to", CHART_DIR)

# --------------------------------------------------------------------------
# 6. TRAIN / VAL / TEST SPLIT
# --------------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 6: TRAIN / VALIDATION / TEST SPLIT (70/15/15, stratified)")
print("=" * 70)
idx = np.arange(len(X))
idx_train, idx_temp = train_test_split(
    idx, test_size=0.30, random_state=RANDOM_SEED, stratify=y
)
idx_val, idx_test = train_test_split(
    idx_temp, test_size=0.50, random_state=RANDOM_SEED, stratify=y.iloc[idx_temp]
)

X_train, y_train = X.iloc[idx_train], y.iloc[idx_train]
X_val, y_val = X.iloc[idx_val], y.iloc[idx_val]
X_test, y_test = X.iloc[idx_test], y.iloc[idx_test]
text_train, text_val, text_test = (
    review_text.iloc[idx_train], review_text.iloc[idx_val], review_text.iloc[idx_test]
)
print(f"Train: {X_train.shape}  Validation: {X_val.shape}  Test: {X_test.shape}")

# --------------------------------------------------------------------------
# 7. PREPROCESSING PIPELINE (tabular)
# --------------------------------------------------------------------------
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])
categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
])
preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numeric_features),
    ("cat", categorical_pipeline, categorical_features),
])
X_train_processed = preprocessor.fit_transform(X_train)
X_val_processed = preprocessor.transform(X_val)
X_test_processed = preprocessor.transform(X_test)
print("Processed train shape:", X_train_processed.shape)
print("Processed val shape:  ", X_val_processed.shape)
print("Processed test shape: ", X_test_processed.shape)

# --------------------------------------------------------------------------
# 8. BASELINE + 6 MODELS (5 tabular + 1 text-based)
# --------------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 7: BASELINE AND MODEL TRAINING")
print("=" * 70)


def classification_metrics(y_true, y_pred, y_prob=None):
    m = {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=0),
        "Recall": recall_score(y_true, y_pred, zero_division=0),
        "F1": f1_score(y_true, y_pred, zero_division=0),
    }
    if y_prob is not None:
        m["ROC-AUC"] = roc_auc_score(y_true, y_prob)
    return m


baseline = DummyClassifier(strategy="most_frequent", random_state=RANDOM_SEED)
baseline.fit(X_train_processed, y_train)
baseline_pred = baseline.predict(X_val_processed)
baseline_metrics = classification_metrics(y_val, baseline_pred)
print("Baseline (majority class) validation metrics:", baseline_metrics)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_SEED),
    "Decision Tree": DecisionTreeClassifier(max_depth=8, random_state=RANDOM_SEED),
    "Random Forest": RandomForestClassifier(
        n_estimators=200, random_state=RANDOM_SEED, n_jobs=-1
    ),
    "KNN": KNeighborsClassifier(n_neighbors=15),
    "SVM": SVC(probability=True, random_state=RANDOM_SEED),
}

trained_models = {}
val_results = []
for name, model in models.items():
    t0 = time.time()
    model.fit(X_train_processed, y_train)
    train_time = time.time() - t0
    pred = model.predict(X_val_processed)
    prob = model.predict_proba(X_val_processed)[:, 1]
    metrics = classification_metrics(y_val, pred, prob)
    metrics["Model"] = name
    metrics["Training Time (s)"] = train_time
    val_results.append(metrics)
    trained_models[name] = model
    print(f"{name}: F1={metrics['F1']:.4f}  Acc={metrics['Accuracy']:.4f}  ({train_time:.2f}s)")

# --- 6th model: text-based classifier on Review Text via TF-IDF ---
tfidf = TfidfVectorizer(lowercase=True, stop_words="english", max_features=5000, ngram_range=(1, 2))
X_train_text = tfidf.fit_transform(text_train)
X_val_text = tfidf.transform(text_val)
X_test_text = tfidf.transform(text_test)
print("\nTF-IDF training shape:", X_train_text.shape)

t0 = time.time()
text_model = LogisticRegression(max_iter=1000, random_state=RANDOM_SEED)
text_model.fit(X_train_text, y_train)
text_train_time = time.time() - t0
text_pred = text_model.predict(X_val_text)
text_prob = text_model.predict_proba(X_val_text)[:, 1]
text_metrics = classification_metrics(y_val, text_pred, text_prob)
text_metrics["Model"] = "Text Logistic Regression (TF-IDF)"
text_metrics["Training Time (s)"] = text_train_time
val_results.append(text_metrics)
print(f"Text Logistic Regression (TF-IDF): F1={text_metrics['F1']:.4f}  Acc={text_metrics['Accuracy']:.4f}")

val_df = pd.DataFrame(val_results).set_index("Model")
val_df = val_df[["Accuracy", "Precision", "Recall", "F1", "ROC-AUC", "Training Time (s)"]].sort_values(
    "F1", ascending=False
)
print("\nValidation comparison (sorted by F1, 6 models):")
print(val_df.to_string())
val_df.to_csv(os.path.join(MODEL_DIR, "model_comparison_validation.csv"))

plt.figure(figsize=(8, 5))
sns.barplot(x=val_df["F1"], y=val_df.index, color="#7c3aed")
plt.title("Model Comparison on Validation Set (F1-score, higher is better)")
plt.xlabel("F1-score")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "06_model_comparison.png"), dpi=120)
plt.close()

# --------------------------------------------------------------------------
# 9. SELECT BEST TABULAR MODEL (deployable via a structured form) AND
#    EVALUATE ON TEST. The text model is reported for comparison but is
#    not the deployed model: it needs raw review text, which is only
#    available AFTER a customer has already written a review, so it is
#    less useful for a "will this product be recommended" prediction
#    made at listing time.
# --------------------------------------------------------------------------
tabular_val_df = val_df.drop(index="Text Logistic Regression (TF-IDF)")
best_model_name = tabular_val_df["F1"].idxmax()
best_model = trained_models[best_model_name]
print(f"\nBest deployable (tabular) model on validation (highest F1): {best_model_name}")

test_pred = best_model.predict(X_test_processed)
test_prob = best_model.predict_proba(X_test_processed)[:, 1]
test_metrics = classification_metrics(y_test, test_pred, test_prob)
print("Test metrics:", test_metrics)

cm = confusion_matrix(y_test, test_pred)
disp = ConfusionMatrixDisplay(cm, display_labels=["Not Recommended", "Recommended"])
fig, ax = plt.subplots(figsize=(5, 5))
disp.plot(ax=ax, cmap="Purples", colorbar=True)
plt.title(f"Confusion Matrix - {best_model_name} (Test)")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "07_confusion_matrix_test.png"), dpi=120)
plt.close()

fig, ax = plt.subplots(figsize=(5.5, 5))
RocCurveDisplay.from_predictions(y_test, test_prob, ax=ax, name=best_model_name)
plt.title("ROC Curve (Test set)")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "08_roc_curve_test.png"), dpi=120)
plt.close()

tn, fp, fn, tp = cm.ravel()
print(f"\nError analysis (test set): TP={tp} TN={tn} FP={fp} FN={fn}")
print(f"  Total: {len(y_test)}  Correct: {tp+tn}  Incorrect: {fp+fn}")

# --------------------------------------------------------------------------
# 10. PERSIST
# --------------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 8: PERSISTING MODEL")
print("=" * 70)
full_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", best_model),
])
full_pipeline.fit(X_train, y_train)
joblib.dump(full_pipeline, os.path.join(MODEL_DIR, "model_pipeline.joblib"))

# Also persist the text pipeline (TF-IDF + Logistic Regression) as a
# secondary artifact, usable to analyze free-text reviews directly.
text_pipeline = Pipeline([
    ("tfidf", tfidf),
    ("model", text_model),
])
joblib.dump(text_pipeline, os.path.join(MODEL_DIR, "text_model_pipeline.joblib"))

categorical_options = {c: sorted(df_clean[c].unique().tolist()) for c in categorical_features}
meta = {
    "app": "ecommerce",
    "best_model_name": best_model_name,
    "feature_cols": feature_cols,
    "numeric_cols": numeric_features,
    "categorical_cols": categorical_features,
    "categorical_options": categorical_options,
    "target_col": target_col,
    "class_labels": {"0": "Not recommended", "1": "Recommended"},
    "test_metrics": test_metrics,
    "validation_comparison": val_df.reset_index().to_dict(orient="records"),
    "baseline_metrics": baseline_metrics,
    "text_model_metrics": text_metrics,
    "random_seed": RANDOM_SEED,
}
with open(os.path.join(MODEL_DIR, "meta.json"), "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

print("Saved model_pipeline.joblib, text_model_pipeline.joblib and meta.json to", MODEL_DIR)
print("\nDONE.")
