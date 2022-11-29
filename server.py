from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
import time
import numpy as np
import itertools
from agent import *
from model import StreetModel

start = time.time()
exec_time = 10000
gens = 0
X = 10
Y = 10
vacuums = 3
dirt_percentage = 0.8

simulationParams = {
    "M": X,
    "N": Y,
}
'''
    "vacuums": UserSettableParameter(
        "slider",
        "Vacuums",
        3, #default
        1, #min
        20, #max
        1, #step
        description="Choose the number of vacuums.",
    ),
    "dirty_percentage": UserSettableParameter(
        "slider",
        "Dirty percentage",
        0.5, #default
        0.1, #min
        1, #max
        0.1, #step
        description="Choose the number of dirty percentage.",
    ),
    "exec_time": UserSettableParameter(
        "slider",
        "Execution time",
        100, #default
        10, #min
        10000, #max
        10, #step
        description="Choose the execution time.",
    ),
    '''

def agent_portrayal(agent):
    portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Color": "red",
                    "Layer": 1,
                    "w": 0,
                    "h": 0}
    if type(agent) is GrassAgent:
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Color": "green",
                    "Layer": 0,
                    "r": 0.5,
                    "w": 1,
                    "h": 1}
    if type(agent) is TrafficLightAgent:
        if agent.state == "Red":
            portrayal = {"Shape": "rect",
                        "Filled": "true",
                        "Color": "red",
                        "Layer": 0,
                        "w": 0.2,
                        "h": 0.6}
        elif agent.state == "Yellow":
            portrayal = {"Shape": "rect",
                        "Filled": "true",
                        "Color": "yellow",
                        "Layer": 0,
                        "w": 0.2,
                        "h": 0.6}
        elif agent.state == "Green":
            portrayal = {"Shape": "rect",
                        "Filled": "true",
                        "Color": "green",
                        "Layer": 0,
                        "w": 0.2,
                        "h": 0.6}
    if type(agent) is CarAgent:
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Color": "red",
                    "Layer": 1,
                    "w": 0.5,
                    "h": 0.5}
    if type(agent) is CarAgentDifferentA:
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Color": "blue",
                    "Layer": 1,
                    "w": 0.5,
                    "h": 0.5}
    if type(agent) is CarAgentDifferentB:
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Color": "purple",
                    "Layer": 1,
                    "w": 0.5,
                    "h": 0.5}
    if type(agent) is CarAgentDifferentC:
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Color": "orange",
                    "Layer": 1,
                    "w": 0.5,
                    "h": 0.5}
    if type(agent) is RoadAgent:
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Color": "red",
                    "Layer": 1,
                    "w": 0,
                    "h": 0}

    if type(agent) is CrashAgent:
        portrayal = {"Shape": "circle",
                    "Filled": "true",
                    "Color": "black",
                    "Layer": 3,
                    "r": 1}

    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)



server = ModularServer(StreetModel,[grid],"Street Model",simulationParams)
server.port = 8521
server.launch()