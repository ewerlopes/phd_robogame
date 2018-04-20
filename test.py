from flappy import *
from flappy import GameSettings

diff = GameSettings(group_pipe_separation=150, jump_vel=7)

agent = Agent(diff)

# the pre-trained weights are saved into 'weights.pkl' which you can use.
agent.load('weights_mytrain.pkl')

# play one episode
agent.play_reflex(1)
