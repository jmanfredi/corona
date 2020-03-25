from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

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

# Full model
grid = CanvasGrid(agent_portrayal, 40, 40, 500, 500)
# Simple example
#grid = CanvasGrid(agent_portrayal, 4, 4, 500, 500)

chart = ChartModule(#[{"Label": "Alive","Color": "Black"},
                     [{"Label": "NumCarriers","Color": "Red"},
                     {"Label": "NumCureds","Color": "Green"}],
                     #{"Label": "NumDeads","Color": "Orange"}],
                     canvas_height = 200,
                     canvas_width = 500,
                     data_collector_name='datacollector')

server = ModularServer(CoronaModel,
                       [grid, chart],
                       "Corona Model",
#                       {"N":2, "width":4, "height":4})
                       {"N":1000, "width":40, "height":40, "sd_step":-20})
server.port = 8521
server.launch()