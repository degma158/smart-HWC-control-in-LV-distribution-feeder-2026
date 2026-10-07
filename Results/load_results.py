# Code for plotting all per-house metrics against control

import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import os

from scipy.stats import gaussian_kde

# -----------------------------
# Create function to load results
# -----------------------------

controls = ['thermo', 'price', 'price_rand', 'current','voltage', 'voltage_prob'] # 'voltage'
penetrations = [0,20,40,50,60,80,100]


def load_results(controls, penetrations):
    pth = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Individual results nz"

    results = {}
    trial = {}

    for control in controls:

        results[control] = {}
        trial[control] = {}

        for p in penetrations:

            if p == 0:
                mean_path = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Initial nz\thermo_mean.dat"
                trial_path = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Initial nz\thermo_trial.dat"

            else:
                mean_path = f'{pth}/{p}%/{control}_mean.dat'
                trial_path = f'{pth}/{p}%/{control}_trial.dat'


            # Skip if files do not exist
            if not os.path.exists(mean_path) or not os.path.exists(trial_path):
                print(f"Skipping {control}, {p}% (file missing)")
                continue


            # Load results
            with open(mean_path, 'rb') as f:
                results[control][p] = pickle.load(f)

            with open(trial_path, 'rb') as f:
                trial[control][p] = pickle.load(f)

    return results, trial

        






