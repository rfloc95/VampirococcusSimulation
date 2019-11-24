from mesa import Agent
from vampiro_chromatium.food import FoodPatch



class Chromatium(Agent):
    '''
    A chromatium that walks around, gradient dependend
    The init is the same as the GradientWalker + if you want to add more features
    '''

    grid = None
    x = None
    y = None
    moore = True
    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
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
            next_move = self.random.choice(food_patches)
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
