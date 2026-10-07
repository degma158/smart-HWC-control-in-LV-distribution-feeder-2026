# Code to determine the average daily hot water cylinder energy consumption.

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

pth = r"C:\Users\Max de Groot\Git\Honours-Project-2026\Outputs\HWC energy"

plt.rcParams['font.family'] = 'Times New Roman'

# --------------------------------
# Load Daily Energy for HWC
# --------------------------------

with open(pth + '/thermo_mean.dat', 'rb') as f:
    results = pickle.load(f)
results.keys()

E_hwc_house = results['E_hwc_house']
P_sum = results['P_sum']
P_sum.shape

# -----------------------------------
# Feeder Power Plot
# -----------------------------------

time_hours = np.arange(1440)/60

P_sum_mean = np.mean(P_sum, axis=1)

P_sum_trial = P_sum[:,1]

out_pth = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\methodology"

plt.figure(figsize=(6,4))
plt.plot(time_hours, P_sum_mean, color='black')
plt.xlabel('Hour of Day', fontsize=18)
plt.ylabel('Feeder Active Power (kW)', fontsize=19)
#plt.title('Average Daily Hot Water Flow Profile')
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.grid(axis='y', alpha=0.5)
plt.tight_layout()
plt.savefig(
    out_pth + '/HWC only feeder power profile.pdf'
)
plt.show()

# plt.figure(figsize=(9,6))
# plt.plot(time_hours, P_sum_trial)
# plt.xlabel('Hour of Day', fontsize=18)
# plt.ylabel('Feeder Active Power Demand (kW)', fontsize=18)
# #plt.title('Average Daily Hot Water Flow Profile')
# plt.xticks(fontsize=15)
# plt.yticks(fontsize=15)
# plt.grid(True)
# plt.show()

# plt.figure(figsize=(9,6))
# for t in [1,2,3]:
#     plt.plot(time_hours, P_sum[:,t], label=f'Trial {t}')
# plt.xlabel('Hour of Day', fontsize=18)
# plt.ylabel('Feeder Active Power Demand (kW)', fontsize=18)
# #plt.title('Average Daily Hot Water Flow Profile')
# plt.xticks(fontsize=15)
# plt.yticks(fontsize=15)
# plt.legend(fontsize=15)
# plt.grid(True)
# plt.show()


# Mean daily hot water cylinder energy consumption (averaged over all days and houses)
E_hwc_mean = np.mean(E_hwc_house)

print(E_hwc_mean)
