"""
Application 2 - House Price Prediction
Assignment 02 - Intelligent System Development (PTIT)

Pipeline: Raw Data -> Understand -> Clean -> Represent -> Learn -> Evaluate -> Persist

Dataset: Vietnam Housing Dataset (Kaggle) - listings scraped from a Vietnamese
real-estate portal. One observation = one house/apartment listing.
Target: Price (billion VND).
This is a REGRESSION problem.
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
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DATA_PATH = os.path.join(ROOT_DIR, "data", "vietnam_housing.csv")
CHART_DIR = os.path.join(ROOT_DIR, "charts")
MODEL_DIR = os.path.join(ROOT_DIR, "model")
os.makedirs(CHART_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")

# --------------------------------------------------------------------------
# 1. RAW DATA
# --------------------------------------------------------------------------
print("=" * 70)
print("STEP 1-2: RAW DATA & UNDERSTANDING")
print("=" * 70)
df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
print("Dataset shape:", df.shape)
print(df.head(3).to_string())
print("\nDtypes:")
print(df.dtypes)
print("\nMissing values per column:")
print(df.isna().sum())
print("\nDuplicated rows (full):", df.duplicated().sum())
print("\nDescribe numeric:")
print(df.describe().to_string())

# --------------------------------------------------------------------------
# 2. CLEAN
# --------------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 3: DATA CLEANING")
print("=" * 70)
df_clean = df.copy()

# Remove exact duplicate rows (if any)
before = len(df_clean)
df_clean = df_clean.drop_duplicates()
print(f"Removed {before - len(df_clean)} exact duplicate rows.")

# Invalid-value checks
invalid_checks = {
    "Area <= 0": (df_clean["Area"] <= 0).sum(),
    "Price <= 0": (df_clean["Price"] <= 0).sum(),
    "Floors <= 0": (df_clean["Floors"] <= 0).sum(),
    "Bedrooms <= 0": (df_clean["Bedrooms"] <= 0).sum(),
    "Bathrooms <= 0": (df_clean["Bathrooms"] <= 0).sum(),
}
print("Invalid value counts:", invalid_checks)
# The dataset has no non-positive values for these columns, so no rows are
# removed on this basis; the checks are still performed and reported.

# Outlier analysis (IQR) - report only, values are kept because they can
# represent genuine (if unusual) high-end or low-end real-estate listings.
outlier_summary = []
for col in ["Area", "Frontage", "Access Road", "Price"]:
    q1, q3 = df_clean[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    n_out = ((df_clean[col] < lower) | (df_clean[col] > upper)).sum()
    outlier_summary.append((col, lower, upper, n_out))
print("\nOutlier summary (IQR method):")
for col, lower, upper, n_out in outlier_summary:
    print(f"  {col}: bounds=({lower:.2f}, {upper:.2f}) outliers={n_out}")

# Feature engineering: extract Province from the free-text Address column
def extract_province(addr: str) -> str:
    parts = [p.strip().rstrip(".").strip() for p in str(addr).split(",")]
    return parts[-1] if parts and parts[-1] else "Unknown"

df_clean["Province"] = df_clean["Address"].apply(extract_province)
top_provinces = df_clean["Province"].value_counts().head(12).index.tolist()
df_clean["ProvinceGroup"] = df_clean["Province"].where(
    df_clean["Province"].isin(top_provinces), "Khac"
)
print("\nProvinceGroup distribution:")
print(df_clean["ProvinceGroup"].value_counts())

# Missing categorical values are treated as their own explicit category
# ("Unknown") rather than dropped, because "no information reported" is
# itself informative for a real-estate listing.
categorical_features = [
    "Legal status",
    "Furniture state",
    "House direction",
    "Balcony direction",
    "ProvinceGroup",
]
numeric_features = ["Area", "Frontage", "Access Road", "Floors", "Bedrooms", "Bathrooms"]
target_col = "Price"

for c in categorical_features:
    df_clean[c] = df_clean[c].fillna("Unknown")

print(f"\nCleaned dataset shape: {df_clean.shape}")

# --------------------------------------------------------------------------
# 3. REPRESENT
# --------------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 4: DATA REPRESENTATION")
print("=" * 70)
feature_cols = numeric_features + categorical_features
X = df_clean[feature_cols].copy()
y = df_clean[target_col].copy()
print(f"X shape (raw feature matrix): {X.shape}  ->  X in R^(N x d), N={X.shape[0]}, d={X.shape[1]}")
print(f"y shape (target vector): {y.shape}")
print("Numeric features:", numeric_features)
print("Categorical features:", categorical_features)

# --------------------------------------------------------------------------
# 4. EDA (charts saved to /charts)
# --------------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 5: EXPLORATORY DATA ANALYSIS")
print("=" * 70)

plt.figure(figsize=(7, 4.5))
sns.histplot(y, bins=40, kde=True, color="#2563eb")
plt.title("Distribution of House Prices (billion VND)")
plt.xlabel("Price (billion VND)")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "01_price_distribution.png"), dpi=120)
plt.close()

plt.figure(figsize=(7, 4.5))
sns.scatterplot(x=X["Area"], y=y, alpha=0.25, s=12, color="#2563eb")
plt.title("Area vs Price")
plt.xlabel("Area (m2)")
plt.ylabel("Price (billion VND)")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "02_area_vs_price.png"), dpi=120)
plt.close()

plt.figure(figsize=(7, 4.5))
sns.boxplot(x=df_clean["Legal status"], y=y, color="#38bdf8")
plt.title("Price by Legal Status")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "03_price_by_legal_status.png"), dpi=120)
plt.close()

plt.figure(figsize=(8, 5))
top_price_by_province = df_clean.groupby("ProvinceGroup")[target_col].mean().sort_values(ascending=False)
sns.barplot(x=top_price_by_province.values, y=top_price_by_province.index, color="#2563eb")
plt.title("Average Price by Province")
plt.xlabel("Average price (billion VND)")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "04_price_by_province.png"), dpi=120)
plt.close()

plt.figure(figsize=(7, 6))
corr_cols = numeric_features + [target_col]
corr = df_clean[corr_cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="Reds")
plt.title("Correlation Matrix of Numerical Features")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "05_correlation_matrix.png"), dpi=120)
plt.close()

print("Saved 5 EDA charts to", CHART_DIR)

# --------------------------------------------------------------------------
# 5. TRAIN / VALIDATION / TEST SPLIT
# --------------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 6: TRAIN / VALIDATION / TEST SPLIT (70/15/15)")
print("=" * 70)
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, random_state=RANDOM_SEED
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, random_state=RANDOM_SEED
)
print(f"Train: {X_train.shape}  Validation: {X_val.shape}  Test: {X_test.shape}")

# --------------------------------------------------------------------------
# 6. PREPROCESSING PIPELINE (fit ONLY on train, to avoid data leakage)
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
# 7. BASELINE + MODELS
# --------------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 7: BASELINE AND MODEL TRAINING")
print("=" * 70)


def regression_metrics(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    return {"MAE": mae, "MSE": mse, "RMSE": rmse, "R2": r2}


baseline = DummyRegressor(strategy="mean")
baseline.fit(X_train_processed, y_train)
baseline_pred = baseline.predict(X_val_processed)
baseline_metrics = regression_metrics(y_val, baseline_pred)
print("Baseline (mean predictor) validation metrics:", baseline_metrics)

models = {
    "Linear Regression": LinearRegression(),
    "Ridge": Ridge(alpha=1.0, random_state=RANDOM_SEED),
    "Decision Tree": DecisionTreeRegressor(max_depth=8, random_state=RANDOM_SEED),
    "Random Forest": RandomForestRegressor(
        n_estimators=200, random_state=RANDOM_SEED, n_jobs=-1
    ),
    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=200, random_state=RANDOM_SEED
    ),
}

trained_models = {}
val_results = []
for name, model in models.items():
    t0 = time.time()
    model.fit(X_train_processed, y_train)
    train_time = time.time() - t0
    pred = model.predict(X_val_processed)
    metrics = regression_metrics(y_val, pred)
    metrics["Model"] = name
    metrics["Training Time (s)"] = train_time
    val_results.append(metrics)
    trained_models[name] = model
    print(f"{name}: RMSE={metrics['RMSE']:.4f}  R2={metrics['R2']:.4f}  ({train_time:.2f}s)")

val_df = pd.DataFrame(val_results).set_index("Model")
val_df = val_df[["MAE", "MSE", "RMSE", "R2", "Training Time (s)"]].sort_values("RMSE")
print("\nValidation comparison (sorted by RMSE):")
print(val_df.to_string())
val_df.to_csv(os.path.join(MODEL_DIR, "model_comparison_validation.csv"))

plt.figure(figsize=(8, 5))
sns.barplot(x=val_df["RMSE"], y=val_df.index, color="#2563eb")
plt.title("Model Comparison on Validation Set (RMSE, lower is better)")
plt.xlabel("RMSE (billion VND)")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "06_model_comparison.png"), dpi=120)
plt.close()

# --------------------------------------------------------------------------
# 8. SELECT BEST MODEL AND EVALUATE ON TEST
# --------------------------------------------------------------------------
best_model_name = val_df["RMSE"].idxmin()
best_model = trained_models[best_model_name]
print(f"\nBest model on validation (lowest RMSE): {best_model_name}")

test_pred = best_model.predict(X_test_processed)
test_metrics = regression_metrics(y_test, test_pred)
print("Test metrics:", test_metrics)

plt.figure(figsize=(6, 6))
plt.scatter(y_test, test_pred, alpha=0.25, s=12, color="#2563eb")
lims = [min(y_test.min(), test_pred.min()), max(y_test.max(), test_pred.max())]
plt.plot(lims, lims, "r--", linewidth=1)
plt.xlabel("Actual price")
plt.ylabel("Predicted price")
plt.title(f"{best_model_name}: Actual vs Predicted (Test set)")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "07_actual_vs_predicted_test.png"), dpi=120)
plt.close()

# Error analysis
residuals = y_test.values - test_pred
error_df = pd.DataFrame({"actual": y_test.values, "predicted": test_pred, "abs_error": np.abs(residuals)})
print("\nError analysis (test set):")
print(f"  Mean absolute error: {error_df['abs_error'].mean():.4f}")
print(f"  Median absolute error: {error_df['abs_error'].median():.4f}")
print(f"  Max absolute error: {error_df['abs_error'].max():.4f}")
worst = error_df.sort_values("abs_error", ascending=False).head(5)
print("  5 worst predictions:")
print(worst.to_string())

# --------------------------------------------------------------------------
# 9. PERSIST MODEL + PREPROCESSING PIPELINE
# --------------------------------------------------------------------------
print("\n" + "=" * 70)
print("STEP 8: PERSISTING MODEL")
print("=" * 70)
full_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", best_model),
])
# Re-fit the full pipeline object on train only, so a single joblib file
# contains both the fitted preprocessing AND the fitted model.
full_pipeline.fit(X_train, y_train)

joblib.dump(full_pipeline, os.path.join(MODEL_DIR, "model_pipeline.joblib"))

categorical_options = {c: sorted(df_clean[c].unique().tolist()) for c in categorical_features}
meta = {
    "app": "house_price",
    "best_model_name": best_model_name,
    "feature_cols": feature_cols,
    "numeric_cols": numeric_features,
    "categorical_cols": categorical_features,
    "categorical_options": categorical_options,
    "target_col": target_col,
    "target_unit": "billion VND",
    "test_metrics": test_metrics,
    "validation_comparison": val_df.reset_index().to_dict(orient="records"),
    "baseline_metrics": baseline_metrics,
    "random_seed": RANDOM_SEED,
}
with open(os.path.join(MODEL_DIR, "meta.json"), "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

print("Saved model_pipeline.joblib and meta.json to", MODEL_DIR)
print("\nDONE.")
