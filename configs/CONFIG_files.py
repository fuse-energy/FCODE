import pathlib
cwd = str(pathlib.Path(__file__).parent.parent.resolve())

# File path CONFIG
results_dir = f"{cwd}/results"
simulation_path = f"{results_dir}/simulation.csv"
initial_path = f"{results_dir}/initial.csv"
results_path = f"{results_dir}/results.csv"
params_path = f"{results_dir}/params.csv"

inputs_dir = f"{cwd}/inputs"
screamer_wf_path = f"{inputs_dir}/screamer_wf.csv"

MAX_ITERATIONS = 200000
use_SCREAMER = False

# PLOT SMOOTHING
use_SMOOTHING = True
SAVGOL_WINDOW = 333
SMOOTHING_COL = ['Cr', 'P', 'BaP', 'Th', 'R', 'Ecomp', 'Efuel', 'TM']