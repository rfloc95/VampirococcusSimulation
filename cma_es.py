import cma
from inspyred import benchmarks
import inspyred_utils
import plot_utils

from pylab import *


def run(random,display=False, num_vars=0, problem_class=benchmarks.Sphere, 
           **kwargs) :
    
    problem = problem_class(num_vars)
    if "pop_init_range" in kwargs :
        generator=inspyred_utils.generator
    else :
        generator=inspyred_utils.generator_wrapper(problem.generator)
    
    es = cma.CMAEvolutionStrategy(generator(random, kwargs),
                                   kwargs["sigma"],
                                   {'popsize': kwargs["num_offspring"],
                                    'seed' : random.rand() * 100000,
                                    'CMA_mu' : kwargs["pop_size"]}) 
    
    if display :
        animator = plot_utils.Animator(**kwargs)
    else :
        animator = None
    
    gen = 0
    while gen < kwargs["max_generations"] :
        candidates = es.ask()    # get list of new solutions
        fitnesses = problem.evaluator(candidates, kwargs)
        if gen == 0 :
            initial_pop = asarray(candidates).copy()
            initial_fitnesses = asarray(fitnesses).copy()
        
        
        if animator is not None :
            mean_fit = mean(fitnesses)
            if gen == 0 :  
                # put in data to scale figure
                animator.queue.put((kwargs["max_generations"], mean_fit))
            best_fit = es.best.f
            animator.queue.put((gen,best_fit,mean_fit))
            pause(0.0001)
        
        es.tell(candidates, fitnesses)
        gen += 1
    
    final_pop = asarray(es.ask())
    final_pop_fitnesses = asarray(problem.evaluator(final_pop, kwargs))
    
    best_guy = es.best.x
    best_fitness = es.best.f
    
    if display : 
        animator.stop()
        # Plot the parent and the offspring on the fitness landscape 
        # (only for 1D or 2D functions)
        if num_vars == 1 :
            plot_utils.plot_results_1D(problem, initial_pop, 
                                  initial_fitnesses, 
                                  final_pop, final_pop_fitnesses,
                                  'Initial Population', 'Final Population')
    
        elif num_vars == 2 :
            plot_utils.plot_results_2D(problem, initial_pop, 
                                  final_pop, 'Initial Population', 
                                  'Final Population')

    return best_guy, best_fitness
