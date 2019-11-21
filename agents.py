from vampiro_chromatium import FoodPatch, GradientWalker



class Chromatium(GradientWalker):
    '''
    A chromatium that walks around, gradient dependend
    The init is the same as the GradientWalker + if you want to add more features
    '''

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)

    def step(self):
        '''
        Model step to implement!
        '''
        self.gradient_walk()
