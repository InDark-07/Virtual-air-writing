
class GestureController:
    WRITE = "WRITE"
    ERASE = "ERASE"
    IDLE = "IDLE"

    def recognize(self, index_up, middle_up):
        if index_up and middle_up:
            return self.ERASE

        if index_up and not middle_up:
            return self.WRITE

        return self.IDLE
