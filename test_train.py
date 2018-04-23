import signal, sys
from flappy import Agent
from difficulty import DIFFICULTY

agent = Agent(DIFFICULTY)
file_weights = 'model/modelB.pkl'

def handler(signum, frame):
    print "Aborting...."
    print "Saving weights"
    # the pre-trained weights are save
    agent.save(filename=file_weights)
    sys.exit(0)


signal.signal(signal.SIGINT, handler)

# train for x iterations
agent.train(1000, force_fps=True)

print "Saving weights"
agent.save(filename=file_weights)

