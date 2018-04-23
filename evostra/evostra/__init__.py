from __future__ import print_function
import numpy as np
import time

class EvolutionStrategy(object):

    def __init__(self, weights, get_reward_func,
                 population_size=50, sigma=0.1, learning_rate=0.001, decay=1.0):
        np.random.seed(0)
        self.weights = weights
        self.get_reward = get_reward_func
        self.POPULATION_SIZE = population_size
        self.SIGMA = sigma
        self.LEARNING_RATE = learning_rate
        self.decay = decay

    def _get_weights_try(self, w, p):
        weights_try = []
        for index, i in enumerate(p):
            jittered = self.SIGMA*i
            weights_try.append(w[index] + jittered)
        return weights_try

    def get_weights(self):
        return self.weights

    def end_by_time_tolerance(self, max_time_min_tol, start, iteration):
        t = time.time() - start
        hours = t // 3600
        t = t - 3600 * hours
        minutes = t // 60
        seconds = t - 60 * minutes

        if minutes >= max_time_min_tol and seconds > 0:
            print("Time tolerance of {} minutes achieved.".format(max_time_min_tol))
            return True
        else:
            print('Going through population in iteration #{} took: {} min and {:.2f} sec(s)'.format(iteration,
                                                                                                    minutes,
                                                                                                    seconds))
            return False

    def run(self, iterations, print_step=10,  max_time_min_tol=5):
        """
        Run evostra
        :param iterations: number of iterations
        :param print_step: the step for printing verbose
        :param max_time_min_tol: the max time tolerance (in minutes) for iteration
        :return:
        """
        for iteration in range(iterations):
            population = []
            rewards = np.zeros(self.POPULATION_SIZE)
            for i in range(self.POPULATION_SIZE):
                x = []
                for w in self.weights:                 
                    x.append(np.random.randn(*w.shape))
                population.append(x)

            start = time.time()
            for i in range(self.POPULATION_SIZE):
                weights_try = self._get_weights_try(self.weights, population[i])
                rewards[i] = self.get_reward(weights_try, max_time_min_tol)

            max_pop_reward = max(rewards)
            rewards = (rewards - np.mean(rewards)) / np.std(rewards)

            for index, w in enumerate(self.weights):
                A = np.array([p[index] for p in population])
                self.weights[index] = w + self.LEARNING_RATE/(self.POPULATION_SIZE*self.SIGMA) * np.dot(A.T, rewards).T

            self.LEARNING_RATE *= self.decay

            if (iteration+1) % print_step == 0:
                print('iter %d. max pop member reward: %f' % (iteration+1, max_pop_reward))

            if self.end_by_time_tolerance(max_time_min_tol, start, iteration):
                break

