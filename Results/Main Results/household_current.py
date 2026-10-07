import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import sys
import os

sys.path.append(r"C:\Users\Max de Groot\Git\Honours-Project-2026\My Code")
os.chdir(r"C:\Users\Max de Groot\Git\Honours-Project-2026\My Code")

import load_results

from scipy.stats import gaussian_kde

from plotting_customisation import colours, control_label, marker_styles, line_styles

out_pth = rf"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\household current"

# -----------------------------
# Load results
# -----------------------------

# Simulation results
controls = ['thermo', 'price', 'price_rand', 'current','voltage', 'voltage_prob']
penetrations = [0,50,60,80,100]
results, trial = load_results.load_results(controls, penetrations)

#------------------------------
# Plotting customization
#------------------------------

time_minutes = np.arange(0,1440,1)
time_hours = time_minutes/60

plt.rcParams['font.family'] = 'Times New Roman'


# -----------------------------
# Whole dataset distribution dataframe
# -----------------------------

calculate_distributions = True
distribution_penetrations = [60]
distribution_controls = ['thermo', 'price_rand', 'current', 'voltage_prob'] #['thermo', 'price', 'price_rand', 'current','voltage', 'voltage_prob']

if calculate_distributions == True:
    distribution_df = {}

    # Controlled cases
    for control in distribution_controls:
        distribution_df[control] = {}

        for p in distribution_penetrations:
            V_flat = results[control][p]['I_house'].flatten()
            kde = gaussian_kde(V_flat)
            x = np.linspace(V_flat.min(), V_flat.max(), 500)
            pdf = kde(x)

            distribution_df[control][p] = pd.DataFrame({
                'pdf': pdf,
                'x': x
            })

    distribution_df.keys()













# ============================================================
# Household current distributions
# ============================================================

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np


distributions_to_plot = [
    'thermo',
    'price_rand',
    'current',
    'voltage_prob'
]

dist_p_to_plot = 60


fig, ax = plt.subplots(
    figsize=(8, 4)
)


# ============================================================
# Plot distributions
# ============================================================

for control in distributions_to_plot:

    # Distribution
    ax.plot(
        distribution_df[control][dist_p_to_plot]['x'],
        distribution_df[control][dist_p_to_plot]['pdf'],
        color=colours[control],
        linestyle='--' if control == 'thermo' else line_styles[control],
        linewidth=2,
        alpha=0.8
    )

    # Actual maximum household current
    I_max = results[control][dist_p_to_plot]['I_house'].max()

    ax.scatter(
        I_max,
        0,
        color=colours[control],
        marker=marker_styles[control],
        s=70,
        zorder=5,
        alpha=0.8
    )

    # 95th percentile household current
    I_95th = np.percentile(
        results[control][dist_p_to_plot]['I_house'],
        95
    )

    ax.axvline(
        I_95th,
        color=colours[control],
        linestyle=':',
        linewidth=2,
        alpha=0.8
    )


# ============================================================
# Legend
# ============================================================

legend_handles = [
    Line2D(
        [0], [0],
        color=colours[control],
        linestyle='--' if control == 'thermo' else line_styles[control],
        marker=marker_styles[control],
        linewidth=2,
        markersize=7,
        label=control_label[control]
    )
    for control in distributions_to_plot
]

ax.legend(
    handles=legend_handles,
    loc='center right',
    bbox_to_anchor=(1.6,0.5),
    ncol=1,
    fontsize=16,
    frameon=False
)


# ============================================================
# Formatting
# ============================================================

ax.set_xlabel(
    'Household Current (A)',
    fontsize=19
)

ax.set_ylabel(
    'Probability Density',
    fontsize=19
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
# Save
# ============================================================

plt.savefig(
    r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\household metrics\household metric plots\household_current_distribution.pdf',
    bbox_inches='tight'
)

plt.show()
