import cv2
import mediapipe as mp

class HandDetector:
    """
    Lớp đóng vai trò Input Processor:
    Sử dụng MediaPipe Hand để thu thập tọa độ các mốc khớp (Landmarks) trên bàn tay.
    """
    def __init__(self, mode=False, max_hands=1, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        # Khởi tạo giải pháp MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        """Chuyển ảnh sang RGB và gọi MediaPipe xử lý"""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        # Vẽ khung xương tay lên webcam
        if self.results.multi_hand_landmarks and draw:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img):
        """
        Trích xuất danh sách tọa độ (x, y) dạng pixel của 21 Landmark.
        Trả về mảng lm_list: [[id, x, y], ...]
        """
        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[0]
            h, w, _ = img.shape
            for id, lm in enumerate(my_hand.landmark):
                # Chuyển đổi tọa độ chuẩn hóa (0.0 - 1.0) sang tọa độ Pixel thực tế
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
        return lm_list