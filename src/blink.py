import math
import time
import pyautogui


class BlinkDetector:
    def __init__(self):
        self.closed_frames = 0

        self.last_left_click = 0
        self.last_right_click = 0
        self.last_blink_time = 0

        self.left_cooldown = 0.45
        self.right_cooldown = 1.0

        self.quick_blink_frames = 2
        self.hold_blink_frames = 10

        self.double_window = 0.55

        self.drag_mode = False

    def distance(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def ear(self, eye):
        horizontal = self.distance(eye[0], eye[3])
        v1 = self.distance(eye[1], eye[5])
        v2 = self.distance(eye[2], eye[4])

        if horizontal == 0:
            return 0

        return (v1 + v2) / (2.0 * horizontal)

    def update(self, left_eye, right_eye):
        left_ear = self.ear(left_eye)
        right_ear = self.ear(right_eye)

        avg_ear = (left_ear + right_ear) / 2.0

        threshold = 0.22
        now = time.time()

        action = None

        if avg_ear < threshold:
            self.closed_frames += 1

            # Long blink = drag toggle
            if self.closed_frames >= self.hold_blink_frames:
                if now - self.last_right_click > self.right_cooldown:

                    if not self.drag_mode:
                        pyautogui.mouseDown()
                        self.drag_mode = True
                        action = "DRAG ON"
                    else:
                        pyautogui.mouseUp()
                        self.drag_mode = False
                        action = "DRAG OFF"

                    self.last_right_click = now
                    self.closed_frames = 0

        else:
            # Eyes reopened
            if self.quick_blink_frames <= self.closed_frames < self.hold_blink_frames:

                # Double blink
                if now - self.last_blink_time < self.double_window:
                    pyautogui.doubleClick()
                    action = "DOUBLE CLICK"

                else:
                    if now - self.last_left_click > self.left_cooldown:
                        pyautogui.click()
                        action = "LEFT CLICK"
                        self.last_left_click = now

                self.last_blink_time = now

            self.closed_frames = 0

        return avg_ear, action