class Bid():
    def __init__(self, agent, value):
        self.value = value
        self.agent = agent


    def __repr__(self):
        return "Agent " + str(self.agent.id) + " submits Bid for " + str(self.value)
