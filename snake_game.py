import cv2
import numpy as np
import random
import math
from config import (CANVAS_WIDTH, CANVAS_HEIGHT, SNAKE_INIT_LENGTH, 
                    FOOD_GROWTH, BODY_COLLISION_DIST, FOOD_EAT_DIST)

class SnakeGame:
    def __init__(self):
        self.points, self.lengths = [], []
        self.current_length = 0   
        self.allowed_length = SNAKE_INIT_LENGTH 
        self.previous_head = (CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
        self.food_point = (0, 0)
        self.random_food_location()
        self.score, self.game_over = 0, False

    def random_food_location(self):
        self.food_point = random.randint(300, 1150), random.randint(120, 600)

    def draw_background(self, img):
        img[:] = (20, 24, 30)
        h, w, _ = img.shape
        for x in range(0, w, 40): cv2.line(img, (x, 0), (x, h), (35, 42, 52), 1)
        for y in range(0, h, 40): cv2.line(img, (0, y), (w, y), (35, 42, 52), 1)
        cv2.rectangle(img, (20, 20), (w - 20, h - 20), (0, 255, 200), 3)

    def draw_apple_2d(self, img, pos):
        x, y = pos
        cv2.circle(img, (x, y), 18, (40, 40, 230), -1)
        cv2.circle(img, (x, y), 18, (0, 0, 0), 2)             
        cv2.circle(img, (x - 6, y - 6), 4, (255, 255, 255), -1) 
        cv2.line(img, (x, y - 18), (x + 4, y - 26), (20, 70, 120), 3)   
        cv2.ellipse(img, (x + 8, y - 24), (8, 4), 30, 0, 360, (50, 200, 50), -1) 

    def draw_snake_head_2d(self, img, head_pos, prev_pos):
        hx, hy = head_pos
        angle = math.atan2(hy - prev_pos[1], hx - prev_pos[0])

        # 1. VẼ LƯỠI RẮN THÂN DÀI VƯƠN XA - KHOÉT TAM GIÁC NÔNG Ở ĐẦU
        def p(r, a_off):
            return [int(hx + r * math.cos(angle + a_off)), int(hy + r * math.sin(angle + a_off))]

        # Chiều dài tổng thể = 42px; Thân thẳng dài tới 32px; Vết khoét nông từ 32px -> 42px
        tongue_poly = np.array([
            p(10, -0.16),   # Gốc lưỡi trái (trong miệng)
            p(42, -0.16),   # Đỉnh chẻ 1 (góc ngoài cùng bên trái)
            p(32, 0.0),     # Vết khoét tam giác nông ở giữa
            p(42, 0.16),    # Đỉnh chẻ 2 (góc ngoài cùng bên phải)
            p(10, 0.16)     # Gốc lưỡi phải (trong miệng)
        ], np.int32)

        # Tô màu đỏ tươi liền khối
        cv2.fillPoly(img, [tongue_poly], (30, 30, 230), cv2.LINE_AA)

        # 2. VẼ ĐẦU RẮN & MẮT
        cv2.circle(img, (hx, hy), 22, (0, 220, 100), -1)
        cv2.circle(img, (hx, hy), 22, (0, 0, 0), 3)

        eye_offset = 11
        for a_off in [-0.65, 0.65]:
            ex = int(hx + eye_offset * math.cos(angle + a_off))
            ey = int(hy + eye_offset * math.sin(angle + a_off))
            cv2.circle(img, (ex, ey), 7, (255, 255, 255), -1)
            cv2.circle(img, (ex, ey), 7, (0, 0, 0), 1)
            p_dx, p_dy = int(2.5 * math.cos(angle)), int(2.5 * math.sin(angle))
            cv2.circle(img, (ex + p_dx, ey + p_dy), 3, (0, 0, 0), -1)

    def draw_game_over_centered(self, img):
        cx, cy = CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2
        cv2.rectangle(img, (cx - 340, cy - 160), (cx + 340, cy + 160), (15, 18, 24), -1)
        cv2.rectangle(img, (cx - 340, cy - 160), (cx + 340, cy + 160), (0, 0, 255), 3)

        lines = [
            ("GAME OVER", cv2.FONT_HERSHEY_DUPLEX, 2.0, (0, 0, 255), 4, -65),
            (f"TOTAL SCORE: {self.score}", cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2, 15),
            ("Press 'R' to Restart | 'Q' to Quit", cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, 80)
        ]
        for text, font, scale, color, thick, off_y in lines:
            (tw, th), _ = cv2.getTextSize(text, font, scale, thick)
            cv2.putText(img, text, (cx - tw // 2, cy + off_y + th // 2), font, scale, color, thick, cv2.LINE_AA)

    def update(self, img_main, current_head):
        self.draw_background(img_main)
        if self.game_over:
            self.draw_game_over_centered(img_main)
            return img_main

        px, py = self.previous_head
        cx, cy = current_head
        distance = math.hypot(cx - px, cy - py)

        if distance > 4:
            self.points.append([cx, cy])
            self.lengths.append(distance)
            self.current_length += distance
            self.previous_head = (cx, cy)

            while self.current_length > self.allowed_length and self.lengths:
                self.current_length -= self.lengths.pop(0)
                self.points.pop(0)

        rx, ry = self.food_point
        if math.hypot(cx - rx, cy - ry) < FOOD_EAT_DIST:
            self.random_food_location()
            self.allowed_length += FOOD_GROWTH
            self.score += 1

        total_pts = len(self.points)
        if total_pts > 0:
            for i in range(1, total_pts):
                pt1, pt2 = tuple(self.points[i - 1]), tuple(self.points[i])
                cv2.line(img_main, pt1, pt2, (0, 0, 0), 22)
                cv2.line(img_main, pt1, pt2, (0, 200, 80), 16)

            for i in range(0, total_pts, 3):
                pt = tuple(self.points[i])
                radius = int(14 * (i / total_pts)) + 4
                cv2.circle(img_main, pt, radius, (0, 230, 110), -1)
                cv2.circle(img_main, pt, radius, (0, 0, 0), 1)

            if total_pts > 3:
                self.draw_snake_head_2d(img_main, (cx, cy), tuple(self.points[-3]))
        else:
            cv2.circle(img_main, (cx, cy), 22, (0, 220, 100), -1)

        self.draw_apple_2d(img_main, self.food_point)

        if self.score > 0 and total_pts > 20:
            for pt in self.points[:-12]:
                if math.hypot(cx - pt[0], cy - pt[1]) < BODY_COLLISION_DIST:
                    self.game_over = True

        cv2.rectangle(img_main, (40, 40), (280, 95), (15, 18, 24), -1)
        cv2.rectangle(img_main, (40, 40), (280, 95), (0, 255, 200), 2)
        cv2.putText(img_main, f"SCORE: {self.score}", (60, 80), cv2.FONT_HERSHEY_DUPLEX, 1.1, (255, 255, 255), 2)

        return img_main