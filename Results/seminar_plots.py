import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import sys
import os

sys.path.append(r"C:\Users\Max de Groot\Git\Honours-Project-2026\Results")
os.chdir(r"C:\Users\Max de Groot\Git\Honours-Project-2026\Results")

import load_results

from scipy.stats import gaussian_kde

out_pth = rf"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\feeder power"

# -----------------------------
# Load results
# -----------------------------
controls = ['thermo', 'price', 'price_rand', 'current','voltage', 'voltage_prob']
penetrations = [0,50,60,80,100]

load_data = True

if load_data == True:
    results, trial = load_results.load_results(controls, penetrations)

with open(r"C:\Users\Max de Groot\Git\Honours-Project-2026\Outputs\Initial nz" + '/control_signals.dat', 'rb') as f:
    Ctrl_sigs = pickle.load(f)
Ctrl_sigs.keys()

#------------------------------
# Plotting customization
#------------------------------

time_minutes = np.arange(0,1440,1)
time_hours = time_minutes/60

plt.rcParams['font.family'] = 'Times New Roman'

control_label = {
    "thermo": "Baseline",
    "price": "Price Control\n(Original)",
    "price_rand": "Price Control\n(Randomised)",
    "current": "Current Control",
    "voltage": "Voltage Control\n(Original)",
    "voltage_prob": "Voltage Control\n(Probabilistic)"
}

profile_control_label = {
    "thermo": "Baseline",
    "price": "Price Control\n(Original)",
    "price_rand": "Price Control\n(Randomised)",
    "current": "Current Control",
    "voltage": "Voltage\nControl\n(Original)",
    "voltage_prob": "Voltage\nControl\n(Probabilistic)"
}

marker_styles = {
    "thermo": "o",
    "price": "s",
    "price_rand": "D",
    "current": "^",
    "voltage": "v",
    "voltage_prob": "X"
}

colours = {
    "thermo": "#4D4D4D",        # dark grey - baseline/reference
    "price": "#0072B2",         # blue - market/economic signal
    "price_rand": "#56B4E9",    # lighter blue - modified price control
    "current": "#E69F00",       # orange - electrical/current constraint
    "voltage": "#7CAE00",        # yellow-green      # green - voltage/network support
    "voltage_prob": "#009E73",  # same family - stochastic improvement
    "threshold": "black",     # neutral grey - control boundaries
    "maximum": "#D55E00",       # red-orange - upper limit/warning
    "minimum": "#CC79A7"        # purple/pink - lower limit
}

line_styles = {
    "thermo": "-",
    "price": "--",
    'price_rand': "-",
    "current": "-",
    "voltage": "--",
    'voltage_prob': "-",
    "threshold": ":",
    "maximum": "--",
    "minimum": "--"
}


#------------------------
# Plotting Aggressive vs baseline
# -------------------------
h = 2

trial['thermo'][100]['temp_vector'].shape

thermo_temp = trial['thermo'][100]['temp_vector'][:,h]
price_temp = trial['price_rand'][100]['temp_vector'][:,h]

plt.figure(figsize=(15,4))
plt.plot(time_hours, thermo_temp, label='Baseline (Normal Control)')
plt.plot(time_hours, price_temp, label='Aggresive/Conservative')
plt.axhline(70, color = colours["threshold"], linestyle=line_styles["threshold"])
plt.axhline(73, color = colours["threshold"], linestyle=line_styles["threshold"])
plt.axhline(60, color = colours["threshold"], linestyle=line_styles["threshold"])
plt.axhline(63, color = colours["threshold"], linestyle=line_styles["threshold"])
plt.xlabel('Time (Hours)', fontsize=13)
plt.ylabel('Temperature (degC)', fontsize=13)
plt.grid(True)
plt.ylim(45, 75)
plt.legend(fontsize=13)
plt.tight_layout
plt.show()

















#------------------------
# Plotting Voltage Ctrl Synchronisation
# -------------------------

V = trial['voltage'][100]['Voltage']
category = trial['voltage'][100]['category']
state = trial['voltage'][100]['element_state_log']
temp = trial['voltage'][100]['temp_vector']

V_thresh_high = np.mean(Ctrl_sigs['voltage_thresh_high'])
V_thresh_low = np.mean(Ctrl_sigs['voltage_thresh_low'])

start, end = 615, 640
houses = [29,30,33]

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 7), sharex=True)

for h in houses:
    ax1.plot(time_minutes[start:end]-start, V[start:end, h], label=f'House {h+1}', alpha=0.75)
    ax2.step(time_minutes[start:end]-start, category[start:end, h], where='post', alpha=0.75)
    ax3.step(time_minutes[start:end]-start, state[start:end, h], where='post', alpha=0.75)

ax1.axhline(V_thresh_high, ls=line_styles['threshold'], color=colours['threshold'], label='Mean\nVoltage\nThresholds')
ax1.axhline(V_thresh_low, ls=line_styles['threshold'], color=colours['threshold'])
ax1.set_ylabel('Voltage (V)', fontsize=19)
ax1.set_ylim(210,245)
ax1.legend(
    handles=[ax1.lines[-2]],
    labels=['Mean Voltage Thresholds'],
    fontsize=16,
    loc='lower left'
)

ax2.set_yticks([0, 1])
ax2.set_yticklabels(['Conservative\nCharging', 'Aggressive\nCharging'], fontsize=14)
ax2.set_ylabel('Category', fontsize=19)
ax2.set_ylim(-0.1, 1.1)

ax3.set_yticks([0, 1])
ax3.set_yticklabels(['Off', 'On'], fontsize=16)
ax3.set_ylim(-0.1, 1.1)
ax3.set_ylabel('Element State', fontsize=19)
ax3.set_xlabel('Time (Minutes)', fontsize=19)


for ax in [ax1, ax2, ax3]:
    ax.tick_params(axis='both', labelsize=16)
    ax.minorticks_on()
    ax.grid(axis='x', which='major', alpha=0.5)
    ax.grid(axis='x', which='minor', alpha=0.25)

# House legend handles
house_handles, house_labels = ax1.get_legend_handles_labels()

# Keep only the house entries
house_handles = house_handles[:len(houses)]
house_labels = house_labels[:len(houses)]

# # House legend below whole figure
# fig.legend(
#     house_handles,
#     house_labels,
#     loc='lower center',
#     bbox_to_anchor=(0.5, -0.03),
#     ncol=len(houses),
#     fontsize=16,
#     frameon=False
# )

fig.subplots_adjust(
    hspace=0.12,
    bottom=0.3
)

fig.subplots_adjust(hspace=0.12)
fig.tight_layout()

plt.savefig(
r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\modelling limitation plots\voltage_ctrl_synchronisation_oscilation.pdf"
    )

plt.show()


















# -----------------------------
# Current control
# -----------------------------

trial['current'][100].keys()

I = trial['thermo'][100]['Current']
category = trial['thermo'][100]['element_state_log']

Ctrl_sigs.keys()

I_thresh_low = Ctrl_sigs['current_thresh_low']
I_thresh_high = Ctrl_sigs['current_thresh_high']

h = 13

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9,6), sharex=True)

ax1.plot(time_hours, I[:,h])

ax2.step(time_hours, category[:,h], where='post')

ax1.axhline(I_thresh_high, ls=line_styles["threshold"], 
            color=colours["threshold"], label='Thresholds')

ax1.axhline(I_thresh_low, ls=line_styles["threshold"], 
            color=colours["threshold"])

ax1.set_ylabel('Current (A)', fontsize=19)

ax1.grid()
ax1.legend(fontsize=16)

ax2.set_xlabel('Time (Hours)', fontsize=19)
ax2.set(yticks=[0,1], ylim=(-0.1,1.1))

ax2.set_ylabel('Element State', fontsize=19)

ax2.set_yticklabels(['On', 'Off'], fontsize=19)
ax2.tick_params(axis='x', labelsize=16)
ax1.tick_params(axis='y', labelsize=19)

ax2.grid()
ax2.legend(fontsize=16)

plt.tight_layout()

plt.show()


# ---------------------------------------------
# Voltage control
# ----------------------------------------------

V_house = results['thermo'][50]['V_house']
V_house_mean = np.mean(results['thermo'][50]['V_house'], axis=2)

V_thresh_high = Ctrl_sigs['voltage_thresh_high']
V_thresh_low = Ctrl_sigs['voltage_thresh_low']

V_house.shape
# Plot of daily household current profile for single house averaged over days
# Daily household voltage profile
plt.figure(figsize=(9, 4))

plt.plot(time_hours, V_house[:, h, 10])

plt.axhline(
    V_thresh_high[h],
    color=colours["threshold"],
    linestyle=line_styles["threshold"],
    label='Thresholds'
)
plt.axhline(
    V_thresh_low[h],
    color=colours["threshold"],
    linestyle=line_styles["threshold"]
)

plt.xlabel('Hour of Day', fontsize=19)
plt.ylabel('Household Voltage (V)', fontsize=19)
plt.title('Daily Profile', fontsize=19)
plt.tick_params(axis='both', labelsize=16)
plt.legend(fontsize=16)
plt.grid(True)

plt.tight_layout()
plt.show()


# Voltage distribution
V_flat = V_house[:, h, :].flatten()

kde = gaussian_kde(V_flat)
x = np.linspace(V_flat.min(), V_flat.max(), 500)
pdf = kde(x)

plt.figure(figsize=(9, 4))

plt.plot(x, pdf)

plt.axvline(
    V_thresh_high[h],
    color=colours["threshold"],
    linestyle=line_styles["threshold"],
    label='Thresholds'
)
plt.axvline(
    V_thresh_low[h],
    color=colours["threshold"],
    linestyle=line_styles["threshold"]
)

plt.xlabel('Household Voltage (V)', fontsize=19)
plt.ylabel('Estimated Probability Density', fontsize=19)
plt.title('Voltage Distribution', fontsize=19)
plt.tick_params(axis='both', labelsize=16)
plt.legend(fontsize=16)
plt.grid(True)

plt.tight_layout()
plt.show()


V_flat = V_house[:, h, :].flatten()

fig = plt.figure(figsize=(11, 5))
gs = fig.add_gridspec(1, 2, width_ratios=[4, 1], wspace=0.05)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1], sharey=ax1)

# -------------------------
# Voltage profile
# -------------------------
ax1.plot(time_hours, V_house[:, h, 10])

ax1.axhline(
    V_thresh_high[h],
    color=colours["threshold"],
    linestyle=line_styles["threshold"],
    label='Thresholds'
)
ax1.axhline(
    V_thresh_low[h],
    color=colours["threshold"],
    linestyle=line_styles["threshold"]
)

ax1.set_xlabel('Hour of Day', fontsize=19)
ax1.set_ylabel('Household Voltage (V)', fontsize=19)
ax1.set_title('Daily Profile', fontsize=19)

ax1.tick_params(axis='both', labelsize=16)
ax1.grid(True)
ax1.legend(fontsize=16)


# -------------------------
# Voltage histogram
# -------------------------
ax2.hist(
    V_flat,
    bins=30,
    orientation='horizontal',
    density=True
)
ax2.axhline(
    V_thresh_high[h],
    color=colours["threshold"],
    linestyle=line_styles["threshold"],
    label='Thresholds'
)
ax2.axhline(
    V_thresh_low[h],
    color=colours["threshold"],
    linestyle=line_styles["threshold"]
)

ax2.set_xlabel('Estimated\nProbability\nDensity', fontsize=16)
ax2.set_title('Histogram', fontsize=19)
ax2.tick_params(axis='x', labelsize=14)
ax2.tick_params(axis='y', labelleft=False)

ax2.grid(True, axis='x')


plt.tight_layout()
plt.show()


# --------------------------------------------------------------
# disertation coincedent vs diversity plot
# --------------------------------------------------------------


x