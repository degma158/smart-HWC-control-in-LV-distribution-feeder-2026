# Code showing the determination of control thresholds (etc.) and how they work.

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

pth = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Initial nz"

# out_pth = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures"

plt.rcParams['font.family'] = 'Times New Roman'

# --------------------------------
# Load Base Case Control Signal Results
# --------------------------------

with open(pth + '/control_information.dat', 'rb') as f:
    Ctrl_info = pickle.load(f)
Ctrl_info.keys()

P_sum = Ctrl_info['P_sum']#[:, 1:]
V_house = Ctrl_info['V_house']#[:, :, 1:]
I_house = Ctrl_info['I_house']#[:,1:55,:] #[:, :, 1:]
delta_V_est = Ctrl_info['delta_V_est']
delta_I_est = Ctrl_info['delta_I_est']#[1,:]

with open(pth + '/thermo_trial.dat', 'rb') as f:
    Thermo_trial = pickle.load(f)
Thermo_trial.keys()

with open(pth + '/thermo_mean.dat', 'rb') as f:
    results = pickle.load(f)
results.keys()

element_state = Thermo_trial['element_state_log']

time_vector = np.arange(0,1440,1)
time_hours = time_vector/60
time_of_day = np.array([
    f"{m//60:02d}:{m%60:02d}"
    for m in time_vector
])



# --------------------------------
# Price Control Signal
# --------------------------------

# Important variables
P_sum_mean = np.mean(P_sum, axis=1)
P_sum_max = np.max(P_sum, axis=1)
P_sum_min = np.min(P_sum, axis=1)
P_smooth = pd.Series(P_sum_mean).rolling(60, center=True).mean()
P_smooth_50th = np.percentile(P_smooth.dropna(), 50) # P_smoothed 50th percentile
P_50th = np. percentile(P_sum, 50)

# Initial plot
plt.figure(figsize=(9,6))
# Mean and smoothed line
plt.plot(time_hours, P_sum_mean, label='Mean Daily Profile', linewidth=2)
# Min / Max envelope
plt.plot(time_hours, P_sum_min, linestyle='--', alpha=0.6, label='Minimum Power')
plt.plot(time_hours, P_sum_max, linestyle='--', alpha=0.6, label='Maximum Power')
# Horizontal reference lines (overall stats)
#plt.axhline(P_smooth_50th, color='black', linestyle=':', label='Smoothed Median')
plt.axhline(np.mean(P_sum), color='black', linestyle=':', label='Absolute Mean')
plt.xlabel("Hour of Day", fontsize=18)
plt.ylabel("Total Feeder Power (kW)", fontsize=18)
#plt.title("Daily Feeder Power Profile")
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.legend(fontsize=15)
plt.grid(True)
plt.show()

# Define threshold and high vs low price times

thresh = P_50th # 50th percentile power
thresh = np.mean(P_sum)
high_price = P_sum_mean > thresh # high price when above thresh

# Package removes small periods of change (i.e. for the short push up to high price in middle of two main peaks)
from scipy.ndimage import binary_opening, binary_closing 

high_price = binary_closing(high_price, iterations=10)
high_price = binary_opening(high_price, iterations=10)
#high_price[700:1000] = 0
price_signal = np.where(high_price, 1, 0) # Price signal

# Plot to check correct control signal
price_out_pth = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\results\price control"

fig, ax1 = plt.subplots(figsize=(6,5))
# Primary axis (power)
ax1.plot(time_hours, P_sum_mean, label='Mean Power\nProfile', color="#4D4D4D")
ax1.axhline(thresh, linestyle=':', linewidth=2, label='Absolute\nMean Power', color="#4D4D4D")
ax1.set_xlabel('Hour of Day',fontsize=19)
ax1.set_ylabel('Feeder Active Power (kW)',fontsize=19)
ax1.grid(axis='y', alpha=0.5)
ax1.set_ylim(0,115)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
# Secondary axis (price signal)
ax2 = ax1.twinx()
ax2.step(time_hours, price_signal, where='post', label='Price\nSignal', color="#0072B2")
ax2.set_ylabel(
    'Price Category',
    fontsize=19,
    rotation=270,
    labelpad=20
)
ax2.set_ylim(-0.1, 1.1)
ax2.set_yticks([0, 1])
ax2.set_yticklabels(['Low', 'High'])
# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax1.legend(
    lines1 + lines2,
    labels1 + labels2,
    fontsize=16,
    loc='upper center',
    bbox_to_anchor=(0.5, -0.22),
    ncol=3,
    frameon=False
)

# Add ons
#plt.title('Smoothed Feeder Power and Electricity Price Signal')
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
plt.savefig(
    r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\methodology\price control' + '/baseline feeder power price signal.pdf'
        )
plt.show()







#------------------------------------------------
# Current Control
# -----------------------------------------------


houses = range(54)
I_house_mean = np.mean(I_house, axis=2) # Mean current over days for each house

current_thresh_low = 3
current_thresh_high = 16

# Plot of all distributions with thresholds
fig, ax = plt.subplots(figsize=(6, 4))
# individual distributions (background layer)
for l in range(1,54):
    I_flat = I_house[:,l,:].flatten()
    kde = gaussian_kde(I_flat, bw_method=0.25)
    x = np.linspace(I_flat.min(), I_flat.max(), 500)
    pdf = kde(x)
    if l == 1:
        ax.plot(x,pdf,color='gray',alpha=0.2,linewidth=1, label='Individual\nHousehold\nDistributions')
    else:
        ax.plot(x,pdf,color='gray',alpha=0.2,linewidth=1)
# Overal distribution (foreground, dominant)
I_flat = I_house.flatten()
kde = gaussian_kde(I_flat, bw_method=0.25) # bw_method=0.15)
x = np.linspace(I_flat.min(), I_flat.max(), 500)
pdf = kde(x)
ax.plot(x,pdf,color='black',linewidth=1,label='Overal\nDistribution')
ax.axvline(current_thresh_low, color='red', linestyle=':', label='Thresholds')
ax.axvline(current_thresh_high, color='red', linestyle=':')
ax.set_xlabel('Household Current (A)', fontsize=19)
ax.set_ylabel('Probability Density', fontsize=19)
# ax.set_title('Daily Household Current Distributions Averaged Over Days')
ax.grid(alpha=0.5)
ax.legend(fontsize=16)

ax.tick_params(axis='both', labelsize=16)
ax.set_xlim(0, 30)
plt.tight_layout()
plt.savefig(
    r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\methodology\current control\household_distributions.pdf"
        )
plt.show()







# -----------------------------------------------
# Voltage Thresholds
# -----------------------------------------------

houses = range(54)
V_house_mean = np.mean(V_house, axis=2)
V_mean = np.mean(V_house_mean, axis=1)

V_house.shape
V_house_mean.shape

high = 40
low = 10

voltage_thresh_high = np.percentile(V_house, high, axis=(0,2))
voltage_thresh_low = np.percentile(V_house, low, axis=(0,2))

voltage_thresh_high.shape

h = 10

V_flat = V_house[:,h,:].flatten()
kde = gaussian_kde(V_flat)
x = np.linspace(V_flat.min(), V_flat.max(), 500)
pdf = kde(x)

plt.figure(figsize=(6,4))
plt.plot(x, pdf, color='#4D4D4D')
plt.axvline(voltage_thresh_high[h], color='red',linestyle=':')
plt.axvline(voltage_thresh_low[h], color='red',linestyle=':', label='Thresholds')
# plt.axvline(np.percentile(V_house[:,h,:], low))
# plt.axvline(np.percentile(V_house[:,h,:], high))
plt.xlabel('Household Voltage (V)', fontsize=19)
plt.ylabel('Probability Density', fontsize=19)
plt.tick_params('both', labelsize=16)
plt.legend(fontsize=16)
plt.grid(alpha=0.5)
plt.tight_layout()
plt.savefig(
    r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\methodology\voltage control\single house distribution with thresholds.pdf"
        )
plt.show()







# --------------------------------------------------------------------
# Voltage Tolerance Curves
# --------------------------------------------------------------------

P = np.linspace(0,100,166)
h = 10

# Percentile matrix (1440 x 55)
V_house_pdf = np.zeros((len(P),55,100))

V_house.shape
for t in np.arange(0,100):
    for l in np.arange(0,55):
        V_house_pdf[:,l,t] = np.percentile(V_house[:,l,t],P)

V_house_mean_pdf = np.mean(V_house_pdf,axis=2)

V_tolerance = V_house_mean_pdf[66:,:]
prob = np.linspace(0,100,len(V_tolerance))

fig, axs = plt.subplots(1, 2, figsize=(9, 4), constrained_layout=True)

# Voltage Percentile Curve
# -------------------------
axs[0].plot(P, V_house_mean_pdf[:, h], color='#4D4D4D')
axs[0].axvline(low, color='red', linestyle=':', label='Control\nThresholds') #label=f'{low}th Percentile (Low Threshold)')
axs[0].axvline(high, color='red', linestyle=':') #, label=f'{high}th Percentile (High Threshold)')
axs[0].set_xlabel('Percentile', fontsize=19)
axs[0].set_ylabel('Household Voltage (V)', fontsize=19)
axs[0].legend(fontsize=16)
axs[0].tick_params(axis='both', labelsize=16)
axs[0].grid(alpha=0.5)

# -------------------------
# Switching Probability Curve
# -------------------------
axs[1].plot(prob, V_tolerance[:, h], color='#4D4D4D')
axs[1].axvline(0, color='red', linestyle=':', label='Upper Control Threshold') #label=f'{high}th Percentile (High Threshold)')
axs[1].set_xlabel('Probability of Switching (%)', fontsize=19)
axs[1].set_ylabel('Household Voltage (V)', fontsize=19)
axs[1].legend(fontsize=16)
axs[1].tick_params(axis='both', labelsize=16)
axs[1].grid(alpha=0.5)

plt.savefig(
    r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\methodology\voltage control' + '/probablistic voltage control design.pdf'
)

plt.show()


# -----------------------------------------------
# Save new signals
# -----------------------------------------------

save_signals = True

if save_signals == True:

    Control_signals = {'price_signal': price_signal,
                    'current_thresh_low':current_thresh_low,
                    'current_thresh_high':current_thresh_high,
                    'voltage_thresh_low':voltage_thresh_low,
                    'voltage_thresh_high':voltage_thresh_high,
                    'delta_V_est':delta_V_est,
                    'delta_I_est':delta_I_est,
                    'V_tolerance':V_tolerance
                    }

    with open(
        r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Initial nz\control_signals.dat',
        'wb'
    ) as f:
        pickle.dump(Control_signals, f)
