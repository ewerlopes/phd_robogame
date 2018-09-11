import pygame
from socket_client import Client
from model import Model
import time


class View():
    def __init__(self, world_size):

        pygame.init()
        self.world_size = world_size

        # Variables for displaying text
        pygame.font.init()
        self.myfont = pygame.font.Font('src/Audiowide-Regular.ttf', 70)
        self.myfont2 = pygame.font.Font('src/Audiowide-Regular.ttf', 40)

        # Display's variable
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Game simulation for Deception')

        # Management variables
        self.start_time = 0         # variable used for checking the 2.5s that must be elapsed for winning a led on a tower
        self.game_over = False
        self.new_game = False
        self.main_menu=True
        self.clock = pygame.time.Clock()
        self.FPS = 300
        self.dt = 0

    def display(self, model):
        self.screen.fill(BLACK)
        if not self.game_over:
            if self.main_menu:
                self.main_menu_view()
            else:
                self.game_view(model)
        else:
            self.game_over_view()

        self.dt = self.clock.tick(self.FPS)
        pygame.display.update()

    def main_menu_view(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        text_surface = self.myfont.render('ROBOT GAME', True, RED)
        text_rect = text_surface.get_rect()
        self.screen.blit(text_surface, (50 + (self.world_size - text_rect.width) / 2, 100))

        if 150 + 300 > mouse[0] > 150 and 250 + 100 > mouse[1] > 250:
            pygame.draw.rect(self.screen, GREEN, (150, 250, 300, 100))

            if click[0] == 1:
                self.main_menu = False
        else:
            pygame.draw.rect(self.screen, BLUE, (150, 250, 300, 100))

        text_surface = self.myfont2.render('Start Game', True, WHITE)
        text_rect = text_surface.get_rect()

        self.screen.blit(text_surface, (150 + (300 - text_rect.width) / 2, 250 + (100 - text_rect.height) / 2))

    def game_view(self, model):
        buffer = model.getRederingBuffer()
        self.draw_borders()

        towers = self.draw_towers(buffer)

        # Drawing the agents
        robot,player = self.draw_agents(buffer)

        # self.screen.blit(buffer[1].image, (buffer[1].x, buffer[1].y, 20, 20))

        self.check_collisions(robot, towers, player, model)

    def draw_agents(self, buffer):
        robot = buffer[1].shape.move(buffer[1].x, buffer[1].y)
        player = buffer[2].shape.move(buffer[2].x, buffer[2].y)
        pygame.draw.rect(self.screen, BLUE, robot)  # ROBOT
        pygame.draw.rect(self.screen, VIOLET, player)  # PLAYER
        return robot, player

    def draw_towers(self, buffer):
        towers = [1, 2, 3, 4]
        for t in range(4):
            towers[t] = pygame.Rect(buffer[0].towers[t][0], buffer[0].towers[t][1], buffer[0].tower_size,
                                    buffer[0].tower_size, width=2)
            pygame.draw.rect(self.screen, buffer[0].colors[t], towers[t])
        return towers

    def draw_borders(self):
        pygame.draw.line(self.screen, WHITE, (40, 40), (560, 40), 2)
        pygame.draw.line(self.screen, WHITE, (40, 40), (40, 560), 2)
        pygame.draw.line(self.screen, WHITE, (560, 40), (560, 560), 2)
        pygame.draw.line(self.screen, WHITE, (40, 560), (560, 560), 2)

    def game_over_view(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        text_surface = self.myfont.render('GAME OVER', True, RED)
        text_rect = text_surface.get_rect()
        self.screen.blit(text_surface, ((self.world_size - text_rect.width)/2, 100))

        if 150 + 300 > mouse[0] > 150 and 250 + 100 > mouse[1] > 250:
            pygame.draw.rect(self.screen, GREEN, (150, 250, 300, 100))

            if click[0] == 1:
                self.game_over = False
                self.new_game = True

        else:
            pygame.draw.rect(self.screen, BLUE, (150, 250, 300, 100))

        text_surface = self.myfont2.render('Start Again', True, WHITE)
        text_rect = text_surface.get_rect()

        self.screen.blit(text_surface, (150 + (300 - text_rect.width) / 2, 250 + (100 - text_rect.height) / 2))

    def check_collisions(self, robot, towers, player, model):
        if robot.collidelist(towers) > -1:
            self.game_over =True
        index = player.collidelist(towers)
        if index > -1:
            if self.start_time == 0:
                self.start_time = int(round(time.time() * 1000))
            if int(round(time.time() * 1000))-self.start_time >= 2500:
                if model.playground.win_percentage[index] == 4:
                    model.playground.colors[index] = GREEN

                if model.playground.win_percentage[index] == 4:
                    model.playground.colors[index] = GREEN
                else:
                    model.playground.win_percentage[index] += 1
                    model.playground.colors[index] = YELLOW
                pygame.draw.rect(self.screen, model.playground.colors[index], towers[index])
                self.start_time = 0
        else:
            self.start_time = 0




class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self.model.WORLD_SIZE)
        self.view.main_menu = True
        # self.model.robot.image=self.model.robot.image.convert(pygame.Surface((20, 20)))
        # self.model.robot.image=self.model.robot.image.convert_alpha(pygame.Surface((20, 20)))
        # self.model.robot.image.set_colorkey((255,255,255))
    
    def Run(self, ):


        main = self.model.get_keyboard()            # checking if QUIT has been pressed
        if self.view.new_game:
            self.model.restart()
            self.view.new_game = False
        if (not self.view.game_over) and (not self.view.main_menu):
            self.model.get_position_agents()            # analyzing social situation
            self.model.update_won_towers()
            self.model.get_targets()
            self.model.get_outcome_matrices()
            self.model.map_outcome_matrices_in_interdependence_space()
            self.model.check_for_deception()
            self.model.move(self.view.dt)                           # moving the agents
        self.view.display(self.model)
        if not main:
            return False
        else:
            return True


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (100, 100, 200)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

if __name__=="__main__":

    # client = Client()
    # client.connection_to_server()

    C = Controller()

    main = True
    while main:
        main = C.Run()
        # client.connection_to_server()
        # client.send_message_to_client(C.model.alpha_r, C.model.beta)
        # client.close_connection()
