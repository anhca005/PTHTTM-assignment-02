# Danh sách ảnh cần chụp từ Jupyter (Anaconda) cho báo cáo

**Cập nhật:** tất cả biểu đồ (EDA, so sánh mô hình, confusion matrix, ROC...) giờ đều phải là
ảnh chụp thật từ Jupyter (có cả code lẫn kết quả), không dùng ảnh do script tự vẽ nữa. Tổng
cộng **40 ảnh** (mỗi ứng dụng ~13-14 ảnh).

Mở từng notebook bằng **Anaconda Jupyter Notebook/Lab** (đã có sẵn kernel `python3`, mọi cell
đều đã có output, **không cần Run lại**). Dùng Snipping Tool / Win+Shift+S để chụp đúng vùng
code + kết quả (giống phong cách ảnh trong `bai_mau.pdf`), lưu file **đúng tên** vào đúng thư
mục bên dưới. Báo tôi khi xong (hoặc gửi ảnh) để tôi chạy lại `build_report.py` — ảnh thật sẽ
tự động thay thế khung placeholder tương ứng, không cần sửa gì trong Word.

Thư mục lưu ảnh: `A02/report/images/<app>/<ten_file>.png`

---
## 1) Diabetes — mở `A02/diabetes/notebook/diabetes.ipynb`
Lưu vào `A02/report/images/diabetes/`

### Nhóm A — Tổng quan / làm sạch / biểu diễn / huấn luyện (không đổi so với trước)
| Tên file | Chụp cell nào |
|---|---|
| `diabetes_01_overview.png` | Mục "4. Dataset inspection": `df_raw.head()`, `df_raw.info()`, `df_raw.describe()` |
| `diabetes_02_missing_duplicates.png` | Mục "6. Missing-value analysis" + "7. Duplicate analysis" |
| `diabetes_03_representation.png` | Mục "12. Data representation": cell `print("=== One raw CSV record ===")` |
| `diabetes_04_split.png` | Mục "14. Train / Validation / Test split" |
| `diabetes_05_training.png` | Mục "17. Model training" (cell bắt đầu `from sklearn.tree import DecisionTreeClassifier`) |
| `diabetes_06_inference.png` | Mục "23. Inference test" (cell cuối `loaded_pipe = joblib.load(...)`) |

### Nhóm B — Biểu đồ EDA và kết quả mô hình (MỚI — cần chụp cả code lẫn hình)
| Tên file | Chụp cell nào | Nội dung biểu đồ |
|---|---|---|
| `01_target_distribution.png` | Mục "10. EDA", cell `sns.countplot(x=TARGET_COL...)` | Phân bố biến mục tiêu |
| `02_bmi_by_target.png` | Cell `sns.histplot(...x="bmi"...)` | Phân bố BMI theo nhóm |
| `03_hba1c_by_target.png` | Cell `sns.histplot(...x="HbA1c_level"...)` | Phân bố HbA1c theo nhóm |
| `04_glucose_by_target.png` | Cell `sns.histplot(...x="blood_glucose_level"...)` | Phân bố đường huyết theo nhóm |
| `05_correlation_matrix.png` | Cell `plt.figure(figsize=(8,6))` + `sns.heatmap(corr...)` | Ma trận tương quan |
| `06_model_comparison.png` | Mục "18. Model comparison", cell `fig, axes = plt.subplots(1, 2, ...)` | So sánh 5 mô hình (ROC-AUC, Recall) |
| `07_confusion_matrix_test.png` | Mục "19. Evaluation", cell `ConfusionMatrixDisplay(...).plot(...)` | Confusion Matrix trên Test |

---
## 2) House Price — mở `A02/house_price/notebook/house_price.ipynb`
Lưu vào `A02/report/images/house_price/`

### Nhóm A
| Tên file | Chụp cell nào |
|---|---|
| `house_01_overview.png` | 2 cell đầu mục "1–2": `df = pd.read_csv(...)` (head) và `df.info()` |
| `house_02_missing.png` | Cell `print("Missing values per column:")` |
| `house_03_cleaning.png` | Mục "3. Data Cleaning": cell `df_clean = df.drop_duplicates()...` và cell `extract_province(...)` |
| `house_04_representation_split.png` | Cell `feature_cols = ...` và cell `train_test_split(...)` |
| `house_05_training.png` | Mục "8. Baseline and Model Training": cell `models = {...}` |
| `house_06_inference.png` | Mục "12. Inference Test" (cell cuối) |

### Nhóm B — MỚI
| Tên file | Chụp cell nào | Nội dung biểu đồ |
|---|---|---|
| `01_price_distribution.png` | Mục "5. EDA", cell `plt.figure(figsize=(7, 4.5))` đầu tiên (histplot Price) | Phân bố giá nhà |
| `02_area_vs_price.png` | Cell `sns.scatterplot(x=X["Area"], y=y...)` | Diện tích vs Giá |
| `03_price_by_legal_status.png` | Cell `sns.boxplot(x=df_clean["Legal status"], y=y...)` | Giá theo pháp lý |
| `04_price_by_province.png` | Cell `sns.barplot(x=avg_price.values, y=avg_price.index...)` | Giá theo tỉnh/thành |
| `05_correlation_matrix.png` | Cell `plt.figure(figsize=(7, 6))` + `sns.heatmap(corr...)` | Ma trận tương quan |
| `06_model_comparison.png` | Mục "8. Baseline and Model Training", cell `plt.figure(figsize=(8, 5))` sau vòng lặp huấn luyện | So sánh 5 mô hình (RMSE) |
| `07_actual_vs_predicted_test.png` | Mục "9. Model Selection...", cell `plt.figure(figsize=(6, 6))` (scatter actual vs predicted) | Giá thực tế vs dự đoán |

---
## 3) E-commerce — mở `A02/ecommerce/notebook/ecommerce.ipynb`
Lưu vào `A02/report/images/ecommerce/`

### Nhóm A
| Tên file | Chụp cell nào |
|---|---|
| `ecom_01_overview.png` | 2 cell đầu mục "1–2": `df = pd.read_csv(...)` (head) và `df.info()` |
| `ecom_02_missing.png` | Cell `print("Missing values per column:")` |
| `ecom_03_cleaning.png` | Mục "3. Data Cleaning": cell `df_clean = df.drop_duplicates()...` |
| `ecom_04_representation_split.png` | Cell `numeric_features = [...]` và cell `idx = np.arange(...)` |
| `ecom_05_training.png` | Mục "8. Baseline and Six Models": cell `models = {...}` và cell TF-IDF |
| `ecom_06_inference.png` | Mục "12. Inference Test" (cell cuối) |

### Nhóm B — MỚI
| Tên file | Chụp cell nào | Nội dung biểu đồ |
|---|---|---|
| `01_target_distribution.png` | Mục "5. EDA", cell `sns.countplot(x=y...)` | Phân bố Recommended IND |
| `02_recommend_by_rating.png` | Cell `ct.plot(kind="bar", stacked=True...)` | Tỉ lệ đề xuất theo Rating |
| `03_review_length_distribution.png` | Cell `sns.histplot(df_clean["Review Length"]...)` | Phân bố độ dài đánh giá |
| `04_reviews_per_department.png` | Cell `sns.barplot(x=top_dept.values, y=top_dept.index...)` | Số đánh giá theo ngành hàng |
| `05_correlation_matrix.png` | Cell `plt.figure(figsize=(6, 5))` + `sns.heatmap(corr...)` | Ma trận tương quan |
| `06_model_comparison.png` | Mục "8. Baseline and Six Models", cell `plt.figure(figsize=(8, 5))` sau vòng lặp | So sánh 6 mô hình (F1) |
| `07_confusion_matrix_test.png` | Mục "9. Model Selection...", cell `ConfusionMatrixDisplay(...)` | Confusion Matrix Test |
| `08_roc_curve_test.png` | Cell `RocCurveDisplay.from_predictions(...)` | Đường cong ROC |

---
**Lưu ý:**
- Không bắt buộc pixel-perfect — miễn nhìn rõ code + kết quả là dùng được.
- Ảnh Web/Mobile (6 ảnh) **không cần chụp** — đã được tôi tự động chụp thật từ API đang chạy
  (Playwright), có sẵn trong `report/images/<app>/<app>_web_ui.png` và `..._mobile_ui.png`.
