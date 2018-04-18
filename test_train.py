import signal
import sys
from flappy import *

agent = Agent()

def handler(signum, frame):
    print "Aborting...."
    print "Saving weights"
    # the pre-trained weights are save
    agent.save('weights_mytrain.pkl')
    sys.exit(0)

signal.signal(signal.SIGINT, handler)


# train for x iterations
agent.train(1000)

