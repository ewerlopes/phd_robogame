from agents import Robot
from playground import Playground
from math import cos, sin, pi
import pygame
import sys
import random


class Model(object):
    def __init__(self):
        self.WORLD_SIZE = 500
        self.robot = Robot(self.WORLD_SIZE)
        self.player = Robot(self.WORLD_SIZE)
        self.robot.setOpponent(self.player)
        self.playground = Playground(size=self.WORLD_SIZE)

    def move(self):
        self.robot.oppOnSense()
        r = (random.randrange(-1, 2)*(pi/16)) % (2*pi)           # the player complex turning
        self.player.move(r, random.random()*5.0)
    
    def getRederingBuffer(self):
        return [self.playground, self.robot, self.player, self.robot.oppTrackParticles]


class View():
    def __init__(self,world_size):
        pygame.init()
        self.world_size = world_size

        self.screen = pygame.display.set_mode((world_size,world_size)) 
        pygame.display.set_caption('Game simulation - by Ewerton Lopes - Dec 16, 2015')

        self. clock = pygame.time.Clock()
        self.FPS = 25
        self.total_frames = 0


    def display(self,buffer):
        self.screen.fill([255,255,255])

        for t in range(4):
            pygame.draw.rect(self.screen, (0,1,0), pygame.Rect(buffer[0].towers[t][0], buffer[0].towers[t][1],
                                                               buffer[0].tower_size, buffer[0].tower_size, width=2))

        for obj in buffer[1:-1]:
            pygame.draw.circle(self.screen, obj.color, (int(obj.x),int(obj.y)), 20, 1)
            pygame.draw.line(self.screen, obj.color, (int(obj.x),int(obj.y)),
                             (int(obj.x + 19*cos(obj.orientation)),int(obj.y+19*sin(obj.orientation))), 3)
        
        for obj in buffer[-1]:
            print obj
            pygame.draw.circle(self.screen, [0,0,0], [int(obj.x),int(obj.y)], 2, 0)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        
        pygame.display.flip()
        self.clock.tick(self.FPS)
        self.total_frames += 1


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self.model.WORLD_SIZE)
    
    def Run(self):
        while True:
            self.view.display(self.model.getRederingBuffer())
            self.model.move()

if __name__=="__main__": 
    C = Controller()
    C.Run()
