from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
import numpy as np
import math

class Ant(Agent):
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.direction = np.random.rand() * 2 * math.pi
        self.location = model.center

    def move(self):
        min = self.direction - (math.pi/4)
        r = np.random.rand()
        self.direction = (r * (math.pi/2)) + min
        dx = np.cos(self.direction)
        dy = np.sin(self.direction)
        self.location = (self.location[0]+dx, self.location[1]+dy)
        self.model.space.move_agent(self, self.location)

    def step(self):
        self.move()
        pass


class Food(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.value = 1

class Nest(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class World(Model):
    def __init__(self, num_agents, num_food, width, height):
        self.center = (width/2, height/2)
        self.num_agents = num_agents
        self.num_food = num_food
        self.space = ContinuousSpace(width, height, False, 0, 0)
        self.schedule = RandomActivation(self)
        self.generate_ants()
        self.generate_nest()
        self.generate_food()

    def generate_ants(self):
        for i in range(self.num_agents):
            a = Ant(i, self)
            self.schedule.add(a)
            self.space.place_agent(a, self.center)

    def generate_nest(self):
        n = Nest(0, self)
        self.schedule.add(n)
        self.space.place_agent(n, self.center)

    def generate_food(self):
        for i in range(self.num_food):
            f = Food(i, self)
            x = np.random.rand() * self.space.width
            y = np.random.rand() * self.space.height
            self.schedule.add(f)
            self.space.place_agent(f, (x, y))

    def step(self):
        self.schedule.step()
