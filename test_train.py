import signal, sys
from flappy import Agent
from difficulty import DIFFICULTY

agent = Agent(DIFFICULTY)

def handler(signum, frame):
    print "Aborting...."
    print "Saving weights"
    # the pre-trained weights are save
    agent.save('model/weights_mytrain.pkl')
    sys.exit(0)


signal.signal(signal.SIGINT, handler)

#agent.load('model/weights_mytrain.pkl')

# train for x iterations
agent.train(1000, force_fps=True)
agent.save()

