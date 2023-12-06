class Ask():
    def __init__(self, agent, value):
        self.value = value
        self.agent = agent


    def __repr__(self):
        return "Agent " + str(self.agent.id) + " submits Ask for " + str(self.value) 
