from configs.CONFIG_files import *

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import matplotlib

matplotlib.rcParams['font.family'] = 'Lucida Sans Unicode'
matplotlib.rcParams["figure.dpi"] = 50
plt.style.use('fivethirtyeight')







##################################
#                                #
#   GENERAL FUNCTIONS             
#                                #
##################################

# Sets x-axis title to be time in nanoseconds
set_xlabel_time = lambda x: x.set_xlabel("time (ns)")

def label_point(ax, x, y, label, y_offset=0.02):
  # Insert a point-label combination on a graph.
  y_offset = (ax.get_ylim()[1] - ax.get_ylim()[0])*y_offset
  scatter = ax.scatter(x, y, color='white', edgecolors='black', linewidth=2, s=75)
  scatter.set_zorder(10)

  ax.text(x, y+y_offset, label, fontsize=16, ha='center', va='bottom')


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







def maglif_plot():



  ##################################
  #                                #
  #   READ FROM CSV FILES             
  #                                #
  ##################################
  data = pd.read_csv(simulation_path, sep=',', header=1, skiprows=[2])
  time = data['T']


  results = pd.read_csv(results_path).to_dict(orient='records')[0]
  Tstagnation = results["Tstagnation"]*1e9
  linerBUtime = results["linerBUtime"]*1e9




  ##################################
  #                                #
  #   PEAKS DETECTION              
  #                                #
  ##################################

  # Iteration count for easy access
  it = {
    "Tstagnation": binary_search(time, Tstagnation),
    "linerBUtime": binary_search(time, linerBUtime),
    "zoom_time": binary_search(time, Tstagnation - 3.2),
    "peak_cr": np.argmax(data["Cr"])
  }

  it['peak_I'] = np.argmax(data["I"][:it["Tstagnation"]])
  it["peak_liner_KE"] = np.argmax(data["Liner KE"][:it["Tstagnation"]])

  



  ##################################
  #                                #
  #   PLOTS              
  #                                #
  ##################################

  d = data
  dz = data_zoom = data.truncate(before=it["zoom_time"])

  fig = plt.figure()
  gs = fig.add_gridspec(3,3)






  fig3_upper_ylim = int(np.max(d['Rout'])*1.33)
  fig3_lower_ylim = -fig3_upper_ylim/20

  fig3 = fig.add_subplot(gs[0:2, 1:3])
  fig3.set_ylim(fig3_lower_ylim, fig3_upper_ylim)
  fig3.set_ylabel("T (keV), Radius (mm)")
  fig3.set_title("Fig. 3: Current, linear radius, fuel temperature over time")


  fig3.plot(d['T'], d['Rout'], label='Rout')
  fig3.plot(d['T'], d['TM'], label='T')



  fig3_I = fig3.twinx()
  fig3_I.set_ylabel("Current (MA)")
  fig3_I.plot(d['T'], d['I']/1e6, label='I', color="g")

  try:
    fig3_I.plot(d['T'], d['screamer_I']/1e6, label='I_drop', color="black", linestyle='dashed', linewidth=1.25)
    fig3_I.plot(d['T'], -d['Idrop']/1e6, label='I_screamer', color="grey")
  except:
    pass
  

  for peak in [it['peak_I']]:
    label_point(fig3_I, x=d['T'][peak], y=d['I'][peak]/1e6,label=f"{str(round(d['I'][peak]/1e6, 1))} MA", y_offset=0.01)

  fig3.text(Tstagnation-0.65, fig3.get_ylim()[0]*1.5, f"t={round(Tstagnation, 3)}ns", rotation='vertical', va='bottom', ha='center', color='black', alpha=0.8)
  fig3.text(linerBUtime+0.7, fig3.get_ylim()[0]*1.5, f"t={round(linerBUtime, 3)}ns", rotation='vertical', va='bottom', ha='center', color='red', alpha=0.6)






  fig4_upper_ylim = np.max(dz['Cr'])*1.2
  fig4_lower_ylim = -fig4_upper_ylim/20

  fig4 = fig.add_subplot(gs[0, 0])
  fig4.set_ylim(fig4_lower_ylim, fig4_upper_ylim)
  fig4.set_ylabel("Temperature (keV), CR (1)")
  fig4.set_title("Fig. 4: Compression ratio and fuel temperature over time")

  fig4.plot(dz['T'], dz['TM'], label='T')
  fig4.plot(dz['T'], dz['Cr'], label='CR')

  for peak in [it["peak_cr"], it["Tstagnation"]]:
    label_point(fig4, x=d['T'][peak], y=d['Cr'][peak],label=str(round(d['Cr'][peak], 2)))
    label_point(fig4, x=d['T'][peak], y=d['TM'][peak],label=str(round(d['TM'][peak], 2)))






  fig5 = fig.add_subplot(gs[1, 0])
  fig5.set_yscale("log")
  fig5.set_ylabel("Pressure (Pa)")
  fig5.set_title("Fig. 5: Fuel pressure and bias magnetic pressure over time")

  fig5.plot(dz['T'], dz['P'], label='P')
  fig5.plot(dz['T'], dz['BaP'], label='BaP')

  for peak in [it["peak_cr"]]:
    label_point(fig5, x=d['T'][peak], y=d['P'][peak],label=f"{d['P'][peak]:.2e} Pa", y_offset=0)
    label_point(fig5, x=d['T'][peak], y=d['BaP'][peak],label=f"{d['BaP'][peak]:.2e} Pa", y_offset=0)






  fig6 = fig.add_subplot(gs[2, 0])
  fig6.set_ylabel("Thickness, Radius (mm)")
  fig6.set_title("Fig. 6: Liner radius, fuel radius, liner thickness over time")

  fig6.plot(dz['T'], dz['Th'], label='Th')
  fig6.plot(dz['T'], dz['Rout'], label='Rout')
  fig6.plot(dz['T'], dz['R'], label='R')

  for peak in [it["Tstagnation"]]:
    label_point(fig6, x=d['T'][peak], y=d['Rout'][peak],label=f"{d['Rout'][peak]:.3f} mm")






  fig7 = fig.add_subplot(gs[2, 1])
  fig7.set_title("Fig. 7: D-T neutron yield over time")

  fig7.plot(dz['T'], dz['NTN'], label='NTN')

  for peak in [it["linerBUtime"]]:
    label_point(fig7, x=d['T'][peak], y=d['NTN'][peak],label=f"{d['NTN'][peak]:.3e} ({round(d['Efusion'][peak]/1e6, 1)} MJ)")




  fig8_upper_ylim = np.max(d['Liner KE'][:it["Tstagnation"]])*1.3
  fig8_lower_ylim = -fig8_upper_ylim

  fig8 = fig.add_subplot(gs[2, 2])
  fig8.set_ylim(fig8_lower_ylim, fig8_upper_ylim)
  fig8.set_ylabel("Energy (J)")
  fig8.set_title("Fig. 8: Fusion energy, liner KE, fuel energy, Eabc over time")

  fig8.plot(dz['T'], dz['Efusion'], label='Efusion')
  fig8.plot(dz['T'], dz['Liner KE'], label='Liner KE')
  fig8.plot(dz['T'], dz['Efuel'], label='Efuel')
  fig8.plot(dz['T'], dz['Eabc'], label='Eabc')
  fig8.plot(dz['T'], dz['Ecomp'], label='Ecomp')

  for peak in [it['peak_liner_KE']]:
    label_point(fig8, x=d['T'][peak], y=d['Liner KE'][peak],label=f"{str(round(d['Liner KE'][peak]/1e6, 2))} MJ")





  # Properties for all figures: Legend, x-axis label, vertical line
  axes = [fig3, fig3_I, fig4, fig5, fig6, fig7, fig8]

  for ax in axes:
    set_xlabel_time(ax)

    # Add stagnation time and liner breakup time 
    rect = patches.Rectangle(
      xy=(Tstagnation, ax.get_ylim()[0]), 
      width=linerBUtime-Tstagnation, 
      height=ax.get_ylim()[1] - ax.get_ylim()[0], 
      facecolor='red', 
      alpha=0.2
    )

    ax.axvline(x=Tstagnation, color='black', linestyle='dotted', alpha=0.6, linewidth=2)

    # Add black contour rectangle
    ax.add_patch(rect)
    for spine in ax.spines.values():
      spine.set_visible(False) 

    rect = plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, color='black', linewidth=5, fill=False)
    ax.add_patch(rect)

    # Remove gridlines and add ticks
    ax.tick_params(direction='in', length=10, width=3, grid_alpha=0.0)
    
    ax.legend()

  # Display the plot
  plt.show()

if __name__ == "__main__":
  maglif_plot()