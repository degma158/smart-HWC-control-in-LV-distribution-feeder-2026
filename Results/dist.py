import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import sys
import os

plt.rcParams['font.family'] = 'Times New Roman'

time = np.arange(0, 60)

l1 = np.zeros(time.shape)
l2 = np.zeros(time.shape)
l3 = np.zeros(time.shape)

l1[5:15] = 1.5
l2[25:35] = 2
l3[45:55] = 1

ltot = l1 + l2 + l3

c1 = np.zeros(time.shape)
c2 = np.zeros(time.shape)
c3 = np.zeros(time.shape)

c1[25:35] = 1.5
c2[25:35] = 2
c3[25:35] = 1

ctot = c1 + c2 + c3


fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# Top left
axes[0, 0].plot(time, l1, label='Load 1')
axes[0, 0].plot(time, l2, label='Load 2')
axes[0, 0].plot(time, l3, label='Load 3')

# Bottom left
axes[1, 0].plot(time, ltot, label='Aggregate')

# Top right
axes[0, 1].plot(time, c1, label='Load 1')
axes[0, 1].plot(time, c2, label='Load 2')
axes[0, 1].plot(time, c3, label='Load 3')

# Bottom right
axes[1, 1].plot(time, ctot, label='Aggregate')




axes[0, 0].set_xlabel('Time (minutes)', fontsize=18)
axes[0, 0].set_ylabel('Power (kW)', fontsize=18)
axes[0, 0].legend(fontsize=18)
axes[0, 0].set_ylim(0, 5)

# Plot labels
axes[0, 0].text(0.03, 0.95, '(a)',
                transform=axes[0, 0].transAxes,
                ha='left', va='top', fontsize=14)

axes[0, 1].text(0.03, 0.95, '(b)',
                transform=axes[0, 1].transAxes,
                ha='left', va='top', fontsize=14)

axes[1, 0].text(0.03, 0.95, '(c)',
                transform=axes[1, 0].transAxes,
                ha='left', va='top', fontsize=14)

axes[1, 1].text(0.03, 0.95, '(d)',
                transform=axes[1, 1].transAxes,
                ha='left', va='top', fontsize=14)

plt.tight_layout()
plt.show()