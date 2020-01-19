import pylab
import sys
from inspyred import benchmarks

from vampiro_chromatium.model import VampiroChromatium

import cma_es
import es
from inspyred_utils import NumpyRandomWrapper

def fitness_fn(list_of_4_elements):
    initial_chromatium, initial_vampiro, chromatium_reproduce, vampiro_reproduce = list_of_4_elements
    model = VampiroChromatium(int(initial_chromatium), int(initial_vampiro), chromatium_reproduce, vampiro_reproduce)
    max_steps = 1000
    chr_steps = max_steps
    for i in range(max_steps):
        steps, chrm_count, vamp_count = model.step()
        if chr_steps == max_steps and chrm_count == 0:
            chr_steps = steps
        if vamp_count == 0:
            break
            
    return (chr_steps + steps + (vamp_count + chrm_count) )**-1 

display = True# Plot initial and final populations

# parameters for the GA
args = {}

num_vars = 2
args["pop_size"] = 5 #mu
args["num_offspring"] = 10 #lambda
args["max_generations"] = 1
args["sigma"] = 1.0 # default standard deviation
args["problem_class"] = fitness_fn
#args["problem_class"] = benchmarks.Rastrigin
#/home/riccardo/PycharmProjects/BioAI/home/riccardo/PycharmProjects/BioAI
if __name__ == "__main__":
    
    if len(sys.argv) > 1 :
        rng = NumpyRandomWrapper(int(sys.argv[1]))
    else :
        rng = NumpyRandomWrapper()
        
    # Run the ES
    best_individual, best_fitness = cma_es.run(rng,num_vars=num_vars,
                                           display=display,use_log_scale=True,
                                           **args)
    
    # Note: to run the other ES youmust set args["strategy_mode"] and call
    # es.run(rng,num_vars=num_vars, display=display,**args)
                        
    
    # Display the results
    print("Best Individual:", best_individual)
    print("Best Fitness:", best_fitness)
    
    if display :
        #ioff()
        show()
