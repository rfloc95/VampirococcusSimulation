'''
Vampirococcus and Chromatium Model simulation
'''


from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from vampiro_chromatium.food import FoodPatch
from vampiro_chromatium.chromatium import Chromatium
from vampiro_chromatium.schedule import RandomActivationByBreed


class VampiroChromatium(Model):
    '''
    Vampiro-Chromatium Predation Model
    '''

    height = 20
    width = 20

    initial_chromatium = 10
    initial_vampiro = 50

    chromatium_reproduce = 0.04
    vampiro_reproduce = 0.05

    vampirto_gain_from_food = 20

    food = False
    initial_food = 0.1
    food_regrowth_time = 30
    chromatium_gain_from_food = 4

    verbose = True  # Print-monitoring

    description = 'A model for simulating vampirococcus and chromatium (predator-prey) ecosystem modelling.'

    def __init__(self, height=20, width=20,
                 initial_chromatium=10, initial_vampiro=50,
                 chromatium_reproduce=0.04, vampiro_reproduce=0.05,
                 vampiro_gain_from_food=20,
                 food=False, initial_food=0.1, food_regrowth_time=5000, chromatium_gain_from_food=4):
        '''
        Create a new Vampiro-Chromatium model with the given parameters.

        Args:
            initial_chromatium: Number of chromatium to start with
            initial_vampiro: Number of vampiro to start with
            chromatium_reproduce: Probability of each chromatium reproducing each step
            vampiro_reproduce: Probability of each vampiro reproducing each step
            vampiro_gain_from_food: Energy a vampiro gains from eating a chromatium\
            food: Whether to have the chromatium eat food for energy
            initial_food: initial food as proportion of the total grid 
            food_regrowth_time: How long it takes for a food patch to regrow
                                 once it is eaten
            chromatium_gain_from_food: Energy chromatium gain from food, if enabled.
        '''
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_chromatium = initial_chromatium
        self.initial_vampiro = initial_vampiro
        self.chromatium_reproduce = chromatium_reproduce
        self.vampiro_reproduce = vampiro_reproduce
        self.vampiro_gain_from_food = vampiro_gain_from_food
        self.food = food
        self.food_regrowth_time = food_regrowth_time
        self.chromatium_gain_from_food = chromatium_gain_from_food

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)

        self.datacollector = DataCollector(
            {"Chromatium": lambda m: m.schedule.get_breed_count(Chromatium)})

        # Create Chromatium:
        for i in range(self.initial_chromatium):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.chromatium_gain_from_food)
            chromatium = Chromatium(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(chromatium, (x, y))
            self.schedule.add(chromatium)
        
        # Create Vampiro:
        '''
        for i in range(self.initial_vampiro):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            vampiro = Vampiro(self.next_id(), (x, y), self, True)
            self.grid.place_agent(vampiro, (x, y))
            self.schedule.add(vampiro)
        '''


        # Create food patches:
        # Implemented in this way every cells has only one path of food
        if self.food:
            for agent, x, y in self.grid.coord_iter():

                if self.random.uniform(0,1) < self.initial_food:
                    eatable = True
                else:
                    eatable = False

                if eatable:
                    countdown = self.food_regrowth_time
                else:
                    countdown = self.random.randrange(self.food_regrowth_time)

                patch = FoodPatch(self.next_id(), (x, y), self,
                                   eatable, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

        
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_breed_count(Chromatium)])