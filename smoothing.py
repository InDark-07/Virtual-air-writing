
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
