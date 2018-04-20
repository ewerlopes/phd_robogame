import signal
from flappy import *

diff = GameSettings(group_pipe_separation=150, jump_vel=7)

agent = Agent(diff)


def handler(signum, frame):
    print "Aborting...."
    print "Saving weights"
    # the pre-trained weights are save
    agent.save('weights_mytrain.pkl')
    sys.exit(0)


signal.signal(signal.SIGINT, handler)

# train for x iterations
agent.train(100)

