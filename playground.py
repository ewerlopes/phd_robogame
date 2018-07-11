
class Playground:

    def __init__(self, size=500, tower_size=40):
        self.size = size
        self.tower_size = tower_size


        self.towers = [(0,0), (self.size-self.tower_size, 0),
                       (0, self.size -self.tower_size), (self.size -self.tower_size,self.size -self.tower_size)]
