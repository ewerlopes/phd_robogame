from flappy import *
from flappy import GameSettings

diff = GameSettings(group_pipe_separation=150)

agent = Agent(diff)

# the pre-trained weights are saved into 'weights.pkl' which you can use.
#agent.load('weights_mytrain.pkl')

# play one episode
agent.play(1)
#agent.save(filename='weights_mytrain.pkl')
