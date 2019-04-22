from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
import numpy as np
import math
import json

class Ant(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.direction = np.random.rand() * 2 * math.pi
        self.food = 0
        self.nest_location = (0,0)

    def set_nest_location(self, loc):
        self.nest_location = loc

    def move(self):
        if (self.food):
            self.return_to_nest()
        else:
            self.random_walk()

    def random_walk(self):
        min = self.direction - (math.pi/4)
        r = np.random.rand()
        self.direction = (r * (math.pi/2)) + min
        dx = np.cos(self.direction)
        dy = np.sin(self.direction)
        self.model.space.move_agent(self, (self.pos[0] + dx, self.pos[1] + dy))

    def return_to_nest(self):
        Dx = self.nest_location[0] - self.pos[0]
        Dy = self.nest_location[1] - self.pos[1]
        dist = math.hypot(Dx, Dy)
        dx = Dx/dist
        dy = Dy/dist
        self.model.space.move_agent(self, (self.pos[0] + dx, self.pos[1] + dy))

    def step(self):
        self.move()
        neighbors = self.model.space.get_neighbors(self.pos, 1)
        for n in neighbors:
            if (n.unique_id >= self.model.num_agents):
                # ant collides with a food item
                self.food = 1
                n.decrease_value()
            elif (n.unique_id == 0):
                self.food = 0
        pass


class Food(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.value = 1

    def decrease_value(self):
        self.value = self.value - 1
        #if (self.value < 1):
            #self.model.space.remove_agent(self)

class Nest(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class World(Model):
    def __init__(self, num_agents, num_food, width, height):
        self.center = (width/2, height/2)
        self.num_agents = num_agents
        self.num_food = num_food
        self.space = ContinuousSpace(width, height, True, 0, 0)
        self.schedule = RandomActivation(self)
        self.generate_nest()
        self.generate_ants()
        self.generate_food()
        self.running = True

    def generate_ants(self):
        for i in range(1,self.num_agents):
            a = Ant(i, self)
            a.set_nest_location(self.center)
            self.schedule.add(a)
            self.space.place_agent(a, self.center)

    def generate_nest(self):
        n = Nest(0, self)
        self.schedule.add(n)
        self.space.place_agent(n, self.center)

    def generate_food(self):
        for i in range(self.num_agents, self.num_food):
            f = Food(i, self)
            x = np.random.rand() * self.space.width
            y = np.random.rand() * self.space.height
            self.schedule.add(f)
            self.space.place_agent(f, (x, y))

    def step(self):
        self.schedule.step()
