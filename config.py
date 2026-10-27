# ==========================================
# CẤU HÌNH CAMERA VÀ MÀN HÌNH GAME
# ==========================================
CAM_WIDTH = 640        # Độ phân giải camera đầu vào (nhẹ để xử lý cực nhanh)
CAM_HEIGHT = 480

CANVAS_WIDTH = 1280    # Độ phân giải giao diện Game 2D HD
CANVAS_HEIGHT = 720

# ==========================================
# THAM SỐ THUẬT TOÁN XỬ LÝ ẢNH & LÀM MƯỢT
# ==========================================
ALPHA_SMOOTH = 0.45    # Hệ số làm mượt Exponential Moving Average (EMA)
DETECTION_CONF = 0.5   # Độ tin cậy nhận diện bàn tay của MediaPipe
TRACK_CONF = 0.5

# ==========================================
# THAM SỐ VÙNG CẢM ỨNG ÁO (VIRTUAL PAD)
# Giúp người chơi di chuyển tay ở vùng giữa Cam mà vẫn bò tới mép màn hình Game
# ==========================================
PAD_X_MIN, PAD_X_MAX = 100, 500
PAD_Y_MIN, PAD_Y_MAX = 80, 380

# ==========================================
# THAM SỐ THUẬT TOÁN GAME
# ==========================================
SNAKE_INIT_LENGTH = 200     # Chiều dài ban đầu của rắn (pixel)
FOOD_GROWTH = 60            # Độ dài tăng thêm khi ăn 1 quả táo
BODY_COLLISION_DIST = 16    # Ngưỡng khoảng cách va chạm với thân (pixel)
FOOD_EAT_DIST = 35          # Ngưỡng khoảng cách ăn mồi (pixel)