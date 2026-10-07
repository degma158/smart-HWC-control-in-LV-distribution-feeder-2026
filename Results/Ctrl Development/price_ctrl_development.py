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

with open(r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Initial nz\control_signals.dat', 'rb') as f:
    Ctrl_sigs = pickle.load(f)
Ctrl_sigs.keys()

time_vector = np.arange(0,1440,1)
time_hours = time_vector/60
time_of_day = np.array([
    f"{m//60:02d}:{m%60:02d}"
    for m in time_vector
])

# -----------------------------------
# Single HWC Behaviour
# -----------------------------------
trial['price'][50].keys()

temp = trial['price'][50]['temp_vector']
price_signal = Ctrl_sigs['price_signal']

h = 6

start=0
end=1440


fig, axs = plt.subplots(2, 1, figsize=(6, 4.5), sharex=True, constrained_layout=True)

# Temperature
axs[0].plot(time_hours[start:end], temp[:, h][start:end], color=colours['price'])
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
# Price
axs[1].plot(time_hours[start:end], price_signal, color=colours['price'])
axs[1].set_ylabel('Price Signal', fontsize=19)
axs[1].set_xlabel('Hour of Day')
axs[1].tick_params(axis='both', labelsize=16)
axs[1].set_yticks([0, 1])
axs[1].set_yticklabels(['Low', 'High'])
axs[1].set_ylim(-0.1, 1.1)
axs[1].minorticks_on()
axs[1].grid(axis='x', which='major', alpha=0.5)
axs[1].grid(axis='x', which='minor', alpha=0.25)

plt.tight_layout()
plt.savefig(
r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\methodology\price control\single_price_ctrl_house_temp_price_signal.pdf"
    )

plt.show()