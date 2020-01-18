'''
Vampirococcus and Chromatium Model simulation
'''


from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from vampiro_chromatium.food import FoodPatch
from vampiro_chromatium.chromatium import Chromatium
#from vampiro_chromatium.vampiro import Vampiro
from vampiro_chromatium.vampiro_new import Vampiro

from vampiro_chromatium.schedule import RandomActivationByBreed


class VampiroChromatium(Model):
    '''
    Vampiro-Chromatium Predation Model
    '''

    height = 50
    width = 50

    initial_chromatium = 50
    initial_vampiro = 50

    chromatium_reproduce = 0.8
    vampiro_reproduce = 0.4

    vampiro_gain_from_food = 2

    food = False
    initial_food = 0.1
    food_regrowth_time = 30
    chromatium_gain_from_food = 5

    verbose = False  # Print-monitoring

    description = 'A model for simulating vampirococcus and chromatium (predator-prey) ecosystem modelling.'

    def __init__(self, initial_chromatium, initial_vampiro, chromatium_reproduce=0.3, vampiro_reproduce=0.30,
                height=50, width=50, vampiro_gain_from_food=2,
                food=True, initial_food=0.1, food_regrowth_time=50, chromatium_gain_from_food=5):
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
        self.initial_food = initial_food
        self.chromatium_reproduce = chromatium_reproduce
        self.vampiro_reproduce = vampiro_reproduce
        self.vampiro_gain_from_food = vampiro_gain_from_food
        self.food = food
        self.food_regrowth_time = food_regrowth_time
        self.chromatium_gain_from_food = chromatium_gain_from_food

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)

        self.datacollector = DataCollector(
            {"Vampiro": lambda m: m.schedule.get_breed_count(Vampiro),
             "Chromatium": lambda m: m.schedule.get_breed_count(Chromatium)})

        self.random.seed(30)


        # Create Chromatium:
        for i in range(self.initial_chromatium):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = 2 * self.chromatium_gain_from_food
            chromatium = Chromatium(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(chromatium, (x, y))
            self.schedule.add(chromatium)
        
        # Create Vampiro:
        
        for i in range(self.initial_vampiro):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = 5 * self.vampiro_gain_from_food
            vampiro = Vampiro(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(vampiro, (x, y))
            self.schedule.add(vampiro)
        


        # Create food patches:
        # Implemented in this way every cells has only one path of food
        if self.food:
            for agent, x, y in self.grid.coord_iter():

                if self.random.uniform(0,1) < self.initial_food:
                    eatable = True
                    store_level = self.random.randint(1,10) 
                else:
                    eatable = False
                    store_level = 0
                countdown = self.random.randrange(self.food_regrowth_time)
                patch = FoodPatch(self.next_id(), (x, y), self,
                                   eatable, countdown, store_level)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

        
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_breed_count(Chromatium),
                   self.schedule.get_breed_count(Vampiro)])
        return [self.schedule.time,
                   self.schedule.get_breed_count(Chromatium),
                   self.schedule.get_breed_count(Vampiro)]
    
    def run_model(self, step_count=200):

        if self.verbose:
            print('Initial number vampirococcus: ',
                  self.schedule.get_breed_count(Vampiro))
            print('Initial number chromatium: ',
                  self.schedule.get_breed_count(Chromatium))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number vampirococcus: ',
                  self.schedule.get_breed_count(Vampiro))
            print('Final numberpass chromatium: ',
                  self.schedule.get_breed_count(Chromatium))
