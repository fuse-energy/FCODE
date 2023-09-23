import math
import time
import pandas as pd
import numpy as np

from itertools import product

from configs.CONFIG_files import *
from configs_params.CONFIG_50MA_params import *

start_time = time.time()
num_simul = 0









init_vars = [
  "Ip", "Ba0", "TMLaser", "Rout0", "Th0",
  "b", "Length", "atm", "L0", "aa",
  "bb", "cc", "dd", "ee", "FF",
  "FlagGas", "Tpreheat", "Tpeak"
]

res_vars = [
  "mliner", "mfuel", "TotalNion", "massliner", "massfuel",
  "totalNionpair", "Tstagnation", "fuelBUinterval", "fuelBUtime", "linerBUinterval",
  "linerBUtime"
]

simul_vars = [
  "Tstagnation_ns", "linerBUtime_ns", "peak_I_MA", "peak_CR", "peak_CR_TM", "Tstagnation_TM",
  "Tstagnation_CR", "peak_CR_P", "peak_CR_BaP", "Tstagnation_Rout",
  "linerBU_yield", "linerBU_Efusion_MJ", "linerBU_Pfusion", "peak_liner_KE_MJ"
]

out_vars = init_vars + res_vars + simul_vars

f = open(params_path, "w")
f.write(",".join([v for v in out_vars]))
f.write("\n")










# BINARY SEARCH
def binary_search(arr, x):
  return binary_search_recursive(arr, 0, len(arr)-1, x)

def binary_search_recursive(arr, low, high, x):
  if high >= low:
    mid = (high + low) // 2

    # Element found
    if arr[mid] == x: return mid

    # Recursive: Left subarray
    elif arr[mid] > x: return binary_search_recursive(arr, low, mid - 1, x)

    # Recursive: Right subarray
    else: return binary_search_recursive(arr, mid + 1, high, x)

  else:
    return (low + high) // 2


# PROGRESS BAR
def print_progress_bar(iteration, total, elapsed, length=50, fill='-'):
  percent = 100 * (iteration / float(total))
  remaining = elapsed/percent*(100-percent)
  filled_length = int(length * iteration // total)
  bar = fill * filled_length + ' ' * (length - filled_length)
  prefix = f"{iteration}/{total}"

  print(f'{prefix:<12}\t |{bar}| \t{f"{elapsed:.1f}s elapsed":<21}') # \t {f"Est. {remaining:.1f}s remaining":<28}')











# For Excel columns
HEADER = """
T 	I	Rout	R	Th	Vout	Cr	rhoD	R*rhoD	TM	P	Ba	BaP	ni	NTN	Efusion	Ealpha	Ebrems	Econd	Eabc	Ecomp	T? 	Liner KE	Efuelnoabc	Efuel	Pfusion	Palpha	Pbrems	PcondL	Pcomp	Idot	Idrop	Xe	Pcond3	AB	NTNdot	T ns	I(20MA)	falpha	SIGV	VfuelR	target L	NTN/NpairDT
"""
UNITS = """ 
ns	A	mm	mm	mm	cm/us	TBD	kgm-3	kgm-2	keV	Pa	T	Pa	m-3	number	J	J	J	J	TBD	J	ns	J	J	W	W	W	W	W	W	Hall para	cond fr	TBD	W	ns	x20MA	TBD	TBD	TBD	TBD	cm/us	nH	TBD																																																			
"""



#
###
##
###
#
###
##            OUTER LOOP
###
#
###
##
###
#




permutations = product(Ip_params, Ba0_params, TMLaser_params, Rout0_params, Th0_scale_params, atm_params)
permutations_list = list(permutations)
total_simul = len(permutations_list)
print(f"Simulating {total_simul} permutations of MagLIF:")

for perm in permutations_list:
  num_simul += 1
  start_sim = time.time()

  Ip, Ba0, TMLaser, Rout0, Th0_scale, atm = perm
  Th0 = Rout0*Th0_scale

  # Constants
  Pi = math.pi
  mu = 4 * Pi * 1e-7
  G = 5 / 3
  BC = 1.38e-23
  k = BC * 1.14e-7
  mi = 1.67 * 10 ** -27
  e = 1.602e-19
  masse = 9.1094e-31

  CurrentRate1 = (0.000000125 / Tpeak) * (Ip / (18 * 10 ** 6)) * 0.4 * 1e14  # 1e14 is used for scaling, adapt as needed
  Idotfactor = 1

  # VBA LINE LABEL 1
  bar = 0.18  # Default value
  if FlagGas == 2:
    bar = 0.225

  barpressure = 101000
  rhoD0 = atm * bar
  P0 = atm * barpressure
  rhoB = 1848
  R0 = Rout0 - Th0
  TMambient = 2.63 * 1e-5

  # Other variables and calculations (you'll need to adapt this part according to the logic)

  T = 0
  I = 1e-2  # Small initial value
  Th = Th0
  rowj = 20
  Rout = Rout0
  R = R0
  Ba = Ba0
  TM = TMambient
  volliner = Pi * (Rout0 ** 2 - R0 ** 2)  # Assuming a liner volume calculation

  n0 = 2 * 2.69 * (10 ** 25) * atm
  Vout0 = 0
  FlagLaser = 0
  FlagStagnation = 0
  TotalNion = n0 * Pi * R0 * R0 * Length
  totalNionpair = TotalNion / 2

  volliner0 = Pi * (Rout0 ** 2 - R0 ** 2)
  mliner = volliner0 * rhoB
  massliner = mliner * Length
  mfuel = rhoD0 * Pi * R0 ** 2
  massfuel = mfuel * Length

  # Initial conditions
  T = 0
  I = 10**4
  Th = Th0
  Rout = Rout0
  R = R0
  Ba = Ba0
  TM = TMambient
  volliner = volliner0
  P = P0
  Vout = Vout0
  Cr = 1
  Idrop = 0
  Pcomp = 0
  Palpha = 0
  Pbrems = 0
  Pcond = 0

  d = 0.00000000001
  Tlinear = 0.00000003 * (Tpeak / 0.000000125)
  CurrentFactor = Ip / (18 * 10 ** 6)







  #
  #
  #
  #
  #
  #
  # Saving information

  BIG_LIST = []

  def write_row(variables):
    BIG_LIST.append(variables)















  # Undefined in the VBA code
  Tstagnation = 0
  Eabc = 0
  FlagTlinear = 0
  Edyn = 0
  Pfusion = 0
  rp = 0
  Ecomp = 0
  Econd = 0
  Efusion = 0
  Ealpha = 0
  Ebrems = 0
  RedFuelDen = 0
  NTN = 0
  NTNDOT = 0
  Idot = 0
  Xe = 0 
  Pcond3 = 0
  AB = 0
  falpha = 0
  SIGV = 0
  L = 0

  iterations = 0


  # Main loop (you'll need to implement this part based on your requirements)
  while True:  # Adjust the condition as needed
    # Main calculations and assignments inside the loop
    iterations += 1

    if iterations > MAX_ITERATIONS:
      print("Max iterations reached.")
      break
    
    # VBA LINE LABEL 10
    ni = n0 * Cr ** 2
    Term1 = (mu * I * I) / (4 * Pi * Rout)
    Term2 = -P * 2 * Pi * R
    Term3 = -(Pi * R / mu) * (Ba) ** 2

    Aout = -(1 / mliner) * (Term1 + Term2 + Term3)
    LinerKE = 0.5 * massliner * Vout * Vout
    Efuel = ((BC * 2 * ni) * (Pi * R * R * Length)) * TM * 11400000#
    Efuelnoabc = Efuel - Eabc
    
    # OUTPUT
    if iterations > 1:
      variables = [
        T * 1000000000, I, Rout * 1000, R * 1000, Th * 1000,
        Vout / 10000, Cr, rhoD, R * rhoD, TM,
        P, Ba, BaP, ni, NTN, 
        Efusion, Ealpha, -Ebrems, -Econd, Eabc,
        Ecomp, T * 1000000000, LinerKE, Efuelnoabc, Efuel,
        Pfusion, Palpha, Pbrems, Pcond, Pcomp, 
        Idot, Idrop, Xe, Pcond3, AB, 
        NTNDOT, T * 1000000000, I / 20000000, falpha, SIGV, 
        -VfuelR / 10000, L * 10 ** 9, NTN / totalNionpair
      ]
      write_row(variables)


    # VBA LINE LABEL 45
    Rold = R
    T = T + d

    Vout = Vout + Aout * d
    Rout = Rout + Vout * d



    # VBA LINE LABEL 100
    if FlagTlinear == 1:
      try:
        L = (mu / (2 * Pi)) * Length * math.log(max(b / Rout, 1E-200))
      except TypeError:
        print(b, Rout)
      Ldot = -(mu / (2 * Pi)) * Length * Vout / Rout
      Idot = -I * Ldot / (L + L0)
      Idrop = Idrop + Idot * d
      Rdyn = 0.5 * Ldot
      Pdyn = Rdyn * I * I
      Edyn = Edyn + Pdyn * d

      x = T * 1000000000#
      y = aa * x ** 5 + bb * x ** 4 + cc * x ** 3 + dd * x ** 2 + ee * x + FF
      I = y * 1000000#
      I = I * CurrentFactor
      I = I + Idrop
    
    # VBA LINE LABEL 110
    elif T < Tlinear:
      I = I + CurrentRate1 * d

    else:
      FlagTlinear = 1
    
    # VBA LINE LABEL 150
    R = Rout - Th
    VfuelR = (Rold - R) / d
    
    
    
    
    if T > Tpreheat:
      pass
      
    else:
      Cr = R0 / R
      Ba = Ba0 * Cr ** 2
      rhoD = rhoD0 * Cr ** 2
      BaP = (Ba ** 2) / (2 * mu)

      Termvolliner1 = 2 * P0 + (Ba0 ** 2) / mu
      Termvolliner2 = 2 * P + 2 * BaP
      Termvolliner = ((Termvolliner1) / (Termvolliner2))
      volliner = volliner0 * (Cr ** (1 / G)) * Termvolliner ** (1 / G)
      Th = ((R ** 2) + (volliner / Pi)) ** 0.5 - (R)

      P = 74900000000 * rhoD * TM
      Pcomp = 471000000000 * (rhoD * R) * TM * VfuelR * Length
      Ecomp = Ecomp + Pcomp * d
      TMdot = (675000000000000 / (ni * R * R * Length)) * (Pcomp + Palpha - Pbrems - Pcond)
      TM = TM + TMdot * d
      
      continue
    
    # VBA LINE LABEL 220
    if not FlagLaser == 1:
      ThLaser = Th
      RoutLaser = Rout
      RLaser = R
      rhoDLaser = rhoD
      BaLaser = Ba
      vollinerLaser = volliner
      voutLaser = Vout
      CrLaser = Cr
      IdropLaser = Idrop
      
      if TM > TMLaser:
        TMLaser = TM
      else:
        TM = TMLaser
      
      PLaser = 4 * P0 * (rhoDLaser / rhoD0) * (TMLaser / TMambient)
      FlagLaser = 1
      d = 0.000000000002
      
      if FlagStagnation == 1:
        d = 0.000000000002
    
    else:
      # VBA LINE LABEL 240
      if Cr >= 10:
        d = 0.000000000001

    # VBA LINE LABEL 244
    CR2 = (RLaser / R)
    Cr = CR2 * CrLaser
    Ba = BaLaser * CR2 ** 2
    BaP = (Ba ** 2) / (2 * mu)
    rhoD = rhoDLaser * CR2 ** 2

    P = 74900000000 * rhoD * TM
    Pcomp = 471000000000 * (rhoD * R) * TM * VfuelR * Length
    Ecomp = Ecomp + Pcomp * d
    TMdot = (675000000000000 / (ni * R * R * Length)) * (Pcomp + Palpha - Pbrems - Pcond)
    TM = TM + TMdot * d

    Termvolliner1 = 2 * PLaser + (BaLaser ** 2) / mu
    Termvolliner2 = 2 * P + (Ba ** 2) / mu
    Termvolliner = ((Termvolliner1) / (Termvolliner2))
    volliner = vollinerLaser * (CR2 ** (1 / G)) * Termvolliner ** (1 / G)
    Th = ((R ** 2) + (volliner / Pi)) ** 0.5 - (R)
    
    # VBA LINE LABEL 250
    Ralpha = 0.01 * 26.5 / Ba
    bee = R / Ralpha
    Rangealpha = 10 * 0.015 * TM ** (1 / 2)
    Xalpha1 = (rhoD * R) / Rangealpha
    Xalpha2 = bee ** 2
    Xalpha3 = (9 * (bee ** 2) + 1000) ** (1 / 2)
    Xalpha4 = Xalpha2 / Xalpha3
    Xalpha = (8 / 3) * (Xalpha1 + Xalpha4)
    falpha1 = Xalpha + Xalpha ** 2
    falpha2 = 1 + (13 * Xalpha / 9) + (Xalpha ** 2)
    falpha = falpha1 / falpha2
    Palpha = (Pfusion / 5) * falpha
    Ealpha = Ealpha + Palpha * d
    
    Xe = 0.0011 * TM ** (3 / 2) * Ba / (0.001 * rhoD)
    Pcond1 = 1 + 0.39 * Xe ** 2
    Pcond2 = 1 + 3.9 * Xe ** 2 + 0.26 * Xe ** 4
    Pcond3 = Pcond1 / Pcond2
    Pcond = 8700000000000 * TM ** (7 / 2) * Length * 100 * Pcond3
    Econd = Econd + Pcond * d
    
    Pbrems1 = (2.6E-40) * ni * ni * ((TM * 11400000) ** 0.5) * Pi * (R * R) * Length
    PM = 1.66 * (10 ** -11) * (rp * 100) * (ni * (10 ** -6)) / ((1000 * TM) ** 1.5)
    AB = 1 + (((10 ** -14) * (ni * (10 ** -6))) / ((1000 * TM) ** 3.5))
    AB = 1 / AB
    AB = AB ** (1 + PM)
    Pbrems = AB * Pbrems1
    Ebrems = Ebrems + Pbrems * d
    Eabc = Ealpha - Ebrems - Econd
    
    
    # VBA LINE LABEL 260
    if FlagGas == 2:
      SIGV = 3.68 * (10 ** -18) * (math.e ** (-19.94 * (TM ** (-1 / 3)))) * (TM ** -(2 / 3))
      nD = 0.5 * ni - RedFuelDen
      nT = 0.5 * ni - RedFuelDen
      
    else:
      SIGV = 2.33 * (10 ** -20) * (math.e ** (-18.76 * (TM ** (-1 / 3)))) * (TM ** -(2 / 3))
      SIGV = 0.5 * SIGV

    # VBA LINE LABEL 270
    NTNDOT = nD * nT * Pi * (R * R) * Length * SIGV
    Pfusion = NTNDOT * 0.0000000000028
    NTN = NTN + NTNDOT * d
    RedFuelDen = NTN / (Pi * R * R * Length)
    Efusion = Efusion + Pfusion * d
      
    # VBA LINE LABEL 300-310
    if FlagStagnation == 1:
      if T > Tstagnation + 1e-9:
        break
    
    else:
      if Vout > 100: 
        Tstagnation = T
        FlagStagnation = 1

      SDSfuel = ((5 / 3) * P / rhoD) ** 0.5
      fuelBUinterval = R / SDSfuel
      fuelBUtime = Tstagnation + fuelBUinterval

      rholiner = mliner / volliner
      SDSliner = ((5 / 3) * P / rholiner) ** 0.5
      linerBUinterval = Th / SDSliner
      linerBUtime = Tstagnation + linerBUinterval




  # End of main loop
  end_time = round(time.time() - start_sim, 3)
  total_time = round(time.time() - start_time, 3)
  if num_simul % 10 == 0 or num_simul in [1, total_simul]:
    print_progress_bar(num_simul, total_simul, total_time)
  #print(f"{num_simul} \t Simulated {iterations} iterations in {end_time}s ({total_time}s).")








  #
  #
  #
  #
  #
  #
  # INITIATE DATA FRAME
  df_header = [e.strip() for e in HEADER.split("\t") if e.strip()]
  d = df = pd.DataFrame(BIG_LIST, columns=df_header)


  #
  #
  #
  #
  # 
  #
  # RESULTS

  data_t = d["T"]
  Tstagnation_ns = Tstagnation*1e9
  linerBUtime_ns = linerBUtime*1e9


  it = {
    "Tstagnation": binary_search(data_t, Tstagnation_ns),
    "linerBUtime": binary_search(data_t, linerBUtime_ns),
    "peak_CR": np.argmax(d["Cr"])
  }

  it["peak_I"] = np.argmax(d[d["T"] < Tstagnation_ns]["I"])
  it["peak_liner_KE"] = np.argmax(d[d["T"] < Tstagnation_ns]["Liner KE"])


  peak_I = d["I"][it["peak_I"]]
  peak_CR = d["Cr"][it["peak_CR"]]
  Tstagnation_CR = d["Cr"][it["Tstagnation"]]
  peak_CR_TM = d["TM"][it["peak_CR"]]
  Tstagnation_TM = d["TM"][it["Tstagnation"]]
  peak_CR_P = d["P"][it["peak_CR"]]
  peak_CR_BaP = d["BaP"][it["peak_CR"]]
  Tstagnation_Rout = d["Rout"][it["Tstagnation"]]
  linerBU_yield = d["NTN"][it["linerBUtime"]]
  linerBU_Efusion = d["Efusion"][it["linerBUtime"]]
  linerBU_Pfusion = d["Pfusion"][it["linerBUtime"]]
  peak_liner_KE = d["Liner KE"][it["peak_liner_KE"]]

  # RESULTS (EASIER-TO-UNDERSTAND UNITS)
  peak_I_MA = peak_I/1e6
  linerBU_Efusion_MJ = linerBU_Efusion/1e6
  peak_liner_KE_MJ = peak_liner_KE/1e6


  # OUTPUT
  gvar = globals()

  f.write(",".join([str(gvar[v]) for v in out_vars]))
  f.write("\n")











f.close()