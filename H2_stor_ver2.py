import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
plt.tight_layout()
trans = 0.9 # transformer efficiency
comp = 0.85 # compressor efficiency
pow_elec = 0.9 # power controller electronics efficiency
tot_veh_E = 26.5732# (* 0.5) total vehicle energy demand

stor_night_charge_time = 12 #hr
colors = ('red','blue','green','darkorange')
ec = 0.8 # electrolyzer efficiency
fc = 0.6 # fuel cell efficiency

grid2h = trans * pow_elec * ec * comp # grid to hydrogen efficiency
h2elec = fc * pow_elec # hydrogen to vehicle efficiency


linewidth=2
plt.figure(figsize=(12,12))
plt.rc('font', size=15)


charge_time = 0.5 #hr
storage_charge_time = 3 #hr

mw_lst = np.array([1,2,3])
# mw_lst = mw_lst + 0.558 # from solar month 18
runtime = np.arange(0,1,0.001)

for i in list(mw_lst):
    ###########
    grid = i
    act_veh_usage_1c = runtime*tot_veh_E/3
    grid_charge_pow = grid * trans * pow_elec
    grid_charge_energy = charge_time * grid_charge_pow
    elec_from_storage = np.where(act_veh_usage_1c - grid_charge_energy > 0, act_veh_usage_1c - grid_charge_energy,0)
    
    # H2
    need_h2_1c = elec_from_storage/h2elec
    max_h2_stor = grid * storage_charge_time * grid2h
    extra_h2_night = np.where(need_h2_1c-max_h2_stor > 0,need_h2_1c-max_h2_stor,0)
    extra_h2_need_3c = extra_h2_night*3
    h2_prod_night = stor_night_charge_time * grid * grid2h
    import_h2 = need_h2_1c*3-(h2_prod_night+max_h2_stor)
    tot_h2_stor_size = np.where(h2_prod_night+max_h2_stor<need_h2_1c*3,h2_prod_night+max_h2_stor,need_h2_1c*3)
    plt.plot(runtime,import_h2,":",color=colors[np.argmin(np.abs((mw_lst)-i))],linewidth=linewidth)
    plt.plot(runtime,tot_h2_stor_size,"-.",color=colors[np.argmin(np.abs((mw_lst)-i))],linewidth=linewidth)

tot_veh_E = 25.2# (* 0.5) total vehicle energy demand
mw_lst = np.array([1,2,3])
mw_lst = mw_lst + 0.558 # from solar month 18
# runtime = np.arange(0,1,0.001)

for i in list(mw_lst):
    ###########
    grid = i
    act_veh_usage_1c = runtime*tot_veh_E/3
    grid_charge_pow = grid * trans * pow_elec
    grid_charge_energy = charge_time * grid_charge_pow
    elec_from_storage = np.where(act_veh_usage_1c - grid_charge_energy > 0, act_veh_usage_1c - grid_charge_energy,0)
    
    # H2
    need_h2_1c = elec_from_storage/h2elec
    max_h2_stor = grid * storage_charge_time * grid2h
    extra_h2_night = np.where(need_h2_1c-max_h2_stor > 0,need_h2_1c-max_h2_stor,0)
    extra_h2_need_3c = extra_h2_night*3
    h2_prod_night = stor_night_charge_time * grid * grid2h
    import_h2 = need_h2_1c*3-(h2_prod_night+max_h2_stor)
    tot_h2_stor_size = np.where(h2_prod_night+max_h2_stor<need_h2_1c*3,h2_prod_night+max_h2_stor,need_h2_1c*3)
    plt.plot(runtime,import_h2,"--",color=colors[np.argmin(np.abs(np.array(mw_lst)-i))],linewidth=linewidth)
    plt.plot(runtime,tot_h2_stor_size,"-",color=colors[np.argmin(np.abs(np.array(mw_lst)-i))],linewidth=linewidth)
    
plt.xticks(np.arange(0, 1+0.1, step=0.1))
plt.yticks(np.arange(0, 50+5, step=1))
plt.grid()
plt.ylim(0,45)
plt.xlim(0,1)
storage_cap_sol = Line2D([0], [0], label='Storage Capacities with solar power', color='black', linestyle='-',linewidth=linewidth)
storage_cap_nosol = Line2D([0], [0], label='Storage Capacities without solar power', color='black', linestyle='-.',linewidth=linewidth)
import_h2_sol = Line2D([0], [0], label='Imported Hydrogen with solar power', color='black', linestyle='--',linewidth=linewidth)
import_h2_nosol = Line2D([0], [0], label='Imported Hydrogen without solar power', color='black', linestyle=':',linewidth=linewidth)
grid1 = mpatches.Patch(label='1 MW Grid', color='red')
grid2 = mpatches.Patch(label='2 MW Grid', color='blue')
grid3 = mpatches.Patch(label='3 MW Grid', color='green')
plt.legend(handles=[storage_cap_sol,storage_cap_nosol,import_h2_sol,import_h2_nosol,grid1,grid2,grid3],ncol=2,loc='upper left')
plt.xlabel('Runtime fraction')
plt.ylabel('Energy storage capacity/Imported Hydrogen (MWh)')
plt.title('Hydrogen energy storage capacity vs. runtime fraction ($η_{EC}/η_{FC} = 0.8/0.6$)')

plt.show()