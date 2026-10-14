
import cv2

from config import (
    CAMERA_INDEX,
    MAX_NUM_HANDS,
    MIN_DETECTION_CONFIDENCE,
    BRUSH_COLOR,
    BRUSH_THICKNESS,
    ERASER_RADIUS,
    FINGERTIP_RADIUS,
    WINDOW_NAME,
    CLEAR_KEY,
    QUIT_KEY,
    SAVE_KEY,
    INCREASE_BRUSH_KEY,
    DECREASE_BRUSH_KEY,
    INCREASE_ERASER_KEY,
    DECREASE_ERASER_KEY,
)

from hand_tracker import HandTracker
from gesture_controller import GestureController
from drawing_canvas import DrawingCanvas
from smoothing import PointSmoother


def main():
    tracker = HandTracker(
        max_num_hands=MAX_NUM_HANDS,
        min_detection_confidence=MIN_DETECTION_CONFIDENCE,
    )

    smoother = PointSmoother(alpha=0.35)
    controller = GestureController()

    drawing = DrawingCanvas(
        brush_color=BRUSH_COLOR,
        brush_thickness=BRUSH_THICKNESS,
        eraser_radius=ERASER_RADIUS,
    )

    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        tracker.close()
        raise RuntimeError("Could not open webcam.")

    try:
        while True:
            success, frame = cap.read()

            if not success:
                break

            frame = cv2.flip(frame, 1)
            height, width = frame.shape[:2]

            if drawing.canvas is None:
                drawing.initialize(height, width)

            hand = tracker.detect(frame)

            if hand is not None:
                # Get current fingertip coordinates
                x, y = tracker.get_fingertip(
                    hand, width, height
                )

                # Smooth fingertip movement
                x, y = smoother.smooth(x, y)

                index_up, middle_up = tracker.fingers_up(
                    hand
                )

                gesture = controller.recognize(
                    index_up, middle_up
                )

                cv2.circle(
                    frame,
                    (x, y),
                    FINGERTIP_RADIUS,
                    (255, 0, 255),
                    cv2.FILLED,
                )

                if gesture == controller.WRITE:
                    drawing.draw(x, y)

                elif gesture == controller.ERASE:
                    drawing.erase(x, y)
                    smoother.reset()

                else:
                    drawing.reset_position()
                    smoother.reset()

            else:
                drawing.reset_position()
                smoother.reset()

            frame = drawing.overlay(frame)

            cv2.imshow(WINDOW_NAME, frame)
            
            
            key = cv2.waitKey(1) & 0xFF

            # Clear the canvas
            if key == CLEAR_KEY:
                drawing.clear()
                smoother.reset()

            # Save the drawing
            elif key == SAVE_KEY:
                saved = drawing.save("drawing.png")
                print(
                    "Drawing saved as drawing.png"
                    if saved else "Failed to save drawing"
                )

            # Increase brush thickness
            elif key == INCREASE_BRUSH_KEY:
                drawing.brush_thickness = min(
                    drawing.brush_thickness + 1, 30
                )
                print("Brush thickness:", drawing.brush_thickness)

            # Decrease brush thickness
            elif key == DECREASE_BRUSH_KEY:
                drawing.brush_thickness = max(
                    drawing.brush_thickness - 1, 1
                )
                print("Brush thickness:", drawing.brush_thickness)

            # Increase eraser size
            elif key == INCREASE_ERASER_KEY:
                drawing.eraser_radius = min(
                    drawing.eraser_radius + 5, 100
                )
                print("Eraser radius:", drawing.eraser_radius)

            # Decrease eraser size
            elif key == DECREASE_ERASER_KEY:
                drawing.eraser_radius = max(
                    drawing.eraser_radius - 5, 5
                )
                print("Eraser radius:", drawing.eraser_radius)

            # Quit
            elif key == QUIT_KEY:
                break

    finally:
        cap.release()
        tracker.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()