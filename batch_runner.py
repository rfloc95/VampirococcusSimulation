from mesa.batchrunner import BatchRunner
from vampiro_chromatium.model import VampiroChromatium
from vampiro_chromatium.chromatium import Chromatium
from vampiro_chromatium.vampiro_new import Vampiro
import matplotlib.pyplot as plt

fixed_params = {
    "width": 50,
    "height": 50,
    "vampiro_gain_from_food": 2,
    "initial_food": 0.1,
    "food_regrowth_time": 50,
    "chromatium_gain_from_food": 5
}

variable_params = {
    "initial_chromatium": [80],
    "initial_vampiro": [20],
    "chromatium_reproduce": [0.04],
    "vampiro_reproduce": [0.05]
}

batch_run = BatchRunner(
    VampiroChromatium,
    variable_params,
    fixed_params,
    iterations=1,
    max_steps=500,
    model_reporters={"Vampiro": lambda m: m.schedule.get_breed_count(Vampiro),
             "Chromatium": lambda m: m.schedule.get_breed_count(Chromatium)}
    )

batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
print(run_data.head())
plt.scatter(run_data.Chromatium, run_data.Vampiro)
plt.show()