from mesa import Agent

class FoodPatch(Agent):
    '''
    A patch of food that grows at a fixed rate and it is eaten by chromatium
    '''

    def __init__(self, unique_id, pos, model, eatable, countdown, store_level):
        '''
        Creates a new patch of food

        Args:
            eatable: (boolean) Whether the patch of food reached the necessary concentration to produce energy or not
            countdown: Time for the patch of food to be max_conc
            store_level: The times a foodpatch is eatable
        '''
        super().__init__(unique_id, model)
        self.eatable = eatable
        self.countdown = countdown
        self.pos = pos
        self.store_level = store_level
    
    def __lt__(self, other):
        '''
        Sorting list of this class by attribute store_level, descending order
        '''
        return self.store_level > other.store_level

    def step(self):
        if not self.eatable:
            if self.countdown <= 0:
                # Set as maximum concentration
                self.eatable = True
                self.countdown = self.model.food_regrowth_time
                self.store_level = 1
            else:
                self.countdown -= 1
        else:
            if self.countdown <= 0:
                # Reset countdown at max and store plus 1
                self.countdown = self.model.food_regrowth_time
                self.store_level += 1
            else:
                self.countdown -= 1

