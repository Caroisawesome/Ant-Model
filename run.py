# run.py
from model import *  # omit this in jupyter notebooks


## parameters for the world/simulation
num_iterations = 500
num_ants = 50
num_food = 100
width = 50
height = 50

## parameters for the ants
prob_peromones = 0.4
prob_drop_nest = 0.001




model = World(num_ants, num_food, width, height, prob_peromones, prob_drop_nest)

num_food_collected = 0
for i in range(num_iterations):
    num_food_collected = model.step()

print(num_food_collected, "out of", num_food, "food was collected in", num_iterations, "iterations")
