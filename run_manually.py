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

import cma
import numpy as np
import math



# Fitness function
def fitness_fn(list_of_2_elements):
    initial_chromatium, initial_vampiro = list_of_2_elements
    model = VampiroChromatium(int(initial_chromatium), int(initial_vampiro))
    max_steps = 5000
    chr_steps = max_steps
    for i in range(max_steps):
        steps, chrm_count, vamp_count = model.step()
        if chr_steps == max_steps and chrm_count == 0:
            chr_steps = steps
        if vamp_count == 0:
            break
            
    return (chr_steps + steps + (vamp_count + chrm_count) )**-1 


## FIXED PARAMS
# Check that model has these values!!
height = 50
width = 50
initial_food = 0.1
food_regrowth_time = 30
vampiro_gain_from_food = 2
chromatium_gain_from_food = 5
vampiro_reproduce = 0.15
chromatium_reprodice = 0.3


# nella lista i paramtreti per popolazione chrm e vamp
es = cma.CMAEvolutionStrategy([60, 20], 10, {'maxiter':100, 'popsize':20})
while not es.stop():
    solutions = es.ask()
    es.tell(solutions, [fitness_fn(s) for s in solutions])
    es.disp()
    es.result_pretty()
res = es.result

print(res[0])


