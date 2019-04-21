# run.py
from model import *  # omit this in jupyter notebooks

num_iterations = 10
num_ants = 10
num_food = 5
width = 50
height = 50

model = World(num_ants, num_food, width, height)
for i in range(num_iterations):
    model.step()
