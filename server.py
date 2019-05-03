from mesa.visualization.ModularVisualization import ModularServer
from model import World
from SimpleContinuousModule import SimpleCanvas



### MODEL PARAMETERS! update them here
model_params = {
    "num_agents": 10,
    "num_food": 100,
    "width": 100,
    "height": 80,
    "prob_pheromones": 1,
    "prob_create_nest" :0.0008,
    "min_dist_between_nests": 15
}

def draw(agent):

    agent_type = type(agent).__name__
    portrayal = {}

    if (agent_type == "Food"):
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 3,
                     "Color": "blue",
                     "w": 1/50,
                     "h": 1/50
        }
    elif (agent_type == "Ant"):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 4,
                     "Color": "red",
                     "r": 4}
    elif (agent_type == "Nest"):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 3,
                     "Color": "orange",
                     "r": 8}

    else:
        portrayal = {"Shape": "circle",
                     "Filled": "false",
                     "Layer": 0,
                     "Color": "#ADD8E6",
                     "r": 6}

    return portrayal

canvas = SimpleCanvas(draw, 500, 500)

server = ModularServer(World,
                       [canvas],
                       "World",
                       model_params)

server.launch()
