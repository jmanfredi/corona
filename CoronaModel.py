from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

class Person(Agent):
    """A normal person, who can be healthy or sick"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.alive = 1
        self.carrier = 0
        self.sickdays = 0
        self.cured = 0 # assuming immunity after recovery

    def step(self):
        # Move around, interact with other agents
        if self.alive == 1:
            if self.carrier == 1:
                self.sickdays = self.sickdays + 1
                if self.sickdays > 14:
                    self.cured = 1
                    self.carrier = 0

            # Interact with neighbors

    def move(self):
        # Move action, without quarantine for now
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore = True,
            include_center = True
            )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def infect(self):
        # For each agent in the same cell, process infect action
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for buddy in cellmantes:
            if self.random.randint(0,100) < 10 and buddy.cured == 0:
                buddy.carrier = 1



class CoronaModel(Model):
    """A model with N persons that tracks who gets sick, and when"""
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        # Create agents
        for i in range (self.num_agents):
            a = Person(i, self)
            self.schedule.add(a)

            # Add person to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x,y))

    def step(self):
        # Advance the model by one step
        self.schedule.step()
        
