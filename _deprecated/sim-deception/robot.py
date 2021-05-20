import pygame


class Robot:
    def __init__(self, world_size, offset):

        self.offset = offset
        self.world_size = world_size
        self.x = world_size/2
        self.y = world_size/2 + 90

        self.shape = pygame.Rect(0, 0, 20, 20)
        self.image = pygame.image.load('src/robot2.png')
        self.image = pygame.transform.scale(self.image,(20,20))

        self.target = 0
        self.towers_xy = []

        self.deception = False
        self.deception_done = False
        self.type_deception = 0
        self.fake_target = 0
        self.real_target = 0

        self.count_slopes = 0
        self.num_slopes = 0
        self.current_slopes = 0

        '''Simulation easy difficulty'''

        self.max_acceleration = 0.1
        self.max_speed = 30 #62.5 #0.5
        self.min_speed = 6.25 #0.05

        self.current_speed = 0

    def restart(self):
        self.x = self.world_size / 2
        self.y = self.world_size / 2 + 90

    def move(self, dt):

        if self.deception:
            self.check_type_movement(dt)
        else:
            target_coordinates = self.towers_xy[self.target]
            self.move_x(target_coordinates, dt)
            self.move_y(target_coordinates, dt)
        self.check_boundaries()

    def move_x(self, target_coordinates, dt):
        if self.x < target_coordinates[0]:
            self.x += self.max_speed * dt * 0.001
        else:
            if self.x > target_coordinates[0]:
                self.x -= self.max_speed * dt * 0.001

    def move_y(self, target_coordinates, dt):
        if self.y < target_coordinates[1]:
            self.y += self.max_speed * dt * 0.001
        else:
            if self.y > target_coordinates[1]:
                self.y -= self.max_speed * dt * 0.001

    def check_type_movement(self, dt):
        if self.type_deception == 1 :
            target_coordinates = self.towers_xy[self.target]
            self.move_y(target_coordinates, dt)
            return

        if self.type_deception == 2:
            target_coordinates = self.towers_xy[self.target]
            self.move_x(target_coordinates, dt)
            return

        if self.type_deception == 3:
            print("Fake target ", self.fake_target)
            print("Real target ", self.target)
            if self.count_slopes % 50 == 0:
                self.current_slopes += 1
            if self.current_slopes % 2 ==0:
                target_coordinates= self.towers_xy[self.fake_target]
            else:
                target_coordinates = self.towers_xy[self.target]
            self.move_y(target_coordinates, dt)
            self.move_x(target_coordinates, dt)
            self.count_slopes += 1
            return

        if self.type_deception == 4:
            target_coordinates = self.towers_xy[self.target] #self.towers_xy[self.fake_target]
            self.move_x(target_coordinates, dt)
            self.move_y(target_coordinates, dt)
            return

    def check_boundaries(self):
        if self.x > self.offset + self.world_size:
            self.x = self.offset + self.world_size
        if self.y > self.offset + self.world_size:
            self.y = self.offset + self.world_size
        if self.x < self.offset:
            self.x = self.offset
        if self.y < self.offset:
            self.y = self.offset

    def acceleration_robot(self, t, current_speed, target_speed):
        if (target_speed - current_speed)/t > self.max_acceleration:
            return False
        else:
            return (target_speed - current_speed)/t

