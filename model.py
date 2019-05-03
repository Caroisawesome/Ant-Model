from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
import numpy as np
import math
import json

class Ant(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.model.increment_agent_count()
        self.direction = np.random.rand() * 2 * math.pi
        self.food = 0
        self.nest_location = (0,0)
        self.dx_from_nest = 0
        self.dy_from_nest = 0
        self.drop_pheromone = False
        self.food_position = False

    def set_nest_location(self, loc):
        self.nest_location = loc

    def move(self):
        if (self.food):
            self.return_to_nest()
        elif (self.food_position and self.food == 0):
            self.return_to_food()
        else:
            self.random_walk()

    def random_walk(self):
        min = self.direction - (math.pi/4)
        r = np.random.rand()
        self.direction = (r * (math.pi/2)) + min
        dx = np.cos(self.direction)
        dy = np.sin(self.direction)
        new_position = (self.pos[0] + dx, self.pos[1] + dy)
        self.model.space.move_agent(self, new_position)

    def return_to_nest(self):
        Dx = self.nest_location[0] - self.pos[0]
        Dy = self.nest_location[1] - self.pos[1]
        dist = math.hypot(Dx, Dy)
        if (dist != 0):
            dx = Dx/dist
            dy = Dy/dist
            self.model.space.move_agent(self, (self.pos[0] + dx, self.pos[1] + dy))

    def return_to_food(self):
        Dx = self.food_position[0] - self.pos[0]
        Dy = self.food_position[1] - self.pos[1]
        dist = math.hypot(Dx, Dy)
        if (dist < 2):
            self.food_position = False
        elif (dist != 0):
            dx = Dx/dist
            dy = Dy/dist
            self.model.space.move_agent(self, (self.pos[0] + dx, self.pos[1] + dy))

    def pick_up_food(self, food):
        self.food = 1
        self.food_position = self.pos
        food.decrease_value()
        if (food.get_value() < 1):
            self.model.space.remove_agent(food)
            self.model.decrease_food_count()

    # scan current location for food or nest
    def scan_area(self):
        neighbors = self.model.space.get_neighbors(self.pos, 3)
        for n in neighbors:
            agent_type = type(n).__name__

            # ant collides with a food item, pick up food item
            if (agent_type == "Food"):
                self.pick_up_food(n)

            # drop food item if it is at a nest
            elif (agent_type == "Nest"):
                self.food = 0
                self.remember_nest()

            # site fidelity, returned to location of food
            elif (self.food_position == self.pos):
                self.food_position = False

    def remember_nest(self):
        self.nest_location = self.pos

    def randomly_generate_nest(self):
        if (np.random.rand() < self.model.prob_create_nest):
            Dx = self.nest_location[0] - self.pos[0]
            Dy = self.nest_location[1] - self.pos[1]
            dist = math.hypot(Dx, Dy)
            if (dist > self.model.min_dist_between_nests):
                self.model.generate_nest(self.pos)
                self.remember_nest()

    def step(self):
        self.move()
        self.scan_area()
        self.randomly_generate_nest()
        pass


class Food(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.model.increment_agent_count()
        self.value = 1

    def decrease_value(self):
        self.value = self.value - 1

    def get_value(self):
        return self.value

class Nest(Agent):
    def __init__(self, model):
        unique_id = model.get_agent_count()
        super().__init__(unique_id, model)
        self.model.increment_agent_count()

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
