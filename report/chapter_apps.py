# -*- coding: utf-8 -*-
"""Writes the per-application chapter (VII / VIII / IX) for a given app."""

APP_INFO = {
    "diabetes": {
        "kaggle_name": "Diabetes Prediction Dataset",
        "kaggle_url": "https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset",
        "problem_type": "Phân loại nhị phân (Classification)",
        "observation": "một bệnh nhân",
        "target_desc": "diabetes — 0: không mắc tiểu đường, 1: thuộc nhóm nguy cơ tiểu đường",
        "raw_shape": "(100.000, 9)",
        "raw_shape_note": "100.000 bệnh nhân, 8 đặc trưng đầu vào và 1 biến mục tiêu.",
        "feature_table": [
            ("gender", "Phân loại", "Giới tính bệnh nhân (Female/Male/Other)"),
            ("age", "Số", "Tuổi bệnh nhân"),
            ("hypertension", "Số (nhị phân)", "Tình trạng tăng huyết áp (0/1)"),
            ("heart_disease", "Số (nhị phân)", "Tình trạng bệnh tim (0/1)"),
            ("smoking_history", "Phân loại", "Tiền sử hút thuốc (6 nhóm)"),
            ("bmi", "Số", "Chỉ số khối cơ thể"),
            ("HbA1c_level", "Số", "Chỉ số HbA1c"),
            ("blood_glucose_level", "Số", "Mức đường huyết"),
            ("diabetes", "Target", "Nhãn tiểu đường (0/1)"),
        ],
        "missing_text": "Bộ dữ liệu không có giá trị thiếu ở bất kỳ cột nào.",
        "dup_text": "Có 3.854 bản ghi trùng lặp hoàn toàn (≈3,85% tổng số bản ghi), được loại "
                    "bỏ bằng drop_duplicates() vì chúng khiến cùng một hồ sơ bệnh nhân xuất hiện "
                    "nhiều lần, làm lệch phân bố dữ liệu và ảnh hưởng đến quá trình huấn luyện.",
        "invalid_text": "Kiểm tra age ≤ 0: không có trường hợp nào. Kiểm tra bmi ngoài khoảng "
                         "[10, 80] (không hợp lý về mặt lâm sàng cho một người còn sống): phát "
                         "hiện 9 bản ghi, được loại bỏ.",
        "outlier_text": "BMI có một số giá trị ngoại lệ cao (>60) nhưng vẫn có thể là các "
                         "trường hợp béo phì nặng thực tế trong lâm sàng nên được giữ lại.",
        "cleaned_shape": "100.000 → sau loại trùng lặp → 96.146 → sau loại giá trị BMI không "
                          "hợp lệ → 96.137 bản ghi.",
        "numeric_cols": ["age", "bmi", "HbA1c_level", "blood_glucose_level", "hypertension",
                          "heart_disease"],
        "categorical_cols": ["gender", "smoking_history"],
        "raw_dim": "96.137 × 8  (N=96.137 bệnh nhân, d=8 đặc trưng đầu vào thô)",
        "encoded_dim": 15,
        "encoded_note": "gender (3 nhóm) và smoking_history (6 nhóm) mở rộng thành các cột "
                         "nhị phân sau One-Hot Encoding, nâng số chiều từ 8 lên 15.",
        "split_text": "Train: (67.293, 8)  —  Validation: (14.423, 8)  —  Test: (14.421, 8)  "
                       "(tỉ lệ 70,0% / 15,0% / 15,0%, chia theo stratified split).",
        "target_dist": "Sau làm sạch: lớp 0 (không tiểu đường) chiếm ≈91,2%, lớp 1 (tiểu đường) "
                        "chiếm ≈8,8% — dữ liệu mất cân bằng rõ rệt.",
        "eda_figs": [
            ("01_target_distribution.png", "Phân bố biến mục tiêu diabetes — mất cân bằng lớp rõ rệt."),
            ("02_bmi_by_target.png", "Phân bố BMI theo nhóm diabetes — nhóm dương có BMI cao hơn."),
            ("03_hba1c_by_target.png", "Phân bố HbA1c theo nhóm diabetes — tách biệt khá rõ quanh ngưỡng lâm sàng."),
            ("04_glucose_by_target.png", "Phân bố đường huyết theo nhóm diabetes."),
            ("05_correlation_matrix.png", "Ma trận tương quan giữa các đặc trưng số và biến mục tiêu."),
        ],
        "models": ["Logistic Regression", "Decision Tree", "Random Forest", "SVM", "KNN"],
        "n_models": 5,
        "criterion": "ROC-AUC trên tập Validation",
        "val_table_headers": ["Model", "Accuracy", "Precision", "Recall", "F1", "ROC-AUC", "Thời gian huấn luyện (s)"],
        "val_table_rows": [
            ["Decision Tree", "0,9707", "0,9840", "0,6785", "0,8032", "0,9745", "0,21"],
            ["Random Forest", "0,9707", "0,9988", "0,6690", "0,8013", "0,9744", "4,25"],
            ["Logistic Regression", "0,9581", "0,8670", "0,6203", "0,7232", "0,9639", "0,22"],
            ["KNN", "0,9592", "0,9535", "0,5645", "0,7091", "0,9460", "0,19"],
            ["SVM", "0,9605", "0,9731", "0,5684", "0,7176", "0,9308", "123,78"],
        ],
        "best_model": "Decision Tree",
        "best_model_reason": "Decision Tree và Random Forest gần như tương đương và vượt trội "
                              "các mô hình còn lại về ROC-AUC trên Validation; Decision Tree "
                              "được chọn vì có ROC-AUC cao nhất (0,9745), đồng thời đơn giản "
                              "hơn và huấn luyện nhanh hơn nhiều so với Random Forest.",
        "test_table_headers": ["Accuracy", "Precision", "Recall", "F1", "ROC-AUC"],
        "test_table_row": ["0,9681", "0,9845", "0,6486", "0,7820", "0,9711"],
        "confusion": "TN=13.136, FP=13, FN=447, TP=825 (trên 14.421 mẫu Test).",
        "error_text": "Mô hình bỏ sót 447 bệnh nhân thực sự mắc tiểu đường (False Negative) "
                       "nhưng chỉ chẩn đoán nhầm 13 người khỏe mạnh (False Positive) — Precision "
                       "rất cao (0,9845) trong khi Recall thấp hơn đáng kể (0,6486). Điều này "
                       "cho thấy mô hình khá thận trọng khi gán nhãn dương tính; trong bối cảnh "
                       "y tế, ngưỡng phân loại có thể được hạ xuống để tăng Recall nếu ưu tiên "
                       "không bỏ sót bệnh nhân, đánh đổi bằng nhiều cảnh báo giả hơn.",
        "final_fig": ("07_confusion_matrix_test.png", "Confusion Matrix của Decision Tree trên tập Test."),
        "cmp_fig": ("06_model_comparison.png", "So sánh 5 mô hình trên tập Validation (ROC-AUC)."),
        "deploy_port": 8000,
        "web_desc": "Form nhập thông tin bệnh nhân (giới tính, tuổi, tăng huyết áp, bệnh tim, "
                     "tiền sử hút thuốc, BMI, HbA1c, đường huyết) → gọi POST /predict → hiển thị "
                     "nhãn dự đoán (No diabetes / Diabetes risk) kèm xác suất tin cậy.",
    },
    "house_price": {
        "kaggle_name": "Vietnam Housing Dataset",
        "kaggle_url": "Dữ liệu tin đăng bất động sản Việt Nam (Kaggle)",
        "problem_type": "Hồi quy (Regression)",
        "observation": "một tin đăng bán nhà/căn hộ",
        "target_desc": "Price — giá bán (đơn vị: tỷ VNĐ)",
        "raw_shape": "(30.229, 12)",
        "raw_shape_note": "30.229 tin đăng bất động sản, 11 đặc trưng đầu vào và 1 biến mục tiêu.",
        "feature_table": [
            ("Area", "Số", "Diện tích (m²)"),
            ("Frontage", "Số", "Chiều rộng mặt tiền (m)"),
            ("Access Road", "Số", "Chiều rộng đường vào (m)"),
            ("Floors", "Số", "Số tầng"),
            ("Bedrooms", "Số", "Số phòng ngủ"),
            ("Bathrooms", "Số", "Số phòng tắm"),
            ("Legal status", "Phân loại", "Tình trạng pháp lý (sổ đỏ / hợp đồng mua bán)"),
            ("Furniture state", "Phân loại", "Tình trạng nội thất"),
            ("House direction", "Phân loại", "Hướng nhà"),
            ("Balcony direction", "Phân loại", "Hướng ban công"),
            ("ProvinceGroup", "Phân loại (trích xuất)", "Tỉnh/thành phố, trích từ cột Address"),
            ("Price", "Target", "Giá bán (tỷ VNĐ)"),
        ],
        "missing_text": "Address và Area, Price không có giá trị thiếu. Các cột còn lại thiếu "
                         "đáng kể: Frontage (38,2%), Access Road (44,0%), House direction "
                         "(70,3%), Balcony direction (82,6%), Floors (11,9%), Bedrooms (17,1%), "
                         "Bathrooms (23,4%), Legal status (14,9%), Furniture state (46,7%) — "
                         "phổ biến với dữ liệu tin đăng bất động sản do người đăng có thể bỏ "
                         "trống các trường tùy chọn.",
        "dup_text": "Không có bản ghi trùng lặp hoàn toàn (0/30.229). Có 261 bản ghi trùng mọi "
                     "cột trừ Address — không bị coi là trùng lặp thật vì đây là các tin đăng "
                     "khác nhau (địa chỉ khác nhau) có thể có cùng đặc điểm căn nhà.",
        "invalid_text": "Kiểm tra Area ≤ 0, Price ≤ 0, Floors ≤ 0, Bedrooms ≤ 0, Bathrooms ≤ 0: "
                         "không phát hiện trường hợp nào không hợp lệ.",
        "outlier_text": "Phương pháp IQR phát hiện outlier ở Area (1.636 bản ghi), Frontage "
                         "(2.305), Access Road (1.110); Price không có outlier (0). Các giá trị "
                         "này được giữ lại vì có thể là các bất động sản diện tích lớn/nhỏ có "
                         "thật, không phải lỗi nhập liệu.",
        "cleaned_shape": "Giữ nguyên 30.229 bản ghi (không loại dòng nào); bổ sung cột "
                          "ProvinceGroup trích xuất từ Address (nhóm 12 tỉnh/thành phố phổ biến "
                          "nhất + nhóm \"Khac\"), và các giá trị phân loại còn thiếu được gán "
                          "nhãn \"Unknown\" thay vì loại bỏ.",
        "numeric_cols": ["Area", "Frontage", "Access Road", "Floors", "Bedrooms", "Bathrooms"],
        "categorical_cols": ["Legal status", "Furniture state", "House direction",
                              "Balcony direction", "ProvinceGroup"],
        "raw_dim": "30.229 × 11  (N=30.229 tin đăng, d=11 đặc trưng đầu vào thô)",
        "encoded_dim": 43,
        "encoded_note": "5 cột phân loại (Legal status, Furniture state, House direction, "
                         "Balcony direction, ProvinceGroup) mở rộng thành nhiều cột nhị phân sau "
                         "One-Hot Encoding, nâng số chiều từ 11 lên 43.",
        "split_text": "Train: (21.160, 11)  —  Validation: (4.534, 11)  —  Test: (4.535, 11)  "
                       "(tỉ lệ 70% / 15% / 15%).",
        "target_dist": "Price dao động từ 1 đến 11,5 tỷ VNĐ, trung bình ≈5,87 tỷ, phân phối gần "
                        "đối xứng quanh giá trị trung tâm (không cần biến đổi log).",
        "eda_figs": [
            ("01_price_distribution.png", "Phân bố giá nhà (tỷ VNĐ)."),
            ("02_area_vs_price.png", "Quan hệ giữa diện tích và giá nhà."),
            ("03_price_by_legal_status.png", "Giá nhà theo tình trạng pháp lý."),
            ("04_price_by_province.png", "Giá nhà trung bình theo tỉnh/thành phố."),
            ("05_correlation_matrix.png", "Ma trận tương quan giữa các đặc trưng số và Price."),
        ],
        "models": ["Linear Regression", "Ridge Regression", "Decision Tree Regressor",
                   "Random Forest Regressor", "Gradient Boosting Regressor"],
        "n_models": 5,
        "criterion": "RMSE trên tập Validation (càng thấp càng tốt)",
        "val_table_headers": ["Model", "MAE", "MSE", "RMSE", "R²", "Thời gian huấn luyện (s)"],
        "val_table_rows": [
            ["Gradient Boosting", "1,2825", "2,6367", "1,6238", "0,4685", "5,86"],
            ["Random Forest", "1,2642", "2,7469", "1,6574", "0,4463", "2,30"],
            ["Decision Tree", "1,3709", "3,0239", "1,7389", "0,3904", "0,07"],
            ["Ridge", "1,4795", "3,3884", "1,8408", "0,3169", "0,02"],
            ["Linear Regression", "1,4794", "3,3884", "1,8408", "0,3169", "0,03"],
        ],
        "best_model": "Gradient Boosting Regressor",
        "best_model_reason": "Gradient Boosting đạt RMSE thấp nhất (1,6238 tỷ VNĐ) và R² cao "
                              "nhất (0,4685) trên tập Validation, vượt trội hai mô hình tuyến "
                              "tính (chỉ đạt R²≈0,32) — cho thấy quan hệ giữa các đặc trưng và "
                              "giá nhà có tính phi tuyến đáng kể.",
        "test_table_headers": ["MAE", "MSE", "RMSE", "R²"],
        "test_table_row": ["1,2479 tỷ", "2,5274", "1,5898 tỷ", "0,4720"],
        "confusion": None,
        "error_text": "R²≈0,47 cho thấy mô hình giải thích được gần một nửa phương sai của giá "
                       "nhà — hợp lý với một bộ dữ liệu chỉ có đặc trưng cấu trúc (không có tọa "
                       "độ chính xác, không có ảnh, không có thông tin nội thất chi tiết). Các "
                       "sai số lớn nhất (tới 6,25 tỷ VNĐ) đều rơi vào những tin đăng có giá lệch "
                       "hẳn so với mức giá kỳ vọng theo diện tích/tỉnh thành — dấu hiệu của các "
                       "yếu tố không quan sát được (vị trí cụ thể, chất lượng hoàn thiện, mức độ "
                       "cấp thiết của người bán).",
        "final_fig": ("07_actual_vs_predicted_test.png", "Gradient Boosting: giá trị thực tế so với giá trị dự đoán trên tập Test."),
        "cmp_fig": ("06_model_comparison.png", "So sánh 5 mô hình trên tập Validation (RMSE)."),
        "deploy_port": 8001,
        "web_desc": "Form nhập đặc điểm căn nhà (diện tích, mặt tiền, đường vào, số tầng, số "
                     "phòng ngủ/tắm, tình trạng pháp lý, nội thất, hướng nhà/ban công, tỉnh "
                     "thành) → gọi POST /predict → hiển thị giá dự đoán (tỷ VNĐ).",
    },
    "ecommerce": {
        "kaggle_name": "Women's Clothing E-Commerce Reviews",
        "kaggle_url": "https://www.kaggle.com/datasets/nicapotato/womens-ecommerce-clothing-reviews",
        "problem_type": "Phân loại nhị phân (Classification)",
        "observation": "một đánh giá (review) của khách hàng về một sản phẩm",
        "target_desc": "Recommended IND — 0: không đề xuất sản phẩm, 1: đề xuất sản phẩm",
        "raw_shape": "(23.486, 10)",
        "raw_shape_note": "23.486 đánh giá, 9 đặc trưng đầu vào (dạng bảng + văn bản) và 1 biến "
                           "mục tiêu (đã loại cột chỉ mục \"Unnamed: 0\").",
        "feature_table": [
            ("Age", "Số", "Tuổi khách hàng"),
            ("Rating", "Số", "Điểm đánh giá sản phẩm (1–5)"),
            ("Positive Feedback Count", "Số", "Số lượng phản hồi \"hữu ích\" cho đánh giá"),
            ("Title", "Văn bản", "Tiêu đề đánh giá"),
            ("Review Text", "Văn bản", "Nội dung đánh giá"),
            ("Division Name", "Phân loại", "Nhóm sản phẩm cấp cao"),
            ("Department Name", "Phân loại", "Ngành hàng"),
            ("Class Name", "Phân loại", "Phân loại chi tiết sản phẩm"),
            ("Recommended IND", "Target", "Khách hàng có đề xuất sản phẩm hay không (0/1)"),
        ],
        "missing_text": "Title thiếu 3.810 dòng (16,2%), Review Text thiếu 845 dòng (3,6%) — "
                         "một số khách hàng chỉ chấm điểm mà không viết nhận xét. Division/"
                         "Department/Class Name mỗi cột thiếu 14 dòng.",
        "dup_text": "Có 21 bản ghi trùng lặp hoàn toàn, được loại bỏ bằng drop_duplicates().",
        "invalid_text": "Kiểm tra Age ≤ 0, Rating ngoài [1,5], Recommended IND ngoài {0,1}, "
                         "Positive Feedback Count < 0: không phát hiện trường hợp nào không hợp lệ.",
        "outlier_text": "Age có 109 giá trị ngoại lệ (ngoài [7, 79]); Positive Feedback Count có "
                         "2.147 giá trị ngoại lệ (ngoài [-4,5, 7,5]) — cả hai đều được giữ lại vì "
                         "phản ánh hành vi khách hàng có thật (khách lớn tuổi, đánh giá được "
                         "nhiều người thấy hữu ích).",
        "cleaned_shape": "23.486 → sau loại trùng lặp → 23.465 → sau loại 14 dòng thiếu thông "
                          "tin nhóm sản phẩm → 23.451 bản ghi.",
        "numeric_cols": ["Age", "Rating", "Positive Feedback Count", "Review Length",
                          "Title Length", "Has Review", "Has Title"],
        "categorical_cols": ["Division Name", "Department Name", "Class Name"],
        "raw_dim": "23.451 × 10  (N=23.451 đánh giá, d=10 đặc trưng dạng bảng)",
        "encoded_dim": 35,
        "encoded_note": "3 cột phân loại sản phẩm mở rộng thành nhiều cột nhị phân sau One-Hot "
                         "Encoding, nâng số chiều từ 10 lên 35. Riêng cột Review Text được biểu "
                         "diễn tách biệt bằng TF-IDF: ma trận (16.415 × 5.000) cho mô hình văn "
                         "bản thứ sáu.",
        "split_text": "Train: (16.415, 10)  —  Validation: (3.518, 10)  —  Test: (3.518, 10)  "
                       "(tỉ lệ 70% / 15% / 15%, chia theo stratified split).",
        "target_dist": "Lớp 1 (đề xuất) chiếm ≈82,2%, lớp 0 (không đề xuất) chiếm ≈17,8% — dữ "
                        "liệu mất cân bằng.",
        "eda_figs": [
            ("01_target_distribution.png", "Phân bố biến mục tiêu Recommended IND."),
            ("02_recommend_by_rating.png", "Tỉ lệ đề xuất theo từng mức Rating."),
            ("03_review_length_distribution.png", "Phân bố độ dài nội dung đánh giá."),
            ("04_reviews_per_department.png", "Số lượng đánh giá theo ngành hàng."),
            ("05_correlation_matrix.png", "Ma trận tương quan giữa Age, Rating, Positive "
             "Feedback Count và Recommended IND."),
        ],
        "models": ["Logistic Regression", "Decision Tree", "Random Forest", "KNN", "SVM",
                   "Text Logistic Regression (TF-IDF trên Review Text)"],
        "n_models": 6,
        "criterion": "F1-score trên tập Validation (do dữ liệu mất cân bằng lớp)",
        "val_table_headers": ["Model", "Accuracy", "Precision", "Recall", "F1", "ROC-AUC"],
        "val_table_rows": [
            ["SVM", "0,9247", "0,9820", "0,9253", "0,9528", "0,9653"],
            ["Logistic Regression", "0,9238", "0,9719", "0,9343", "0,9528", "0,9666"],
            ["Random Forest", "0,9181", "0,9594", "0,9402", "0,9497", "0,9568"],
            ["Decision Tree", "0,9176", "0,9731", "0,9253", "0,9486", "0,9476"],
            ["KNN", "0,9142", "0,9354", "0,9620", "0,9485", "0,9548"],
            ["Text Logistic Regression (TF-IDF)", "0,8778", "0,8908", "0,9703", "0,9288", "0,9168"],
        ],
        "best_model": "SVM (trên biểu diễn dạng bảng)",
        "best_model_reason": "SVM đạt F1 cao nhất trên Validation (0,9528, gần như đồng hạng "
                              "với Logistic Regression). Mô hình văn bản (TF-IDF) tuy vẫn tốt "
                              "hơn nhiều so với baseline nhưng có F1 thấp hơn rõ rệt các mô hình "
                              "dạng bảng — vì vậy mô hình dạng bảng được chọn triển khai chính, "
                              "còn mô hình văn bản được giữ lại như một tính năng phân tích bổ "
                              "sung (\"Analyze with AI\") vì nó cần nội dung đánh giá, thứ chỉ có "
                              "sau khi khách hàng đã viết đánh giá.",
        "test_table_headers": ["Accuracy", "Precision", "Recall", "F1", "ROC-AUC"],
        "test_table_row": ["0,9383", "0,9887", "0,9357", "0,9614", "0,9778"],
        "confusion": "TN=595, FP=31, FN=186, TP=2706 (trên 3.518 mẫu Test).",
        "error_text": "Số lượng False Negative (186 — khách hàng thực sự đề xuất nhưng mô hình "
                       "dự đoán \"không đề xuất\") nhiều hơn False Positive (31), phù hợp với "
                       "Precision (0,9887) cao hơn Recall (0,9357). Mô hình cẩn trọng khi dự "
                       "đoán \"đề xuất\", ưu tiên độ chính xác của dự đoán dương tính.",
        "final_fig": ("07_confusion_matrix_test.png", "Confusion Matrix của SVM trên tập Test."),
        "cmp_fig": ("06_model_comparison.png", "So sánh 6 mô hình trên tập Validation (F1-score)."),
        "extra_fig": ("08_roc_curve_test.png", "Đường cong ROC của SVM trên tập Test."),
        "deploy_port": 8002,
        "web_desc": "Hai phần: (1) form có cấu trúc (tuổi, rating, số phản hồi tích cực, tiêu "
                     "đề/nội dung đánh giá, nhóm sản phẩm) → gọi POST /predict, dùng mô hình SVM "
                     "đã triển khai; (2) ô nhập văn bản tự do → gọi POST /analyze_text, dùng mô "
                     "hình TF-IDF + Logistic Regression để phân tích trực tiếp nội dung đánh giá.",
    },
}

SHOT_FILES = {
    "diabetes": [
        ("diabetes_01_overview.png", "df_raw.head(), df_raw.info(), df_raw.describe() — tổng quan dữ liệu thô."),
        ("diabetes_02_missing_duplicates.png", "Kiểm tra giá trị thiếu và bản ghi trùng lặp."),
        ("diabetes_03_representation.png", "Một bản ghi CSV gốc, vector đặc trưng tương ứng và shape ma trận đặc trưng."),
        ("diabetes_04_split.png", "Kết quả chia tập Train/Validation/Test."),
        ("diabetes_05_training.png", "Vòng lặp huấn luyện 5 mô hình phân loại."),
        ("diabetes_06_inference.png", "Tải lại pipeline đã lưu và dự đoán thử trên một bệnh nhân mới."),
    ],
    "house_price": [
        ("house_01_overview.png", "Đọc dữ liệu CSV và xem trước các dòng đầu, kiểu dữ liệu."),
        ("house_02_missing.png", "Kiểm tra giá trị thiếu theo từng cột."),
        ("house_03_cleaning.png", "Kiểm tra giá trị không hợp lệ, ngoại lệ, và trích xuất ProvinceGroup."),
        ("house_04_representation_split.png", "Shape ma trận đặc trưng X và kết quả chia Train/Validation/Test."),
        ("house_05_training.png", "Vòng lặp huấn luyện 5 mô hình hồi quy."),
        ("house_06_inference.png", "Tải lại pipeline đã lưu và dự đoán thử giá một căn nhà mới."),
    ],
    "ecommerce": [
        ("ecom_01_overview.png", "Đọc dữ liệu CSV và xem trước các dòng đầu, kiểu dữ liệu."),
        ("ecom_02_missing.png", "Kiểm tra giá trị thiếu theo từng cột."),
        ("ecom_03_cleaning.png", "Làm sạch dữ liệu: kiểm tra giá trị không hợp lệ, ngoại lệ, loại bỏ dòng thiếu nhóm sản phẩm."),
        ("ecom_04_representation_split.png", "Shape ma trận đặc trưng X và kết quả chia Train/Validation/Test."),
        ("ecom_05_training.png", "Vòng lặp huấn luyện 5 mô hình dạng bảng + mô hình văn bản TF-IDF thứ sáu."),
        ("ecom_06_inference.png", "Tải lại hai pipeline đã lưu (dạng bảng và văn bản) và dự đoán thử."),
    ],
}


def write_chapter_app(doc, app, meta, add_heading, add_para, add_bullets,
                       add_table, add_figure, add_chart, add_page_break,
                       fmt_pct, fmt_num):
    info = APP_INFO[app]

    add_heading("1. Mô tả bài toán", level=2)
    add_para(
        f"Loại bài toán: {info['problem_type']}. Mỗi quan sát tương ứng với {info['observation']}. "
        f"Biến mục tiêu: {info['target_desc']}."
    )

    add_heading("2. Giới thiệu tập dữ liệu", level=2)
    add_para(f"Nguồn dữ liệu (Kaggle): {info['kaggle_name']} — {info['kaggle_url']}")
    add_para(f"Kích thước dữ liệu gốc: {info['raw_shape']}. {info['raw_shape_note']}")
    add_table(["Đặc trưng", "Loại", "Ý nghĩa"], info["feature_table"])

    add_heading("3. Khảo sát và làm sạch dữ liệu", level=2)
    add_para("Giá trị thiếu: " + info["missing_text"])
    add_para("Dữ liệu trùng lặp: " + info["dup_text"])
    add_para("Giá trị không hợp lệ: " + info["invalid_text"])
    add_para("Phân tích ngoại lệ (IQR): " + info["outlier_text"])
    add_para("Kết quả làm sạch: " + info["cleaned_shape"])
    add_figure(app, SHOT_FILES[app][0][0], SHOT_FILES[app][0][1])
    add_figure(app, SHOT_FILES[app][1][0], SHOT_FILES[app][1][1])
    add_figure(app, SHOT_FILES[app][2][0], SHOT_FILES[app][2][1])

    add_heading("4. Biểu diễn dữ liệu", level=2)
    add_para(f"Đặc trưng số ({len(info['numeric_cols'])}): " + ", ".join(info["numeric_cols"]))
    add_para(f"Đặc trưng phân loại ({len(info['categorical_cols'])}): " + ", ".join(info["categorical_cols"]))
    add_para(f"Ma trận đặc trưng thô: X ∈ ℝ^(N×d), {info['raw_dim']}.")
    add_para(
        f"Sau khi qua ColumnTransformer (StandardScaler cho cột số, OneHotEncoder cho cột "
        f"phân loại), số chiều đầu vào của mô hình tăng lên {info['encoded_dim']}. {info['encoded_note']}"
    )

    add_heading("5. Phân tích khám phá dữ liệu (EDA)", level=2)
    for fname, cap in info["eda_figs"]:
        add_chart(app, fname, cap)
    add_para(f"Phân bố biến mục tiêu: {info['target_dist']}")

    add_heading("6. Xây dựng mô hình", level=2)
    add_para(f"Chia dữ liệu Train/Validation/Test: {info['split_text']}")
    add_figure(app, SHOT_FILES[app][3][0], SHOT_FILES[app][3][1])
    add_para(f"Số mô hình được huấn luyện và so sánh: {info['n_models']}.")
    add_bullets(info["models"])
    add_figure(app, SHOT_FILES[app][4][0], SHOT_FILES[app][4][1])

    add_heading("7. Đánh giá và lựa chọn mô hình", level=2)
    add_para(f"Tiêu chí lựa chọn mô hình trên tập Validation: {info['criterion']}.")
    add_table(info["val_table_headers"], info["val_table_rows"])
    add_chart(app, info["cmp_fig"][0], info["cmp_fig"][1])
    add_para(f"Mô hình được chọn: {info['best_model']}. {info['best_model_reason']}")

    add_heading("8. Đánh giá trên tập Test và phân tích lỗi", level=2)
    add_table(info["test_table_headers"], [info["test_table_row"]])
    if info.get("confusion"):
        add_para("Confusion Matrix (Test): " + info["confusion"])
        add_chart(app, info["final_fig"][0], info["final_fig"][1])
        if info.get("extra_fig"):
            add_chart(app, info["extra_fig"][0], info["extra_fig"][1])
    else:
        add_chart(app, info["final_fig"][0], info["final_fig"][1])
    add_para("Phân tích lỗi: " + info["error_text"])

    add_heading("9. Lưu trữ mô hình", level=2)
    add_para(
        "Pipeline tiền xử lý và mô hình được chọn được đóng gói trong một đối tượng "
        "sklearn.Pipeline duy nhất và lưu bằng joblib (model_pipeline.joblib), cùng với "
        "meta.json chứa danh sách đặc trưng, các lựa chọn hợp lệ của biến phân loại và các "
        "chỉ số đánh giá trên tập Test."
    )
    add_figure(app, SHOT_FILES[app][5][0], SHOT_FILES[app][5][1])

    add_heading("10. Triển khai hệ thống", level=2)
    add_para(
        f"Mô hình được triển khai dưới dạng REST API bằng FastAPI, chạy tại cổng "
        f"{info['deploy_port']} (endpoint POST /predict, và GET /meta để lấy schema đặc trưng)."
    )
    add_para("Giao diện Web: " + info["web_desc"])
    add_para(
        "Giao diện Mobile: cùng chức năng với giao diện Web, được thiết kế dạng một cột phù "
        "hợp màn hình điện thoại, gọi cùng REST API (không chạy mô hình trên thiết bị), có thể "
        "thêm vào màn hình chính của điện thoại qua tệp manifest.json (Progressive Web App)."
    )
