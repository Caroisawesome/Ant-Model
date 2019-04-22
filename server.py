from mesa.visualization.ModularVisualization import ModularServer
from model import World
from SimpleContinuousModule import SimpleCanvas

model_params = {
    "num_agents": 10,
    "num_food": 20,
    "width": 40,
    "height": 40
}

def draw(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 2}
    return portrayal

canvas = SimpleCanvas(draw, 500, 500)

server = ModularServer(World,
                       [canvas],
                       "World",
                       model_params)

server.launch()
