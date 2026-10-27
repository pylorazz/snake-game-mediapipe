import cv2
import numpy as np
import time
from hand_tracking import HandDetector
from snake_game import SnakeGame
from config import (CAM_WIDTH, CAM_HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT, 
                    ALPHA_SMOOTH, DETECTION_CONF, TRACK_CONF, 
                    PAD_X_MIN, PAD_X_MAX, PAD_Y_MIN, PAD_Y_MAX)

# Khởi tạo Camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1) # Giảm đệm dữ liệu triệt tiêu lag

detector = HandDetector(detection_con=DETECTION_CONF, track_con=TRACK_CONF)
game = SnakeGame()

pTime = 0
smooth_x, smooth_y = CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # 1. Lật ảnh gương để di chuyển ngón tay tự nhiên
    frame = cv2.flip(frame, 1)
    frame_hands = detector.find_hands(frame)
    lm_list = detector.find_position(frame_hands)

    game_canvas = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH, 3), np.uint8)

    if len(lm_list) != 0:
        # Lấy tọa độ Landmark 8 (Đầu ngón trỏ) từ MediaPipe
        cam_x, cam_y = lm_list[8][1], lm_list[8][2]

        # THUẬT TOÁN 1: Ánh xạ Vùng An Toàn (Virtual Pad) bằng np.interp
        mapped_x = np.interp(cam_x, (PAD_X_MIN, PAD_X_MAX), (40, CANVAS_WIDTH - 40))
        mapped_y = np.interp(cam_y, (PAD_Y_MIN, PAD_Y_MAX), (40, CANVAS_HEIGHT - 40))

        # THUẬT TOÁN 2: Bộ lọc Exponential Moving Average (EMA) triệt tiêu Jitter
        smooth_x = int(smooth_x + ALPHA_SMOOTH * (mapped_x - smooth_x))
        smooth_y = int(smooth_y + ALPHA_SMOOTH * (mapped_y - smooth_y))
        
        game_canvas = game.update(game_canvas, (smooth_x, smooth_y))
    else:
        # Nếu tạm thời mất dấu tay, giữ nguyên vị trí cũ
        game_canvas = game.update(game_canvas, (smooth_x, smooth_y))

    # Ghép ô Mini-Camera ở góc dưới bên trái
    mini_cam = cv2.resize(frame_hands, (200, 150))
    cv2.rectangle(mini_cam, (0, 0), (200, 150), (0, 255, 200), 2)
    game_canvas[550:700, 20:220] = mini_cam

    # Tính và hiển thị FPS thời gian thực
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
    pTime = cTime
    cv2.putText(game_canvas, f"FPS: {int(fps)}", (1140, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 200), 2)

    cv2.imshow("Hand Tracking Snake Game - 2D Arcade", game_canvas)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        game = SnakeGame()
        smooth_x, smooth_y = CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2

cap.release()
cv2.destroyAllWindows()