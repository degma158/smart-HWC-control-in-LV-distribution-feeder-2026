import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy.stats import gaussian_kde
from scipy.stats import rankdata

import sys
import os

sys.path.append(r"C:\Users\Max de Groot\Git\Honours-Project-2026\Results")
os.chdir(r"C:\Users\Max de Groot\Git\Honours-Project-2026\Results")

import load_results

from plotting_customisation import colours, control_label, marker_styles, line_styles

# out_pth = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\methodology"

data_pth =  rf"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Individual results"


plt.rcParams['font.family'] = 'Times New Roman'

# -----------------------------
# Load results
# -----------------------------

controls = ['thermo', 'price', 'price_rand', 'current','voltage', 'voltage_prob']
penetrations = [0,50,60,80,100]

results, trial = load_results.load_results(controls, penetrations)

time_vector = np.arange(0,1440,1)
time_hours = time_vector/60
time_of_day = np.array([
    f"{m//60:02d}:{m%60:02d}"
    for m in time_vector
])

with open(r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Initial\control_signals.dat', 'rb') as f:
    Ctrl_sigs = pickle.load(f)
Ctrl_sigs.keys()







#---------------------------------------
# Single thermo ctrl house
#---------------------------------------

trial['thermo'][0].keys()

temp = trial['thermo'][0]['temp_vector']
flow = trial['thermo'][0]['flow_matrix']*1000 # L/s
state = trial['thermo'][0]['element_state_log']
enrg_in = trial['thermo'][0]['cummulative_energy_in']/1000 # MJ
enrg_out = trial['thermo'][0]['cummulative_energy_out']/1000 # MJ

h = 2

fig, axs = plt.subplots(4, 1, figsize=(6, 9), sharex=True, constrained_layout=True)

# Temperature
axs[0].plot(time_hours, temp[:, h], color=colours['thermo'])
axs[0].axhline(63, color=colours['threshold'], lw=2, linestyle=':', label='Temperature Limits')
axs[0].axhline(60, color=colours['threshold'], lw=2, linestyle=':')
axs[0].set_ylabel('Temperature (°C)', fontsize=19)
axs[0].legend(fontsize=16)
axs[0].tick_params(axis='both', labelsize=16)
axs[0].minorticks_on()
axs[0].grid(axis='x', which='major', alpha=0.5)
axs[0].grid(axis='x', which='minor', alpha=0.25)
# Flow
axs[1].plot(time_hours, flow[:, h], color=colours['thermo'])
axs[1].set_ylabel('Flow (L/s)', fontsize=19)
axs[1].tick_params(axis='both', labelsize=16)
axs[1].minorticks_on()
axs[1].grid(axis='x', which='major', alpha=0.5)
axs[1].grid(axis='x', which='minor', alpha=0.25)
# Element state
axs[2].plot(time_hours, state[:, h], color=colours['thermo'])
axs[2].set_ylabel('Element State', fontsize=19)
axs[2].set_yticks([0, 1])
axs[2].set_yticklabels(['Off', 'On'])
axs[2].set_ylim(-0.1, 1.1)
axs[2].tick_params(axis='both', labelsize=16)
axs[2].minorticks_on()
axs[2].grid(axis='x', which='major', alpha=0.5)
axs[2].grid(axis='x', which='minor', alpha=0.25)
# Cummulative energy
axs[3].plot(time_hours, enrg_in[:, h], color=colours['thermo'], label='Energy In')
axs[3].plot(time_hours, enrg_out[:, h], color=colours['thermo'], label='Energy Out', linestyle='--')
axs[3].set_ylabel('Cumulative\nEnergy (MJ)', fontsize=19)
axs[3].tick_params(axis='both', labelsize=16)
axs[3].legend(fontsize=16)
axs[3].minorticks_on()
axs[3].grid(axis='x', which='major', alpha=0.5)
axs[3].grid(axis='x', which='minor', alpha=0.25)
axs[3].set_xlabel('Hour of Day', fontsize=19)


plt.tight_layout()
plt.savefig(
    r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\methodology' + '/single_thermo_ctrl_house.pdf'
    )

plt.show()




































#---------------------------------------
# Single price ctrl house
#---------------------------------------

trial['price'][100].keys()

temp = trial['price'][50]['temp_vector']
state = trial['price'][50]['element_state_log']
category = trial['price'][50]['category']
price = Ctrl_sigs['price_signal']

h = 6

fig, axs = plt.subplots(4, 1, figsize=(9, 9), sharex=True, constrained_layout=True)

# Temperature
axs[0].plot(time_hours, temp[:, h], color=colours['price'])
axs[0].axhline(63, color=colours['threshold'], lw=2, linestyle=':', label='Temperature Limits')
axs[0].axhline(60, color=colours['threshold'], lw=2, linestyle=':')
axs[0].axhline(70, color=colours['threshold'], lw=2, linestyle=':')
axs[0].axhline(73, color=colours['threshold'], lw=2, linestyle=':')
axs[0].set_ylabel('Temperature (°C)', fontsize=19)
axs[0].legend(fontsize=16)
axs[0].tick_params(axis='both', labelsize=16)
axs[0].minorticks_on()
axs[0].grid(axis='x', which='major', alpha=0.5)
axs[0].grid(axis='x', which='minor', alpha=0.25)
# Element state
axs[1].plot(time_hours, state[:, h], color=colours['price'])
axs[1].set_ylabel('Element State', fontsize=19)
axs[1].set_yticks([0, 1])
axs[1].set_yticklabels(['Off', 'On'])
axs[1].set_ylim(-0.1, 1.1)
axs[1].tick_params(axis='both', labelsize=16)
axs[1].minorticks_on()
axs[1].grid(axis='x', which='major', alpha=0.5)
axs[1].grid(axis='x', which='minor', alpha=0.25)
# Category
axs[2].plot(time_hours, category, color=colours['price'])
axs[2].set_ylabel('Category', fontsize=19)
axs[2].tick_params(axis='both', labelsize=16)
axs[2].set_yticks([0, 1])
axs[2].set_yticklabels(['Conservative', 'Aggressive'])
axs[2].set_ylim(-0.1, 1.1)
axs[2].minorticks_on()
axs[2].grid(axis='x', which='major', alpha=0.5)
axs[2].grid(axis='x', which='minor', alpha=0.25)
# Price signal
axs[3].plot(time_hours, price, color=colours['price'])
axs[3].set_ylabel('Price Signal', fontsize=19)
axs[3].tick_params(axis='both', labelsize=16)
axs[3].set_yticks([0, 1])
axs[3].set_yticklabels(['Low', 'High'])
axs[3].set_ylim(-0.1, 1.1)
axs[3].minorticks_on()
axs[3].grid(axis='x', which='major', alpha=0.5)
axs[3].grid(axis='x', which='minor', alpha=0.25)
axs[3].set_xlabel('Hour of Day', fontsize=19)

plt.tight_layout()
plt.savefig(
    r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\methodology' + '/single_price_ctrl_house.png',
        dpi=600
    )

plt.show()





#---------------------------------------
# Single current ctrl house
#---------------------------------------

trial['current'][100].keys()

temp = trial['current'][100]['temp_vector']
state = trial['current'][100]['element_state_log']
category = trial['current'][100]['category']
current = trial['current'][100]['Current']

low_thresh = Ctrl_sigs['current_thresh_low']
high_thresh = Ctrl_sigs['current_thresh_high']

h = 1

start = 0
end = 1440

fig, axs = plt.subplots(4, 1, figsize=(9, 9), sharex=True, constrained_layout=True)

# Temperature
axs[0].plot(time_hours[start:end], temp[:, h][start:end], color=colours['current'])
axs[0].axhline(63, color=colours['threshold'], lw=2, linestyle=':', label='Temperature Limits')
axs[0].axhline(60, color=colours['threshold'], lw=2, linestyle=':')
axs[0].axhline(70, color=colours['threshold'], lw=2, linestyle=':')
axs[0].axhline(73, color=colours['threshold'], lw=2, linestyle=':')
axs[0].set_ylabel('Temperature (°C)', fontsize=19)
axs[0].legend(fontsize=16)
axs[0].tick_params(axis='both', labelsize=16)
axs[0].minorticks_on()
axs[0].grid(axis='x', which='major', alpha=0.5)
axs[0].grid(axis='x', which='minor', alpha=0.25)
# Element state
axs[1].plot(time_hours[start:end], state[:, h][start:end], color=colours['current'])
axs[1].set_ylabel('Element State', fontsize=19)
axs[1].set_yticks([0, 1])
axs[1].set_yticklabels(['Off', 'On'])
axs[1].set_ylim(-0.1, 1.1)
axs[1].tick_params(axis='both', labelsize=16)
axs[1].minorticks_on()
axs[1].grid(axis='x', which='major', alpha=0.5)
axs[1].grid(axis='x', which='minor', alpha=0.25)
# Category
axs[2].plot(time_hours[start:end], category[:,h][start:end], color=colours['current'])
axs[2].set_ylabel('Category', fontsize=19)
axs[2].tick_params(axis='both', labelsize=16)
axs[2].legend(fontsize=16)
axs[2].set_yticks([0, 1])
axs[2].set_yticklabels(['Conservative', 'Aggressive'])
axs[2].set_ylim(-0.1, 1.1)
axs[2].minorticks_on()
axs[2].grid(axis='x', which='major', alpha=0.5)
axs[2].grid(axis='x', which='minor', alpha=0.25)
# Current
axs[3].plot(time_hours[start:end], current[:,h][start:end], color=colours['current'])
axs[3].axhline(low_thresh, color=colours['threshold'], linestyle=':', label='Thresholds', lw=2)
axs[3].axhline(high_thresh, color=colours['threshold'], linestyle=':', lw=2)
axs[3].set_ylabel('Household\nCurrent (A)', fontsize=19)
axs[3].tick_params(axis='both', labelsize=16)
axs[3].legend(fontsize=16)
axs[3].minorticks_on()
axs[3].grid(axis='x', which='major', alpha=0.5)
axs[3].grid(axis='x', which='minor', alpha=0.25)
axs[3].set_xlabel('Hour of Day', fontsize=19)

plt.tight_layout()
plt.savefig(
    r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\methodology' + '/single_current_ctrl_house.png',
        dpi=600
    )

plt.show()



#---------------------------------------
# Single voltage ctrl house
#---------------------------------------

trial['voltage'][100].keys()

temp = trial['voltage'][100]['temp_vector']
state = trial['voltage'][100]['element_state_log']
category = trial['voltage'][100]['category']
voltage = trial['voltage'][100]['Voltage']

Ctrl_sigs.keys()

low_thresh = Ctrl_sigs['voltage_thresh_low']
high_thresh = Ctrl_sigs['voltage_thresh_high']

h = 1

start = 0
end = 1440

fig, axs = plt.subplots(4, 1, figsize=(9, 9), sharex=True, constrained_layout=True)

# Temperature
axs[0].plot(time_hours[start:end], temp[:, h][start:end], color=colours['voltage'])
axs[0].axhline(63, color=colours['threshold'], lw=2, linestyle=':', label='Temperature Limits')
axs[0].axhline(60, color=colours['threshold'], lw=2, linestyle=':')
axs[0].axhline(70, color=colours['threshold'], lw=2, linestyle=':')
axs[0].axhline(73, color=colours['threshold'], lw=2, linestyle=':')
axs[0].set_ylabel('Temperature (°C)', fontsize=19)
axs[0].legend(fontsize=16)
axs[0].tick_params(axis='both', labelsize=16)
axs[0].minorticks_on()
axs[0].grid(axis='x', which='major', alpha=0.5)
axs[0].grid(axis='x', which='minor', alpha=0.25)
# Element state
axs[1].plot(time_hours[start:end], state[:, h][start:end], color=colours['voltage'])
axs[1].set_ylabel('Element State', fontsize=19)
axs[1].set_yticks([0, 1])
axs[1].set_yticklabels(['Off', 'On'])
axs[1].set_ylim(-0.1, 1.1)
axs[1].tick_params(axis='both', labelsize=16)
axs[1].minorticks_on()
axs[1].grid(axis='x', which='major', alpha=0.5)
axs[1].grid(axis='x', which='minor', alpha=0.25)
# Category
axs[2].plot(time_hours[start:end], category[:,h][start:end], color=colours['voltage'])
axs[2].set_ylabel('Category', fontsize=19)
axs[2].tick_params(axis='both', labelsize=16)
axs[2].legend(fontsize=16)
axs[2].set_yticks([0, 1])
axs[2].set_yticklabels(['Conservative', 'Aggressive'])
axs[2].set_ylim(-0.1, 1.1)
axs[2].minorticks_on()
axs[2].grid(axis='x', which='major', alpha=0.5)
axs[2].grid(axis='x', which='minor', alpha=0.25)
# Current
axs[3].plot(time_hours[start:end], voltage[:,h][start:end], color=colours['voltage'])
axs[3].axhline(low_thresh[h], color=colours['threshold'], linestyle=':', label='Thresholds', lw=2)
axs[3].axhline(high_thresh[h], color=colours['threshold'], linestyle=':', lw=2)
axs[3].set_ylabel('Household\nVoltage (V)', fontsize=19)
axs[3].tick_params(axis='both', labelsize=16)
axs[3].legend(fontsize=16)
axs[3].minorticks_on()
axs[3].grid(axis='x', which='major', alpha=0.5)
axs[3].grid(axis='x', which='minor', alpha=0.25)
axs[3].set_xlabel('Hour of Day', fontsize=19)


plt.tight_layout()
plt.savefig(
    r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\methodology' + '/single_voltage_ctrl_house.png',
        dpi=600
    )

plt.show()


#---------------------------------------
# Single voltage_prob ctrl house
#---------------------------------------

temp = trial['voltage_prob'][100]['temp_vector']
state = trial['voltage_prob'][100]['element_state_log']
category = trial['voltage_prob'][100]['category']
voltage = trial['voltage_prob'][100]['Voltage']

low_thresh = Ctrl_sigs['voltage_thresh_low']
high_thresh = Ctrl_sigs['voltage_thresh_high']

h = 1
start = 0
end = 1440

fig, axs = plt.subplots(4, 1, figsize=(9, 9), sharex=True, constrained_layout=True)

# Temperature
axs[0].plot(time_hours[start:end], temp[:, h][start:end], color=colours['voltage_prob'])
axs[0].axhline(63, color=colours['threshold'], lw=2, linestyle=':', label='Temperature Limits')
axs[0].axhline(60, color=colours['threshold'], lw=2, linestyle=':')
axs[0].axhline(70, color=colours['threshold'], lw=2, linestyle=':')
axs[0].axhline(73, color=colours['threshold'], lw=2, linestyle=':')
axs[0].set_ylabel('Temperature (°C)', fontsize=19)
axs[0].legend(fontsize=16)
axs[0].tick_params(axis='both', labelsize=16)
axs[0].minorticks_on()
axs[0].grid(axis='x', which='major', alpha=0.5)
axs[0].grid(axis='x', which='minor', alpha=0.25)

# Element state
axs[1].plot(time_hours[start:end], state[:, h][start:end], color=colours['voltage_prob'])
axs[1].set_ylabel('Element State', fontsize=19)
axs[1].set_yticks([0, 1])
axs[1].set_yticklabels(['Off', 'On'])
axs[1].set_ylim(-0.1, 1.1)
axs[1].tick_params(axis='both', labelsize=16)
axs[1].minorticks_on()
axs[1].grid(axis='x', which='major', alpha=0.5)
axs[1].grid(axis='x', which='minor', alpha=0.25)

# Category
axs[2].plot(time_hours[start:end], category[:, h][start:end], color=colours['voltage_prob'])
axs[2].set_ylabel('Category', fontsize=19)
axs[2].set_yticks([0, 1])
axs[2].set_yticklabels(['Conservative', 'Aggressive'])
axs[2].set_ylim(-0.1, 1.1)
axs[2].tick_params(axis='both', labelsize=16)
axs[2].minorticks_on()
axs[2].grid(axis='x', which='major', alpha=0.5)
axs[2].grid(axis='x', which='minor', alpha=0.25)

# Voltage
axs[3].plot(time_hours[start:end], voltage[:, h][start:end], color=colours['voltage_prob'])
axs[3].axhline(low_thresh[h], color=colours['threshold'], linestyle=':', label='Thresholds', lw=2)
axs[3].axhline(high_thresh[h], color=colours['threshold'], linestyle=':', lw=2)
axs[3].set_ylabel('Household\nVoltage (V)', fontsize=19)
axs[3].tick_params(axis='both', labelsize=16)
axs[3].legend(fontsize=16)
axs[3].minorticks_on()
axs[3].grid(axis='x', which='major', alpha=0.5)
axs[3].grid(axis='x', which='minor', alpha=0.25)
axs[3].set_xlabel('Hour of Day', fontsize=19)

plt.tight_layout()

plt.savefig(
    r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\methodology'
    + '/single_voltage_prob_ctrl_house.png',
    dpi=600
)

plt.show()