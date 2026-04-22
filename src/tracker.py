import cv2
import mediapipe as mp
import threading
import time

from mouse_control import MouseController
from blink import BlinkDetector


class FaceTracker:
    def __init__(self):
        self.running = False
        self.thread = None

        self.mouse = MouseController()
        self.blink = BlinkDetector()

        self.mp_face_mesh = mp.solutions.face_mesh

        self.base_x = None
        self.base_y = None

        self.prev_dx = 0
        self.prev_dy = 0

        self.calibrated = False
        self.paused = False

    def start(self):
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def smooth(self, current, previous, factor=0.82):
        return previous * factor + current * (1 - factor)

    def accelerate(self, value):
        sign = 1 if value >= 0 else -1
        value = abs(value)

        if value < 4:
            return 0

        return sign * int((value ** 1.25) * 0.35)

    def calibrate(self, center_x, center_y):
        self.base_x = center_x
        self.base_y = center_y
        self.calibrated = True

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        start_time = None

        with self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as face_mesh:

            while self.running:
                success, frame = cap.read()

                if not success:
                    continue

                frame = cv2.flip(frame, 1)

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(rgb)

                status = ""

                if results.multi_face_landmarks:
                    face = results.multi_face_landmarks[0]
                    lm = face.landmark

                    h, w, _ = frame.shape

                    face_ids = [
                        10, 338, 297, 332, 284,
                        251, 389, 356, 454, 323,
                        361, 288, 397, 365, 379,
                        378, 400, 377, 152, 148,
                        176, 149, 150, 136, 172,
                        58, 132, 93, 234, 127,
                        162, 21, 54, 103, 67, 109
                    ]

                    xs = [int(lm[i].x * w) for i in face_ids]
                    ys = [int(lm[i].y * h) for i in face_ids]

                    min_x = min(xs)
                    max_x = max(xs)
                    min_y = min(ys)
                    max_y = max(ys)

                    center_x = (min_x + max_x) // 2
                    center_y = (min_y + max_y) // 2

                    # ---------------- CALIBRATION ----------------
                    if not self.calibrated:

                        if start_time is None:
                            start_time = time.time()

                        elapsed = time.time() - start_time
                        remain = max(0, 3 - int(elapsed))

                        status = f"Calibrating... {remain}"

                        if elapsed >= 3:
                            self.calibrate(center_x, center_y)

                    # ---------------- PAUSED ----------------
                    elif self.paused:
                        status = "PAUSED (SPACE)"

                    # ---------------- ACTIVE ----------------
                    else:
                        shift_x = center_x - self.base_x
                        shift_y = center_y - self.base_y

                        dx = self.accelerate(-shift_x * 0.60)
                        dy = self.accelerate(-shift_y * 0.55)

                        dx = int(self.smooth(dx, self.prev_dx))
                        dy = int(self.smooth(dy, self.prev_dy))

                        self.prev_dx = dx
                        self.prev_dy = dy

                        self.mouse.move_relative(dx, dy)

                        # Eye points
                        left_ids = [33, 160, 158, 133, 153, 144]
                        right_ids = [362, 385, 387, 263, 373, 380]

                        left_eye = [
                            (int(lm[i].x * w), int(lm[i].y * h))
                            for i in left_ids
                        ]

                        right_eye = [
                            (int(lm[i].x * w), int(lm[i].y * h))
                            for i in right_ids
                        ]

                        ear, action = self.blink.update(left_eye, right_eye)

                        status = f"EAR:{ear:.2f}"

                        if action:
                            status = action

                    # Draw face box
                    cv2.rectangle(
                        frame,
                        (min_x, min_y),
                        (max_x, max_y),
                        (0, 255, 0),
                        2
                    )

                    cv2.circle(
                        frame,
                        (center_x, center_y),
                        5,
                        (0, 255, 0),
                        -1
                    )

                    cv2.putText(
                        frame,
                        status,
                        (10, 35),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 255),
                        2
                    )

                cv2.imshow("FaceMouse AI Camera", frame)

                key = cv2.waitKey(1) & 0xFF

                if key == 27:
                    self.running = False
                    break

                elif key == ord("r"):
                    self.calibrated = False
                    start_time = None

                elif key == 32:
                    if self.calibrated:
                        self.paused = not self.paused

        cap.release()
        cv2.destroyAllWindows()