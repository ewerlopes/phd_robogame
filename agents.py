from math import *
import sys
import random
import util


class Agent:
    def __init__(self, world_size):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.world_size = world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0;
        self.turn_noise    = 0.0;
        self.sense_noise   = 0.0;
        
    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= self.world_size:
            raise ValueError, 'X coordinate out of bound'
        if new_y < 0 or new_y >= self.world_size:
            raise ValueError, 'Y coordinate out of bound'
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)
    
    
    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise);
        self.turn_noise    = float(new_t_noise);
        self.sense_noise   = float(new_s_noise);
    
    
    def sense(self):
        util.raiseNotDefined()
    
    
    def move(self, turn, forward):
        util.raiseNotDefined()
    
     
    def Gaussian(self, mu, sigma, x): 
        """ calculates the probability of x for 1-dim 
            Gaussian with mean mu and var. sigma"""
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
    
    
    def measurement_prob(self, measurement):       
        util.raiseNotDefined()
    
    
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))

    
class Particles(Agent):
    def __init__(self,world_size):
        Agent.__init__(self,world_size)
        
    def move(self,target):
        "This is the particle motion model, responsable for allowing to track the player"
        # turn, and add randomness to the turning command
        
        devProb = 0.5
        prob = random.random()
        x = 0
        y = 0
        orientation = self.orientation
        
        if prob < devProb:
            orientation = self.orientation + random.gauss(0.0,self.turn_noise)
            orientation %= 2 * pi

            # move, and add randomness to the motion command
            dist = float(target.lastMotion) + random.gauss(0.0, self.forward_noise)
            x = self.x + (cos(orientation) * dist)
            y = self.y + (sin(orientation) * dist)
            x %= self.world_size    # cyclic truncate
            y %= self.world_size
        else:
            # move, and add randomness to the motion command
            dist = float(target.lastMotion) 
            x = self.x + (cos(orientation) * dist)
            y = self.y + (sin(orientation) * dist)
            x %= self.world_size    # cyclic truncate
            y %= self.world_size
            
        # set particle
        res = Particles(self.world_size)
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res
    
    def measurement_prob(self, measurement,opponent):
        """Calculates how likely a measurement should be."""
        prob = 1.0;
        dist = sqrt((self.x - opponent.x) ** 2 + (self.y - opponent.y) ** 2)
        prob *= self.Gaussian(dist, self.sense_noise, measurement)
        return prob

class Robot(Agent):
    def __init__(self, world_size,color=[23,45,67]):
        Agent.__init__(self,world_size)
        self.NO_OPPON_PARTICLES = []
        self.oppTrackParticles = []
        self.color = color
        self.opponent = None
        self.lastMotion = 0
    
    def setOpponent(self,opponent, opp_particles=10):
        self.opponent = opponent
        self.NO_OPPON_PARTICLES = opp_particles
        for i in range(self.NO_OPPON_PARTICLES):            # CREATING PARTICLES (RANDOM POSITION)
            x = Particles(self.world_size)
            x.set_noise(0.05, 0.05, 5.0)
            self.oppTrackParticles.append(x)
    
    
    def sense(self):
        dist = sqrt((self.x - self.opponent.x) ** 2 + (self.y - self.opponent.y) ** 2)
        dist += random.gauss(0.0, self.sense_noise)
        return dist
    
    
    def move(self, turn, forward):
        if forward < 0:
            raise ValueError, 'Robot cannot move backwards'         
        
        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi
        
        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= self.world_size    # cyclic truncate
        y %= self.world_size
        
        self.x = x
        self.y = y
        self.orientation = orientation
        self.lastMotion = dist
        
    def sample(self,impWeights):
        p = []
        index = int(random.random() * self.NO_OPPON_PARTICLES)            # GETTING A RANDOM INDEX FOR SAMPLING
        beta = 0.0
        mw = max(impWeights)                        # GETTING THE MAXIMUN WEIGHT
        for i in range(self.NO_OPPON_PARTICLES):                          # THE SAMPLING WHEEL FOR KEEPING THE BEST WEIGHTED PARTICLE
            beta += random.random() * 2.0 *mw
            while beta > impWeights[index]:
                beta -= impWeights[index]
                index = (index + 1) % self.NO_OPPON_PARTICLES
            p.append(self.oppTrackParticles[index])
        return p
    
    def oppOnSense(self):
        if self.opponent != None:
            Z = self.sense()                            # PERFORMS A MEASUREMENT
            particles = []
            for i in range(self.NO_OPPON_PARTICLES):
                particles.append(self.oppTrackParticles[i].move(self.opponent))          # MOVE PARTICLES
            
            w = []
            for i in range(self.NO_OPPON_PARTICLES):    # CALCULATES THE WEIGTH OF THE PARTICLE
                w.append(particles[i].measurement_prob(Z,self.opponent))
            
            print w
            s = sum(w)
            w = [w[i]/s for i in range(len(w))]         # THE NORMALIZATION OF WEIGHTS
            self.oppTrackParticles = self.sample(w)
        
    
    def printOppParticles(self):
        for i in len(self.oppTrackParticles):
            return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.oppTrackParticles[i].x), str(self.oppTrackParticles[i].y), 
                                                    str(self.oppTrackParticles[i].orientation))
            