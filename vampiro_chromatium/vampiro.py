
from mesa import Agent
import math
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

    def __init__(self, unique_id, pos, model, moore, energy=None, prey=None):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore
        self.energy = energy
        self.prey = prey
    
    def gradient_move(self):
        '''
        Gradient move depending on Chromatium
        '''
        neigh_obj = self.model.grid.get_neighbors(self.pos, self.moore, include_center=True, radius=1)
        food_patches = [obj for obj in neigh_obj if isinstance(obj, Chromatium)]
        if len(food_patches) > 0:
            next_move = self.random.choice(food_patches)
            self.model.grid.move_agent(self, next_move.pos)

        # Otherwise move random
        else:
            next_move = self.random.choice(neigh_obj)
            self.model.grid.move_agent(self, next_move.pos)
    
    
    
    
    def step(self):

        self.energy -= 1
        
        # EATING
        if self.prey == None:
            self.gradient_move()
            # Check for chromatium
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            Chrome = [obj for obj in this_cell if isinstance(obj, Chromatium)]
            if len(Chrome) > 0:
                self.prey = self.random.choice(Chrome)
                self.energy += self.model.vampiro_gain_from_food
                self.prey.energy -= self.model.vampiro_gain_from_food
        else:
            if self.prey.energy > 0:
                self.model.grid.move_agent(self, self.prey.pos)
                self.energy += self.model.vampiro_gain_from_food
                self.prey.energy -= self.model.vampiro_gain_from_food
            else:
                self.prey = None
                self.gradient_move()

        # If energy == o of prey => kill chromatium
        if self.prey != None and self.prey.energy < 0:
                self.model.grid._remove_agent(self.prey.pos, self.prey)
                self.model.schedule.remove(self.prey)
                self.prey = None
        
        # Death
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            
        # Reproduce    
        if self.random.random() < self.model.vampiro_reproduce and self.prey != None:
            self.energy = math.floor(self.energy/2)
            vampirino = Vampiro(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
            self.model.grid.place_agent(vampirino, vampirino.pos)
            self.model.schedule.add(vampirino)
        
                
