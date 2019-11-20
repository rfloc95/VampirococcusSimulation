'''
Generalized move behaviour of agents Chromatium and Vampiro, one grid cell at a time.
'''

from mesa import Agent
from agents import FoodPatch

class GradientWalker(Agent):
        '''
        Class implementing random walker methods in a generalized manner.

        Not indended to be used on its own, but to inherit its methods to multiple
        other agents.

        '''

        grid = None
        x = None
        y = None
        moore = True

        def __init__(self, unique_id, pos, model, moore=True):
            '''
            grid: The MultiGrid object in which the agent lives.
            x: The agent's current x coordinate
            y: The agent's current y coordinate
            moore: If True, may move in all 8 directions.
                    Otherwise, only up, down, left, right.
            '''
            super().__init__(unique_id, model)
            self.pos = pos
            self.moore = moore
