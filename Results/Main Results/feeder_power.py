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

out_pth = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\feeder power"

data_pth =  rf"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Individual results nz"


plt.rcParams['font.family'] = 'Times New Roman'

# -----------------------------
# Load results
# -----------------------------

controls = ['thermo', 'price', 'price_rand', 'current','voltage', 'voltage_prob']
penetrations = [0,50,60,80,100]

results, trial = load_results.load_results(controls, penetrations)

time_vector = np.arange(0,1440,1)
time_hours = time_vector/60
time_of_day = np.array([
    f"{m//60:02d}:{m%60:02d}"
    for m in time_vector
])

with open(r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Initial nz\control_signals.dat', 'rb') as f:
    Ctrl_sigs = pickle.load(f)
Ctrl_sigs.keys()


# -----------------------------
# Distribution dataframe
# -----------------------------

calculate_distributions = True
distribution_penetrations = [60]

if calculate_distributions == True:
    distribution_df = {}

    # Controlled cases
    for control in controls:
        distribution_df[control] = {}

        for p in distribution_penetrations:
            if control == 'thermo':
                P_flat = results['thermo'][0]['P_sum'].flatten()
            else:
                P_flat = results[control][p]['P_sum'].flatten()
            kde = gaussian_kde(P_flat)
            x = np.linspace(P_flat.min(), P_flat.max(), 500)
            pdf = kde(x)

            distribution_df[control][p] = pd.DataFrame({
                'pdf': pdf,
                'x': x
            })

    distribution_df.keys()















#-------------------------------------------
# Feeder Power Subplot
#----------------------------------------------

profiles_to_plot = ['price', 'current'] #, 'voltage']
penetration_to_plot = {'price': 60,
                       'current': 60,
                       'voltage': 60,
                       'voltage_prob': 60}

profile_control_label = {
    "thermo": "Baseline",
    "price": "Price Control\n(Origional)",
    "price_rand": "Price Control\n(Randomised)",
    "current": "Current Control",
    "voltage": "Voltage\nControl (Origional)",
    "voltage_prob": "Voltage\nControl (Probabilistic)"
}

# ============================================================
# Feeder active power profile comparison
# ============================================================

panel_labels = {
    'price': '(a)',
    'current': '(b)'
}

fig, axs = plt.subplots(
    1, 2,
    figsize=(10, 8),
    sharex=True,
    sharey=True
)

ax1, ax2 = axs


for ax, control in zip(axs, profiles_to_plot):

    p = penetration_to_plot[control]


    # --------------------------------------------------------
    # Baseline
    # --------------------------------------------------------

    P_baseline = np.mean(
        results['thermo'][0]['P_sum'],
        axis=1
    )

    ax.plot(
        time_hours,
        P_baseline,
        label=profile_control_label['thermo'],
        color=colours['thermo'],
        linestyle='--',
        linewidth=2,
        alpha=0.8
    )


    # --------------------------------------------------------
    # Main controller
    # --------------------------------------------------------

    P_control = np.mean(
        results[control][p]['P_sum'],
        axis=1
    )

    ax.plot(
        time_hours,
        P_control,
        label=profile_control_label[control],
        color=colours[control],
        linestyle='-',
        linewidth=2,
        alpha=0.8
    )


    # --------------------------------------------------------
    # Additional comparison controllers
    # --------------------------------------------------------

    if control == 'price':

        P_price_rand = np.mean(
            results['price_rand'][p]['P_sum'],
            axis=1
        )

        ax.plot(
            time_hours,
            P_price_rand,
            label=profile_control_label['price_rand'],
            color=colours['price_rand'],
            linestyle=line_styles['price_rand'],
            linewidth=2,
            alpha=0.8
        )


    if control == 'current':

        P_voltage = np.mean(
            results['voltage'][p]['P_sum'],
            axis=1
        )

        P_voltage_prob = np.mean(
            results['voltage_prob'][p]['P_sum'],
            axis=1
        )

        ax.plot(
            time_hours,
            P_voltage,
            label=profile_control_label['voltage'],
            color=colours['voltage'],
            linestyle='-',
            linewidth=2,
            alpha=0.8
        )

        ax.plot(
            time_hours,
            P_voltage_prob,
            label=profile_control_label['voltage_prob'],
            color=colours['voltage_prob'],
            linestyle=line_styles['voltage_prob'],
            linewidth=2,
            alpha=0.8
        )


    # --------------------------------------------------------
    # Formatting
    # --------------------------------------------------------

    ax.set_xlabel(
        'Hour of Day',
        fontsize=19
    )

    ax.tick_params(
        axis='both',
        labelsize=16
    )

    ax.grid(
        axis='y',
        alpha=0.5
    )

    ax.set_xlim(0, 24)

    ax.set_box_aspect(4.5 / 6)


    # Panel label
    ax.text(
        0.03, 0.97,
        panel_labels[control],
        transform=ax.transAxes,
        fontsize=19,
        fontweight='bold',
        va='top',
        ha='left'
    )


# ============================================================
# Shared y-axis formatting
# ============================================================

ax1.set_ylabel(
    'Feeder Active Power (kW)',
    fontsize=19
)

ax2.tick_params(
    axis='y',
    labelleft=False
)


# ============================================================
# Combined legend
# ============================================================

handles = []
labels = []

for ax in axs:
    h, l = ax.get_legend_handles_labels()
    handles.extend(h)
    labels.extend(l)

# Remove duplicate entries while preserving order
by_label = dict(zip(labels, handles))

fig.legend(
    by_label.values(),
    by_label.keys(),
    loc='lower center',
    bbox_to_anchor=(0.5, -0.08),
    ncol=3,
    fontsize=16,
    frameon=False
)


# ============================================================
# Figure spacing
# ============================================================

fig.subplots_adjust(
    bottom=-0.15,
    left=0.11,
    right=0.98,
    wspace=0.08
)


# ============================================================
# Save
# ============================================================

plt.savefig(
    out_pth +
    '/feeder power plots/control_feeder_power_profiles_combined.pdf',
    bbox_inches='tight'
)

plt.show()



















# ---------------------------------------------------
# Distribution of price rand and voltage probablistic
# ----------------------------------------------------

from matplotlib.lines import Line2D

controls = ['price_rand', 'voltage_prob']

dist_p_to_plot = 60

fig, ax = plt.subplots(figsize=(8, 4))

# Baseline distribution
ax.plot(distribution_df['thermo'][dist_p_to_plot]['x'],distribution_df['thermo'][dist_p_to_plot]['pdf'],color=colours['thermo'],linestyle='--')

# Baseline 95th percentile
ax.axvline(np.percentile(results['thermo'][0]['P_sum'], 95),color=colours['thermo'],linestyle=':',linewidth=2)

# baseline max
ax.scatter(distribution_df['thermo'][dist_p_to_plot]['x'].max(),0,color=colours['thermo'],s=60,zorder=5, marker=marker_styles['thermo'], alpha=0.8)

# Controlled distributions
for control in controls:
    ax.plot(
        distribution_df[control][dist_p_to_plot]['x'],
        distribution_df[control][dist_p_to_plot]['pdf'],
        color=colours[control],
        linestyle='-')

    ax.axvline(
        np.percentile(results[control][dist_p_to_plot]['P_sum'], 95),
        color=colours[control],
        linestyle=':',
        linewidth=2)

    ax.scatter(distribution_df[control][dist_p_to_plot]['x'].max(),0,color=colours[control],s=60,zorder=5, marker=marker_styles[control], alpha=0.8)


# --------------------------------
# Legend 1: Controller / colour
# --------------------------------

control_handles = [
    Line2D([0], [0],
           color=colours['thermo'],
           linewidth=2,
           label=control_label['thermo'],
           linestyle='--',
           marker=marker_styles['thermo']),

    Line2D([0], [0],
           color=colours['price_rand'],
           linewidth=2,
           label=control_label['price_rand'],
           marker=marker_styles['price_rand']),

    Line2D([0], [0],
           color=colours['voltage_prob'],
           linewidth=2,
           label=control_label['voltage_prob'],
           marker=marker_styles['voltage_prob']),
]

legend1 = ax.legend(
    handles=control_handles,
    loc='center right',
    bbox_to_anchor=(1.6,0.5),
    ncol=1,
    fontsize=16,
    frameon=False
)

ax.set_xlabel('Feeder Active Power (kW)', fontsize=19)
ax.set_ylabel('Probability Density', fontsize=19)

ax.set_box_aspect(4.5 / 6)

ax.grid(True)
ax.tick_params(axis='both', labelsize=16)

plt.tight_layout()

plt.savefig(
    out_pth + '/feeder power plots/feeder_power_distribution_comparison.pdf',
    bbox_inches='tight'
)

plt.show()





