from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from Ant import Ant
from food import Food
from nest import Nest
import numpy as np
import math
import json

class World(Model):
    def __init__(self, num_agents, num_food, width, height, prob_pheromones, prob_create_nest, min_dist_between_nests):
        self.width = width
        self.height = height
        self.center = (width/2, height/2)
        self.num_agents = num_agents
        self.num_food = num_food
        self.prob_pheromones = prob_pheromones
        self.prob_create_nest = prob_create_nest
        self.min_dist_between_nests = min_dist_between_nests
        self.space = ContinuousSpace(width, height, True, 0, 0)
        self.schedule = RandomActivation(self)
        self.running = True
        self.agent_count = 0
        self.generate_nest(self.center)
        self.generate_ants()
        self.generate_food()

    def increment_agent_count(self):
        self.agent_count+=1

    def get_agent_count(self):
        return self.agent_count

    def generate_ants(self):
        for i in range(1,self.num_agents):
            a = Ant(i, self)
            a.set_nest_location(self.center)
            self.schedule.add(a)
            self.space.place_agent(a, self.center)

    def generate_nest(self, position):
        n = Nest(self)
        self.schedule.add(n)
        self.space.place_agent(n, position)

    def generate_food(self):
        for i in range(self.num_agents, self.num_food):
            f = Food(i, self)
            x = np.random.rand() * self.space.width
            y = np.random.rand() * self.space.height
            self.schedule.add(f)
            self.space.place_agent(f, (x, y))

    def decrease_food_count(self):
        self.num_food = self.num_food - 1

    def step(self):
        self.schedule.step()
        return self.num_food
