#!/usr/bin/env python
# coding: utf-8

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from IconicityModel import *

# workaround for the tornado 5.0 bug
#import nest_asyncio
#nest_asyncio.apply()


def agent_representation(agent):
    iconicity_level = round(agent.iconicity_ratio() * 100)
    representation = {
                      # shape and colour of the agent
                      "Shape": "circle",
                      "Filled": "true",
                      "r": 0.5,
                      
                      # visible properties in visualisation
                      "Age of acquisition": agent.aoa,
                      "Age": agent.age,
                      "Avg. iconicity level": str(iconicity_level) + "%",
        
                      # drawing layer
                      "Layer": 0,
                      }
    
    if agent.age == 0:
        representation["r"] = 0.3
    elif agent.age == 1:
        representation["r"] = 0.5
        
    if agent.aoa == "L1":
        representation["Color"] = "green"
    elif agent.aoa == "L2":
        representation["Color"] = "red"

    return representation


grid = CanvasGrid(agent_representation, 10, 10, 500, 500)


server = ModularServer(IconicityModel,
                       [grid],
                       "Iconicity Model",
                       {"width": 10, "height": 10, "vocab_size": 10, "word_length": 5,
                        "initial_degree_of_iconicity": 0.8})
#server.port = 8521
#server.launch()
