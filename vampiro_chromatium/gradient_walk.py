'''
Generalized move behaviour of agents Chromatium and Vampiro, one grid cell at a time.
'''

from mesa import Agent
from vampiro_chromatium.food import FoodPatch

class GradientWalker(Agent):
        '''
        Class implementing gradient walker methods in a generalized manner.

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
            foodclass: which class to use as food for gradient between FoodPatch and other
            '''
            super().__init__(unique_id, model)
            self.pos = pos
            self.moore = moore

        def gradient_move(self):
            neigh_obj = self.model.grid.get_neighbors(self.pos, self.moore, include_center=True, radius=1)
            food_patches = [obj for obj in neigh_obj if isinstance(obj, FoodPatch) and obj.eatable]
            if len(food_patches) > 0:
                next_move = self.random.choice(food_patches)
                self.model.grid.move_agent(self, next_move.pos)

            # Otherwise move random
            else:
                next_move = self.random.choice(neigh_obj)
                self.model.grid.move_agent(self, next_move.pos)



