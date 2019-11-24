from vampiro_chromatium.gradient_walk import GradientWalker
from vampiro_chromatium.food import FoodPatch



class Chromatium(GradientWalker):
    '''
    A chromatium that walks around, gradient dependend
    The init is the same as the GradientWalker + if you want to add more features
    '''
    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        '''
        Model step to implement!
        '''
        self.gradient_move()
