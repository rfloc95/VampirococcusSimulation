from mesa import Agent


class FoodPatch(Agent):
    '''
    A patch of food that grows at a fixed rate and it is eaten by chromatium
    '''

    def __init__(self, unique_id, pos, model, eatable, countdown):
        '''
        Creates a new patch of food

        Args:
            eatable: (boolean) Whether the patch of food reached the necessary concentration to produce energy or not
            countdown: Time for the patch of food to be max_conc
        '''
        super().__init__(unique_id, model)
        self.eatable = eatable
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.eatable:
            if self.countdown <= 0:
                # Set as maximum concentration
                self.eatable = True
                self.countdown = self.model.food_regrowth_time
            else:
                self.countdown -= 1
