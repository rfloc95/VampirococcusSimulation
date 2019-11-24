from mesa import Agent
from vampiro_chromatium.chromatium import Chromatium


class Vampiro(Agent):
    '''
    A vampirococcus that walks around, chromatium gradient dependent
    '''

    grid = None
    x = None
    y = None
    moore = True
    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore
        self.energy = energy
    
    def gradient_move(self):
        '''
        Gradient move depending on Chromatium
        '''
        neigh_obj = self.model.grid.get_neighboor(self.pos, self.moore, include_center=True, radius=1)
        food_patches = [obj for obj in neigh_obj if isinstance(obj, Chromatium)]
        if len(food_patches) > 0:
            next_move = self.random.choice(food_patches)
            self.model.grid.move_agent(self, next_move.pos)
        
        # Otherwise move random
        else:
            next_move = self.random.choice(neigh_obj)
            self.model.grid.move_agent(self, next_move.pos)
    
    def step(self):
        '''
        Step mpdel todo!!!
        '''
        self.gradient_move()