# -*- coding: utf-8 -*-
"""Topic-first report sections (1..10), each spanning all three applications.

This organization follows the assignment's own required Report Structure
(Part I-XII / "Report Structure" list: Introduction -> Data sources -> Data
understanding -> Representation -> Preprocessing/EDA -> Model development ->
Evaluation -> Deployment -> Discussion -> Conclusion) rather than writing one
long chapter per application.
"""
from chapter_apps import APP_INFO, SHOT_FILES
from qa_data import QA_15, QA_ECOMMERCE_EXTRA

APP_ORDER = ["diabetes", "house_price", "ecommerce"]
APP_LABEL = {"diabetes": "Diabetes", "house_price": "House Price", "ecommerce": "E-commerce"}


def section_1(doc, H):
    add_heading, add_para, add_bullets = H["heading"], H["para"], H["bullets"]
    add_heading("1. Đặt vấn đề và mục tiêu", level=1)
    add_para(
        "Assignment 02 yêu cầu xây dựng ba hệ thống thông minh hoàn chỉnh — dự đoán bệnh tiểu "
        "đường, dự đoán giá nhà, và phân tích hành vi khách hàng thương mại điện tử — nhằm minh "
        "họa nguyên tắc trung tâm của Lecture 02: "
    )
    add_para("Dữ liệu thực tế → Biểu diễn số → Mô hình tính toán", bold=True)
    add_para(
        "và của Assignment 02: Raw Data → Understand → Clean → Represent → Learn → Evaluate → "
        "Persist → Deploy. Báo cáo này không dừng lại ở việc huấn luyện ba mô hình, mà trình "
        "bày đầy đủ cách dữ liệu thô của mỗi bộ dữ liệu được biến đổi thành một biểu diễn số "
        "(vector/ma trận đặc trưng, hoặc token/TF-IDF đối với văn bản) mà mô hình học máy có "
        "thể xử lý, sau đó được đóng gói và triển khai thành dịch vụ Web/Mobile có thể dùng lại."
    )
    add_bullets([
        "Hiểu và phân tích ba bộ dữ liệu thực tế lấy từ Kaggle.",
        "Biểu diễn dữ liệu bảng thành X ∈ ℝ^(N×d); biểu diễn văn bản đánh giá khách hàng thành "
        "vector TF-IDF (Text → Tokens → Token IDs → Vector).",
        "Tiền xử lý có hệ thống, tái lập được, không rò rỉ dữ liệu.",
        "So sánh nhiều mô hình học máy cho mỗi bài toán (5/5/6 mô hình) và chọn mô hình triển khai.",
        "Lưu trữ mô hình + pipeline, triển khai thành REST API, giao diện Web và Mobile.",
    ])


def section_2(doc, META, H):
    add_heading, add_para, add_table = H["heading"], H["para"], H["table"]
    add_heading("2. Nguồn dữ liệu và định nghĩa bài toán", level=1)
    rows = []
    for app in APP_ORDER:
        info = APP_INFO[app]
        n = META[app].get("feature_cols") and len(META[app]["feature_cols"])
        rows.append([APP_LABEL[app], info["raw_shape"].strip("()").split(",")[0],
                     str(n), META[app]["target_col"]])
    add_para("Bảng tổng hợp ba ứng dụng (theo yêu cầu Part I của đề bài):")
    add_table(["Application", "Rows", "Features", "Target"], rows)

    for app in APP_ORDER:
        info = APP_INFO[app]
        add_heading(f"2.{APP_ORDER.index(app)+1}. {APP_LABEL[app]}", level=2)
        add_para(f"Nguồn Kaggle: {info['kaggle_name']} — {info['kaggle_url']}")
        add_para(
            f"Loại bài toán: {info['problem_type']}. Một observation = {info['observation']}. "
            f"X = {'đặc trưng bệnh nhân' if app=='diabetes' else 'đặc trưng căn nhà' if app=='house_price' else 'đặc trưng hành vi + văn bản đánh giá khách hàng'}, "
            f"y = {info['target_desc']}."
        )


def section_3(doc, H):
    add_heading, add_para, add_table, add_figure = H["heading"], H["para"], H["table"], H["figure"]
    add_heading("3. Khảo sát và chất lượng dữ liệu", level=1)
    add_para(
        "Cả ba bộ dữ liệu được khảo sát theo cùng bộ tiêu chí: df.shape, df.info(), "
        "df.describe(), df.isna().sum(), df.duplicated().sum(), giá trị không hợp lệ, ngoại lệ "
        "(IQR) và mất cân bằng lớp (nếu có)."
    )
    rows = []
    for app in APP_ORDER:
        info = APP_INFO[app]
        rows.append([APP_LABEL[app], info["raw_shape"], info["missing_text"][:70] + "…",
                     info["dup_text"][:60] + "…"])
    add_table(["Ứng dụng", "Kích thước gốc", "Giá trị thiếu (tóm tắt)", "Trùng lặp (tóm tắt)"], rows)

    for app in APP_ORDER:
        info = APP_INFO[app]
        add_heading(f"3.{APP_ORDER.index(app)+1}. {APP_LABEL[app]}", level=2)
        add_para("Giá trị thiếu: " + info["missing_text"])
        add_para("Trùng lặp: " + info["dup_text"])
        add_para("Giá trị không hợp lệ: " + info["invalid_text"])
        add_para("Ngoại lệ (IQR): " + info["outlier_text"])
        add_para("Kết quả làm sạch: " + info["cleaned_shape"])
        add_figure(app, SHOT_FILES[app][0][0], SHOT_FILES[app][0][1])
        add_figure(app, SHOT_FILES[app][1][0], SHOT_FILES[app][1][1])


def section_4(doc, H):
    add_heading, add_para, add_table, add_figure = H["heading"], H["para"], H["table"], H["figure"]
    add_heading("4. Biểu diễn dữ liệu", level=1)
    add_para(
        "Đây là phần trọng tâm của Assignment 02 (liên hệ trực tiếp Lecture 02). Bảng dưới đây "
        "là bảng tóm tắt biểu diễn dữ liệu bắt buộc theo đề bài:"
    )
    add_table(
        ["Application", "Raw form", "Numerical representation", "Model input"],
        [
            ["Diabetes", "CSV / bảng", "Feature vector / matrix (One-Hot + StandardScaler)", "(batch, 15)"],
            ["House Price", "CSV / bảng", "Encoded feature matrix (One-Hot + StandardScaler)", "(batch, 43)"],
            ["E-commerce", "CSV + bình luận khách hàng", "Tabular feature vectors + TF-IDF text vectors",
             "(batch, 35) và/hoặc (batch, 5000)"],
        ],
    )
    for app in APP_ORDER:
        info = APP_INFO[app]
        add_heading(f"4.{APP_ORDER.index(app)+1}. {APP_LABEL[app]}", level=2)
        add_para(f"Đặc trưng số ({len(info['numeric_cols'])}): " + ", ".join(info["numeric_cols"]))
        add_para(f"Đặc trưng phân loại ({len(info['categorical_cols'])}): " + ", ".join(info["categorical_cols"]))
        add_para(f"Ma trận đặc trưng thô: {info['raw_dim']}.")
        add_para(
            f"Sau ColumnTransformer, số chiều đầu vào mô hình tăng lên {info['encoded_dim']}. "
            f"{info['encoded_note']}"
        )
        add_figure(app, SHOT_FILES[app][2][0], SHOT_FILES[app][2][1])
    add_para(
        "Riêng E-commerce: nội dung Review Text được biểu diễn theo sơ đồ Text → Tokens → "
        "Token IDs → Vector bằng TfidfVectorizer (unigram+bigram, tối đa 5.000 token), tạo ra "
        "ma trận thưa (16.415 × 5.000) dùng cho mô hình phân loại văn bản thứ sáu."
    )


def section_5(doc, H):
    add_heading, add_para, add_figure = H["heading"], H["para"], H["figure"]
    add_heading("5. Tiền xử lý và phân tích khám phá dữ liệu (EDA)", level=1)
    add_para(
        "Pipeline tiền xử lý dùng chung một cấu trúc ColumnTransformer cho cả ba ứng dụng: "
        "nhánh số (SimpleImputer trung vị + StandardScaler), nhánh phân loại (SimpleImputer "
        "giá trị phổ biến nhất + OneHotEncoder(handle_unknown=\"ignore\")). Pipeline được "
        "fit() duy nhất trên tập Train và transform() trên Validation/Test — không có thao tác "
        "tiền xử lý nào được fit lại trên dữ liệu ngoài tập Train, tránh Data Leakage."
    )
    for app in APP_ORDER:
        info = APP_INFO[app]
        add_heading(f"5.{APP_ORDER.index(app)+1}. {APP_LABEL[app]}", level=2)
        for fname, cap in info["eda_figs"]:
            add_figure(app, fname, cap)
        add_para(f"Phân bố biến mục tiêu: {info['target_dist']}")


def section_6(doc, H):
    add_heading, add_para, add_bullets, add_figure = H["heading"], H["para"], H["bullets"], H["figure"]
    add_heading("6. Xây dựng mô hình", level=1)
    add_para(
        "Mỗi ứng dụng có một mô hình baseline: DummyClassifier(strategy=\"most_frequent\") cho "
        "hai bài toán phân loại, DummyRegressor(strategy=\"mean\") cho bài toán hồi quy — dùng "
        "làm mốc để đánh giá mức độ hữu ích thực sự của các mô hình học máy."
    )
    for app in APP_ORDER:
        info = APP_INFO[app]
        add_heading(f"6.{APP_ORDER.index(app)+1}. {APP_LABEL[app]} ({info['n_models']} mô hình)", level=2)
        add_bullets(info["models"])
        add_para(f"Chia dữ liệu: {info['split_text']}")
        add_figure(app, SHOT_FILES[app][3][0], SHOT_FILES[app][3][1])
        add_figure(app, SHOT_FILES[app][4][0], SHOT_FILES[app][4][1])


def section_7(doc, H):
    add_heading, add_para, add_table, add_figure = H["heading"], H["para"], H["table"], H["figure"]
    add_heading("7. Đánh giá và so sánh mô hình", level=1)
    for app in APP_ORDER:
        info = APP_INFO[app]
        add_heading(f"7.{APP_ORDER.index(app)+1}. {APP_LABEL[app]}", level=2)
        add_para(f"Tiêu chí chọn mô hình trên Validation: {info['criterion']}.")
        add_table(info["val_table_headers"], info["val_table_rows"])
        add_figure(app, info["cmp_fig"][0], info["cmp_fig"][1])
        add_para(f"Mô hình được chọn: {info['best_model']}. {info['best_model_reason']}")
        add_para("Kết quả trên tập Test:")
        add_table(info["test_table_headers"], [info["test_table_row"]])
        if info.get("confusion"):
            add_para("Confusion Matrix (Test): " + info["confusion"])
        add_figure(app, info["final_fig"][0], info["final_fig"][1])
        if info.get("extra_fig"):
            add_figure(app, info["extra_fig"][0], info["extra_fig"][1])
        add_para("Phân tích lỗi: " + info["error_text"])


def section_8(doc, H):
    add_heading, add_para, add_table, add_figure = H["heading"], H["para"], H["table"], H["figure"]
    add_heading("8. Triển khai Web và Mobile", level=1)
    add_para(
        "Kiến trúc triển khai dùng chung cho cả ba hệ thống: Web/Mobile UI → REST API "
        "(FastAPI) → Validation → Pipeline tiền xử lý đã lưu → Mô hình đã lưu → Kết quả dự "
        "đoán → Web/Mobile UI. Mobile không chạy mô hình trên thiết bị; nó chỉ là client gọi "
        "cùng REST API như giao diện Web."
    )
    add_table(
        ["Ứng dụng", "Cổng API", "Endpoint chính", "Ghi chú"],
        [
            ["Diabetes", "8000", "POST /predict", "Trả nhãn + xác suất"],
            ["House Price", "8001", "POST /predict", "Trả giá dự đoán (tỷ VNĐ)"],
            ["E-commerce", "8002", "POST /predict, POST /analyze_text", "Thêm endpoint phân tích văn bản tự do"],
        ],
    )
    add_para(
        "Các ảnh dưới đây là ảnh chụp THẬT (chụp tự động bằng Playwright, gửi request thật đến "
        "API đang chạy) — không phải ảnh dựng, thể hiện đúng dữ liệu nhập và kết quả trả về."
    )
    for app in APP_ORDER:
        info = APP_INFO[app]
        add_heading(f"8.{APP_ORDER.index(app)+1}. {APP_LABEL[app]}", level=2)
        add_para(info["web_desc"])
        add_figure(app, f"{app}_web_ui.png", f"Giao diện Web {APP_LABEL[app]} — kết quả dự đoán thật từ API.")
        add_figure(app, f"{app}_mobile_ui.png", f"Giao diện Mobile {APP_LABEL[app]} (khung điện thoại) — cùng API.")
        add_figure(app, SHOT_FILES[app][5][0], SHOT_FILES[app][5][1])


def section_9(doc, H):
    add_heading, add_para, add_table = H["heading"], H["para"], H["table"]
    add_heading("9. Thảo luận", level=1)
    add_para(
        "Mục này trả lời đầy đủ 15 câu hỏi thảo luận bắt buộc cho mỗi ứng dụng (tổng 45 câu) và "
        "6 câu hỏi bổ sung dành riêng cho ứng dụng E-commerce, trình bày dạng bảng để súc tích."
    )
    for app in APP_ORDER:
        add_heading(f"9.{APP_ORDER.index(app)+1}. {APP_LABEL[app]}", level=2)
        rows = [[f"{i+1}. {q}", a] for i, (q, a) in enumerate(QA_15[app])]
        add_table(["Câu hỏi", "Trả lời"], rows)

    add_heading("9.4. Câu hỏi bổ sung cho E-commerce", level=2)
    rows = [[f"{i+1}. {q}", a] for i, (q, a) in enumerate(QA_ECOMMERCE_EXTRA)]
    add_table(["Câu hỏi", "Trả lời"], rows)

    add_heading("9.5. So sánh chéo ba hệ thống", level=2)
    add_table(
        ["Khía cạnh", "Diabetes", "House Price", "E-commerce"],
        [
            ["Loại bài toán", "Phân loại", "Hồi quy", "Phân loại"],
            ["Observation", "Bệnh nhân", "Tin đăng nhà", "Đánh giá sản phẩm"],
            ["Target", "diabetes (0/1)", "Price (tỷ VNĐ)", "Recommended IND (0/1)"],
            ["Biểu diễn đầu vào", "Vector 15 chiều", "Vector 43 chiều", "Vector 35 chiều + TF-IDF 5.000 chiều"],
            ["Vấn đề chất lượng dữ liệu chính", "Trùng lặp (3,85%)", "Thiếu dữ liệu diện rộng (>80% ở một số cột)", "Thiếu văn bản đánh giá (~16%)"],
            ["Mô hình tốt nhất", "Decision Tree", "Gradient Boosting", "SVM"],
            ["Độ đo chính", "ROC-AUC / F1", "RMSE / R²", "F1"],
            ["Triển khai Web", "Có", "Có", "Có"],
            ["Triển khai Mobile", "Có", "Có", "Có"],
            ["Hạn chế chính", "Recall thấp hơn Precision (bỏ sót một số ca dương tính)",
             "R² vừa phải do thiếu tọa độ địa lý chi tiết", "Mô hình văn bản kém hơn mô hình dạng bảng"],
        ],
    )


def section_10(doc, H):
    add_heading, add_para, add_bullets = H["heading"], H["para"], H["bullets"]
    add_heading("10. Kết luận", level=1)
    add_para(
        "Ba hệ thống được xây dựng theo cùng một khung phát triển (Data → Understand → Clean → "
        "Represent → Learn → Evaluate → Persist → Deploy), chứng minh rằng một hệ thống thông "
        "minh triển khai được không chỉ là một mô hình học máy, mà là sự kết hợp giữa dữ liệu, "
        "biểu diễn dữ liệu, quá trình học, đánh giá, phần mềm và tương tác người dùng."
    )
    add_bullets([
        "Bài học kỹ thuật quan trọng nhất: chất lượng hệ thống phụ thuộc nhiều vào cách biểu "
        "diễn dữ liệu (số chiều, mã hóa, chuẩn hóa) trước khi vào mô hình.",
        "Thách thức lớn nhất: xử lý dữ liệu thiếu quy mô lớn (cột House direction thiếu >70%) "
        "mà không mất quá nhiều thông tin.",
        "Vấn đề biểu diễn đáng chú ý nhất: kết hợp dữ liệu bảng với văn bản tự do (E-commerce), "
        "cần hai đường ống song song (ColumnTransformer và TfidfVectorizer).",
        "Bài học ML: mô hình phức tạp hơn không luôn tốt hơn — Decision Tree đơn giản ngang "
        "Random Forest ở Diabetes; mô hình cây vượt trội mô hình tuyến tính ở House Price do "
        "quan hệ phi tuyến.",
        "Bài học triển khai: đóng gói pipeline tiền xử lý cùng mô hình trong một đối tượng duy "
        "nhất là cách hiệu quả nhất để đảm bảo nhất quán train/inference, tránh rò rỉ dữ liệu.",
        "Hướng cải tiến: bổ sung tọa độ địa lý cho bài toán giá nhà; thử kết hợp đồng thời đặc "
        "trưng bảng và văn bản trong một mô hình duy nhất cho E-commerce.",
    ])
