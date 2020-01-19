# Vampirococcus Agent-Based Model Simulation

## Summary

A simple ecological model, consisting of three agent types: bacteria Vampirococcus, bacteria Chromatium, and food. The Vampirococcus and the Chromatium wander around the grid by gradient. Vampirococcus and Chromatium both expend energy moving around, and replenish it by eating. Chromatium eat food, and Vampirococcus eat Chromatium if they end up on the same grid cell.


The model is tests and demonstrates several Mesa concepts and features:
 - MultiGrid
 - Multiple agent types (vampiro, chromatium, food)
 - Overlay arbitrary text (vampiro's energy) on agent's shapes while drawing on CanvasGrid
 - Writing a model composed of multiple files.
 - Dynamically adding and removing agents from the schedule

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```
NOTE: python3 required!!!

## Running Simulation

To run the interactive simulation from the main folder type:

```
   $ python run.py
```

## Running Optimization

To perform CMA-ES optimization of initial population (it will require a lot of time):

```
   $ python Deap.py
```

You can also try to optimize only reproduction rates (it will also require a lot of time):

```
   $ python Deap_small.py
```
