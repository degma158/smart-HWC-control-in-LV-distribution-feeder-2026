import pickle
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

import sys
import os

sys.path.append(r"C:\Users\Max de Groot\Git\Honours-Project-2026\My Code")
os.chdir(r"C:\Users\Max de Groot\Git\Honours-Project-2026\My Code")

import load_results

from scipy.stats import gaussian_kde

out_pth = rf"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\household metrics"

# -----------------------------
# Load results
# -----------------------------

controls = ['thermo', 'price_rand', 'current', 'voltage', 'voltage_prob']
penetrations = [0,20,40,50,60,80,100]

results, trial = load_results.load_results(controls, penetrations)

#------------------------------
# Plotting customization
#------------------------------

time_minutes = np.arange(0,1440,1)
time_hours = time_minutes/60

plt.rcParams['font.family'] = 'Times New Roman'

control_label = {
    "thermo": "Baseline",
    "price": "Price Control\n(Original)",
    "price_rand": "Price Control\n(Randomised)",
    "current": "Current Control",
    "voltage": "Voltage Control\n(Original)",
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
    "price": "#0072B2",         # blue - market/economic signal
    "price_rand": "#56B4E9",    # lighter blue - modified price control
    "current": "#E69F00",       # orange - electrical/current constraint
    "voltage": "#7CAE00",        # yellow-green      # green - voltage/network support
    "voltage_prob": "#009E73",  # same family - stochastic improvement
    "threshold": "#999999",     # neutral grey - control boundaries
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

# -----------------------------
# Creating summary dataframe
# -----------------------------

# Electricity prices ($/kWh)
high_price = 0.42
low_price = 0.255

# mean_cost_example calculation
mean_cost_house = high_price*np.mean(results['thermo'][0]['E_on_peak_house'], axis=1) + low_price*np.mean(results['thermo'][0]['E_off_peak_house'], axis=1)

# Summary data frame
summary = {}
pens_to_plot = [20,40,60,80,100]

for control in controls:
    rows = []

    datasets = {
        0: (
            results['thermo'][0]['E_on_peak_house'],
            results['thermo'][0]['E_off_peak_house'],
            results['thermo'][0]['E_hwc_house']
        )
    }
    datasets.update({
        p: (
            results[control][p]['E_on_peak_house'],
            results[control][p]['E_off_peak_house'],
            results[control][p]['E_hwc_house']
        )
        for p in pens_to_plot
    })

    for p, (E_on, E_off, E_hwc) in datasets.items():

        # Average on and off peak energy
        mean_E_on_house = np.mean(E_on, axis=1)
        mean_E_off_house = np.mean(E_off, axis=1)
        mean_E_hwc_house = np.mean(E_hwc, axis=1)
        mean_E_net_house = mean_E_off_house + mean_E_on_house

        # Average daily electricity cost for each house across all trials
        mean_cost_house = (high_price * np.mean(E_on, axis=1) + low_price * np.mean(E_off, axis=1))

        rows.append({
            'penetration': p,
            'number_of_houses': int(np.ceil(55 * p / 100)),
            'cost': np.mean(mean_cost_house),
            'E_on': np.mean(mean_E_on_house),
            'E_off': np.mean(mean_E_off_house),
            'E_net': np.mean(mean_E_net_house),
            'E_hwc': np.mean(mean_E_hwc_house)
        })

    summary[control] = pd.DataFrame(rows)










#-----------------------------------------------------
# Plotting on/off peak energy vs penetration
#-----------------------------------------------------

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np


# ============================================================
# Household energy change vs penetration
# ============================================================

df_thermo = summary['thermo']

controls = [
    'price_rand',
    'current',
    'voltage_prob'
]

fig, axs = plt.subplots(
    2, 2,
    figsize=(11.2, 8),
    sharex=True
)

ax_on = axs[0, 0]
ax_off = axs[0, 1]
ax_total = axs[1, 0]
ax_legend = axs[1, 1]


# ============================================================
# Plot controllers
# ============================================================

for control in controls:

    df = summary[control]

    # Changes relative to baseline
    delta_on = (df['E_on'] -df_thermo['E_on'])
    delta_off = (df['E_off'] -df_thermo['E_off'])
    delta_total = (delta_on +delta_off)

    # On-peak
    ax_on.plot(
        df['penetration'],
        delta_on,
        color=colours[control],
        linestyle=line_styles[control],
        marker=marker_styles[control],
        linewidth=2,
        markersize=7,
        alpha=0.8
    )

    # Off-peak
    ax_off.plot(
        df['penetration'],
        delta_off,
        color=colours[control],
        linestyle=line_styles[control],
        marker=marker_styles[control],
        linewidth=2,
        markersize=7,
        alpha=0.8
    )

    # Total
    ax_total.plot(
        df['penetration'],
        delta_total,
        color=colours[control],
        linestyle=line_styles[control],
        marker=marker_styles[control],
        linewidth=2,
        markersize=7,
        alpha=0.8
    )

# ============================================================
# Plot formatting
# ============================================================

plot_axes = [ax_on,ax_off,ax_total]

for ax in plot_axes:

    # Baseline reference
    ax.axhline(
        0,
        color=colours['thermo'],
        linestyle='--',
        linewidth=1.5,
        alpha=0.8
    )

    ax.grid(
        alpha=0.5
    )

    ax.tick_params(
        axis='both',
        labelsize=16
    )

    ax.set_xticks(
        [0, 20, 40, 60, 80, 100]
    )

    ax.set_box_aspect(
        4.5 / 6
    )

    ax.set_xlabel('Penetration (%)', fontsize=19)


# Show x tick labels on upper plots
ax_on.tick_params(
    axis='x',
    labelbottom=True
)

ax_off.tick_params(
    axis='x',
    labelbottom=True
)


# ============================================================
# Panel labels
# ============================================================

ax_on.text(
    0.03, 0.97,
    '(a)',
    transform=ax_on.transAxes,
    fontsize=19,
    fontweight='bold',
    va='top',
    ha='left'
)

ax_off.text(
    0.03, 0.97,
    '(b)',
    transform=ax_off.transAxes,
    fontsize=19,
    fontweight='bold',
    va='top',
    ha='left'
)

ax_total.text(
    0.03, 0.97,
    '(c)',
    transform=ax_total.transAxes,
    fontsize=19,
    fontweight='bold',
    va='top',
    ha='left'
)


# ============================================================
# Legend
# ============================================================

control_handles = [
    Line2D(
        [0], [0],
        color=colours[control],
        linestyle=line_styles[control],
        marker=marker_styles[control],
        linewidth=2,
        markersize=7,
        label=control_label[control]
    )
    for control in controls
]

ax_legend.axis('off')

ax_legend.legend(
    handles=control_handles,
    loc='center',
    fontsize=19,
    frameon=False
)


# ============================================================
# Y axis labels
# ============================================================
ax_on.set_ylabel(r'$\Delta E_{On}$ (kWh/day)', fontsize=19)
ax_off.set_ylabel(r'$\Delta E_{Off}$ (kWh/day)', fontsize=19)
ax_total.set_ylabel(r'$\Delta E_{Total}$ (kWh/day)', fontsize=19)

# ============================================================
# Figure spacing
# ============================================================

fig.subplots_adjust(
    left=0.12,
    right=0.98,
    bottom=0.12,
    top=0.98,
    hspace=0.30,
    wspace=0.20
)

#----------------------
# ylims
#----------------------

ax_on.set_ylim(-2.8,0.5)

# ============================================================
# Save
# ============================================================

plt.savefig(
    out_pth +
    '/household metric plots/on_off_peak_total_energy_penetration.pdf',
    bbox_inches='tight'
)

plt.show()














# ============================================================
# Household electricity cost change vs penetration
# ============================================================

controls = [
    'price_rand',
    'current',
    'voltage_prob'
]

fig, ax = plt.subplots(
    figsize=(11.2, 7)
)


# ============================================================
# Plot controllers
# ============================================================

for control in controls:

    df = summary[control]

    delta_cost = (
        df['cost'] -
        df_thermo['cost']
    )

    ax.plot(
        df['penetration'],
        delta_cost,
        color=colours[control],
        linestyle=line_styles[control],
        marker=marker_styles[control],
        linewidth=2,
        markersize=7,
        alpha=0.8,
        label=control_label[control]
    )


# ============================================================
# Baseline reference
# ============================================================

ax.axhline(
    0,
    color=colours['thermo'],
    linestyle='--',
    linewidth=1.5,
    alpha=0.8
)


# ============================================================
# Formatting
# ============================================================

ax.set_xlabel(
    'Penetration (%)',
    fontsize=19
)

ax.set_ylabel(
    r'$\Delta C_{elec}$ (\$/day)',
    
    fontsize=19
)

ax.set_xticks(
    [0, 20, 40, 60, 80, 100]
)

ax.tick_params(
    axis='both',
    labelsize=16
)

ax.grid(
    alpha=0.5
)

ax.set_box_aspect(
    4.5 / 6
)


# ============================================================
# Legend
# ============================================================

ax.legend(
    fontsize=16,
    loc='upper center',
    bbox_to_anchor=(0.5, -0.20),
    ncol=2,
    frameon=False
)


# ============================================================
# Figure spacing
# ============================================================

fig.subplots_adjust(
    bottom=0.30
)


# ============================================================
# Save
# ============================================================

plt.savefig(
    out_pth +
    '/household metric plots/electricity_cost_penetration.pdf',
    bbox_inches='tight'
)

plt.show()

































# -----------------------------------------------------
# Plotting household energy and electricity cost vs penetration combined
# -----------------------------------------------------

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np


# ============================================================
# Setup
# ============================================================

df_thermo = summary['thermo']

controls = [
    'price_rand',
    'current',
    'voltage_prob'
]

fig, axs = plt.subplots(
    2, 2,
    figsize=(11.2, 8),
    sharex=True
)

ax_on = axs[0, 0]
ax_off = axs[0, 1]
ax_total = axs[1, 0]
ax_cost = axs[1, 1]


# ============================================================
# Plot controllers
# ============================================================

for control in controls:

    df = summary[control]

    # Changes relative to baseline
    delta_on = df['E_on'] - df_thermo['E_on']
    delta_off = df['E_off'] - df_thermo['E_off']
    delta_total = delta_on + delta_off
    delta_cost = df['cost'] - df_thermo['cost']

    # On-peak energy
    ax_on.plot(
        df['penetration'],
        delta_on,
        color=colours[control],
        linestyle=line_styles[control],
        marker=marker_styles[control],
        linewidth=2,
        markersize=7,
        alpha=0.8
    )

    # Off-peak energy
    ax_off.plot(
        df['penetration'],
        delta_off,
        color=colours[control],
        linestyle=line_styles[control],
        marker=marker_styles[control],
        linewidth=2,
        markersize=7,
        alpha=0.8
    )

    # Total energy
    ax_total.plot(
        df['penetration'],
        delta_total,
        color=colours[control],
        linestyle=line_styles[control],
        marker=marker_styles[control],
        linewidth=2,
        markersize=7,
        alpha=0.8
    )

    # Electricity cost
    ax_cost.plot(
        df['penetration'],
        delta_cost,
        color=colours[control],
        linestyle=line_styles[control],
        marker=marker_styles[control],
        linewidth=2,
        markersize=7,
        alpha=0.8
    )


# ============================================================
# Plot formatting
# ============================================================

plot_axes = [
    ax_on,
    ax_off,
    ax_total,
    ax_cost
]

for ax in plot_axes:

    # Baseline reference
    ax.axhline(
        0,
        color=colours['thermo'],
        linestyle='--',
        linewidth=1.5,
        alpha=0.8
    )

    ax.grid(alpha=0.5)

    ax.tick_params(
        axis='both',
        labelsize=16
    )

    ax.set_xticks(
        [0, 20, 40, 60, 80, 100]
    )

    ax.set_box_aspect(
        4.5 / 6
    )

    ax.set_xlabel(
        'Penetration (%)',
        fontsize=19
    )


# Show x tick labels on upper plots
ax_on.tick_params(
    axis='x',
    labelbottom=True
)

ax_off.tick_params(
    axis='x',
    labelbottom=True
)


# ============================================================
# Y-axis labels
# ============================================================

ax_on.set_ylabel(
    r'$\Delta E_{On}$ (kWh/day)',
    fontsize=19
)

ax_off.set_ylabel(
    r'$\Delta E_{Off}$ (kWh/day)',
    fontsize=19
)

ax_total.set_ylabel(
    r'$\Delta E_{Total}$ (kWh/day)',
    fontsize=19
)

ax_cost.set_ylabel(
    r'$\Delta C_{elec}$ (\$/day)',
    fontsize=19
)


# ============================================================
# Panel labels
# ============================================================

panel_labels = ['(a)', '(b)', '(c)', '(d)']

for ax, label in zip(plot_axes, panel_labels):

    ax.text(
        0.03,
        0.97,
        label,
        transform=ax.transAxes,
        fontsize=19,
        fontweight='bold',
        va='top',
        ha='left'
    )


# ============================================================
# Y limits
# ============================================================

ax_on.set_ylim(-2.8, 0.5)


# ============================================================
# Common legend
# ============================================================

control_handles = [
    Line2D(
        [0], [0],
        color=colours[control],
        linestyle=line_styles[control],
        marker=marker_styles[control],
        linewidth=2,
        markersize=7,
        label=control_label[control]
    )
    for control in controls
]

fig.legend(
    handles=control_handles,
    loc='lower center',
    bbox_to_anchor=(0.5, -0.05),
    ncol=3,
    fontsize=17,
    frameon=False
)


# ============================================================
# Figure spacing
# ============================================================

fig.subplots_adjust(
    left=0.10,
    right=0.98,
    bottom=0.16,
    top=0.98,
    hspace=0.30,
    wspace=0.05
)


# ============================================================
# Save
# ============================================================

plt.savefig(
    out_pth +
    '/household metric plots/energy_cost_penetration.pdf',
    bbox_inches='tight'
)

plt.show()