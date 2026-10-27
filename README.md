# 🐍 Hand Tracking Snake Game 2D (OpenCV & MediaPipe)

Trò chơi Rắn săn mồi 2D được điều khiển trực tiếp bằng cử chỉ ngón tay thời gian thực thông qua Webcam, sử dụng thư viện OpenCV và MediaPipe.

Hướng dẫn Sử dụng & Điều khiển
1. Cách chơi:
   - Đưa bàn tay lên trước Webcam, sử dụng Đầu ngón trỏ để điều khiển Đầu rắn di chuyển trên màn hình.
   - Điều khiển đầu rắn chạm vào Quả táo đỏ để ăn mồi (điểm số tăng +1 và chiều dài rắn tăng thêm).
   - Xử thua (Game Over): Khi đầu rắn đâm vào các đốt thân phía sau.
2. Thao tác phím bấm:
   - R: Chơi lại ván mới khi bị Game Over (Restart game).
   - Q: Thoát chương trình (Quit).
---

## 🛠 1. Danh sách Thư viện & Yêu cầu Hệ thống
- **Ngôn ngữ:** Python 3.8+
- **Các thư viện phụ thuộc chính:**
  - `opencv-python`: Xử lý hình ảnh, vẽ đồ họa canvas 2D và mở luồng Webcam.
  - `mediapipe`: Nhận diện và theo dõi tọa độ mốc ngón tay (Landmarks) thời gian thực.
  - `numpy`: Ánh xạ vùng cảm ứng (Virtual Pad) và tính toán tọa độ làm mượt.

---
## 🚀 2. Hướng dẫn Cài đặt & Chạy Chương trình

### Cách 1: Tải trực tiếp file ZIP (Dành cho người dùng phổ thông)
1. Truy cập vào trang GitHub của dự án và chọn nút màu xanh **Code** -> Chọn **Download ZIP**.
2. Giải nén file `.zip` vừa tải về trên máy tính.
3. Mở thư mục vừa giải nén bằng **VS Code** (hoặc trình soạn thảo Python bất kỳ).
4. Mở **Terminal** trong VS Code (phím tắt `Ctrl + ` `) và chạy lệnh cài đặt thư viện:
```text
pip install -r requirements.txt
```
5. Khởi chạy game bằng lệnh:
```text
python main.py
```

---

### Cách 2: Sử dụng Git Clone (Dành cho lập trình viên)
1. Mở Terminal / Command Prompt trên máy tính và gõ lệnh:
```text
git clone https://github.com/pylorazz/snake-game-mediapipe
```
2. Di chuyển vào thư mục dự án:
```text
cd snake-game-mediapipe
```
3. Cài đặt các thư viện phụ thuộc:
```text
pip install -r requirements.txt
```
4. Khởi chạy game bằng lệnh:
```text
python main.py
```
