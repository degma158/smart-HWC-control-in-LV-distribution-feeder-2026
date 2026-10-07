import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy.stats import gaussian_kde
from scipy.stats import rankdata

pth = r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Initial'

out_pth = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\results\baseline behaviour"

plt.rcParams['font.family'] = 'Times New Roman'

# -----------------------------
# Load results
# -----------------------------

with open(pth + '/thermo_mean.dat', 'rb') as f:
    results = pickle.load(f)
results.keys()

with open(pth + '/thermo_trial.dat', 'rb') as f:
    trial = pickle.load(f)
trial.keys()

time_vector = np.arange(0,1440,1)
time_hours = time_vector/60
time_of_day = np.array([
    f"{m//60:02d}:{m%60:02d}"
    for m in time_vector
])


# -----------------------------
# Single House Thermo Behaviour
# -----------------------------

h = 25

fig, axs = plt.subplots(3, 1, figsize=(9, 7.5), sharex=True, constrained_layout=True)

# Temperature
axs[0].plot(time_hours, trial['temp_vector'][:, h], color='#4D4D4D')
axs[0].axhline(63, color='#7F7F7F', linestyle=':', label='Temperature Limits')
axs[0].axhline(60, color='#7F7F7F', linestyle=':')
axs[0].set_ylabel('Temperature (°C)', fontsize=19)
#axs[0].set_title(f'Thermo Control For House {h} Over One Day')
axs[0].legend(fontsize=16)
axs[0].tick_params(axis='both', labelsize=16)
axs[0].grid(True)

# Flow
axs[1].plot(time_hours, trial['flow_matrix'][:, h], color='#4D4D4D')
axs[1].set_ylabel('Flow (m3/s)', fontsize=19)
axs[1].tick_params(axis='both', labelsize=16)
axs[1].grid(True)

# Element state
axs[2].plot(time_hours, trial['element_state_log'][:, h], color='#4D4D4D')
axs[2].set_ylabel('Element State', fontsize=19)
axs[2].set_xlabel('Hour of Day', fontsize=19)
axs[2].set_yticks([0, 1])
axs[2].set_yticklabels(['Off', 'On'])
axs[2].set_ylim(-0.1, 1.1)
axs[2].tick_params(axis='both', labelsize=16)
axs[2].grid(True)

plt.savefig(
    out_pth + '/thermo control single house.png',
        dpi=600
)
plt.show()

# -----------------------------
# On Fraction
# -----------------------------

on_frac_mean = 100*np.mean(results['on_fraction'], axis=1)
on_frac_min = 100*np.min(results['on_fraction'], axis=1)
on_frac_max = 100*np.max(results['on_fraction'], axis=1)

plt.figure(figsize=(9,6))
# Mean and smoothed line
plt.plot(time_hours, on_frac_mean, label='Mean', linewidth=2, color='#4D4D4D')
# Min / Max envelope
plt.plot(time_hours, on_frac_min, linestyle='--', alpha=0.6, label='Minimum', color='#CC79A7')
plt.plot(time_hours, on_frac_max, linestyle='--', alpha=0.6, label='Maximum', color='#D55E00')
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

# -----------------------------
# Feeder Power Profile
# -----------------------------

P_sum_mean = np.mean(results['P_sum'], axis=1)
P_sum_min = np.min(results['P_sum'], axis=1)
P_sum_max = np.max(results['P_sum'], axis=1)

plt.figure(figsize=(9,6))
# Mean and smoothed line
plt.plot(time_hours, P_sum_mean, label='Mean', linewidth=2, color='#4D4D4D')
# Min / Max envelope
plt.plot(time_hours, P_sum_max, linestyle='--', alpha=0.6, label='Maximum', color='#D55E00')
plt.plot(time_hours, P_sum_min, linestyle='--', alpha=0.6, label='Minimum', color='#CC79A7')
# Horizontal reference lines (overall stats)
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

# -----------------------------
# Feeder Power Distribution
# -----------------------------

P_sum_flat = results['P_sum'].flatten()

P_sum_kde = gaussian_kde(P_sum_flat)
P_sum_x = np.linspace(P_sum_flat.min(), P_sum_flat.max(), 500)
P_sum_pdf = P_sum_kde(P_sum_x)

plt.figure(figsize=(9,6))
# Mean and smoothed line
plt.plot(P_sum_x, P_sum_pdf, linewidth=2, color='#4D4D4D')
plt.xlabel("Total Feeder Power (kW)", fontsize=19)
plt.ylabel("Estimated Probability Distribution", fontsize=19)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize=16)
plt.grid(True)
plt.savefig(
    out_pth + '/feeder power distribution.png',
        dpi=600
)
plt.show()

# -----------------------------
# Feeder Power Metrics
# -----------------------------

P_sum_mean = np.mean(results['P_sum'])
mean_P_sum_95th = np.mean(np.percentile(results['P_sum'], 95, axis=0))
mean_P_sum_peak = np.mean(np.max(results['P_sum'], axis=0))
abs_P_sum_95th = np.percentile(results['P_sum'], 95)
abs_P_sum_peak = np.max(results['P_sum'])

P_sum_metrics = pd.DataFrame({
    'Metric': ['Mean Power Demand','Mean Daily 95th Percentile','Mean Daily Peak Demand','Absolute 95th Percentile','Absolute Peak Demand'],
    'Value (kW)': [P_sum_mean,mean_P_sum_95th,mean_P_sum_peak,abs_P_sum_95th,abs_P_sum_peak]
})

# format values for display
P_sum_metrics['Value (kW)'] = P_sum_metrics['Value (kW)'].round(3)

P_sum_metrics

# -----------------------------
# Voltage Profile
# -----------------------------

V_house_mean = np.mean(np.mean(results['V_house'], axis=2), axis=1)
V_house_min = np.min(np.mean(results['V_house'], axis=1), axis=1)
V_house_max = np.max(np.mean(results['V_house'], axis=1), axis=1)

plt.figure(figsize=(9,6))
# Mean and smoothed line
plt.plot(time_hours, V_house_mean, label='Mean', linewidth=2, color='#4D4D4D')
# Min / Max envelope
plt.plot(time_hours, V_house_min, linestyle='--', alpha=0.6, label='Minimum', color='#CC79A7')
plt.plot(time_hours, V_house_max, linestyle='--', alpha=0.6, label='Maximum', color='#D55E00')
# Horizontal reference lines (overall stats)
plt.xlabel("Hour of Day", fontsize=19)
plt.ylabel("Household Voltage (V)", fontsize=19)
#plt.title("Daily Feeder Power Profile")
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize=16)
plt.grid(True)
plt.savefig(
    out_pth + '/household voltage profile.png',
        dpi=600
)
plt.show()

# -----------------------------
# Voltage Distribution
# -----------------------------

V_house_flat = results['V_house'].flatten()

V_house_kde = gaussian_kde(V_house_flat)
V_house_x = np.linspace(V_house_flat.min(), V_house_flat.max(), 500)
V_house_pdf = V_house_kde(V_house_x)

plt.figure(figsize=(9,6))
# Mean and smoothed line
plt.plot(V_house_x, V_house_pdf, linewidth=2, color='#4D4D4D')
plt.xlabel("Household Voltage (V)", fontsize=19)
plt.ylabel("Estimated Probability Distribution", fontsize=19)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize=16)
plt.grid(True)
plt.savefig(
    out_pth + '/household voltage distribution.png',
        dpi=600
)
plt.show()

# -----------------------------
# Household Voltage Metrics
# -----------------------------

V_house_mean = np.mean(results['V_house'])
mean_V_5th = np.mean(np.percentile(results['V_house'], 5, axis=0))
mean_V_min = np.mean(np.min(results['V_house'], axis=0))
abs_V_5th = np.percentile(results['V_house'], 5)
abs_V_min = np.min(results['V_house'])


V_metrics = pd.DataFrame({'Metric': ['Mean Voltage','Mean Daily 5th Percentile Voltage','Mean Daily Minimum Voltage','Absolute 5th Percentile Voltage','Absolute Minimum Voltage'],
                        'Value (V)': [V_house_mean,mean_V_5th,mean_V_min,abs_V_5th,abs_V_min]
})

# format values for display
V_metrics['Value (V)'] = V_metrics['Value (V)'].round(3)

V_metrics

# -----------------------------
# Houshold Current Profile
# -----------------------------

I_house_mean = np.mean(np.mean(results['I_house'], axis=2), axis=1)
I_house_min = np.min(np.mean(results['I_house'], axis=1), axis=1)
I_house_max = np.max(np.mean(results['I_house'], axis=1), axis=1)

plt.figure(figsize=(9,6))
# Mean and smoothed line
plt.plot(time_hours, I_house_mean, label='Mean', linewidth=2, color='#4D4D4D')
# Min / Max envelope
plt.plot(time_hours, I_house_min, linestyle='--', alpha=0.6, label='Minimum', color='#CC79A7')
plt.plot(time_hours, I_house_max, linestyle='--', alpha=0.6, label='Maximum', color='#D55E00')
# Horizontal reference lines (overall stats)
plt.xlabel("Hour of Day", fontsize=19)
plt.ylabel("Household Current (A)", fontsize=19)
#plt.title("Daily Feeder Power Profile")
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize=16)
plt.grid(True)
plt.savefig(
    out_pth + '/household current profile.png',
        dpi=600
)
plt.show()

# -----------------------------
# Household Current Distribution
# -----------------------------

I_house_flat = results['I_house'].flatten()

I_house_kde = gaussian_kde(I_house_flat)
I_house_x = np.linspace(I_house_flat.min(), I_house_flat.max(), 500)
I_house_pdf = I_house_kde(I_house_x)

plt.figure(figsize=(9,6))
# Mean and smoothed line
plt.plot(I_house_x, I_house_pdf, linewidth=2, color='#4D4D4D')
plt.xlabel("Household Current (A)", fontsize=19)
plt.ylabel("Estimated Probability Distribution", fontsize=19)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize=16)
plt.grid(True)
plt.savefig(
    out_pth + '/household current distribution.png',
        dpi=600
)
plt.show()

# -----------------------------
# Household Current Percentile Curve
# -----------------------------

I_house_sorted = np.sort(I_house_flat)

# Corresponding percentiles
percentiles_I = np.linspace(0, 100, len(I_house_sorted))

plt.figure(figsize=(9,6))
plt.plot(percentiles_I, I_house_sorted, linewidth=2, color='#4D4D4D')

plt.xlabel("Percentile", fontsize=19)
plt.ylabel("Household Current (A)", fontsize=19)

plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.grid(True)

# plt.savefig(
#     out_pth + '/household current percentiles.png',
#     dpi=600
# )

plt.show()


# -----------------------------
# Household Current Metrics
# -----------------------------

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
