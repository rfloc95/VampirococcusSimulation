
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
        '''
        Step mpdel todo!!!
        '''
        self.gradient_move()

	    #If there is a Chromatium, eat one
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        Chrome = [obj for obj in this_cell if isinstance(obj, Chromatium)]
        if len(Chrome) > 0: 
            chrome_to_eat = self.random.choice(Chrome)
            self.energy += self.model.vampiro_gain_from_food
            #kill the Chromatium
            self.model.grid._remove_agent(self.pos, chrome_to_eat)
            self.model.schedule.remove(chrome_to_eat)
        
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.vampiro_reproduce:
                self.energy /= 2
                vampirino = Vampiro(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
                self.model.grid.place_agent(vampirino, vampirino.pos)
                self.model.schedule.add(vampirino)
                
