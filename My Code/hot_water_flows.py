# Code to analyse the generated hot water flows

# Import dependencies
import pandas as pd
from dss import dss
from altdss import altdss
from dss import SolveModes
from importlib import reload
import matplotlib.pyplot as plt
import os
import numpy as np
import pickle
import random

import importlib.util
import sys

#-----------------------------------------------------
# Load flows
#-----------------------------------------------------

flows_pth = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Hot water model\Final Data\real\synthetic_profile[0].csv"
flow_data = pd.read_csv(flows_pth)
flow_vector = flow_data['Winter[undifferentiated_days]'] # in L/min
flow_vector = flow_vector*0.000016667 # convert from L/min to m3/s

n = 1440 # number of time steps in a day (1 minute resolution)
h = 55 # no. of houses

# Create flow matrix (1440 time steps, 55 houses, 100 trials)
flow_matrix = np.zeros((n, h, 100))
for t in range(100): # for each trial
    for l in range(h): # for each house

        start = t*n*h + l*n
        end = start + n

        flow_matrix[:,l,t] = flow_vector.iloc[start:end].values

flow_mean = np.mean(np.mean(flow_matrix, axis=1), axis=1)

#--------------------------------------------------------
# Plot flows
#--------------------------------------------------------

time_hours = np.arange(1440)/60

plt.figure()
plt.plot(time_hours, flow_mean)
plt.show()

house_to_plot = [0,10,20,30,40,50]
trial_to_plot = [0,10,20,30,40,50,60,70,80,90,99]

for h in house_to_plot:
    for t in trial_to_plot:
        plt.figure()
        plt.plot(time_hours, flow_matrix[:,h, t])
        plt.show()
