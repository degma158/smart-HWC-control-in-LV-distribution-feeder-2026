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

out_pth = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\methodology\voltage control"

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

with open(r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Initial nz\control_signals.dat", 'rb') as f:
    Ctrl_sigs = pickle.load(f)
Ctrl_sigs.keys()

#--------------------------------
# Baseline signel house with thresholds and histogram
#--------------------------------

# voltage = trial['thermo'][0]['Voltage']
# V_flat = voltage.flatten()

# V_thresh_low = Ctrl_sigs['voltage_thresh_low']
# V_thresh_high = Ctrl_sigs['voltage_thresh_high']

# h = 1

# fig = plt.figure(figsize=(9, 5))
# gs = fig.add_gridspec(1, 2, width_ratios=[4, 1], wspace=0.05)
# ax1 = fig.add_subplot(gs[0])
# ax2 = fig.add_subplot(gs[1], sharey=ax1)

# # Voltage profile
# ax1.plot(time_hours, voltage[:, h], color=colours['thermo'])
# ax1.axhline(V_thresh_high[h],color=colours["threshold"],linestyle=line_styles["threshold"],label='Thresholds')
# ax1.axhline(V_thresh_low[h],color=colours["threshold"],linestyle=line_styles["threshold"])
# ax1.set_xlabel('Hour of Day', fontsize=19)
# ax1.set_ylabel('Household Voltage (V)', fontsize=19)
# # ax1.set_title('Daily Profile', fontsize=19)
# ax1.tick_params(axis='both', labelsize=16)
# ax1.grid(axis='y', alpha=0.5)
# ax1.legend(fontsize=16)
# ax1.set_xlim([0,24])
# # ax1.set_ylim([240,255])

# # Voltage histogram
# ax2.hist(voltage[:, h],bins=25,orientation='horizontal',density=True, color=colours['thermo'])
# # ax2.hist(V_flat,bins=100,orientation='horizontal',density=True, color=colours['thermo'])
# ax2.axhline(V_thresh_high[h],color=colours["threshold"],linestyle=line_styles["threshold"],label='Thresholds')
# ax2.axhline(V_thresh_low[h],color=colours["threshold"],linestyle=line_styles["threshold"])
# ax2.set_xlabel('Estimated Probability\nDensity', fontsize=19)
# # ax2.set_title('Histogram', fontsize=19)
# ax2.tick_params(axis='x', labelsize=16)
# ax2.tick_params(axis='y', labelleft=False)

# plt.tight_layout()
# plt.savefig(
#     out_pth + '/baseline single house voltage behaviour.png',
#         dpi=600
#     )

# plt.show()


# ----------------------------------------------------
# Example Voltage thresholds on distribution
# ----------------------------------------------------

# h = 11

# V_house = results['thermo'][0]['V_house']
# V_flat = V_house[:,h,:].flatten()
# kde = gaussian_kde(V_flat)
# x = np.linspace(V_flat.min(), V_flat.max(), 500)
# pdf = kde(x)

# plt.figure(figsize=(9,6))
# plt.plot(x, pdf, color=colours['thermo'])
# plt.axvline(V_thresh_high[h], color=colours['threshold'], linestyle=line_styles['threshold'])
# plt.axvline(V_thresh_low[h], color=colours['threshold'], linestyle=line_styles['threshold'], label='Thresholds')
# plt.xlabel('Household Voltage (V)', fontsize=19)
# plt.ylabel('Estimated Probability Density', fontsize=19)
# plt.tick_params(axis='both', labelsize=16)
# plt.grid(alpha=0.5)
# plt.show()


# -------------------------------------------------
# Single threshold excessive switching behaviour
# -------------------------------------------------

with open(r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\voltage control development\voltage_single_trial.dat", 'rb') as f:
    data = pickle.load(f)
data.keys()

voltage = data['Voltage']
state = data['element_state_log']
temp = data['temp_vector']
category = data['category']
control_mask = data['control_mask']

V_thresh_high = Ctrl_sigs['voltage_thresh_high']

control_mask

h = 11
start = 500
end = 700

fig, axs = plt.subplots(3, 1, figsize=(9, 6), sharex=True, constrained_layout=True)
# Element state
axs[2].step(time_vector[start:end]-start, state[:, h][start:end], color=colours['voltage'], where='post')
axs[2].set_ylabel('Element State', fontsize=19)
axs[2].set_yticks([0, 1])
axs[2].set_yticklabels(['Off', 'On'])
axs[2].set_ylim(-0.1, 1.1)
axs[2].tick_params(axis='both', labelsize=16)
axs[2].minorticks_on()
axs[2].grid(axis='x', which='major', alpha=0.5)
axs[2].grid(axis='x', which='minor', alpha=0.25)
axs[2].set_xlabel('Time (minutes)', fontsize=19)
# Category
axs[1].step(time_vector[start:end]-start, category[:,h][start:end], color=colours['voltage'], where='post')
axs[1].set_ylabel('Category', fontsize=19)
axs[1].tick_params(axis='both', labelsize=16)
axs[1].set_yticks([0, 1])
axs[1].set_yticklabels(['Conservative','Aggressive'])
axs[1].set_ylim(-0.1, 1.1)
axs[1].minorticks_on()
axs[1].grid(axis='x', which='major', alpha=0.5)
axs[1].grid(axis='x', which='minor', alpha=0.25)
# Voltage
axs[0].plot(time_vector[start:end]-start, voltage[:, h][start:end], color=colours['voltage'])
axs[0].axhline(V_thresh_high[h], color = colours['threshold'], linestyle=':', lw=2, label='Threshold')
axs[0].set_ylabel('Household\nVoltage (V)', fontsize=19)
axs[0].tick_params(axis='both', labelsize=16)
axs[0].legend(fontsize=14, loc='lower right')
axs[0].minorticks_on()
axs[0].grid(axis='x', which='major', alpha=0.5)
axs[0].grid(axis='x', which='minor', alpha=0.25)

plt.tight_layout()
# plt.savefig(
#     out_pth + '/single threshold voltage controller.png',
#         dpi=600
#     )

plt.show()





# -------------------------------------------------
# Double threshold running mean
# -------------------------------------------------

with open(r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\voltage control development\voltage_running double_trial.dat", 'rb') as f:
    data = pickle.load(f)
data.keys()

voltage = data['Voltage']
state = data['element_state_log']
temp = data['temp_vector']
category = data['category']
control_mask = data['control_mask']

V_thresh_high = Ctrl_sigs['voltage_thresh_high']
V_thresh_low = Ctrl_sigs['voltage_thresh_low']

control_mask

h = 11

V_mean = np.array([
    np.mean(voltage[:,h][max(0, i-4):i+1])
    for i in range(len(voltage[:,h]))
])

fig, axs = plt.subplots(3, 1, figsize=(9, 6), sharex=True, constrained_layout=True)
# Element state
axs[2].step(time_vector[start:end]-start, state[:, h][start:end], color=colours['voltage'], where='post')
axs[2].set_ylabel('Element State', fontsize=19)
axs[2].set_yticks([0, 1])
axs[2].set_yticklabels(['Off', 'On'])
axs[2].set_ylim(-0.1, 1.1)
axs[2].tick_params(axis='both', labelsize=16)
axs[2].minorticks_on()
axs[2].grid(axis='x', which='major', alpha=0.5)
axs[2].grid(axis='x', which='minor', alpha=0.25)
axs[2].set_xlabel('Time (minutes)', fontsize=19)
# Category
axs[1].step(time_vector[start:end]-start, category[:,h][start:end], color=colours['voltage'], where='post')
axs[1].set_ylabel('Category', fontsize=19)
axs[1].tick_params(axis='both', labelsize=16)
axs[1].set_yticks([0, 1])
axs[1].set_yticklabels(['Conservative','Aggressive'])
axs[1].set_ylim(-0.1, 1.1)
axs[1].minorticks_on()
axs[1].grid(axis='x', which='major', alpha=0.5)
axs[1].grid(axis='x', which='minor', alpha=0.25)
# Voltage
axs[0].plot(time_vector[start:end]-start, voltage[:, h][start:end], color=colours['voltage'], label='Househould Voltage')
axs[0].plot(time_vector[start:end]-start, V_mean[start:end], color=colours['voltage'], linestyle='--', label='Running Mean of V')
axs[0].axhline(V_thresh_high[h], color = colours['threshold'], linestyle=':', lw=2, label='Thresholds')
axs[0].axhline(V_thresh_low[h], color = colours['threshold'], linestyle=':', lw=2)
axs[0].set_ylabel('Household\nVoltage (V)', fontsize=19)
axs[0].tick_params(axis='both', labelsize=16)
axs[0].minorticks_on()
axs[0].grid(axis='x', which='major', alpha=0.5)
axs[0].grid(axis='x', which='minor', alpha=0.25)
axs[0].legend(
    loc='lower center',
    bbox_to_anchor=(0.5, 1.02),
    ncol=3,
    fontsize=14
)

plt.tight_layout()
plt.savefig(
    out_pth + '/running mean + double threshold voltage controller.png',
        dpi=600
    )

plt.show()



# -------------------------------------------------
# V pred inclusion
# -------------------------------------------------

with open(r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\voltage control development\voltage_pred running double_trial.dat", 'rb') as f:
    data = pickle.load(f)
data.keys()

voltage = data['Voltage']
state = data['element_state_log']
temp = data['temp_vector']
category = data['category']
control_mask = data['control_mask']

V_thresh_high = Ctrl_sigs['voltage_thresh_high']
V_thresh_low = Ctrl_sigs['voltage_thresh_low']

control_mask

h = 11

delta_V_est = Ctrl_sigs['delta_V_est'][h]

V_pred = voltage[:,h] - (1-state[:,h])*delta_V_est

V_pred_mean = np.array([
    np.mean(V_pred[max(0, i-4):i+1])
    for i in range(len(voltage[:,h]))
])

fig, axs = plt.subplots(3, 1, figsize=(9, 6), sharex=True, constrained_layout=True)
# Element state
axs[2].step(time_vector[start:end]-start, state[:, h][start:end], color=colours['voltage'], where='post')
axs[2].set_ylabel('Element State', fontsize=19)
axs[2].set_yticks([0, 1])
axs[2].set_yticklabels(['Off', 'On'])
axs[2].set_ylim(-0.1, 1.1)
axs[2].tick_params(axis='both', labelsize=16)
axs[2].minorticks_on()
axs[2].grid(axis='x', which='major', alpha=0.5)
axs[2].grid(axis='x', which='minor', alpha=0.25)
axs[2].set_xlabel('Time (minutes)', fontsize=19)
# Category
axs[1].step(time_vector[start:end]-start, category[:,h][start:end], color=colours['voltage'], where='post')
axs[1].set_ylabel('Category', fontsize=19)
axs[1].tick_params(axis='both', labelsize=16)
axs[1].set_yticks([0, 1])
axs[1].set_yticklabels(['Conservative','Aggressive'])
axs[1].set_ylim(-0.1, 1.1)
axs[1].minorticks_on()
axs[1].grid(axis='x', which='major', alpha=0.5)
axs[1].grid(axis='x', which='minor', alpha=0.25)
# Voltage
axs[0].plot(time_vector[start:end]-start, voltage[:, h][start:end], color=colours['voltage'], label='Household Voltage')
axs[0].plot(time_vector[start:end]-start, V_pred_mean[start:end], color=colours['voltage'], linestyle='--', label='Running Mean of V$_{pred}$')
axs[0].axhline(V_thresh_high[h], color = colours['threshold'], linestyle=':', lw=2, label='Thresholds')
axs[0].axhline(V_thresh_low[h], color = colours['threshold'], linestyle=':', lw=2)
axs[0].set_ylabel('Household\nVoltage (V)', fontsize=19)
axs[0].tick_params(axis='both', labelsize=16)
axs[0].minorticks_on()
axs[0].grid(axis='x', which='major', alpha=0.5)
axs[0].grid(axis='x', which='minor', alpha=0.25)
# Voltage legend
axs[0].legend(
    loc='lower center',
    bbox_to_anchor=(0.5, 1.02),
    ncol=3,
    fontsize=14
)

plt.tight_layout()
plt.savefig(
    out_pth + '/V_pred + running mean + double threshold voltage controller.png',
        dpi=600
    )

plt.show()





#-------------------------------------------------------
#-------------------------------------------------------
#------------------------------------------------------
# All developments progression plots
# --------------------------------------------------------

# -------------------------------------------------
# Combined voltage controller development figure
# -------------------------------------------------

# Plot window
h = 11
start = 550
end = 640

t = time_vector[start:end] - time_vector[start]


# =================================================
# Load data
# =================================================

# (a) Single threshold
with open(
    r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\voltage control development\voltage_single_trial.dat",
    'rb'
) as f:
    data_single = pickle.load(f)

voltage_single = data_single['Voltage']
state_single = data_single['element_state_log']
category_single = data_single['category']


# (b) Double threshold + running mean
with open(
    r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\voltage control development\voltage_running double_trial.dat",
    'rb'
) as f:
    data_double = pickle.load(f)

voltage_double = data_double['Voltage']
state_double = data_double['element_state_log']
category_double = data_double['category']


# (c) V_pred inclusion
with open(
    r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\voltage control development\voltage_pred running double_trial.dat",
    'rb'
) as f:
    data_pred = pickle.load(f)

voltage_pred = data_pred['Voltage']
state_pred = data_pred['element_state_log']
category_pred = data_pred['category']


# =================================================
# Controller signals
# =================================================

V_thresh_high = Ctrl_sigs['voltage_thresh_high']
V_thresh_low = Ctrl_sigs['voltage_thresh_low']

# 5-minute running mean for (b)
V_mean = np.array([
    np.mean(voltage_double[max(0, i - 4):i + 1, h])
    for i in range(len(voltage_double))
])

# Predicted voltage for (c)
delta_V_est = Ctrl_sigs['delta_V_est'][h]

V_pred = (
    voltage_pred[:, h]
    - (1 - state_pred[:, h]) * delta_V_est
)

V_pred_mean = np.array([
    np.mean(V_pred[max(0, i - 4):i + 1])
    for i in range(len(V_pred))
])


# =================================================
# Create figure
# Rows:
#   0 = Voltage
#   1 = Category
#   2 = Element state
#
# Columns:
#   0 = Single threshold
#   1 = Double threshold + running mean
#   2 = V_pred inclusion
# =================================================

fig, axs = plt.subplots(3, 3,figsize=(9, 7),sharex='col',constrained_layout=True)


# =================================================
# (a) Single threshold
# =================================================

# Voltage
axs[0, 0].plot(t,voltage_single[start:end, h],color=colours['voltage'])
axs[0, 0].axhline(V_thresh_high[h],color=colours['threshold'],linestyle=':',lw=2,label='Threshold')
axs[0, 0].legend(fontsize=12, loc='lower right')

# Category
axs[1, 0].step(t,category_single[start:end, h],color=colours['voltage'],where='post')

# Element state
axs[2, 0].step(t,state_single[start:end, h],color=colours['voltage'],where='post')

# =================================================
# (b) Double threshold + running mean
# =================================================

# Voltage
axs[0, 1].plot(t,voltage_double[start:end, h],color=colours['voltage'],label='V')
axs[0, 1].plot(t,V_mean[start:end],color=colours['voltage'],linestyle='--',label=r'V$_{mean}$')
axs[0, 1].axhline(V_thresh_high[h],color=colours['threshold'],linestyle=':',lw=2,label='Thresholds')
axs[0, 1].axhline(V_thresh_low[h],color=colours['threshold'],linestyle=':',lw=2)
axs[0, 1].legend(fontsize=12,loc='lower right')

# Category
axs[1, 1].step(t,category_double[start:end, h],color=colours['voltage'],where='post')

# Element state
axs[2, 1].step(t,state_double[start:end, h],color=colours['voltage'],where='post')

# =================================================
# (c) V_pred inclusion
# =================================================

# Voltage
axs[0, 2].plot(t,voltage_pred[start:end, h],color=colours['voltage'],label='V')
axs[0, 2].plot(t,V_pred_mean[start:end],color=colours['voltage'],linestyle='--',label=r'V$_{pred, mean}$')
axs[0, 2].axhline(V_thresh_high[h],color=colours['threshold'],linestyle=':',lw=2,label='Thresholds')
axs[0, 2].axhline(V_thresh_low[h],color=colours['threshold'],linestyle=':',lw=2)
axs[0, 2].legend(fontsize=12,loc='lower right')

# Category
axs[1, 2].step(t,category_pred[start:end, h],color=colours['voltage'],where='post')

# Element state
axs[2, 2].step(t,state_pred[start:end, h],color=colours['voltage'],where='post')


# =================================================
# Formatting
# =================================================

column_titles = [
    'Column (a)',
    'Column (b)',
    'Column (c)'
]

for col in range(3):

    # Column title
    axs[0, col].set_title(column_titles[col],fontsize=19,pad=12)
    axs[0,col].set_ylim([232,244])

    # Category formatting
    axs[1, col].set_yticks([0, 1])
    if col == 0:
        axs[1, col].set_yticklabels(['Conservative', 'Aggressive'],fontsize=16)
    else:
        axs[1, col].set_yticklabels(['', ''],fontsize=16)
    axs[1, col].set_ylim(-0.1, 1.1)

    # Element state formatting
    axs[2, col].set_yticks([0, 1])
    if col == 0:
        axs[2, col].set_yticklabels(['Off', 'On'],fontsize=16)
    else:
        axs[2, col].set_yticklabels(['', ''],fontsize=16)
    axs[2, col].set_ylim(-0.1, 1.1)

    # X-axis
    axs[2, col].set_xlabel('Time (minutes)',fontsize=19)

    if col != 0:
        axs[0,col].tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

    # General formatting
    for row in range(3):
        axs[row, col].tick_params(axis='both', labelsize=16)
        axs[row, col].minorticks_on()
        axs[row, col].grid(axis='x',which='major',alpha=0.5)
        axs[row, col].grid(axis='x',which='minor',alpha=0.2)



# =================================================
# Y-axis labels only on left-hand column
# =================================================

axs[0, 0].set_ylabel(
    'Household\nVoltage (V)',
    fontsize=19
)

axs[1, 0].set_ylabel(
    'Category',
    fontsize=19
)

axs[2, 0].set_ylabel(
    'Element State',
    fontsize=19
)




# =================================================
# Save
# =================================================

plt.savefig(
    out_pth + '/combined voltage controller development.pdf'
)

plt.show()