import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

I = 50

matplotlib.rcParams['font.family'] = 'Lucida Sans Unicode'
matplotlib.rcParams["figure.dpi"] = 50
plt.style.use('fivethirtyeight')

path = f'results/params_{I}MA.csv'
data = pd.read_csv(path,skiprows=None)
data['Q_s'] = data['linerBU_Efusion_MJ']/data['peak_liner_KE_MJ']
atm_values = sorted(list(set(data["atm"])))





#
#
#
# MAXIMUM
for v in atm_values:
  d = data[data['atm'] == v]
  max_MJ = np.argmax(data[data['atm'] == v]['linerBU_Efusion_MJ'])

  results = [
    int(d.iloc[max_MJ]['atm']),
    round(d.iloc[max_MJ]['peak_I_MA'], 2),
    round(d.iloc[max_MJ]['Rout0']*1000, 2),
    round(d.iloc[max_MJ]['linerBU_Efusion_MJ'], 2)
  ]
  
  print("\t".join([str(r) for r in results]))




#
#
#
# PLOTTING

fig = plt.figure()
gs = fig.add_gridspec(2,3)
colors = ["C1", "C2", "C3", "C4", "C5", "C6", "b", "c", "C9",]

def plot_Rout(fig, atm, y_col):
  d = data[data['atm'] == atm]
  color = colors[atm_values.index(atm)]

  x = d['Rout0']*1000
  y = d[y_col]

  fig.plot(x, y, label=f"{atm} atm", color=color)
  
fig1 = fig.add_subplot(gs[0, 0])
fig2 = fig.add_subplot(gs[0, 1])
fig3 = fig.add_subplot(gs[0, 2])
fig4 = fig.add_subplot(gs[1, 0])
fig5 = fig.add_subplot(gs[1, 1])
fig6 = fig.add_subplot(gs[1, 2])

figs = [fig1, fig2, fig3, fig4, fig5, fig6]

for v in atm_values:
  plot_Rout(fig1, v, 'linerBU_Efusion_MJ')
  plot_Rout(fig2, v, 'peak_liner_KE_MJ')
  plot_Rout(fig3, v, 'Tstagnation_ns')
  plot_Rout(fig4, v, 'Q_s')
  plot_Rout(fig5, v, 'Tstagnation_TM')
  plot_Rout(fig6, v, 'peak_CR_TM')

for fig in figs:
  fig.legend()
  fig.set_xlabel('Liner Radius (mm)')

fig1.set_ylabel("Fusion Energy (MJ)")
fig1.set_title("Fusion Energy")

fig2.set_ylabel("Liner Kinetic Energy (MJ)")
fig2.set_title("Peak Liner Kinetic Energy")

fig3.set_ylabel("Stagnation Time (ns)")
fig3.set_title("Stagnation Time")

fig4.set_ylabel("Scientific Q")
fig4.set_title("Scientific Q")

fig5.set_ylabel("Temperature at Stagnation Time (keV)")
fig5.set_title("Temperature at Stagnation Time")

fig6.set_ylabel("Temperature at Peak CR Time (keV)")
fig6.set_title("Temperature at Peak CR Time")

plt.show()