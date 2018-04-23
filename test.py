from flappy import Agent
from difficulty import DIFFICULTY

agent = Agent(DIFFICULTY)

# the pre-trained weights are saved into 'weights.pkl' which you can use.
agent.load('model/modelA.pkl')

# play one episode
#agent.play_reflex(1)
agent.play(1)
