# Code to see if heating elements are synchronising/oscilating together in the initial thermo simulation

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

pth = r"C:\Users\Max de Groot\Git\Honours-Project-2026\Outputs\Initial"

# --------------------------------
# Load Base Case Single Trial Results
# --------------------------------

with open(pth + '/thermo_trial.dat', 'rb') as f:
    results = pickle.load(f)
results.keys()

time_vector = np.arange(0,1440,1)
time_hours = time_vector/60
time_of_day = np.array([
    f"{m//60:02d}:{m%60:02d}"
    for m in time_vector
])

# ---------------------------------------------
# Check element state
#----------------------------------------------

houses = [50,51,52,53,54]
houses = np.arange(54)

plt.figure(figsize=(15,3))
for h in houses:
    plt.plot(time_hours, results['element_state_log'][:,h])
plt.show()

mean_state = np.mean(results['element_state_log'], axis=1)

plt.figure(figsize=(15,4))
plt.plot(time_hours, mean_state)
plt.xlabel('Time (hours)')
plt.ylabel('HWC Element State')
plt.title('Average Daily Fraction of Hot Water Cylinder Elements On')
plt.grid(True)
plt.show()