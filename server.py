from mesa.visualization.ModularVisualization import ModularServer
from model import World
from SimpleContinuousModule import SimpleCanvas



### MODEL PARAMETERS! update them here
model_params = {
    "num_agents": 10,
    "num_food": 20,
    "width": 40,
    "height": 40,
    "prob_pheromones": 0.4,
    "prob_drop_nest" :0.001
}

def draw(agent):

    agent_type = type(agent).__name__
    portrayal = {}

    if (agent_type == "Food"):
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "blue",
                     "w": 1/50,
                     "h": 1/50
        }
    elif (agent_type == "Ant"):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 1,
                     "Color": "red",
                     "r": 4}
    elif (agent_type == "Nest"):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 2,
                     "Color": "orange",
                     "r": 8}
    return portrayal

canvas = SimpleCanvas(draw, 500, 500)

server = ModularServer(World,
                       [canvas],
                       "World",
                       model_params)

server.launch()
