# 3 App Mobile (Flutter, Android) — Assignment 02

3 file `.apk` thật, build sẵn (release, đã ký bằng debug key nên cài trực tiếp được, không cần Play Store):

| File | Ứng dụng | Gọi API (cổng) |
|---|---|---|
| `DiabetesCheck.apk` | Dự đoán bệnh tiểu đường | 8000 |
| `HousePriceCheck.apk` | Dự đoán giá nhà | 8001 |
| `RecommendCheck.apk` | Đề xuất sản phẩm E-commerce (+ phân tích văn bản) | 8002 |

## 1. Cài đặt lên điện thoại Android
1. Copy file `.apk` vào điện thoại (USB, Zalo/Telegram gửi cho chính mình, Google Drive...).
2. Trên điện thoại: bật **Cài đặt từ nguồn không xác định** (Settings → Security → Install unknown apps → cho phép với ứng dụng bạn dùng để mở file, ví dụ Files/Chrome).
3. Mở file `.apk` → Install.

## 2. Chạy 3 API trên máy tính, cho phép truy cập từ điện thoại
Mặc định API chỉ chạy ở `localhost` (127.0.0.1) — điện thoại **không** vào được. Cần chạy với `--host 0.0.0.0`:

```bash
cd A02/diabetes/api    && uvicorn app:app --host 0.0.0.0 --port 8000
cd A02/house_price/api && uvicorn app:app --host 0.0.0.0 --port 8001
cd A02/ecommerce/api   && uvicorn app:app --host 0.0.0.0 --port 8002
```

Tìm IP LAN của máy tính (để nhập vào app):
```powershell
ipconfig   # xem dòng "IPv4 Address" của Wi-Fi, ví dụ 192.168.1.23
```

## 3. Cấu hình app
- Điện thoại và máy tính phải **cùng mạng Wi-Fi**.
- Mở app trên điện thoại → sửa ô **"API Base URL"** ở đầu màn hình thành `http://<IP-máy-tính>:<cổng>` (ví dụ `http://192.168.1.23:8000`) → bấm **Predict**.
- Muốn dùng được từ bất kỳ đâu (không cùng Wi-Fi): deploy API lên cloud (Render/Railway/Fly.io...) rồi nhập URL public vào ô đó thay vì IP LAN.

## 4. Mã nguồn
Toàn bộ mã nguồn Dart nằm ở `A02/<app>/mobile_flutter/lib/main.dart` (1 file, dễ đọc). Muốn build lại:
```bash
cd A02/<app>/mobile_flutter
flutter pub get
flutter build apk --release
```
File kết quả: `build/app/outputs/flutter-apk/app-release.apk`.
