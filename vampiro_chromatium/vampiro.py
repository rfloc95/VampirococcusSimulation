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

    def __init__(self, unique_id, pos, model, moore, energy=None, ):
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
        self.energy -= 1
        
       
	    #If there is a Chromatium, eat one
        this_cell = self.model.grid.get_neighbors(self.pos, self.moore, include_center=True, radius=1) #this_cell = self.model.grid.get_cell_list_contents([self.pos])
        Chrome = [obj for obj in this_cell if isinstance(obj, Chromatium)]
        id_list = [obj.unique_id for obj in Chrome]      
        
        if len(Chrome) > 0: #devo capire come prendere l'agente da Chrome con l'id giusto, magari con un ciclo for che mi mette in un oggetto l'agente ma solo quello con l'id giusto
            has_eaten = False
            if id_unico in id_list: 
                self.energy += self.model.vampiro_gain_from_food
                Chrome.energy -= self.model.vampiro_gain_from_food 
                has_eaten = True
                self.model.grid.move_agent(self, Chrome.pos)
                #kill the Chromatium
                if Chrome.energy == 0:
                    self.model.grid._remove_agent(Chrome.pos, Chrome)
                    self.model.schedule.remove(Chrome)               
            elif has_eaten == False: 
                chrome_to_eat = self.random.choice(Chrome)
                self.energy += self.model.vampiro_gain_from_food
                chrome_to_eat.energy -= self.model.vampiro_gain_from_food
                id_unico = chrome_to_eat.unique_id
            #kill the Chromatium
                if chrome_to_eat.energy == 0:
                    self.model.grid._remove_agent(chrome_to_eat.pos, chrome_to_eat)
                    self.model.schedule.remove(chrome_to_eat)
            #attach to the chromatium and follow it
                self.model.grid.move_agent(self, chrome_to_eat.pos)  
                has_eaten = True
        else:
            self.gradient_move()
        

        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.vampiro_reproduce:
                self.energy /= 2
                vampirino = Vampiro(self.model.next_id(), self.pos, self.model, self.moore, self.energy)
                self.model.grid.place_agent(vampirino, vampirino.pos)
                self.model.schedule.add(vampirino)
        
                
