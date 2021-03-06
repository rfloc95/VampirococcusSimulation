#imports
import random
import deap
import numpy
import statistics
import matplotlib.pyplot as plt
import pandas as pd
from deap import cma
from deap import base
from deap import creator
from deap import tools
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from vampiro_chromatium.food import FoodPatch
from vampiro_chromatium.chromatium import Chromatium
from vampiro_chromatium.vampiro import Vampiro
from vampiro_chromatium.model import VampiroChromatium
from vampiro_chromatium.schedule import RandomActivationByBreed
import datetime

best_of_all = []
#defining the fitness function(basically a weighted sum of the populations by the steps take + the average difference of the population during the simulation)
def fitness_fn(list_of_two):
    model = VampiroChromatium(100,100,chromatium_reproduce=list_of_two[0], vampiro_reproduce=list_of_two[1])
    max_steps = 5000 #the maximum number of steps the simulation will do before stopping
    if list_of_two[0] < 0.1 or list_of_two[1] < 0.1:
        fitness_i = -10**30
    elif list_of_two[0] > 1 or list_of_two[1] > 1:
        fitness_i = -10**30
    else:
        for i in range(max_steps):
            steps, chrm_count, vamp_count = model.step()
            if chrm_count == 0 or vamp_count == 0:
                break
        if steps >= max_steps-1:
            fitness_i = steps *(chrm_count + vamp_count + 1)
        else:
            fitness_i = steps
        print(steps) 
    
    return fitness_i,

#randomly generate individuals for the population
def indiv_creator():
    chrome = random.uniform(0,1)
    vampa = random.uniform(0,1) 
    return [chrome, vampa]

#deap
creator.create("FitnessMin", base.Fitness, weights=(1.0,)) #generating the fitness in deap, which maximizes the objective
creator.create("Individual", list, fitness=creator.FitnessMin) #creation of the individual in deap
toolbox = base.Toolbox()
toolbox.register("individual_creator", indiv_creator) #recalls the indiv_creator function in the toolbox
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.individual_creator, 1) #generates one individual 
toolbox.register("evaluate", fitness_fn) #registrates the fitness function in the toolbox

#plot the fitness of every generation
def plottin(logbook):
    average = []
    minimum = []
    maximum = []
    generation = []
    counter = 0
    for i in logbook:
        generation.append(logbook[counter][0]["gen"])
        average.append(logbook[counter][0]["avg"])
        minimum.append(logbook[counter][0]["min"])
        maximum.append(logbook[counter][0]["max"])
        counter += 1 
    df=pd.DataFrame({'x': generation, 'y1': average, 'y2': minimum, 'y3': maximum })
    plt.plot( 'x', 'y1', data=df, marker='', color='red', linewidth=2, label = "average")
    plt.plot( 'x', 'y2', data=df, marker='', color='black', linewidth=2, label = "minimum")
    plt.plot( 'x', 'y3', data=df, marker='', color='blue', linewidth=2, label="maximum")
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.legend()
    plt.show()

#main algorithm, using DEAP cma strategy to find the best parameters for the solution
def main():
    strategy = deap.cma.Strategy(centroid = [0.5,0.5], sigma = 0.05, lambda_ = 20) #using the cma strategy starting from individuals around 60,20 as parameters, 10 as std.dev, 20 offprings to generate
    toolbox.register("generate", strategy.generate, creator.Individual)
    toolbox.register("update", strategy.update)
    hof = tools.HallOfFame(3, similar = numpy.array_equal) #Hall of fame of the three best individuals of all time
    stats = tools.Statistics(lambda ind: ind.fitness.values) #statistics to compile during the evaluations
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    ngen = 20 #the number of generations the algorithm will do 
    logbooks = list()
    best_of_gen = []
    best_fitness_gen = 0
    for g in range(ngen):
        print("Generation {}/{}     time: {}".format(g,ngen, datetime.datetime.now()))
        logbooks.append(tools.Logbook())
        logbooks[-1].header = "gen", "evals", "std", "min", "avg", "max"
        population = toolbox.generate()
        fitnesses = toolbox.map(toolbox.evaluate, population) #fitness for each individual is generated 
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit
            if fit[0] > best_fitness_gen:
                best_fitness_gen = fit[0]
                best_of_gen = ind
        toolbox.update(population) #population is updated
        hof.update(population) #hof is updated
        record = stats.compile(population) #statistics are recorded 
        logbooks[-1].record(gen=g, evals=20, **record)
        print("The best of generation " + str(g) + " is "+ str(best_of_gen) + " that has a fitness of: " + str(best_fitness_gen))
        best_of_gen = []
        best_fitness_gen = 0
    print("The best set of parameters is: " + str(hof[0]))
    print("You can also try: " + str(hof[1]) + " or " + str(hof[2]))
    return logbooks
     
plottin(main())
print(best_of_all)