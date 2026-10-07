import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy.stats import gaussian_kde
from scipy.stats import rankdata

out_pth = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures"

data_pth =  rf"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Individual results"


plt.rcParams['font.family'] = 'Times New Roman'

# -----------------------------
# Load results
# -----------------------------

with open(data_pth + '/100%/voltage_trial.dat', 'rb') as f:
    no_prob_trial = pickle.load(f)
no_prob_trial.keys()

with open(r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Initial\thermo_mean.dat', 'rb') as f:
    baseline = pickle.load(f)
baseline.keys()

with open(data_pth + '/50%/voltage_prob_mean.dat', 'rb') as f:
    results = pickle.load(f)
results.keys()

with open(data_pth + '/50%/voltage_prob_trial.dat', 'rb') as f:
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
# Single house no prob switching
# -----------------------------

h = 4

fig, axs = plt.subplots(4, 1, figsize=(9, 10), sharex=True, constrained_layout=True)

# Temperature
axs[0].plot(time_hours, no_prob_trial['temp_vector'][:, h], color='#0072B2')
axs[0].axhline(63, color='black', linestyle=':', label='Temperature Limits')
axs[0].axhline(60, color='#7F7F7F', linestyle=':')
axs[0].axhline(73, color='#7F7F7F', linestyle=':')
axs[0].axhline(70, color='#7F7F7F', linestyle=':')
axs[0].set_ylabel('Temperature (°C)', fontsize=19)
axs[0].legend(fontsize=16)
axs[0].tick_params(axis='both', labelsize=16)
axs[0].grid(True)

# Element state
axs[1].plot(time_hours, no_prob_trial['element_state_log'][:, h], color='#0072B2')
axs[1].set_ylabel('Element State', fontsize=19)
axs[1].set_yticks([0, 1])
axs[1].set_yticklabels(['Off', 'On'])
axs[1].set_ylim(-0.1, 1.1)
axs[1].tick_params(axis='both', labelsize=16)
axs[1].grid(True)

# Category
axs[2].plot(time_hours, no_prob_trial['category'][:,h], color='#0072B2')
axs[2].set_ylabel('Category', fontsize=19)
axs[2].set_yticks([0, 1])
axs[2].set_yticklabels(['Cons', 'Aggr'])
axs[2].tick_params(axis='both', labelsize=16)
axs[2].set_ylim(-0.1, 1.1)
axs[2].grid(True)

# Voltage
axs[3].plot(time_hours, no_prob_trial['Voltage'][:, h], color='#0072B2')
axs[3].axhline(Ctrl_sigs['voltage_thresh_low'][h], color='#7F7F7F', linestyle=':', label='Thresholds')
axs[3].axhline(Ctrl_sigs['voltage_thresh_high'][h], color='#7F7F7F', linestyle=':')
axs[3].set_ylabel('Voltage (V)', fontsize=19)
axs[3].set_xlabel('Hour of Day', fontsize=19)
axs[3].tick_params(axis='both', labelsize=16)
axs[3].grid(True)

plt.show()

# # -----------------------------
# # Single house with delay
# # -----------------------------

h = 4

fig, axs = plt.subplots(4, 1, figsize=(9, 10), sharex=True, constrained_layout=True)

# Temperature
axs[0].plot(time_hours, trial['temp_vector'][:, h], color='#0072B2')
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

# Voltage
axs[3].plot(time_hours, trial['Voltage'][:, h], color='#0072B2')
axs[3].axhline(Ctrl_sigs['voltage_thresh_low'][h], color='#7F7F7F', linestyle=':', label='Thresholds')
axs[3].axhline(Ctrl_sigs['voltage_thresh_high'][h], color='#7F7F7F', linestyle=':')
axs[3].set_ylabel('Voltage (V)', fontsize=19)
axs[3].set_xlabel('Hour of Day', fontsize=19)
axs[3].tick_params(axis='both', labelsize=16)
axs[3].grid(True)

plt.show()

# -----------------------------
# Feeder Power Profile
# -----------------------------

plt.figure(figsize=(9,6))
plt.plot(time_hours, np.mean(baseline["P_sum"], axis=1), label='Baseline', color='#4D4D4D')
plt.plot(time_hours, np.mean(results['P_sum'], axis=1), label='Voltage Control', color='#0072B2')
plt.xlabel("Hour of Day", fontsize=19)
plt.ylabel("Total Feeder Power (kW)", fontsize=19)
#plt.title("Daily Feeder Power Profile")
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize=16)
plt.grid(True)
plt.savefig(
    out_pth + '/feeder power profile.png',
        dpi=600
)
plt.show()

# # -----------------------------
# # On Fraction Profile
# # -----------------------------

plt.figure(figsize=(9,6))
# Mean and smoothed line
plt.plot(time_hours, 100*np.mean(baseline["on_fraction"], axis=1), label='Baseline', color='#4D4D4D')
# Min / Max envelope
plt.plot(time_hours, 100*np.mean(results['on_fraction'], axis=1), label='Voltage Control', color='#0072B2')
# Horizontal reference lines (overall stats)
plt.xlabel("Hour of Day", fontsize=19)
plt.ylabel("Portion of HWC Elements On (%)", fontsize=19)
#plt.title("Daily Feeder Power Profile")
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize=16)
plt.grid(True)
plt.savefig(
    out_pth + '/on fraction profile.png',
        dpi=600
)
plt.show()

# # -----------------------------
# # Household Voltage Profile
# # -----------------------------

plt.figure(figsize=(9,6))
# Mean and smoothed line
plt.plot(time_hours, np.mean(np.mean(baseline["V_house"], axis=1), axis=1), label='Baseline', color='#4D4D4D')
# Min / Max envelope
plt.plot(time_hours, np.mean(np.mean(results["V_house"], axis=1), axis=1), label='Voltage Control', color='#0072B2')
# Horizontal reference lines (overall stats)
plt.xlabel("Hour of Day", fontsize=19)
plt.ylabel("Household Voltage (V)", fontsize=19)
#plt.title("Daily Feeder Power Profile")
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize=16)
plt.grid(True)
plt.savefig(
    out_pth + '/voltage profile.png',
        dpi=600
)
plt.show()

# # -----------------------------
# # Household Current Profile
# # -----------------------------

plt.figure(figsize=(9,6))
# Mean and smoothed line
plt.plot(time_hours, np.mean(np.mean(baseline["I_house"], axis=1), axis=1), label='Baseline', color='#4D4D4D')
# Min / Max envelope
plt.plot(time_hours, np.mean(np.mean(results["I_house"], axis=1), axis=1), label='Voltage Control', color='#0072B2')
# Horizontal reference lines (overall stats)
plt.xlabel("Hour of Day", fontsize=19)
plt.ylabel("Household Current (A)", fontsize=19)
#plt.title("Daily Feeder Power Profile")
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize=16)
plt.grid(True)
plt.savefig(
    out_pth + '/current profile.png',
        dpi=600
)
plt.show()

# # -----------------------------
# # Metrics (Not good unless do a full 100 trial simulation)
# # -----------------------------

I_house_mean = np.mean(results['I_house'])
mean_I_95th = np.mean(np.percentile(results['I_house'], 95, axis=0))
mean_I_peak = np.mean(np.max(results['I_house'], axis=0))
abs_I_95th = np.percentile(results['I_house'], 95)
abs_I_peak = np.max(results['I_house'])

I_metrics = pd.DataFrame({'Metric': ['Mean Current','Average Daily 95th Percentile Current','Average Daily Peak Current','Absolute 95th Percentile Current','Absolute Peak Current'],
    'Value (A)': [I_house_mean,mean_I_95th,mean_I_peak,abs_I_95th,abs_I_peak]
})

# format values for display
I_metrics['Value (A)'] = I_metrics['Value (A)'].round(3)

I_metrics

# # -----------------------------
# # Single HWC behaviour
# # -----------------------------

h = 2

fig, axs = plt.subplots(4, 1, figsize=(9, 10), sharex=True, constrained_layout=True)

# Temperature
axs[0].plot(time_hours, trial['temp_vector'][:, h], color='#0072B2')
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

