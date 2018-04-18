import random
import cPickle as pickle
import numpy as np
import time
import json
import sys
from evostra import EvolutionStrategy
from ple import PLE
from ple.games.flappybird import FlappyBird
from model import Model


class GameSettings:
    """ Holds the game setting parameters for the game. Specialy, those related to difficulty

    Attributes:
        group_pipe_separation : More distance between pipes is easier to play,
                                giving more time to react to changing gap locations. Change distance
                                between each group of 3 pipes

        pipe_gap        : The distance between the upper pipe and the lower pipe.
                          Narrower gaps are more difficult as the bird has less room to
                          maneuver, requiring better motor skills.

        pipe_width      : Wider pipes increase difficulty as the bird spends more time in the narrow pipe gap.

        pipe_gap_loc_range : The pipe gap locations are uniformly randomly distributed in a range somewhere
                             between the ceiling and the floor. Larger ranges are harder because there is
                             more distance to travel between a high gap and a low gap.

        gravity           : Acceleration of the bird in the y direction, subtracted from the bird's y velocity
                              each frame. Higher gravity causes the bird to drop faster, lowering the margin of
                              error.

        jump_vel           : When the bird flaps, its vertical velocity is set to jump_vel, making it jump upward.
                              Higher velocity makes higher jumps.

        bird_vel           : Speed at which the bird travels to the right (alternately, the speed at which pipes
                                travel to the left).

        world_width        : Screen width. In Flappy Bird, this is defined by the display resolution.

        world_height       : Distance between ceiling and floor. In Flappy Bird, this is defined by the
                              display resolution.

        bird_width         : width of the bird's hit box. The wider and taller the bird, the harder it
                            will be to jump through gaps.

        bird_height        : height of the bird's hit box. The wider and taller the bird, the harder it
                            will be to jump through gaps.
        """
    def __init__(self, group_pipe_separation=0.5, pipe_width=0, pipe_gap_loc_range=0, gravity=1.1, jump_vel=6,
                 bird_vel=4.0, bird_width=0, bird_height=0, pipe_gap=150, world_height=512, world_width=288):
        self.group_pipe_separation = group_pipe_separation      # OK
        self.pipe_gap = pipe_gap                                # OK
        self.pipe_width = pipe_width
        self.pipe_gap_loc_range = pipe_gap_loc_range
        self.gravity = gravity                                  # OK
        self.jump_vel = jump_vel                                # OK
        self.bird_vel = bird_vel                                # OK
        self.world_width = world_width                          # OK
        self.world_height = world_height                        # OK
        self.bird_width = bird_width
        self.bird_height = bird_height


class Agent:

    AGENT_HISTORY_LENGTH = 1
    NUM_OF_ACTIONS = 2
    POPULATION_SIZE = 15
    EPS_AVG = 1
    SIGMA = 0.1
    LEARNING_RATE = 0.03
    INITIAL_EXPLORATION = 0.0
    FINAL_EXPLORATION = 0.0
    EXPLORATION_DEC_STEPS = 100000

    def __init__(self, settings, actions_per_second=15):
        self.model = Model()
        # self.game = FlappyBird(pipe_gap=150)
        self.game = FlappyBird(settings)
        self.settings  = settings
        self.env = PLE(self.game, fps=30, display_screen=False)
        self.env.init()
        self.env.getGameState = self.game.getGameState
        self.es = EvolutionStrategy(self.model.get_weights(), self.get_reward, self.POPULATION_SIZE, self.SIGMA, self.LEARNING_RATE)
        self.exploration = self.INITIAL_EXPLORATION
        self.actions_per_second = actions_per_second
        self.period = 1.0 / self.actions_per_second

    def get_predicted_action(self, sequence):
        prediction = self.model.predict(np.array(sequence))
        x = np.argmax(prediction)
        return 119 if x == 1 else None

    def load(self, filename='weights.pkl'):
        with open(filename,'rb') as fp:
            self.model.set_weights(pickle.load(fp))
        self.es.weights = self.model.get_weights()

    def get_observation(self):
        state = self.env.getGameState()
        return np.array(state.values())

    def save(self, filename='weights.pkl'):
        with open(filename, 'wb') as fp:
            pickle.dump(self.es.get_weights(), fp)

    def timed_call(callback, calls_per_second, *args, **kw):
        """
        Create an iterator which will call a function a set number
        of times per second.
        """
        time_time = time.time
        start = time_time()
        period = 1.0 / calls_per_second
        while True:
            if (time_time() - start) > period:
                start += period
                callback(*args, **kw)
            yield None

    def get_isaken_AI_action(self):
        """
        Implements the AI where each time the bird drops below a target
        path, the AI immediately executes a flap
        (which sets vertical bird velocity vy instantly to jump velocity j).
        Reference: Exploring Game Space Using Survival Analysis. Isaken et al. 2015.
        """
        state = self.env.getGameState()
        # print json.dumps(state, indent=4)

        if (state['player_y']) > (state['next_pipe_bottom_y'] - self.settings.pipe_gap/1.5):
            return 119
        else:
            return

    def play(self, episodes):
        self.env.display_screen = True
        self.model.set_weights(self.es.weights)
        for episode in xrange(episodes):
            self.env.reset_game()
            observation = self.get_observation()
            sequence = [observation]*self.AGENT_HISTORY_LENGTH
            done = False
            score = 0

            time_time = time.time
            action_time = time_time()
            a_count = 0
            while not done:
                action = None
                if (time_time() - action_time) > self.period:        # allow only 'actions_per_second' times
                    action_time = time_time()
                    a_count +=1
                    # action = self.get_predicted_action(sequence)
                    action = self.get_isaken_AI_action()
                reward = self.env.act(action)
                observation = self.get_observation()
                sequence = sequence[1:]
                sequence.append(observation)
                done = self.env.game_over()

                if self.game.getScore() > score:
                    score = self.game.getScore()
                    print "score: %d" % score

                if (self.env.getFrameNumber() % 30) == 0:
                    print "Action_per_sec: {}".format(a_count)
                    a_count = 0
        print 'Game over! Final score: {}'.format(score)
        self.env.display_screen = False

    def train(self, iterations):
        self.es.run(iterations, print_step=1)

    def get_reward(self, weights):
        total_reward = 0.0
        self.model.set_weights(weights)

        for episode in range(self.EPS_AVG):
            self.env.reset_game()
            observation = self.get_observation()
            sequence = [observation]*self.AGENT_HISTORY_LENGTH
            done = False
            while not done:
                self.exploration = max(self.FINAL_EXPLORATION,
                                       self.exploration - self.INITIAL_EXPLORATION / self.EXPLORATION_DEC_STEPS)
                if random.random() < self.exploration:
                    action = random.choice([119, None])
                else:
                    action = self.get_predicted_action(sequence)
                reward = self.env.act(action)
                reward += random.choice([0.0001, -0.0001])
                total_reward += reward
                observation = self.get_observation()
                sequence = sequence[1:]
                sequence.append(observation)
                done = self.env.game_over()

        return total_reward / self.EPS_AVG
