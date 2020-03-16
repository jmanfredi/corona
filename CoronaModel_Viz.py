from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from CoronaModel import *

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "blue",
                 "r": 0.5}

    if agent.carrier == 1:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.75

    if agent.cured == 1:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.5

    if agent.alive == 0:
        portrayal["r"] = 0.01

    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

server = ModularServer(CoronaModel,
                       [grid],
                       "Corona Model",
                       {"N":50, "width":10, "height":10})
server.port = 8521
server.launch()