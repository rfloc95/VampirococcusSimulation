import numpy as np
import random
import matplotlib.pyplot as plt
from timeit import default_timer as timer
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from vampiro_chromatium.food import FoodPatch
from vampiro_chromatium.chromatium import Chromatium
#from vampiro_chromatium.vampiro import Vampiro
from vampiro_chromatium.vampiro_new import Vampiro
from vampiro_chromatium.model import VampiroChromatium

from vampiro_chromatium.schedule import RandomActivationByBreed





# FIXED PARAMS
height = 30
width = 30
initial_food = 0.1
food_regrowth_time = 30
vampiro_gain_from_food = 2
chromatium_gain_from_food = 5

# VARIABLES PARAMS
initial_chromatium, initial_vampiro, chromatium_reproduce, vampiro_reproduce = [80, 20, 0.04, 0.05]





model = VampiroChromatium(initial_chromatium, initial_vampiro, chromatium_reproduce, vampiro_reproduce, height, width)

def ff(model):
    stop = False
    while not stop:
        time, chrm_count, vamp_count = model.step()
        if vamp_count == 0:
            stop = True
            
    return time

