import cv2
import mediapipe as mp


class HandTracker:
    def __init__(
        self,
        max_num_hands=1,
        min_detection_confidence=0.7,
    ):
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
        )

    def detect(self, frame):
        rgb_frame = cv2.cvtColor(
            frame, cv2.COLOR_BGR2RGB
        )
        result = self.hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            return result.multi_hand_landmarks[0]

        return None

    def get_fingertip(self, hand_landmarks, width, height):
        landmark = hand_landmarks.landmark[8]

        x = int(landmark.x * width)
        y = int(landmark.y * height)

        return x, y

    def fingers_up(self, hand_landmarks):
        landmarks = hand_landmarks.landmark

        index_up = (
            landmarks[8].y < landmarks[6].y
        )
        middle_up = (
            landmarks[12].y < landmarks[10].y
        )

        return index_up, middle_up

    def close(self):
        self.hands.close()



class PointSmoother:
    def __init__(self, alpha=0.35):
        self.alpha = alpha
        self.previous = None

    def smooth(self, x, y):
        if self.previous is None:
            self.previous = (x, y)
            return x, y

        prev_x, prev_y = self.previous

        smooth_x = int(
            self.alpha * x
            + (1 - self.alpha) * prev_x
        )
        smooth_y = int(
            self.alpha * y
            + (1 - self.alpha) * prev_y
        )

        self.previous = (smooth_x, smooth_y)
        return smooth_x, smooth_y

    def reset(self):
        self.previous = None        