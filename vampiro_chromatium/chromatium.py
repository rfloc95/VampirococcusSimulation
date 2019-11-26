
import operator
from mesa import Agent
from vampiro_chromatium.food import FoodPatch



class Chromatium(Agent):
    '''
    A chromatium that walks around, food gradient dependend
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
        Gradient move depending on FoodPatch!
        '''
        neigh_obj = self.model.grid.get_neighbors(self.pos, self.moore, include_center=True, radius=1)
        food_patches = [obj for obj in neigh_obj if isinstance(obj, FoodPatch) and obj.eatable]
        if len(food_patches) > 0:
            # look those with higher store
            food_patches.sort()
            highest_patches = [obj for obj in food_patches if obj.store_level == food_patches[0].store_level]
            next_move = self.random.choice(highest_patches)
            self.model.grid.move_agent(self, next_move.pos)

        # Otherwise move random
        else:
            next_move = self.random.choice(neigh_obj)
            self.model.grid.move_agent(self, next_move.pos)

    def step(self):
        '''
        Model step to implement!
        '''
        self.gradient_move()
        living = True

        # reduce energy each step
        self.energy -= 1

        # Death
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        # if there is food available eat it
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        food_patches = [obj for obj in this_cell if isinstance(obj, FoodPatch)][0]
        if food_patches.eatable:
            self.energy += self.model.chromatium_gain_from_food
            # Reduce quantity of food present in foodpatch depending on store
            if food_patches.store_level < 2:
                food_patches.store_level = 0
                food_patches.eatable = False
            else:
                food_patches.store_level -= 1

        # Reproduction
        if living and self.random.random() < self.model.chromatium_reproduce:
            # Create a new chromatium:
            self.energy /= 2
            chromatium = Chromatium(self.model.next_id(), self.pos, self.model,
                         self.moore, self.energy)
            self.model.grid.place_agent(chromatium, self.pos)
            self.model.schedule.add(chromatium)
        
