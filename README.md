# FCODE

![](docs/TITAN.mp4)

*** 
## Single Simulation
1. Create a config file in the `config` directory to change the initial conditions.
2. Change the import statement (line 5) of `MagLIF.py` to match the name of the newly created config file.
3. Run `MagLIF.py` to run the simulation.
4. The result are stored under the `results` directory. 
  - `simulation.py`: Simulation results, each row is an iteration.
  - `initial.csv`: Key-value pair of initial conditions.
  - `results.csv`: Key-value pair of simulation results.
5. Run `plot.py` to show the plots.

*** 
## Multiple Simulations: Parametric Variation
1. Create a config file in the `config_params` directory to change the initial conditions.
2. Change the import statement (line 9) of `MagLIF_param.py` to match the name of the newly created config file.
3. Run `MagLIF_param.py` to run simulations of all initial condition permutations.
4. The results are stored in `results/params.csv`.
5. Rename the results file to `params_XXMA.csv`, where `XX` is the current in `MA`.
6. In `plot_params.py`, change the `I` variable to match the `XX` from step 5.
7. Run `plot_params.py` to show the plots.


