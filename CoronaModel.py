from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

def get_num_alives(model):
    person_alives = [person.alive for person in model.schedule.agents]
    num_alives = sum ( i for i in person_alives )
    return num_alives

def get_num_carriers(model):
    person_carriers = [person.carrier for person in model.schedule.agents]
    num_carriers = sum ( i for i in person_carriers )
    return num_carriers

def get_num_cureds(model):
    person_cureds = [person.cured for person in model.schedule.agents]
    num_cureds = sum ( i for i in person_cureds )
    return num_cureds

def get_num_deads(model):
    person_deads = [ abs(person.alive - 1) for person in model.schedule.agents ]
    num_deads = sum ( i for i in person_deads )
    return num_deads

def get_r0(model):
    person_transfers = [person.transfers for person in model.schedule.agents]
    num_transfers = sum ( i for i in person_transfers)
    num_carriers = sum ( person.carrier for person in model.schedule.agents )
    num_cureds = sum ( person.cured for person in model.schedule.agents )
    if num_carriers + num_cureds == 0:
        r0 = 0
    else:
        r0 = num_transfers/(num_carriers + num_cureds)
    return r0

class Person(Agent):
    """A normal person, who can be healthy or sick"""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.alive = 1
        self.carrier = 0
        self.sickdays = 0
        self.transfers = 0
        self.interactions = 0
        self.cured = 0 # assuming immunity after recovery
        self.socialdist = 0

    def step(self):
        # Move around, interact with other agents
        if self.alive == 1:
            # Move, unless social distancing
            if self.socialdist == 0:
                self.move()

            # Interact with neighbors (one way)
            if self.carrier == 1:
                self.infect()

                # Check to see if I die
                if self.random.uniform(0,1) < self.model.deathrate:
                    self.alive = 0
                    self.carrier = 0
                else:
                    # Increment sick days
                    self.sickdays = self.sickdays + 1
                    if self.model.socialdist_step < 0 and self.socialdist == 0:  
                        if self.sickdays > 5 and self.random.uniform(0,1) < 0.8:
                            self.socialdist = 1
                    if self.sickdays > 14:
                        self.cured = 1
                        self.carrier = 0
                        self.socialdist = 0



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
        if len(cellmates) > 1:
            for buddy in cellmates:
                self.interactions = self.interactions + 1
                if (self.random.uniform(0,1) < self.model.infrate and 
                  buddy.cured == 0 and
                  buddy.alive == 1 and
                  buddy.carrier == 0):
                    self.transfers = self.transfers + 1
                    buddy.carrier = 1

class CoronaModel(Model):
    """A model with N persons that tracks who gets sick, and when"""
    def __init__(self, N, width, height, sd_step = 50):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.deathrate = 0.0022 #1 - (14th root of 0.97)
        self.infrate = 1.0
        self.step_index = 0
        self.socialdist_step = sd_step

        # Create agents
        for i in range (self.num_agents):
            a = Person(i, self)
            if i == 0:
                a.carrier = 1
            self.schedule.add(a)

            # Add person to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x,y))

        self.datacollector = DataCollector(
            model_reporters={"NumAlives": get_num_alives,
                             "NumCarriers": get_num_carriers,
                             "NumCureds": get_num_cureds,
                             "NumDeads": get_num_deads,
                             "R0": get_r0},
            agent_reporters={"Alive": "alive",
                             "Carrier": "carrier",
                             "Cured": "cured",
                             "SickDays": "sickdays",
                             "Transfers": "transfers",
                             "Interactions": "interactions"})

    def step(self):
        # Advance the model by one step
        self.step_index = self.step_index + 1

        # When we reach the social distancing threshold, change 
        # 80 percent of agents
        if (self.step_index == self.socialdist_step):
            for person in self.schedule.agents:
                if self.random.uniform(0,1) < 0.8:
                    person.socialdist = 1

        self.datacollector.collect(self)
        self.schedule.step()

        
