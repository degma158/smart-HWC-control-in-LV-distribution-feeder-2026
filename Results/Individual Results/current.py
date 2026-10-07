import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy.stats import gaussian_kde
from scipy.stats import rankdata

import sys
import os

# Import custom modules
sys.path.append(r"C:\Users\Max de Groot\Git\Honours-Project-2026\My Code")
os.chdir(r"C:\Users\Max de Groot\Git\Honours-Project-2026\My Code")
import plotting_customisation

out_pth = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\control development\current"

data_pth =  rf"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Individual results"


plt.rcParams['font.family'] = 'Times New Roman'

# -----------------------------
# Load results
# -----------------------------

with open(data_pth + '/50%/current_no_delay_trial.dat', 'rb') as f:
    no_delay_trial = pickle.load(f)
no_delay_trial.keys()

with open(r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Initial\thermo_mean.dat', 'rb') as f:
    baseline = pickle.load(f)
baseline.keys()

with open(data_pth + '/50%/current_mean.dat', 'rb') as f:
    results = pickle.load(f)
results.keys()

with open(data_pth + '/50%/current_trial.dat', 'rb') as f:
    trial = pickle.load(f)
trial.keys()


with open(r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Initial\control_signals.dat', 'rb') as f:
    Ctrl_sigs = pickle.load(f)
Ctrl_sigs.keys()

time_vector = np.arange(0,1440,1)
time_hours = time_vector/60
time_of_day = np.array([
    f"{m//60:02d}:{m%60:02d}"
    for m in time_vector
])

# -----------------------------
# Single house no delay
# -----------------------------

h = 2

fig, axs = plt.subplots(4, 1, figsize=(9, 10), sharex=True, constrained_layout=True)

# Temperature
axs[0].plot(time_hours, no_delay_trial['temp_vector'][:, h], color=colours['current'])
axs[0].axhline(63, color=colours['threshold'], lw=2, linestyle=':', label='Temperature Limits')
axs[0].axhline(60, color=colours['threshold'], lw=2, linestyle=':')
axs[0].axhline(73, color=colours['threshold'], lw=2, linestyle=':')
axs[0].axhline(70, color=colours['threshold'], lw=2, linestyle=':')
axs[0].set_ylabel('Temperature (°C)', fontsize=19)
axs[0].legend(fontsize=16)
axs[0].tick_params(axis='both', labelsize=16)
axs[0].grid(True)

# Element state
axs[1].plot(time_hours, no_delay_trial['element_state_log'][:, h], color=colours['current'])
axs[1].set_ylabel('Element State', fontsize=19)
axs[1].set_yticks([0, 1])
axs[1].set_yticklabels(['Off', 'On'])
axs[1].set_ylim(-0.1, 1.1)
axs[1].tick_params(axis='both', labelsize=16)
axs[1].grid(True)

# Category
axs[2].plot(time_hours, no_delay_trial['category'][:,h], color=colours['current'])
axs[2].set_ylabel('Category', fontsize=19)
axs[2].set_yticks([0, 1])
axs[2].set_yticklabels(['Cons', 'Aggr'])
axs[2].tick_params(axis='both', labelsize=16)
axs[2].set_ylim(-0.1, 1.1)
axs[2].grid(True)

# Current
axs[3].plot(time_hours, no_delay_trial['Current'][:, h], color=colours['current'])
axs[3].axhline(Ctrl_sigs['current_thresh_low'], color=colours['threshold'], lw=2, linestyle=line_styles['threshold'], label='Thresholds')
axs[3].axhline(Ctrl_sigs['current_thresh_high'], color=colours['threshold'], lw=2, linestyle=line_styles['threshold'])
axs[3].set_ylabel('Current', fontsize=19)
axs[3].set_xlabel('Hour of Day', fontsize=19)
axs[3].tick_params(axis='both', labelsize=16)
axs[3].legend(fontsize=16)
axs[3].grid(True)

plt.savefig(
out_pth + f'\single_house_no_delay.png',
    dpi=600
)

plt.show()

# # -----------------------------
# # Single house with delay
# # -----------------------------

h = 2

fig, axs = plt.subplots(4, 1, figsize=(9, 10), sharex=True, constrained_layout=True)

# Temperature
axs[0].plot(time_hours, trial['temp_vector'][:, h], color=colours['current'])
axs[0].axhline(63, color=colours['threshold'], lw=2,linestyle=':', label='Temperature Limits')
axs[0].axhline(60, color=colours['threshold'], lw=2, linestyle=':')
axs[0].axhline(73, color=colours['threshold'], lw=2, linestyle=':')
axs[0].axhline(70, color=colours['threshold'], lw=2, linestyle=':')
axs[0].set_ylabel('Temperature (°C)', fontsize=19)
axs[0].legend(fontsize=16)
axs[0].tick_params(axis='both', labelsize=16)
axs[0].grid(True)

# Element state
axs[1].plot(time_hours, trial['element_state_log'][:, h], color=colours['current'])
axs[1].set_ylabel('Element State', fontsize=19)
axs[1].set_yticks([0, 1])
axs[1].set_yticklabels(['Off', 'On'])
axs[1].set_ylim(-0.1, 1.1)
axs[1].tick_params(axis='both', labelsize=16)
axs[1].grid(True)

# Category
axs[2].plot(time_hours, trial['category'][:,h], color=colours['current'])
axs[2].set_ylabel('Category', fontsize=19)
axs[2].set_yticks([0, 1])
axs[2].set_yticklabels(['Cons', 'Aggr'])
axs[2].tick_params(axis='both', labelsize=16)
axs[2].set_ylim(-0.1, 1.1)
axs[2].grid(True)

# Current
axs[3].plot(time_hours, trial['Current'][:, h], color='#0072B2')
axs[3].axhline(Ctrl_sigs['current_thresh_low'], color=colours['threshold'],lw=2, linestyle=':', label='Thresholds')
axs[3].axhline(Ctrl_sigs['current_thresh_high'], color=colours['threshold'],lw=2, linestyle=':')
axs[3].set_ylabel('Current', fontsize=19)
axs[3].set_xlabel('Hour of Day', fontsize=19)
axs[3].tick_params(axis='both', labelsize=16)
axs[3].grid(True)


plt.show()

# # -----------------------------
# # Metrics (Not good unless do a full 100 trial simulation)
# # -----------------------------

# I_house_mean = np.mean(results['I_house'])
# mean_I_95th = np.mean(np.percentile(results['I_house'], 95, axis=0))
# mean_I_peak = np.mean(np.max(results['I_house'], axis=0))
# abs_I_95th = np.percentile(results['I_house'], 95)
# abs_I_peak = np.max(results['I_house'])

# I_metrics = pd.DataFrame({'Metric': ['Mean Current','Average Daily 95th Percentile Current','Average Daily Peak Current','Absolute 95th Percentile Current','Absolute Peak Current'],
#     'Value (A)': [I_house_mean,mean_I_95th,mean_I_peak,abs_I_95th,abs_I_peak]
# })

# # format values for display
# I_metrics['Value (A)'] = I_metrics['Value (A)'].round(3)

# I_metrics

# # -----------------------------
# # Single HWC behaviour
# # -----------------------------

h = 2

fig, axs = plt.subplots(4, 1, figsize=(9, 10), sharex=True, constrained_layout=True)

# Temperature
axs[0].plot(time_hours, trial['temp_vector'][:, h], color=colours['current'])
axs[0].axhline(63, color='#7F7F7F', linestyle=':', label='Temperature Limits')
axs[0].axhline(60, color='#7F7F7F', linestyle=':')
axs[0].axhline(73, color='#7F7F7F', linestyle=':')
axs[0].axhline(70, color='#7F7F7F', linestyle=':')
axs[0].set_ylabel('Temperature (°C)', fontsize=19)
axs[0].legend(fontsize=16)
axs[0].tick_params(axis='both', labelsize=16)
axs[0].grid(True)

# Element state
axs[1].plot(time_hours, trial['element_state_log'][:, h], color='#0072B2')
axs[1].set_ylabel('Element State', fontsize=19)
axs[1].set_yticks([0, 1])
axs[1].set_yticklabels(['Off', 'On'])
axs[1].set_ylim(-0.1, 1.1)
axs[1].tick_params(axis='both', labelsize=16)
axs[1].grid(True)

# Category
axs[2].plot(time_hours, trial['category'][:,h], color='#0072B2')
axs[2].set_ylabel('Category', fontsize=19)
axs[2].set_yticks([0, 1])
axs[2].set_yticklabels(['Cons', 'Aggr'])
axs[2].tick_params(axis='both', labelsize=16)
axs[2].set_ylim(-0.1, 1.1)
axs[2].grid(True)

# Current
axs[3].plot(time_hours, trial['Current'][:, h], color='#0072B2')
axs[3].axhline(Ctrl_sigs['current_thresh_low'], color='#7F7F7F', linestyle=':', label='Thresholds')
axs[3].axhline(Ctrl_sigs['current_thresh_high'], color='#7F7F7F', linestyle=':')
axs[3].set_ylabel('Current', fontsize=19)
axs[3].set_xlabel('Hour of Day', fontsize=19)
axs[3].tick_params(axis='both', labelsize=16)
axs[3].grid(True)

# Voltage
# axs[3].plot(time_hours, Trial['Voltage'][:, h], color='#0072B2')
# axs[3].axhline(Ctrl_sigs['voltage_thresh_low'][h], color='#7F7F7F', linestyle=':', label='Thresholds')
# axs[3].axhline(Ctrl_sigs['voltage_thresh_high'][h], color='#7F7F7F', linestyle=':')
# axs[3].set_ylabel('Current', fontsize=19)
# axs[3].set_xlabel('Hour of Day', fontsize=19)
# axs[3].tick_params(axis='both', labelsize=16)
# axs[3].grid(True)

plt.show()

