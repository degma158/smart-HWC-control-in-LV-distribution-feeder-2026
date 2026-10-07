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

out_pth = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\methodology\current control"

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

with open(r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Initial nz\control_signals.dat', 'rb') as f:
    Ctrl_sigs = pickle.load(f)
Ctrl_sigs.keys()




# -------------------------------------
# Baseline current behaviour signle house (time evolution of current and state, added current histogram)
# # -------------------------------------

state = trial['thermo'][0]['element_state_log']
current = trial['thermo'][0]['Current']
I_flat = current.flatten()

I_thresh_low = Ctrl_sigs['current_thresh_low']
I_thresh_high = Ctrl_sigs['current_thresh_high']

h = 5
start = 0
end = 1440

fig = plt.figure(figsize=(9, 6))
gs = fig.add_gridspec(
    2, 2,
    width_ratios=[4, 1],
    height_ratios=[3, 1],
    wspace=0.05,
    hspace=0.05
)
ax1 = fig.add_subplot(gs[0, 0])                  # Current
ax2 = fig.add_subplot(gs[0, 1], sharey=ax1)     # Distribution
ax3 = fig.add_subplot(gs[1, 0], sharex=ax1)     # Element state

# Current
ax1.plot(time_hours[start:end], current[:, h][start:end], color=colours['thermo'])
ax1.axhline(
    I_thresh_high,
    color=colours['threshold'],
    linestyle=line_styles['threshold'],
    label='Thresholds'
)
ax1.axhline(
    I_thresh_low,
    color=colours['threshold'],
    linestyle=line_styles['threshold']
)
ax1.set_ylabel('Current (A)', fontsize=19)
ax1.tick_params(axis='both', labelsize=16)
ax1.legend(fontsize=16)
ax1.grid(axis='y', alpha=0.5)
ax1.set_xlim(0, 24)
ax1.set_ylim(0,25)
plt.setp(ax1.get_xticklabels(), visible=False)

# Current distribution
ax2.hist(
    I_flat,
    bins=100,
    orientation='horizontal',
    density=True,
    color=colours['thermo']
)
ax2.axhline(
    I_thresh_high,
    color=colours['threshold'],
    linestyle=line_styles['threshold']
)
ax2.axhline(
    I_thresh_low,
    color=colours['threshold'],
    linestyle=line_styles['threshold']
)
ax2.set_xlabel('Estimated\nProbability\nDensity', fontsize=19)
ax2.tick_params(axis='x', labelsize=16)
ax2.tick_params(axis='y', labelleft=False)
ax2.set_xlim(0, 0.5)
from matplotlib.ticker import FormatStrFormatter
ax2.set_xticks([0.0, 0.5])
ax2.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))

# Element state
ax3.plot(time_hours[start:end], state[:, h][start:end], color=colours['thermo'])
ax3.set_ylabel('Element\nState', fontsize=19)
ax3.set_xlabel('Hour of Day', fontsize=19)
ax3.set_yticks([0, 1])
ax3.set_yticklabels(['Off', 'On'])
ax3.set_ylim(-0.1, 1.1)
ax3.tick_params(axis='both', labelsize=16)
ax3.grid(axis='x', which='major', alpha=0.5)
ax3.grid(axis='x', which='minor', alpha=0.25)
ax3.set_xlim(0, 24)

# Subplot labels
ax1.text(0.02, 0.96, '(a)', transform=ax1.transAxes,
         fontsize=18, fontweight='bold', va='top', ha='left')

ax2.text(0.08, 0.96, '(b)', transform=ax2.transAxes,
         fontsize=18, fontweight='bold', va='top', ha='left')

ax3.text(0.02, 0.92, '(c)', transform=ax3.transAxes,
         fontsize=18, fontweight='bold', va='top', ha='left')

plt.tight_layout()
plt.savefig(
    out_pth + '/baseline single house current behaviour.pdf',
)

plt.show()





# -----------------------------------
# Distributions
# -------------------------------------

# I_house = results['thermo'][0]['I_house']
# houses = range(54)
# I_house_mean = np.mean(I_house, axis=2) # Mean current over days for each house

# current_thresh_low = 3
# current_thresh_high = 16

# # Plot of all distributions with thresholds
# fig, ax = plt.subplots(figsize=(9, 6))
# # individual distributions (background layer)
# for l in range(1,54):
#     I_flat = I_house[:,l,:].flatten()
#     kde = gaussian_kde(I_flat, bw_method=0.25)
#     x = np.linspace(I_flat.min(), I_flat.max(), 500)
#     pdf = kde(x)
#     if l == 1:
#         ax.plot(x,pdf,color=colours['thermo'],alpha=0.05,linewidth=1, label='Individual\nHousehold Distributions')
#     else:
#         ax.plot(x,pdf,color=colours['thermo'],alpha=0.05,linewidth=1)
# # Overal distribution (foreground, dominant)
# I_flat = I_house.flatten()
# kde = gaussian_kde(I_flat, bw_method=0.25) # bw_method=0.15)
# x = np.linspace(I_flat.min(), I_flat.max(), 500)
# pdf = kde(x)
# ax.plot(x,pdf,color=colours['thermo'],linewidth=1,label='Overal Distribution')
# ax.axvline(current_thresh_low, color='red', linestyle=':', label='Thresholds')
# ax.axvline(current_thresh_high, color='red', linestyle=':')
# ax.set_xlabel('Household Current (A)', fontsize=19)
# ax.set_ylabel('Estimated Probability Density', fontsize=19)
# # ax.set_title('Daily Household Current Distributions Averaged Over Days')
# ax.grid(axis='x', alpha=0.5)
# ax.legend(fontsize=16)
# ax.tick_params(axis='both', labelsize=16)
# ax.set_xlim(0, 30)
# plt.savefig(
#     r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\methodology\current control\household_distributions.png",
#         dpi=600)
# plt.show()





############################
#############################
##############################
# Combined plot
###########################

# -------------------------------------------------
# Current control comparison:
# No delay vs 100-minute delay
# -------------------------------------------------

# =========================
# Load no-delay results
# =========================

with open(
    r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Individual results\50%\current_no_delay_trial.dat",
    'rb'
) as f:
    no_delay = pickle.load(f)

I_no = no_delay['Current']
T_no = no_delay['temp_vector']
category_no = no_delay['category']
state_no = no_delay['state']

h_no = 2
start_no = 0
end_no = 1440


# =========================
# Load 100-minute delay results
# =========================

temp_delay = trial['current'][100]['temp_vector']
state_delay = trial['current'][100]['element_state_log']
category_delay = trial['current'][100]['category']
current_delay = trial['current'][100]['Current']

h_delay = 1
start_delay = 470
end_delay = 670


# Thresholds
low_thresh = Ctrl_sigs['current_thresh_low']
high_thresh = Ctrl_sigs['current_thresh_high']


# =========================
# Time axes
# =========================

# Full day in hours
time_no = time_hours[start_no:end_no]

# Zoomed delay example in minutes from start of window
time_delay = np.arange(end_delay - start_delay)


# =========================
# Combined plot
# =========================

fig, axs = plt.subplots(3, 2,figsize=(8, 7),constrained_layout=True)

# Column titles
axs[0, 0].set_title('Column (a)', fontsize=19)
axs[0, 1].set_title('Column (b)', fontsize=19)

# -------------------------------------------------
# ROW 3: Temperature
# -------------------------------------------------

axs[2, 0].plot(time_no,T_no[start_no:end_no, h_no],color=colours['current'])
axs[2, 1].plot(time_delay,temp_delay[start_delay:end_delay, h_delay],color=colours['current'])

for ax in axs[2, :]:
    ax.axhline(63,color=colours['threshold'],lw=2,linestyle=':',label='Temperature Limits')
    ax.axhline(60, color=colours['threshold'], lw=2, linestyle=':')
    ax.axhline(70, color=colours['threshold'], lw=2, linestyle=':')
    ax.axhline(73, color=colours['threshold'], lw=2, linestyle=':')

    ax.set_ylim(53.25, 74)

    ax.set_ylabel('Temperature (°C)', fontsize=19)
    ax.tick_params(axis='both', labelsize=16)
    ax.minorticks_on()
    ax.grid(axis='x', which='major', alpha=0.5)
    ax.grid(axis='x', which='minor', alpha=0.25)
    ax.legend(fontsize=16)

axs[2,1].set_ylabel('', fontsize=19)
axs[2,1].tick_params(left=False, bottom=True, labelleft=False, labelbottom=True)

# -------------------------------------------------
# ROW 2: Charging Category
# -------------------------------------------------

axs[1, 0].step(time_no,category_no[start_no:end_no, h_no],where='post',color=colours['current'])
axs[1, 1].step(time_delay,category_delay[start_delay:end_delay, h_delay],where='post',color=colours['current'])

for ax in axs[1, :]:
    ax.set_ylabel('Category', fontsize=17)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Conservative', 'Aggressive'])
    ax.set_ylim(-0.1, 1.1)
    ax.tick_params(axis='both', labelsize=16)
    ax.minorticks_on()
    ax.grid(axis='x', which='major', alpha=0.5)
    ax.grid(axis='x', which='minor', alpha=0.25)

axs[1,1].set_ylabel('', fontsize=19)
axs[1,1].set_yticklabels(['', ''])
axs[1,1].tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)


# -------------------------------------------------
# ROW 1: Household Current
# -------------------------------------------------

axs[0, 0].plot(time_no,I_no[start_no:end_no, h_no],color=colours['current'])
axs[0, 1].plot(time_delay,current_delay[start_delay:end_delay, h_delay],color=colours['current'])

for ax in axs[0, :]:
    ax.axhline(low_thresh,color=colours['threshold'],linestyle=':',lw=2,label='Thresholds')
    ax.axhline(high_thresh,color=colours['threshold'],linestyle=':',lw=2)
    ax.set_ylabel('Current (A)', fontsize=19)
    ax.set_ylim([0,25])
    ax.tick_params(axis='both', labelsize=16)
    ax.minorticks_on()
    ax.grid(axis='x', which='major', alpha=0.5)
    ax.grid(axis='x', which='minor', alpha=0.25)
    ax.legend(fontsize=16)

axs[0,1].set_ylabel('', fontsize=19)
axs[0,1].tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

# # -------------------------------------------------
# # Add in delay lines
# # -------------------------------------------------

for row in [0,1,2]:
    x = 46
    axs[row,1].axvline(x, linestyle=':',color='black')
    axs[row,1].axvline(x+100, linestyle=':',color='black')

    if row == 0:

        # Horizontal line
        axs[row, 1].plot([x, x+100],[4, 4],color='black',linewidth=1)
        # Arrow heads
        axs[row, 1].plot(x+2, 4,marker='<', color='black', markersize=5)
        axs[row, 1].plot(x+100-2, 4,marker='>',color='black',markersize=5)
        # text
        axs[row, 1].text(92,4.25,'100 min',ha='center',va='bottom',fontsize=16)

# Different x axes because left is a full day,
# while right is a zoomed switching example
axs[2, 0].set_xlabel('Hour of Day', fontsize=16)
axs[2, 1].set_xlabel('Time (Minutes)', fontsize=16)

plt.savefig(
    out_pth + '/current control no delay vs 100 minute delay.pdf'
)

plt.show()