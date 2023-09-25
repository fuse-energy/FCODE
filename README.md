# FCODE

Accompanying simulation code for [MagLIF: Dynamics and energetics of liner and fuel](https://www.sciencedirect.com/science/article/pii/S0042207X23006681).





https://github.com/fuse-energy/FCODE/assets/77456691/39d5dfd2-c731-4351-a44f-a1cb29a1bc93





## Single Simulation
1. Create a config file in the `config` directory to change the initial conditions.
2. Change the import statement (line 5) of `MagLIF.py` to match the name of the newly created config file.
3. Run `MagLIF.py` to run the simulation.
4. The result are stored under the `results` directory. 
  - `simulation.py`: Simulation results, each row is an iteration.
  - `initial.csv`: Key-value pair of initial conditions.
  - `results.csv`: Key-value pair of simulation results.
5. Run `plot.py` to show the plots.

**Example of plot output**
![70MA90atm](https://github.com/fuse-energy/FCODE/assets/107262205/6b30df5a-979d-4008-906f-a2d9564a6969)

## Multiple Simulations: Parametric Variation
1. Create a config file in the `config_params` directory to change the initial conditions.
2. Change the import statement (line 9) of `MagLIF_param.py` to match the name of the newly created config file.
3. Run `MagLIF_param.py` to run simulations of all initial condition permutations.
4. The results are stored in `results/params.csv`.
5. Rename the results file to `params_XXMA.csv`, where `XX` is the current in `MA`.
6. In `plot_params.py`, change the `I` variable to match the `XX` from step 5.
7. Run `plot_params.py` to show the plots.

**Example of plot output**
![70MA params](https://github.com/fuse-energy/FCODE/assets/107262205/97ed3e70-9aa9-4f33-b994-bd21ce7bf252)
