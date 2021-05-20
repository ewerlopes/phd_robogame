import pygame


class Player:
    def __init__(self, world_size, offset):

        self.offset = offset
        self.world_size = world_size
        self.x = self.offset + world_size / 2
        self.y = self.offset + world_size / 2 + 100

        self.movex = 0  # move along X
        self.movey = 0  # move along Y
        self.frame = 0  # count frames

        self.shape = pygame.Rect(0, 0, 20, 20)

    def restart(self):

        self.x = self.offset + self.world_size / 2
        self.y = self.offset + self.world_size / 2 + 100
        self.movex = 0  # move along X
        self.movey = 0  # move along Y
        self.frame = 0  # count frames

    # Function that memorizes the movement received from keyboard
    def control(self, x, y):
        self.movex += x
        self.movey += y

    def move(self):
        self.x += self.movex
        self.y += self.movey

        # moving left
        if self.movex < 0:
            self.frame += 1
            if self.frame > 3:
                self.frame = 0

        # moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame > 3:
                self.frame = 0

        self.check_boundaries()

    def check_boundaries(self):
        if self.x > self.offset + self.world_size:
            self.x = self.offset + self.world_size
        if self.y > self.offset + self.world_size:
            self.y = self.offset + self.world_size
        if self.x < self.offset:
            self.x = self.offset
        if self.y < self.offset:
            self.y = self.offset


