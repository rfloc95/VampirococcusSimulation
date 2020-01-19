from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from vampiro_chromatium.food import FoodPatch

from vampiro_chromatium.chromatium import Chromatium
from vampiro_chromatium.vampiro import Vampiro

from vampiro_chromatium.model import VampiroChromatium


def vampiro_chromatium_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is FoodPatch:
        if agent.eatable:
            #portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
            portrayal["Color"] = "#68BC3C"
            portrayal["text"] = agent.store_level
            portrayal["text_color"] = "#FEFFE1"
        else:
            #portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
            portrayal["Color"] = "#FEFFE1"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Chromatium:
        '''
        portrayal["Shape"] = "vampiro_chromatium/resources/chromatium.png"
        # https://icons8.com/web-app/433/sheep
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1'''
        portrayal = {"Shape": "circle",
                 "Color": "#FC3636",
                 "Filled": "true",
                 "Layer": 0,
                 "r": .9}
    
    elif type(agent) is Vampiro:
        '''
        portrayal["Shape"] = "vampiro_chromatium/resources/batman.jpg"
        # https://icons8.com/web-app/36821/German-Shepherd
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        #portrayal["text"] = round(agent.energy, 1)
        #portrayal["text_color"] = "Green"'''
        portrayal = {"Shape": "circle",
                 "Color": "#4F4949",
                 "Filled": "true",
                 "Layer": 0,
                 "r": .5}

    return portrayal


canvas_element = CanvasGrid(vampiro_chromatium_portrayal, 50, 50, 600, 600)
chart_element = ChartModule([{"Label": "Vampiro", "Color": "#4F4949"},
                             {"Label": "Chromatium", "Color": "#FC3636"}])
model_params = {"food": UserSettableParameter('checkbox', 'Food Enabled', True),
                "initial_food": UserSettableParameter('slider', 'Initial Food Proportion', 0.2, 0.01, 1.0, 0.01),
                "food_regrowth_time": UserSettableParameter('slider', 'Food Regrowth Time', 50, 1, 300,1),
                "initial_chromatium": UserSettableParameter('slider', 'Initial Chromatium Population', 90, 1, 200,1),
                "chromatium_reproduce": UserSettableParameter('slider', 'Chromatium Reproduction Rate', 0.3, 0.01, 1.0, 0.01),
                "initial_vampiro": UserSettableParameter('slider', 'Initial Vampiro Population', 55, 1, 200, 1),
                "vampiro_reproduce": UserSettableParameter('slider', 'Vampiro Reproduction Rate', 0.15, 0.01, 1.0, 0.01,
                                                       description="The rate at which vampiro agents reproduce."),
                "vampiro_gain_from_food": UserSettableParameter('slider', 'Vampiro Gain From Food Rate', 2, 1, 30, 1),
                "chromatium_gain_from_food": UserSettableParameter('slider', 'Chromatium Gain From Food', 5, 1, 30, 1)
                }
server = ModularServer(VampiroChromatium, [canvas_element, chart_element], "Vampiro Chromatium Predation", model_params)
server.port = 8521
