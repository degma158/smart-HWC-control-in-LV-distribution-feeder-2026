#
# Code to check the results of the voltage control simulation with probablistic switching
#

import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

pth = r"C:\Users\Max de Groot\Git\Honours-Project-2026\Outputs"

# -----------------------------------------------------------------
# Load Results
# -----------------------------------------------------------------

control_type = 'voltage'

with open(f'{pth}/Test/' + control_type + '_trial.dat', 'rb') as f:
#with open(f'{pth}/Test/'+ '/' + control_type+'_trial.dat', 'rb') as f:
    trial = pickle.load(f)
trial.keys()

with open(f'{pth}/initial/control_signals.dat', 'rb') as f:
    control = pickle.load(f)
control.keys()

time_minutes = np.arange(1440)
time_hours = time_minutes/60
time_of_day = np.array([
    f"{m//60:02d}:{m%60:02d}"
    for m in time_minutes
])

# Trial results
voltage = trial['Voltage']
current = trial['Current']
category = trial['category']
temp = trial['temp_vector']
flow = trial['flow_matrix']
state = trial['element_state_log']
enrg_in = trial['cummulative_energy_in']
enrg_out = trial['cummulative_energy_out']
power_demand = trial['power_demand']
switching = trial['switching_events']

# Control values
element_state = trial['element_state_log']
volt_thresh_high = control['voltage_thresh_high']
volt_thresh_low = control['voltage_thresh_low']
curr_thresh_high = control['current_thresh_high']
curr_thresh_low = control['current_thresh_low']
control_mask = trial['control_mask']

houses_controlled = np.where(control_mask)[0]

np.random.seed(0)  # reproducible
houses = np.random.choice(
    np.where(control_mask)[0],
    size=10,
    replace=False
)


# -------------------------------------------------------------------------------
# Physical check plot
# -------------------------------------------------------------------------------
for h in houses:

    fig, axs = plt.subplots(4, 2, figsize=(14, 10), sharex=True)
    axs = axs.ravel()

    axs[0].plot(time_hours, voltage[:, h])
    if control_type == 'voltage':
        axs[0].axhline(volt_thresh_high[h], color='r', linestyle=':', label='Thresholds')
        axs[0].axhline(volt_thresh_low[h], color='r', linestyle=':')
    axs[0].set_ylabel('Voltage')
    axs[0].set_title('Voltage')

    axs[1].plot(time_hours, current[:, h])
    if control_type == 'current':
        axs[1].axhline(curr_thresh_high, color='r', linestyle=':', label='Thresholds')
        axs[1].axhline(curr_thresh_low, color='r', linestyle=':')
    axs[1].set_ylabel('Current')
    axs[1].set_title('Current')
    axs[1].legend()

    axs[2].plot(time_hours, power_demand[:, h])
    axs[2].set_ylabel('Active Power Demand')
    axs[2].set_title('Active Power Demand')

    if control_type in ['price', 'thermo']:
        axs[3].plot(time_hours, category)
    else:
        axs[3].plot(time_hours, category[:, h])
    axs[3].set_ylabel('Category')
    axs[3].set_title('Category')

    axs[4].plot(time_hours, state[:,h])
    axs[4].set_ylabel('State')
    axs[4].set_title('State')

    axs[5].plot(time_hours, flow[:,h])
    axs[5].set_ylabel('Flow')
    axs[5].set_title('Flow')

    axs[6].plot(time_hours, temp[:,h])
    axs[6].set_ylabel('Temp')
    axs[6].set_title('Temperature')

    axs[7].plot(time_hours, enrg_in[:,h], label='In')
    axs[7].plot(time_hours, enrg_out[:,h], label='Out')
    axs[7].set_ylabel('Cumulative Energy (kWh)')
    axs[7].set_title('Energy')
    axs[7].legend()

    # x-labels only on bottom row
    axs[6].set_xlabel('Time (hours)')
    axs[7].set_xlabel('Time (hours)')

    fig.suptitle(f'House {h}')
    plt.tight_layout()
    plt.show()

 

# ------------------------------------------------------------------------------------------------------
# Oscilating Voltages
# ------------------------------------------------------------------------------------------------------

houses = [32,33,34,35]

fig, axes = plt.subplots(len(houses), 1,figsize=(15, 2.5 * len(houses)),sharex=True)

start = 0
end = 1339

for ax, h in zip(axes, houses):
    # Voltage axis
    ax.plot(time_minutes[start:end],voltage[start:end, h],label='Voltage')
    ax.axhline(volt_thresh_high[h])
    ax.axhline(volt_thresh_low[h])
    ax.set_ylabel('V (V)')

    # State axis
    ax_state = ax.twinx()
    ax_state.step(time_minutes[start:end],element_state[start:end, h],alpha=0.5, where='post',linestyle=':',label='State')
    if control_type in ['price','thermo']:
        ax_state.step(time_minutes[start:end],category[start:end],alpha=0.5,where='post',linestyle='--',label='Category')
    else:
        ax_state.step(time_minutes[start:end],category[start:end, h],alpha=0.5,where='post',linestyle='--',label='Category')
    ax_state.set_ylabel('Element State and Control Category')
    ax_state.set_ylim(-0.1, 1.1)

    ax.set_title(f'House {h}')

    # Combined legend
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax_state.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

axes[-1].set_xlabel('Minute of Day')

plt.tight_layout()
plt.show()



# -----------------------------------------
# Oscilating Voltage, state, and control
# ------------------------------------------

start = 0
end = 1339

from matplotlib.lines import Line2D


fig, axs = plt.subplots(
    3, 1,
    figsize=(15, 10),
    sharex=True,
    constrained_layout=True
)

fig.suptitle(
    'Voltage, Element State, and Control Category of Select Voltage Controlled Houses With 100% Control Uptake',
    fontsize=16,
    fontweight='bold'
)

# Store handles for common legend
house_handles = []

# =====================================================
# Voltage
# =====================================================
for h in houses:
    line, = axs[0].plot(
        time_minutes[start:end],
        voltage[start:end, h],
        alpha=0.8,
        label=f'House {h}'
    )
    house_handles.append(line)

axs[0].axhline(
    np.mean(volt_thresh_high),
    linestyle=':',
    color='r',
    linewidth=2,
    label='Mean Thresholds'
)

axs[0].axhline(
    np.mean(volt_thresh_low),
    linestyle=':',
    color='r',
    linewidth=2
)

axs[0].set_ylabel('Voltage (V)')
axs[0].grid(True)

# Only show threshold legend on voltage plot
axs[0].legend(loc='upper right')

# =====================================================
# Element State
# =====================================================
for h in houses:
    axs[1].step(
        time_minutes[start:end],
        element_state[start:end, h],
        where='post',
        alpha=0.8
    )

axs[1].set_ylabel('Element\nState')
axs[1].set_ylim(-0.1, 1.1)
axs[1].set_yticks([0, 1])
axs[1].set_yticklabels(['Off', 'On'])
axs[1].grid(True)

# =====================================================
# Control Category
# =====================================================
if control_type in ['price', 'thermo']:
    axs[2].step(
        time_minutes[start:end],
        category[start:end],
        where='post',
        color='k'
    )
else:
    for h in houses:
        axs[2].step(
            time_minutes[start:end],
            category[start:end, h],
            where='post',
            alpha=0.8
        )

axs[2].set_ylabel('Control\nCategory')
axs[2].set_ylim(-0.1, 1.1)
axs[2].set_yticks([0, 1])
axs[2].set_yticklabels(['Conservative', 'Aggressive'])
axs[2].grid(True)

# =====================================================
# Format x-axis as time of day
# =====================================================
tick_step = 30  # minutes (change to 30 for half-hour ticks)

tick_idx = np.arange(start, end, tick_step)

axs[2].set_xticks(time_minutes[tick_idx])
axs[2].set_xticklabels(
    time_of_day[tick_idx],
    rotation=45,
    ha='right'
)

axs[2].set_xlabel('Time of Day')

# =====================================================
# Common legend for houses
# =====================================================
fig.legend(
    handles=house_handles,
    labels=[f'House {h}' for h in houses],
    title='Controlled Houses',
    loc='center left',
    bbox_to_anchor=(1.01, 0.5)
)

plt.show()