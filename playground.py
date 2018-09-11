RED = (255, 0, 0)

class Playground:

    def __init__(self, size=500, tower_size=20, offset=50):
        self.size = size
        self.offset = offset
        self.tower_size = tower_size
        self.colors = [RED, RED, RED, RED]
        self.win_percentage = [0, 0, 0, 0]
        self.towers = [(0 + self.offset, 0 + self.offset), (self.size - self.tower_size + self.offset, 0 + self.offset),
                    (self.size -self.tower_size + self.offset, self.size -self.tower_size + self.offset), (0+ self.offset, self.size - self.tower_size + self.offset)]

    def restart(self):
        self.colors = [RED, RED, RED, RED]
        self.win_percentage = [0, 0, 0, 0]