from playground import Playground
from player import Player
from robot import Robot

import pygame
import sys
import numpy
import random

import target_finder
import outcome_matrices_creator
import correspondence
import interdependence
import deception

RED = (255, 0, 0)


class Model(object):
    def __init__(self):
        self.WORLD_SIZE = 500
        self.offset = 50

        # Agents declaration
        self.robot = Robot(self.WORLD_SIZE, self.offset)
        self.player = Player(self.WORLD_SIZE, self.offset)
        self.playground = Playground(size=self.WORLD_SIZE, offset=self.offset)

        # Initializing towers' positions and agents' positions
        self.player_xy = self.robot_xy = numpy.zeros(2)
        self.tower_size = 20

        self.towers_xy = numpy.array([[0 + self.offset, 0 + self.offset], [self.WORLD_SIZE - self.tower_size + self.offset, 0 + self.offset], [0+ self.offset, self.WORLD_SIZE - self.tower_size + self.offset], [self.WORLD_SIZE -self.tower_size + self.offset, self.WORLD_SIZE -self.tower_size + self.offset]])
        self.robot.towers_xy = self.towers_xy

        # Target array says for each tower how 'likely' the robot/player wants to win it
        # Target_AGENT says which tower is the chosen one (not really used for the player, it could be implemented)
        self.target_array_robot = self.target_array_player = numpy.zeros(4)
        self.target_robot = self.target_player = [1, 1, 1, 1]

        # Outcome matrices for agents
        self.outcome_matrix_robot = self.outcome_matrix_player = numpy.zeros((4,4))

        # Mapping outcome matrices into social situation space
        # Alpha --> interdependence
        # Beta --> correspondence
        # Check correspondence.py and interdependency.py for more info
        self.alpha_r = 0
        self.beta = 0

        self.cont = 0
        self.num_slopes = 0

    def restart(self):

        self.robot.restart()
        self.player.restart()
        self.playground.restart()

        self.player_xy = self.robot_xy = numpy.zeros(2)
        self.target_array_robot = self.target_array_player = numpy.zeros(4)
        self.target_robot = self.target_player = [1, 1, 1, 1]
        self.outcome_matrix_robot = self.outcome_matrix_player = numpy.zeros((4, 4))
        self.alpha_r = 0
        self.beta = 0
        self.cont = 0

    def move(self,dt):
        self.robot.move(dt)
        self.player.move()

    def getRederingBuffer(self):
        return [self.playground, self.robot, self.player]

    # For player movement using the keyboard
    def get_keyboard(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.player.control(-3, 0)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.player.control(+3, 0)
                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.player.control(0, -3)
                if event.key == pygame.K_DOWN or event.key == ord('x'):
                    self.player.control(0, +3)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.player.control(3, 0)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.player.control(-3, 0)
                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.player.control(0, +3)
                if event.key == pygame.K_DOWN or event.key == ord('x'):
                    self.player.control(0, -3)
                if event.key == ord('q'):
                    pygame.quit()
                    sys.exit()
                    return False
        return True

    def get_position_agents(self):
        # Getting agents' position
        self.player_xy = [self.player.x, self.player.y]
        self.robot_xy = [self.robot.x, self.robot.y]

    def update_won_towers(self):
        for i in range(4):
            if self.playground.win_percentage[i] == 4:
                self.target_robot[i] = 0
                self.target_player[i] = 0
            else:
                self.target_robot[i] = 1
                self.target_player[i] = 1

    def get_targets(self):
        # Calculating how likely to win a tower for the robot
        self.target_array_robot = target_finder.target_preferences_robot(self.player_xy, self.robot_xy, self.towers_xy,
                                                                         self.target_robot)

        # Checking which tower is the target
        self.robot.target = target_finder.find_target(self.target_array_robot)

        self.update_won_towers()

        # To increase the outcome of the target once chosen
        # (for not changing mind during an action)
        # (action is defined as choosing the tower and all the procedure for winning it)
        self.target_robot[self.robot.target] = 1.2
        self.target_array_player = target_finder.target_preferences_player(self.player_xy, self.robot_xy,
                                                                           self.towers_xy,
                                                                           self.target_player)
        self.target_player[target_finder.find_target(self.target_array_player)] = 1

    def get_outcome_matrices(self):
        # Creating the outcome matrices
        self.outcome_matrix_robot = outcome_matrices_creator.outcome_matrix_robot(self.target_array_robot,
                                                                                  self.towers_xy,
                                                                                  self.player_xy, self.robot_xy)

        self.outcome_matrix_player = outcome_matrices_creator.outcome_matrix_player(self.target_array_player,
                                                                                    self.towers_xy,
                                                                                    self.robot_xy)

    def map_outcome_matrices_in_interdependence_space(self):
        # Mapping the outcome matrices to the social situation space
        self.beta = correspondence.correspondence(self.outcome_matrix_robot, self.outcome_matrix_player)
        self.alpha_r = interdependence.interdependence(self.outcome_matrix_robot, self.target_array_robot)

    def check_for_deception(self):
        if self.beta < -0.6 and self.alpha_r > 0.6 and not self.robot.deception:
            if not self.robot.deception_done:
                print ('Possible deception')
                if random.randint(1, 100)/100 > 0.6:
                    self.robot.deception = True
                    self.robot.fake_target = deception.get_fake_target(self.outcome_matrix_robot, self.outcome_matrix_player)
                    self.robot.real_target = self.robot.target
                    type_deception = deception.get_type_deception(self.robot.fake_target, self.robot.real_target, self.robot_xy, self.player_xy)
                    deception.deception_motion_manager(type_deception, self)

        if not self.robot.real_target == self.robot.target:
            self.robot.deception_done = False
            self.robot.deception = False
            self.robot.current_slope = 0
            self.robot.count_slopes = 0

        if self.robot.deception:
            if (self.cont < 50 and not self.robot.type_deception == 3) or (self.robot.type_deception == 3 and self.cont < 50*self.robot.num_slopes):
                self.cont += 1
                # print ('DOING DECEPTION')
            else:
                self.robot.deception = False
                self.robot.deception_done = True
        else:
            self.cont = 0
            # print ('NO DECEPTION')