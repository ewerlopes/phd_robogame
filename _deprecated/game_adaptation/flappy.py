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

    def __init__(self, settings, actions_per_second=7):
        self.model = Model()
        self.game = FlappyBird(settings)
        self.settings = settings
        self.env = PLE(self.game, fps=30, display_screen=False)
        self.env.init()
        self.env.getGameState = self.game.getGameState
        self.es = EvolutionStrategy(self.model.get_weights(), self.get_reward,
                                    self.POPULATION_SIZE, self.SIGMA, self.LEARNING_RATE)
        self.start_time = None
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

    def risk_function(self):
        state = self.env.getGameState()
        return abs(state['player_y'] - (state['next_pipe_bottom_y'] - self.settings.pipe_gap / 2))

    def get_isaken_AI_action(self):
        """
        Implements the AI where each time the bird drops below a target
        path, the AI immediately executes a flap
        (which sets vertical bird velocity vy instantly to jump velocity j).
        Reference: Exploring Game Space Using Survival Analysis. Isaken et al. 2015.
        """
        state = self.env.getGameState()
        # print json.dumps(state, indent=4)

        if (state['player_y'] + self.game.player.height/2) > (state['next_pipe_bottom_y'] - self.settings.pipe_gap/2.0):
            return 119
        else:
            return

    def play_reflex(self, episodes):
        """Uses Isaken et 2015 reflex agent"""
        self.env.display_screen = True
        self.model.set_weights(self.es.weights)
        for episode in xrange(episodes):
            self.env.reset_game()
            observation = self.get_observation()
            sequence = [observation] * self.AGENT_HISTORY_LENGTH
            done = False
            risk = 0

            while not done:
                action = self.get_isaken_AI_action()
                reward = self.env.act(action)
                risk += self.risk_function()

                observation = self.get_observation()
                sequence = sequence[1:]
                sequence.append(observation)
                done = self.env.game_over()

                if (self.env.getFrameNumber() % 30) == 0:
                    print "risk: {} \t | FPS: {}".format(risk, self.game.clock.get_fps())
                    risk = 0

        print 'Game over! Final score: {}'.format(self.game.getScore())
        self.env.display_screen = False

    def play(self, episodes,force_fps=True):
        """Uses the learned weights"""
        self.env.force_fps = force_fps
        self.env.display_screen = True
        self.model.set_weights(self.es.weights)
        for episode in xrange(episodes):
            self.env.reset_game()
            observation = self.get_observation()
            sequence = [observation]*self.AGENT_HISTORY_LENGTH
            done = False
            risk = 0

            while not done:
                action = self.get_predicted_action(sequence)
                reward = self.env.act(action)
                risk += self.risk_function()

                observation = self.get_observation()
                sequence = sequence[1:]
                sequence.append(observation)
                done = self.env.game_over()

                if (self.env.getFrameNumber() % 30) == 0:
                    print "Score: {} \t | risk: {} \t | FPS: {}".format(self.game.getScore(),
                                                                        risk, self.game.clock.get_fps())
                    risk = 0
        print 'Game over! Final score: {}'.format(self.game.getScore())
        self.env.display_screen = False

    def train(self, iterations, force_fps=True):
        self.env.force_fps = force_fps
        self.training = True
        if not self.env.force_fps:
            self.env.display_screen = True
        self.es.run(iterations, print_step=1)

    def end_by_time_tolerance(self, start, max_time_min_tol):
        t = time.time() - start
        hours = t // 3600
        t = t - 3600 * hours
        minutes = t // 60
        seconds = t - 60 * minutes

        if minutes >= max_time_min_tol and seconds > 0:
            print("Time tolerance of {} minutes achieved.".format(max_time_min_tol))
            return True
        else:
            return False

    def get_reward(self, weights, max_time_min_tol):
        total_reward = 0.0
        risk = 0.0
        self.model.set_weights(weights)
        start = time.time()
        for episode in xrange(self.EPS_AVG):
            self.env.reset_game()
            observation = self.get_observation()
            sequence = [observation] * self.AGENT_HISTORY_LENGTH
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
                risk += self.risk_function()
                observation = self.get_observation()
                sequence = sequence[1:]
                sequence.append(observation)
                done = self.env.game_over() or self.end_by_time_tolerance(start, max_time_min_tol)

                if not self.training and (self.env.getFrameNumber() % 30) == 0:
                    print "risk: {} \t | FPS: {}".format(risk, self.game.clock.get_fps())
                    risk = 0
        return total_reward / self.EPS_AVG