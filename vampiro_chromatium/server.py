from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from vampiro_chromatium.food import FoodPatch
from vampiro_chromatium.chromatium import Chromatium
#from vampiro_chromatium.vampiro import Vampiro
from vampiro_chromatium.model import VampiroChromatium


def vampiro_chromatium_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is FoodPatch:
        if agent.eatable:
            portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
            portrayal["text"] = agent.store_level
            portrayal["text_color"] = "Red"
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Chromatium:
        portrayal["Shape"] = "vampiro_chromatium/resources/chromatium.png"
        # https://icons8.com/web-app/433/sheep
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    return portrayal
'''
    elif type(agent) is Wolf:
        portrayal["Shape"] = "wolf_sheep/resources/wolf.png"
        # https://icons8.com/web-app/36821/German-Shepherd
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "White"

    elif type(agent) is GrassPatch:
'''

canvas_element = CanvasGrid(vampiro_chromatium_portrayal, 20, 20, 500, 500)
#chart_element = ChartModule([{"Label": "Vampiro", "Color": "#AA0000"}])#,
#                             {"Label": "Chromatium", "Color": "#666666"}])
model_params = {"food": UserSettableParameter('checkbox', 'Food Enabled', True),
                "initial_food": UserSettableParameter('slider', 'Initial Food Proportion', 0.2, 0, 1.0, 0.01),
                "food_regrowth_time": UserSettableParameter('slider', 'Food Regrowth Time', 50, 1, 200, 1),
                "initial_chromatium": UserSettableParameter('slider', 'Initial Chromatium Population', 20, 1, 100, 1),
                "chromatium_reproduce": UserSettableParameter('slider', 'Chromatium Reproduction Rate', 0.04, 0.01, 1.0,
                                                         0.01)#,
                #"initial_wolves": UserSettableParameter('slider', 'Initial Wolf Population', 50, 10, 300),
                #"wolf_reproduce": UserSettableParameter('slider', 'Wolf Reproduction Rate', 0.05, 0.01, 1.0,
                #                                        0.01,
                #                                        description="The rate at which wolf agents reproduce."),
                #"wolf_gain_from_food": UserSettableParameter('slider', 'Wolf Gain From Food Rate', 20, 1, 50),
                #"sheep_gain_from_food": UserSettableParameter('slider', 'Sheep Gain From Food', 4, 1, 10)
                }

#server = ModularServer(VampiroChromatium, [canvas_element, chart_element], "Vampiro Chromatium Predation", model_params)
server = ModularServer(VampiroChromatium, [canvas_element], "Vampirococcus Chromatium Ecosystem", model_params)
server.port = 8521
