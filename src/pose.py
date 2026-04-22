import cv2
import numpy as np


class HeadPoseEstimator:
    def __init__(self):
        self.model_points = np.array(
            [
                (0.0, 0.0, 0.0),            # Nose tip
                (0.0, -330.0, -65.0),      # Chin
                (-225.0, 170.0, -135.0),   # Left eye corner
                (225.0, 170.0, -135.0),    # Right eye corner
                (-150.0, -150.0, -125.0),  # Left mouth corner
                (150.0, -150.0, -125.0),   # Right mouth corner
            ],
            dtype=np.float64
        )

    def estimate(self, image_points, frame):
        h, w = frame.shape[:2]

        focal_length = float(w)
        center_x = float(w) / 2.0
        center_y = float(h) / 2.0

        camera_matrix = np.array(
            [
                [focal_length, 0.0, center_x],
                [0.0, focal_length, center_y],
                [0.0, 0.0, 1.0]
            ],
            dtype=np.float64
        )

        dist_coeffs = np.zeros((4, 1), dtype=np.float64)

        success, rotation_vector, translation_vector = cv2.solvePnP(
            self.model_points,
            image_points.astype(np.float64),
            camera_matrix,
            dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )

        if not success:
            return 0.0, 0.0

        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)

        angles, _, _, _, _, _ = cv2.RQDecomp3x3(rotation_matrix)

        pitch = float(angles[0])
        yaw = float(angles[1])

        return yaw, pitch