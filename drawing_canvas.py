import cv2
import numpy as np


class DrawingCanvas:
    def __init__(
        self,
        brush_color=(0, 255, 0),
        brush_thickness=5,
        eraser_radius=30,
    ):
        self.canvas = None
        self.prev_x = None
        self.prev_y = None

        self.brush_color = brush_color
        self.brush_thickness = brush_thickness
        self.eraser_radius = eraser_radius

    def initialize(self, height, width):
        self.canvas = np.zeros(
            (height, width, 3), dtype=np.uint8
        )

    def draw(self, x, y):
        if self.prev_x is not None:
            cv2.line(
                self.canvas,
                (self.prev_x, self.prev_y),
                (x, y),
                self.brush_color,
                self.brush_thickness,
            )

        self.prev_x, self.prev_y = x, y

    def erase(self, x, y):
        cv2.circle(
            self.canvas,
            (x, y),
            self.eraser_radius,
            (0, 0, 0),
            -1,
        )
        self.reset_position()

    def reset_position(self):
        self.prev_x = None
        self.prev_y = None

    def clear(self):
        if self.canvas is not None:
            self.canvas.fill(0)

        self.reset_position()

    def overlay(self, frame):
        gray = cv2.cvtColor(
            self.canvas, cv2.COLOR_BGR2GRAY
        )

        _, mask = cv2.threshold(
            gray, 20, 255, cv2.THRESH_BINARY_INV
        )

        background = cv2.bitwise_and(
            frame, frame, mask=mask
        )

        return cv2.bitwise_or(
            background, self.canvas
        )
    def save(self, filename="drawing.png"):
        if self.canvas is None:
            return False

        return cv2.imwrite(filename, self.canvas)    
       