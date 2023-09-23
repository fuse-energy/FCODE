from configs_params.CONFIG_utils import *

# Initial conditions
Ip_params = [35E+06]
Ba0_params =  [8.00]
TMLaser_params = [0.3]
Rout0_params = steps(20/1e4, 46/1e4, 0.4/1e4)
Th0_scale_params = [1/6]
b = 0.010
Length = 0.010
atm_params = steps(15, 40, 5)
L0 = 1.80E-08
aa = 1.9363E-10
bb = 2.9853E-08
cc = -0.000046079
dd = 0.0074388
ee = -0.17692
FF = 1.01E+00
FlagGas = 2
Tpreheat = 8.00E-08
Tpeak = 1.25E-07