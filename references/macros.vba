Sub MAGLIF()
'
' MAGLIF Macro
' Macro recorded 01/01/2023 by IPFS; last modified Melbourne 24/04/2023;
'MAGLIFV4  Equation of liner motion; Equation of compression power with Eabc; liner thickness computed from liner volume compression
' Keyboard Shortcut: Ctrl+a
'
    Range("A20:DA60000").Select
    Selection.ClearContents
    Range("A11:N11").Select
    Selection.ClearContents
    Range("A14:F14").Select
    Selection.ClearContents

Dim backhowmanyrows As Integer
Rem V5 includes fuel and liner BU time
Rem V4 uses Liner Equation of Motion, Fuel compression heating w Eabc, with compressed liner thickness
Rem * G = specific heat ratio
Rem for equations, all units in SI (except stated otherwise); temperature is in keV
Rem * Consider COLUMN OF UNIT LENGTH
Rem * Rout = OUTER RADIUS (in m, for calculations in real quantities)of liner
Rem * Rout0= outer radius of liner,at initial time
Rem * R= INNER RADIUS (in m,  ditto )of liner = outer boundary of fuel
Rem * R0= inner radius, at initial time
Rem * Th= thickness of liner, in m; fixed thickness Th = Th0 in this V3; try Th compressed again this V4
Rem * Th0=thickness on liner, at inital time
Rem * b= coaxial return path radius

Rem * Length=length of column in m; needed when calculating inductance
Rem * ml= mass of Be liner = constant fixed at start, in kg m-1
Rem * volliner=volume of liner per m of column
Rem * volliner0= initial volume of liner
Rem * mfuel- mass of D fuel= constant, in kg m-1
Rem * VolFuel= volume of fuel
Rem * ni= number density of fuel m-3
Rem * Ba= axial bias field, in T (elsewhere denoted as Bz)
Rem * Ba0=axial bias field, at initial time
Rem * P= pressure of fuel in Newton m-2 (which is Pa)
Rem * P0=pressure of fuel
Rem 1 bar=1.01E5 pascal, or Nm-2
Rem * TM= temperature of fuel in keV*
Rem * TM0= temperature of fuel, at initial time
Rem * I= driving current (A)flowing in Be liner, assumed rising time profile,  dynamics-interactive at small radius
Rem * rhoD= density D in kg m-3, is 0.18 kg m-3 at STP (1 bar) or 0.18 mg per cc or 0.18 x10-3 g per cc
Rem * In the code, rhoD IS the fuel density, even for DT case, rhoD has been kept as the fuel density  even for DT mixtures
Rem * rhoT= density T in kg m-3, is 0.27 kg m-3 at STP (1 bar) or 0.27 mg per cc
Rem * rhoDT= density D-T (50-50), is 0.225 kg m-3 at STP (1 bar)or 0.225 mg per cc
Rem * rhoD0= initial density of the D fuel
Rem * rhoB= density Be in kg m-3, is 1848 kg m-3
Rem * L0=external circuit (stray) inductance
Rem * L= time varying inductance of target, assuming current flows at Rout
Rem * Ip=Peak current, selected input parameter, nominally to occur at 120 ns
Rem * psSwitchFactor, selects Rout (relative to Rout0)to switch to ps resolution, saves computation time
Rem * IdotFactor, adjusts the intensity of current drop
Rem * atm is ambient pressure in number of atmosphere
Rem * bar is fuel mass density (kg m-3) at one atmospheric pressure
Rem First 80 ns (up to preheat) d=10 ps; up to Cr=10, d=2 ps, Cr=10 to stagnation d=1ps; then d=2 ps.
Pi = 3.142
mu = 4 * Pi * 0.0000001
G = 5 / 3
Rem mi is amu, D ion weights 2 amu, T weighs 3 amu, BC is Boltzmann Cont in J per K; k is boltzmann constant in J per keV
BC = 1.38E-23
k = BC * 0.000000114
mi = 1.67 * 10 ^ -27
e = 1.602E-19
masse = 9.1094E-31

Rem Parameters are input from Sheet 1 as follows
Ip = ActiveSheet.Cells(6, 1)
Ba0 = ActiveSheet.Cells(6, 2)
TMLaser = ActiveSheet.Cells(6, 3)
Rout0 = ActiveSheet.Cells(6, 4)
Th0 = ActiveSheet.Cells(6, 5)
b = ActiveSheet.Cells(6, 6)
Length = ActiveSheet.Cells(6, 7)
atm = ActiveSheet.Cells(6, 8)
L0 = ActiveSheet.Cells(6, 9)
aa = ActiveSheet.Cells(6, 10)
bb = ActiveSheet.Cells(6, 11)
cc = ActiveSheet.Cells(6, 12)
dd = ActiveSheet.Cells(6, 13)
ee = ActiveSheet.Cells(6, 14)
FF = ActiveSheet.Cells(6, 15)
FlagGas = ActiveSheet.Cells(6, 16)
Tpreheat = ActiveSheet.Cells(6, 17)
Tpeak = ActiveSheet.Cells(6, 18)


CurrentRate1 = (0.000000125 / Tpeak) * (Ip / (18 * 10 ^ 6)) * 0.4 * 100000000000000#
Idotfactor = 1
Rem Choose between D-D or D-T 50:50 mixture
1 If FlagGas = 2 Then GoTo 2
bar = 0.18
GoTo 4
2 bar = 0.225
4 barpressure = 101000
rhoD0 = atm * bar
P0 = atm * barpressure
rhoB = 1848
R0 = Rout0 - Th0
TMambient = 2.63 * 0.00001:
Rem  number of atoms per m3 of molecular gas at 'atm' atmospheric pressure

n0 = 2 * 2.69 * (10 ^ 25) * atm
Vout0 = 0:  FlagLaser = 0: FlagStagnation = 0
TotalNion = n0 * Pi * R0 * R0 * Length
totalNionpair = TotalNion / 2

Rem volliner0 = 2 * Pi * (R0 + Th0) * Th0
volliner0 = Pi * (Rout0 ^ 2 - R0 ^ 2)
Rem mliner is mass of liner in kg m-1; massliner is mass of liner in kg; mfuel is mass fuel in kg m-1, massfuel is mass of fuel in kg
mliner = volliner0 * rhoB
massliner = mliner * Length
mfuel = rhoD0 * Pi * R0 ^ 2
massfuel = mfuel * Length

Rem Set initial conditions, give I a small value to facilitate initialisation, 10ps steps

 T = 0: I = 10 ^ 4
Th = Th0:  rowj = 20: Rout = Rout0: R = R0
Ba = Ba0: TM = TMambient: volliner = volliner0: P = P0
Vout = Vout0: Cr = 1: Idrop = 0
Pcomp = 0: Palpha = 0: Pbrems = 0: Pcond = 0
Rem set time increment at 10ps
d = 0.00000000001
Tlinear = 0.00000003 * (Tpeak / 0.000000125)
ActiveSheet.Cells(11, 1) = mliner
ActiveSheet.Cells(11, 2) = mfuel
ActiveSheet.Cells(11, 3) = TotalNion
ActiveSheet.Cells(11, 4) = massliner
ActiveSheet.Cells(11, 5) = massfuel
ActiveSheet.Cells(11, 6) = totalNionpair

CurrentFactor = Ip / (18 * 10 ^ 6)
10 Rem start of main loop
ni = n0 * Cr ^ 2
20 Term1 = (mu * I * I) / (4 * Pi * Rout)
Term2 = -P * 2 * Pi * R
Term3 = -(Pi * R / mu) * (Ba) ^ 2

Aout = -(1 / mliner) * (Term1 + Term2 + Term3)
LinerKE = 0.5 * massliner * Vout * Vout
Efuel = ((BC * 2 * ni) * (3.142 * R * R * Length)) * TM * 11400000#
Efuelnoabc = Efuel - Eabc

Rem Output time in ns and dimensions in mm and speeds in cm per us, temp in keV

 ActiveSheet.Cells(rowj, 1) = T * 1000000000#
 ActiveSheet.Cells(rowj, 2) = I
ActiveSheet.Cells(rowj, 3) = Rout * 1000
ActiveSheet.Cells(rowj, 4) = R * 1000
ActiveSheet.Cells(rowj, 5) = Th * 1000
ActiveSheet.Cells(rowj, 6) = Vout / 10000
ActiveSheet.Cells(rowj, 7) = Cr
ActiveSheet.Cells(rowj, 8) = rhoD
ActiveSheet.Cells(rowj, 9) = R * rhoD
ActiveSheet.Cells(rowj, 10) = TM
ActiveSheet.Cells(rowj, 11) = P
ActiveSheet.Cells(rowj, 12) = Ba
ActiveSheet.Cells(rowj, 13) = BaP
ActiveSheet.Cells(rowj, 14) = ni
ActiveSheet.Cells(rowj, 15) = NTN
ActiveSheet.Cells(rowj, 16) = Efusion
ActiveSheet.Cells(rowj, 17) = Ealpha
ActiveSheet.Cells(rowj, 18) = -Ebrems
ActiveSheet.Cells(rowj, 19) = -Econd
ActiveSheet.Cells(rowj, 20) = Eabc
ActiveSheet.Cells(rowj, 21) = Ecomp
ActiveSheet.Cells(rowj, 22) = T * 1000000000#
ActiveSheet.Cells(rowj, 23) = LinerKE
ActiveSheet.Cells(rowj, 24) = Efuelnoabc
ActiveSheet.Cells(rowj, 25) = Efuel
ActiveSheet.Cells(rowj, 26) = Pfusion
ActiveSheet.Cells(rowj, 27) = Palpha
ActiveSheet.Cells(rowj, 28) = Pbrems
ActiveSheet.Cells(rowj, 29) = Pcond
ActiveSheet.Cells(rowj, 30) = Pcomp
ActiveSheet.Cells(rowj, 31) = Idot
ActiveSheet.Cells(rowj, 32) = Idrop
ActiveSheet.Cells(rowj, 33) = Xe
ActiveSheet.Cells(rowj, 34) = Pcond3
ActiveSheet.Cells(rowj, 35) = AB
ActiveSheet.Cells(rowj, 36) = NTNDOT
ActiveSheet.Cells(rowj, 37) = T * 1000000000#
 ActiveSheet.Cells(rowj, 38) = I / 20000000
ActiveSheet.Cells(rowj, 39) = falpha
ActiveSheet.Cells(rowj, 40) = SIGV
ActiveSheet.Cells(rowj, 41) = -VfuelR / 10000
ActiveSheet.Cells(rowj, 42) = L * 10 ^ 9
ActiveSheet.Cells(rowj, 43) = NTN / totalNionpair


45 rowj = rowj + 1
Rold = R
50 T = T + d

Vout = Vout + Aout * d
Rout = Rout + Vout * d
Rem Calculate I, linear rise for T<30ns (scaled), else template I, dynamics-interactive to give Idrop

If FlagTlinear = 1 Then GoTo 100
If T < Tlinear Then GoTo 110
FlagTlinear = 1
ActiveSheet.Cells(14, 1) = Tlinear * 1000000000#
100 L = (mu / (2 * Pi)) * Length * Log(b / Rout)
Ldot = -(mu / (2 * Pi)) * Length * Vout / Rout
Rem RdotFactor adjusts the effective Idot
Idot = -I * Ldot / (L + L0)
Idrop = Idrop + Idot * d
Rdyn = 0.5 * Ldot
Pdyn = Rdyn * I * I
Edyn = Edyn + Pdyn * d
ActiveSheet.Cells(rowj, 44) = Rdyn
ActiveSheet.Cells(rowj, 45) = Pdyn
ActiveSheet.Cells(rowj, 46) = Edyn

Rem current template y=current in MA x=time in ns with peak current 18MA(scaled) rise time 125 ns (scaled)
x = T * 1000000000#
y = aa * x ^ 5 + bb * x ^ 4 + cc * x ^ 3 + dd * x ^ 2 + ee * x + FF
I = y * 1000000#
I = I * CurrentFactor
I = I + Idrop

GoTo 150

110 I = I + CurrentRate1 * d
Rem Calculate fuel radius R from liner outer radius and liner thickness
150 R = Rout - Th
VfuelR = (Rold - R) / d

If T > Tpreheat Then GoTo 220

Cr = R0 / R
Ba = Ba0 * Cr ^ 2
rhoD = rhoD0 * Cr ^ 2
BaP = (Ba ^ 2) / (2 * mu)
Rem Calculate liner thickness from liner volume

Termvolliner1 = 2 * P0 + (Ba0 ^ 2) / mu
Termvolliner2 = 2 * P + 2 * BaP
Termvolliner = ((Termvolliner1) / (Termvolliner2))
volliner = volliner0 * (Cr ^ (1 / G)) * Termvolliner ^ (1 / G)
Th = ((R ^ 2) + (volliner / Pi)) ^ 0.5 - (R)

Rem Calculate fuel Temp and P by considering compression heating Ecomp and Eabc
Rem Energy gained by fuel through Ecomp & Eabc is shared by 2 ni particles, ni ions (half D half T)and ni electrons

P = 74900000000# * rhoD * TM
Pcomp = 471000000000# * (rhoD * R) * TM * VfuelR * Length
Ecomp = Ecomp + Pcomp * d
TMdot = (675000000000000# / (ni * R * R * Length)) * (Pcomp + Palpha - Pbrems - Pcond)
TM = TM + TMdot * d

GoTo 320

Rem set time increment to 2 ps
Rem At first instant after T=80 ns, laser preheat to TMLaser, new reference point for adiabatic compression is set
220 If FlagLaser = 1 Then GoTo 240

ActiveSheet.Cells(14, 2) = Tpreheat * 1000000000#
ThLaser = Th:   RoutLaser = Rout: RLaser = R: rhoDLaser = rhoD
BaLaser = Ba:  vollinerLaser = volliner
voutLaser = Vout: CrLaser = Cr: IdropLaser = Idrop:

Rem PLaser = 4 * P0 * (rhoDLaser / rhoD0) * (TMLaser / TMambient)
Rem TM = TMLaser

If TM > TMLaser Then GoTo 222
TM = TMLaser
GoTo 224
222 TMLaser = TM
224 PLaser = 4 * P0 * (rhoDLaser / rhoD0) * (TMLaser / TMambient)

FlagLaser = 1: d = 0.000000000002

If FlagStagnation = 1 Then GoTo 242
240 If Cr < 10 Then GoTo 244
d = 0.000000000001: GoTo 244
242 d = 0.000000000002
244 CR2 = (RLaser / R)
Cr = CR2 * CrLaser
Ba = BaLaser * CR2 ^ 2
BaP = (Ba ^ 2) / (2 * mu)
rhoD = rhoDLaser * CR2 ^ 2

Rem Calculate fuel Temp and P by considering compression heating Ecomp and Eabc
Rem Energy gained by fuel through Ecomp & Eabc is shared by 2 ni particles, ni ions (half D half T)and ni electrons

P = 74900000000# * rhoD * TM
Pcomp = 471000000000# * (rhoD * R) * TM * VfuelR * Length
Ecomp = Ecomp + Pcomp * d
TMdot = (675000000000000# / (ni * R * R * Length)) * (Pcomp + Palpha - Pbrems - Pcond)
TM = TM + TMdot * d

Rem compute volume of liner, with liner compression; then compute liner thickness
Termvolliner1 = 2 * PLaser + (BaLaser ^ 2) / mu
Termvolliner2 = 2 * P + (Ba ^ 2) / mu
Termvolliner = ((Termvolliner1) / (Termvolliner2))
volliner = vollinerLaser * (CR2 ^ (1 / G)) * Termvolliner ^ (1 / G)
Th = ((R ^ 2) + (volliner / Pi)) ^ 0.5 - (R)

Rem calculate alpha heating, Ralpha =26.5/Ba (Tesla) in cm, Rangealpha=0.015TM^1/2 in g/cm2, falpha =fraction of alpha depositing energy in plasma
Rem Palpha= power of alpha deposition of energy, Ealpha= energy deposited by alpha in plasma cumulated to point of calculation.
250 Ralpha = 0.01 * 26.5 / Ba
bee = R / Ralpha
Rangealpha = 10 * 0.015 * TM ^ (1 / 2)
Xalpha1 = (rhoD * R) / Rangealpha
Xalpha2 = bee ^ 2
Xalpha3 = (9 * (bee ^ 2) + 1000) ^ (1 / 2)
Xalpha4 = Xalpha2 / Xalpha3
Xalpha = (8 / 3) * (Xalpha1 + Xalpha4)
falpha1 = Xalpha + Xalpha ^ 2
falpha2 = 1 + (13 * Xalpha / 9) + (Xalpha ^ 2)
falpha = falpha1 / falpha2
Palpha = (Pfusion / 5) * falpha
Ealpha = Ealpha + Palpha * d

Rem Calculate conduction losses, TM in keV, Ba in T, Length and rhoD in m & kg m-3
Rem xe (Hall parameter) & Econd equs adapted from Slutz, Haiphong originally in CGS units
Xe = 0.0011 * TM ^ (3 / 2) * Ba / (0.001 * rhoD)
Pcond1 = 1 + 0.39 * Xe ^ 2
Pcond2 = 1 + 3.9 * Xe ^ 2 + 0.26 * Xe ^ 4
Pcond3 = Pcond1 / Pcond2
Pcond = 8700000000000# * TM ^ (7 / 2) * Length * 100 * Pcond3
Econd = Econd + Pcond * d

Rem Use Lee code brems calc with plasma self absorption
Pbrems1 = (2.6E-40) * ni * ni * ((TM * 11400000#) ^ 0.5) * 3.142 * (R * R) * Length
 Rem Apply Plasma Self Absorption correction to PBR PREC and PLN:
Rem PM is photonic excitation number; AB is absorption corrected factor
Rem If AB<1/2.7183, Radiation goes from volume-like PRAD to surface-like PRADS; PRADS has a limit being Blackbody Rad PBB
Rem We consider only volume (absorption corrected) radiation for PBR PREC and PLINE and PSXR; not including any contribution from surface radiation.
PM = 1.66 * (10 ^ -11) * (rp * 100) * (ni * (10 ^ -6)) / ((1000 * TM) ^ 1.5)
AB = 1 + (((10 ^ -14) * (ni * (10 ^ -6))) / ((1000 * TM) ^ 3.5))
AB = 1 / AB
AB = AB ^ (1 + PM)
Rem Calculate rate of bremsstrhlung loss, fuel plasma 'self absorption'-corrected; calculate cumulative bremsstrahlung energy loss
Pbrems = AB * Pbrems1
Ebrems = Ebrems + Pbrems * d

Rem Calc Eabc, net energy gain/loss of alpha heating, Bremsstrahlung and conduction due to electron
Eabc = Ealpha - Ebrems - Econd

Rem Calculate DD or DT (50:50) neutron yield, NOT using Sluts, Haiphong approximation which use limited temp ranges eg 7-13 keV etc
Rem Use fusion reactivity SIGV (for each temperature) from NRL formulary

If FlagGas = 2 Then GoTo 260
SIGV = 2.33 * (10 ^ -20) * (Exp(-18.76 * (TM ^ (-1 / 3)))) * (TM ^ -(2 / 3))
Rem For identical particle interaction, need factor of (1/2) in NTNDOT equation, inserted here
SIGV = 0.5 * SIGV
GoTo 270
Rem for D-T (50:50), need to half the number density of each D and T
260 SIGV = 3.68 * (10 ^ -18) * (Exp(-19.94 * (TM ^ (-1 / 3)))) * (TM ^ -(2 / 3))
nD = 0.5 * ni - RedFuelDen
nT = 0.5 * ni - RedFuelDen
Rem 270 is calculated in SI units, Ni, R, Length all in m, s SIGV in m3 per s
Rem Pfusion is calculated with (3.5+14 MeV) per fusion event
270 NTNDOT = nD * nT * Pi * (R * R) * Length * SIGV
Pfusion = NTNDOT * 0.0000000000028
NTN = NTN + NTNDOT * d
RedFuelDen = NTN / (3.142 * R * R * Length)
Efusion = Efusion + Pfusion * d

Rem set limit of computation at 1 ns after stagnation.
Rem Stagnation is the point where liner speed =0 (100 is no different from 0 in this situation where liner speed swings from -10^5 to +10^5; and is a housekeeping plus)
Rem Incorporate post stagnation breakup phase, calculate SDS then time of breakup

300 If FlagStagnation = 1 Then GoTo 310
If Vout > 100 Then Tstagnation = T: FlagStagnation = 1

SDSfuel = ((5 / 3) * P / rhoD) ^ 0.5
fuelBUinterval = R / SDSfuel
fuelBUtime = Tstagnation + fuelBUinterval

rholiner = mliner / volliner
SDSliner = ((5 / 3) * P / rholiner) ^ 0.5
linerBUinterval = Th / SDSliner
linerBUtime = Tstagnation + linerBUinterval

ActiveSheet.Cells(11, 8) = Tstagnation * 1000000000#
ActiveSheet.Cells(11, 9) = fuelBUinterval * 1000000000#
ActiveSheet.Cells(11, 10) = fuelBUtime * 1000000000

ActiveSheet.Cells(11, 12) = linerBUinterval * 1000000000#
ActiveSheet.Cells(11, 13) = linerBUtime * 1000000000



GoTo 320
310 If T > Tstagnation + 0.000000001 Then GoTo 1000
320 GoTo 10
Rem Date and Time stamp
1000 Cells(14, 5).Value = Format(Now, "dd/mm/yyyy")
Cells(14, 6).Value = Format(Now, "hh:mm ampm")
 

Stop

End Sub
















