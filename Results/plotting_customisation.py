
import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import sys
import os

sys.path.append(r"C:\Users\Max de Groot\Git\Honours-Project-2026\My Code")
os.chdir(r"C:\Users\Max de Groot\Git\Honours-Project-2026\My Code")

import load_results

#------------------------------
# Plotting customization
#------------------------------

plt.rcParams['font.family'] = 'Times New Roman'

control_label = {
    "thermo": "Baseline",
    "price": "Price Control\n(Origional)",
    "price_rand": "Price Control\n(Randomised)",
    "current": "Current Control",
    "voltage": "Voltage Control\n(Origional)",
    "voltage_prob": "Voltage Control\n(Probabilistic)"
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
    "price": "#921CBA",         # blue - market/economic signal
    "price_rand": "#56B4E9",    # lighter blue - modified price control
    "current": "#E69F00",       # orange - electrical/current constraint
    "voltage": "#7CAE00",        # yellow-green      # green - voltage/network support
    "voltage_prob": "#009E73",  # same family - stochastic improvement
    "threshold": "#D50000",     # red - control boundaries
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