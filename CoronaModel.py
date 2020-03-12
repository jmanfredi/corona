from mesa import Agent, Model
from mesa.time import RandomActivation

class Person(Agent):
    """A normal person, who can be healthy or sick"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.carrier = 0

    def step(self):
        # Move around, interact with other agents
        pass

class CoronaModel(Model):
    """A model with N persons that tracks who gets sick, and when"""
    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        # Create agents
        for i in range (self.num_agents):
            a = Person(i, self)
            self.schedule.add(a)

    def step(self):
        # Advance the model by one step
        self.schedule.step()
        
