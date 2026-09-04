# 3 App Mobile (Flutter, Android) — Assignment 02

3 file `.apk` thật, build sẵn (release, đã ký bằng debug key nên cài trực tiếp được, không cần Play Store).
**Đã cấu hình sẵn API Base URL trỏ tới API thật trên Render** — cài xong là dùng được ngay, không cần localhost/cùng Wi-Fi.

| File | Ứng dụng | API mặc định |
|---|---|---|
| `DiabetesCheck.apk` | Dự đoán bệnh tiểu đường | https://diabetes-api-q1ke.onrender.com |
| `HousePriceCheck.apk` | Dự đoán giá nhà | https://house-price-api-uglg.onrender.com |
| `RecommendCheck.apk` | Đề xuất sản phẩm E-commerce (+ phân tích văn bản) | https://ecommerce-api-0tov.onrender.com |

## 1. Cài đặt lên điện thoại Android
1. Copy file `.apk` vào điện thoại (USB, Zalo/Telegram gửi cho chính mình, Google Drive...).
2. Trên điện thoại: bật **Cài đặt từ nguồn không xác định** (Settings → Security → Install unknown apps → cho phép với ứng dụng bạn dùng để mở file, ví dụ Files/Chrome).
3. Mở file `.apk` → Install → mở app → bấm **Predict** luôn (ô API Base URL đã điền sẵn).

**Lưu ý:** API free trên Render sẽ "ngủ" sau 15 phút không dùng — lần bấm Predict đầu tiên sau đó có thể mất ~30-50s để API "tỉnh dậy", các lần sau nhanh bình thường.

## 2. Muốn trỏ về API khác (vd. chạy local để test)
Mở app → sửa ô **"API Base URL"** ở đầu màn hình thành địa chỉ bạn muốn (ví dụ `http://192.168.1.23:8000` nếu chạy local cùng Wi-Fi) → bấm Predict.

## 3. Mã nguồn
Toàn bộ mã nguồn Dart nằm ở `A02/<app>/mobile_flutter/lib/main.dart` (1 file, dễ đọc). Muốn build lại:
```bash
cd A02/<app>/mobile_flutter
flutter pub get
flutter build apk --release
```
File kết quả: `build/app/outputs/flutter-apk/app-release.apk`.
