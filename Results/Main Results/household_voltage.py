import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import sys
import os

sys.path.append(r"C:\Users\Max de Groot\Git\Honours-Project-2026\Results")
os.chdir(r"C:\Users\Max de Groot\Git\Honours-Project-2026\Results")

import load_results

from scipy.stats import gaussian_kde

out_pth = rf"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\household voltage"

# -----------------------------
# Load results
# -----------------------------
load_data = True

# Simulation results
controls = ['thermo', 'price', 'price_rand', 'current','voltage', 'voltage_prob']
penetrations = [0,20,40,50,60,80,100]

if load_data == True:
    results, trial = load_results.load_results(controls, penetrations)

    # Feeder spatial information
    load_distance = pd.read_csv(r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\load_distance.csv")

#------------------------------
# Plotting customization
#------------------------------

time_minutes = np.arange(0,1440,1)
time_hours = time_minutes/60

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Times New Roman'
plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
plt.rcParams['mathtext.bf'] = 'Times New Roman:bold'

from plotting_customisation import colours, control_label, marker_styles, line_styles


# -----------------------------
# Whole dataset distribution dataframe
# -----------------------------

calculate_distributions = False
distribution_penetrations = [60]
distribution_controls = ['thermo', 'price_rand', 'current', 'voltage_prob'] #['thermo', 'price', 'price_rand', 'current','voltage', 'voltage_prob']

if calculate_distributions == True:
    distribution_df = {}

    # Controlled cases
    for control in distribution_controls:
        distribution_df[control] = {}

        for p in distribution_penetrations:
            V_flat = results[control][p]['V_house'].flatten()
            kde = gaussian_kde(V_flat)
            x = np.linspace(V_flat.min(), V_flat.max(), 500)
            pdf = kde(x)

            distribution_df[control][p] = pd.DataFrame({
                'pdf': pdf,
                'x': x
            })

    distribution_df.keys()


#-------------------------------------------
# Avg distribution across houses
#-------------------------------------------

calculate_indv_distributions = False
indv_distribution_penetrations = [60]
indv_distribution_controls = ['thermo','voltage_prob', 'current', 'price_rand', 'voltage']
indv_distribution_houses = [0,20,54] # refine to pick 3 houses (use house 0 as start and house 54 as end)

house_styles = {
    indv_distribution_houses[0]:  '-',
    indv_distribution_houses[1]: '--',
    indv_distribution_houses[2]: ':'
}

if calculate_indv_distributions == True:
    indv_distribution_df = {}

    # Controlled cases
    for control in indv_distribution_controls:
        indv_distribution_df[control] = {}

        for h in indv_distribution_houses:
            indv_distribution_df[control][h] = {}

            for p in indv_distribution_penetrations:

                V_flat = results[control][p]['V_house'][:,h,:].flatten()
                kde = gaussian_kde(V_flat)
                x = np.linspace(V_flat.min(), V_flat.max(), 500)
                pdf = kde(x)

                indv_distribution_df[control][h][p] = pd.DataFrame({
                    'pdf': pdf,
                    'x': x
                })

    indv_distribution_df.keys()
    indv_distribution_df[indv_distribution_controls[0]].keys()
    indv_distribution_df[indv_distribution_controls[0]][indv_distribution_houses[0]].keys()













# -------------------------------------------------
# Profiles sub plot
# --------------------------------------------------
profiles_to_plot = ['price', 'current']

penetration_to_plot = {
    'price': 60,
    'current': 60,
    'voltage': 60,
    'voltage_prob': 100
}

panel_labels = {
    'price': '(a)',
    'current': '(b)'
}


# ============================================================
# Household voltage profile comparison
# ============================================================

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

    V_baseline = np.mean(
        np.mean(
            results['thermo'][0]['V_house'],
            axis=1
        ),
        axis=1
    )

    ax.plot(
        time_hours,
        V_baseline,
        label=control_label['thermo'],
        color=colours['thermo'],
        linestyle='--',
        linewidth=2,
        alpha=0.8
    )


    # --------------------------------------------------------
    # Main controller
    # --------------------------------------------------------

    V_control = np.mean(
        np.mean(
            results[control][p]['V_house'],
            axis=1
        ),
        axis=1
    )

    ax.plot(
        time_hours,
        V_control,
        label=control_label[control],
        color=colours[control],
        linestyle='-',
        linewidth=2,
        alpha=0.8
    )


    # --------------------------------------------------------
    # Additional comparison controllers
    # --------------------------------------------------------

    if control == 'price':

        V_price_rand = np.mean(
            np.mean(
                results['price_rand'][p]['V_house'],
                axis=1
            ),
            axis=1
        )

        ax.plot(
            time_hours,
            V_price_rand,
            label=control_label['price_rand'],
            color=colours['price_rand'],
            linestyle=line_styles['price_rand'],
            linewidth=2,
            alpha=0.8
        )


    if control == 'current':

        V_voltage = np.mean(
            np.mean(
                results['voltage'][p]['V_house'],
                axis=1
            ),
            axis=1
        )

        V_voltage_prob = np.mean(
            np.mean(
                results['voltage_prob'][p]['V_house'],
                axis=1
            ),
            axis=1
        )

        ax.plot(
            time_hours,
            V_voltage,
            label=control_label['voltage'],
            color=colours['voltage'],
            linestyle='-',
            linewidth=2,
            alpha=0.8
        )

        ax.plot(
            time_hours,
            V_voltage_prob,
            label=control_label['voltage_prob'],
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
    ax.set_ylim(233,243)

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


# Only one y-axis label
ax1.set_ylabel(
    'Household Voltage (V)',
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

# Remove duplicates while retaining order
by_label = dict(zip(labels, handles))

fig.legend(
    by_label.values(),
    by_label.keys(),
    loc='lower center',
    bbox_to_anchor=(0.5, -0.10),
    ncol=3,
    fontsize=16,
    frameon=False
)


# ============================================================
# Figure spacing
# ============================================================

fig.subplots_adjust(
    bottom=-0.2,
    left=0.11,
    right=0.98,
    wspace=0.08
)


# ============================================================
# Save
# ============================================================

plt.savefig(
    out_pth +
    '/household voltage plots/profile comparison.pdf',
    bbox_inches='tight'
)

plt.show()























from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np


# ============================================================
# SETTINGS
# ============================================================

p_to_plot = 60

overall_controls = [
    'thermo',
    'price_rand',
    'voltage_prob'
]

control = 'voltage_prob'

house_labels = {
    0: 'A',
    20: 'B',
    54: 'C'
}

house_marker = {
    0: '^',
    20: '*',
    54: 'v'
}


# ============================================================
# FIGURE 1
# Overall + individual household voltage distributions
# ============================================================

fig, axs = plt.subplots(
    1, 2,
    figsize=(12, 8)
)

ax1, ax2 = axs


# ------------------------------------------------------------
# (a) Overall household voltage distributions
# ------------------------------------------------------------

for ctrl in overall_controls:

    # Distribution
    if ctrl == 'thermo':
        ax1.plot(
            distribution_df[ctrl][p_to_plot]['x'],
            distribution_df[ctrl][p_to_plot]['pdf'],
            color=colours[ctrl],
            linestyle='--',
            linewidth=2,
            alpha=0.8
        )
    else:
        ax1.plot(
            distribution_df[ctrl][p_to_plot]['x'],
            distribution_df[ctrl][p_to_plot]['pdf'],
            color=colours[ctrl],
            linestyle=line_styles[ctrl],
            linewidth=2,
            alpha=0.8
        )

    # Actual minimum voltage
    V_min = results[ctrl][p_to_plot]['V_house'].min()

    ax1.scatter(
        V_min,
        0,
        color=colours[ctrl],
        marker=marker_styles[ctrl],
        s=70,
        zorder=5,
        alpha=0.8
    )

    # 5th percentile
    V_5th = np.percentile(
        results[ctrl][p_to_plot]['V_house'],
        5
    )

    ax1.axvline(
        V_5th,
        color=colours[ctrl],
        linestyle=':',
        linewidth=2,
        alpha=0.8
    )


# Voltage limits
ax1.axvline(
    207.8,
    color='red',
    linestyle='--',
    linewidth=2
)

ax1.axvline(
    254,
    color='red',
    linestyle='--',
    linewidth=2
)


# Legend
overall_handles = [
    Line2D(
        [0], [0],
        color=colours[ctrl],
        linestyle='--' if ctrl == 'thermo' else line_styles[ctrl],
        marker=marker_styles[ctrl],
        linewidth=2,
        markersize=7,
        label=control_label[ctrl]
    )
    for ctrl in overall_controls
]

overall_handles += [
    Line2D(
        [0], [0],
        color='red',
        linestyle='--',
        linewidth=2,
        label='Voltage Limits'
    )
]

ax1.legend(
    handles=overall_handles,
    fontsize=16,
    loc='upper center',
    bbox_to_anchor=(0.5, -0.20),
    ncol=1,
    frameon=False
)


ax1.set_xlabel(
    'Household Voltage (V)',
    fontsize=19
)

ax1.set_ylabel(
    'Probability Density',
    fontsize=19
)

ax1.set_xlim(206.8, 255)
ax1.set_ylim(-0.05, 0.9)

ax1.tick_params(
    axis='both',
    labelsize=16
)

ax1.grid(alpha=0.5)

ax1.text(
    0.03, 0.97,
    '(a)',
    transform=ax1.transAxes,
    fontsize=19,
    fontweight='bold',
    va='top',
    ha='left'
)


# ------------------------------------------------------------
# (b) Individual household voltage distributions
# ------------------------------------------------------------

for h in indv_distribution_houses:

    # Baseline
    ax2.plot(
        indv_distribution_df['thermo'][h][p_to_plot]['x'],
        indv_distribution_df['thermo'][h][p_to_plot]['pdf'],
        color=colours['thermo'],
        linestyle=house_styles[h],
        linewidth=2,
        alpha=0.8
    )

    # Voltage control
    ax2.plot(
        indv_distribution_df[control][h][p_to_plot]['x'],
        indv_distribution_df[control][h][p_to_plot]['pdf'],
        color=colours[control],
        linestyle=house_styles[h],
        linewidth=2,
        alpha=0.8
    )

    # Baseline minimum
    ax2.scatter(
        results['thermo'][p_to_plot]['V_house'][:, h, :].min(),
        0,
        color=colours['thermo'],
        marker=house_marker[h],
        s=80,
        zorder=5
    )

    # Controlled minimum
    ax2.scatter(
        results[control][p_to_plot]['V_house'][:, h, :].min(),
        0,
        color=colours[control],
        marker=house_marker[h],
        s=80,
        zorder=5
    )


# Legend
individual_handles = []

for h in indv_distribution_houses:

    individual_handles.append(
        Line2D(
            [0], [0],
            color=colours['thermo'],
            linestyle=house_styles[h],
            marker=house_marker[h],
            linewidth=2,
            markersize=7,
            label=f'House {house_labels[h]} Baseline'
        )
    )

    individual_handles.append(
        Line2D(
            [0], [0],
            color=colours[control],
            linestyle=house_styles[h],
            marker=house_marker[h],
            linewidth=2,
            markersize=7,
            label=f'House {house_labels[h]} Controlled'
        )
    )


ax2.legend(handles=individual_handles,
    fontsize=16,
    loc='upper center',
    bbox_to_anchor=(0.5, -0.20),
    ncol=1,
    frameon=False
)


ax2.set_xlabel('Household Voltage (V)',fontsize=19)

# Same y quantity as panel (a)
ax2.tick_params(axis='both',labelsize=16,labelleft=False)

ax2.tick_params(axis='y', labelleft=False)

ax2.set_xlim(206.8, 255)
ax2.set_ylim(-0.05, 0.9)

ax2.grid(alpha=0.5)

ax2.text(
    0.03, 0.97,
    '(b)',
    transform=ax2.transAxes,
    fontsize=19,
    fontweight='bold',
    va='top',
    ha='left'
)

# ------------------------------------------------------------
# Formatting
# ------------------------------------------------------------

ax1.set_box_aspect(4.5 / 6)
ax2.set_box_aspect(4.5 / 6)

fig.subplots_adjust(wspace=0.08,bottom=0.3)

plt.savefig(
    out_pth +
    '/household voltage plots/overall_individual_voltage_distribution_subplot.pdf',
    bbox_inches='tight'
)

plt.show()

















# ============================================================
# FIGURE 2
# 5th percentile voltage vs feeder distance
# ============================================================

V_thermo = np.percentile(
    results['thermo'][p_to_plot]['V_house'],
    5,
    axis=(0, 2)
)

V_control = np.percentile(
    results[control][p_to_plot]['V_house'],
    5,
    axis=(0, 2)
)


fig, ax = plt.subplots(
    figsize=(8, 4)
)


# ------------------------------------------------------------
# Data points
# ------------------------------------------------------------

ax.scatter(
    load_distance['Distance'],
    V_thermo,
    color=colours['thermo'],
    alpha=0.8,
    s=60,
    marker=marker_styles['thermo']
)

ax.scatter(
    load_distance['Distance'],
    V_control,
    color=colours[control],
    alpha=0.8,
    s=60,
    marker=marker_styles[control]
)


# ------------------------------------------------------------
# Trend lines
# ------------------------------------------------------------

fit_handles = []

for V, ctrl_key in [
    (V_thermo, 'thermo'),
    (V_control, control)
]:

    slope, intercept = np.polyfit(
        load_distance['Distance'],
        V,
        1
    )

    x_fit = np.linspace(
        load_distance['Distance'].min(),
        load_distance['Distance'].max(),
        100
    )

    y_fit = slope * x_fit + intercept

    ax.plot(
        x_fit,
        y_fit,
        color=colours[ctrl_key],
        linestyle='--',
        linewidth=2,
        alpha=0.8
    )

    fit_handles.append(
        Line2D(
            [0], [0],
            color=colours[ctrl_key],
            linestyle='--',
            marker=marker_styles[ctrl_key],
            linewidth=2,
            markersize=7,
            label=(
                f'{control_label[ctrl_key]}:\n'
                f'Slope = {slope:.1f} V/km'
            )
        )
    )


# ------------------------------------------------------------
# Legend
# ------------------------------------------------------------

ax.legend(
    handles=fit_handles,
    loc='center right',
    bbox_to_anchor=(1.65,0.5),
    ncol=1,
    fontsize=16,
    frameon=False
)


# ------------------------------------------------------------
# Formatting
# ------------------------------------------------------------

ax.set_xlabel(
    'Distance from Feeder Source (km)',
    fontsize=19
)

ax.set_ylabel(
    r'$V_{5\mathrm{th}}$ (V)',
    fontsize=19
)

ax.tick_params(
    axis='both',
    labelsize=16
)

ax.grid(alpha=0.25)

ax.set_box_aspect(4.5 / 6)


plt.savefig(
    out_pth +
    '/household voltage plots/voltage_drop_voltage_control.pdf',
    bbox_inches='tight'
)

plt.show()



























# ------------------------------------------------------------------------
# Overal summary for penetration plot
# ------------------------------------------------------------------------

p_plot_penetrations = [0,20,40,60,80,100]
p_plot_controls = ['thermo','price_rand', 'current', 'voltage', 'voltage_prob']

summary_overall = {}
for control in p_plot_controls:
    summary_overall[control] = {}

    for p in p_plot_penetrations:

        summary_overall[control][p] = {}
        
        if p == 0:
            V = results['thermo'][0]['V_house']
        else:
            V = results[control][p]['V_house']
        

        count_below = np.sum(V < 207.8)
        V_5th_house = np.percentile(V, 5)

        summary_overall[control][p]['V_5th_house'] = V_5th_house
        summary_overall[control][p]['count_below'] = count_below

# ------------------------------------------------------------------------
# Indiv house summary for penetration plot
# ------------------------------------------------------------------------

indv_houses = [0,20,54] #indv_distribution_houses,

house_colours = [
    '#0072B2',  # blue
    '#E69F00',  # orange
    '#009E73',  # green
]

p_plot_penetrations = [0,20,40,60,80,100]
p_plot_controls = ['thermo','price_rand', 'current', 'voltage', 'voltage_prob']

summary_indv = {}
for control in p_plot_controls:
    summary_indv[control] = {}

    for h in indv_houses:
        summary_indv[control][h] = {}

        for p in p_plot_penetrations:
            
            if p == 0:
                V_5th_house = np.percentile(results['thermo'][0]['V_house'], 5, axis=(0,2))[h]
            else:
                V_5th_house = np.percentile(results[control][p]['V_house'], 5, axis=(0,2))[h]

            summary_indv[control][h][p] = V_5th_house

    summary_indv.keys()


pen_plot_control_label = {
    "thermo": "Baseline",
    "price": "Price Control\n(Origional)",
    "price_rand": "Price Control\n(Randomised)",
    "current": "Current\nControl",
    "voltage": "Voltage Control\n(Origional)",
    "voltage_prob": "Voltage Control\n(Probabilistic)"
}

# ------------------------------------------------------------------------
# Combined overall + individual V_5th penetration subplot
# ------------------------------------------------------------------------

fig, axs = plt.subplots(1, 2,figsize=(12, 8),constrained_layout=False)
ax1, ax2 = axs

# ============================================================
# (a) Overall V_5th change
# ============================================================

V_5th_baseline = np.array([summary_overall['thermo'][p]['V_5th_house']
    for p in p_plot_penetrations])

for control in ['price_rand', 'current', 'voltage', 'voltage_prob']:

    V_5th = np.array([summary_overall[control][p]['V_5th_house']
        for p in p_plot_penetrations])

    V_5th_change = 100 * (V_5th - V_5th_baseline) / V_5th_baseline

    ax1.plot(
        p_plot_penetrations,
        V_5th_change,
        label=pen_plot_control_label[control],
        marker=marker_styles[control],
        color=colours[control],
        linestyle=line_styles[control],
        linewidth=2
    )


ax1.axhline(
    0,
    color=colours['thermo'],
    linewidth=1,
    linestyle='--'
)

ax1.set_xlabel('Penetration (%)', fontsize=19)
ax1.set_ylabel(r'$\Delta V_{5\mathrm{th}}$ (%)', fontsize=19)

ax1.tick_params(axis='both', labelsize=16)
ax1.grid(alpha=0.5)

ax1.legend(
    fontsize=16,
    loc='upper center',
    bbox_to_anchor=(0.5, -0.20),
    ncol=1,
    frameon=False
)


# ============================================================
# (b) Individual household V_5th change
# ============================================================

control = 'voltage_prob'

for h in indv_houses:

    V_5th = np.array([summary_indv[control][h][p]
        for p in p_plot_penetrations])

    V_5th_baseline = np.array([summary_indv['thermo'][h][p]
        for p in p_plot_penetrations])

    V_5th_change = 100 * (V_5th - V_5th_baseline) / V_5th_baseline

    ax2.plot(
        p_plot_penetrations,
        V_5th_change,
        label=f'House {house_labels[h]}',
        marker=house_marker[h],
        color=colours[control],
        linestyle=house_styles[h],
        linewidth=2
    )

ax2.axhline(0,color=colours['thermo'],linewidth=1,linestyle='--')

ax2.set_xlabel('Penetration (%)', fontsize=19)
ax2.set_ylabel(r'$\Delta V_{5\mathrm{th}}$ (%)', fontsize=19)

ax2.tick_params(axis='both', labelsize=16)
ax2.grid(alpha=0.25)

ax2.legend(
    fontsize=16,
    loc='upper center',
    bbox_to_anchor=(0.5, -0.20),
    ncol=1,
    frameon=False
)



# ------------------------------------------------
# Axis formatting
# ------------------------------------------------

ax1.set_xlabel('Penetration (%)', fontsize=19)
ax1.set_ylabel(r'$\Delta V_{5\mathrm{th}}$ (%)', fontsize=19)

ax1.tick_params(axis='both', labelsize=16)
ax1.grid(alpha=0.5)

ax2.set_xlabel('Penetration (%)', fontsize=19)

# Remove second subplot y-axis label and tick labels
ax2.set_ylabel('')
ax2.tick_params(
    axis='both',
    labelsize=16,
    labelleft=False
)

ax2.grid(alpha=0.25)


# ------------------------------------------------
# Legends below each subplot
# ------------------------------------------------

ax1.legend(
    fontsize=16,
    loc='upper center',
    bbox_to_anchor=(0.42, -0.20),   # slightly left
    ncol=2,
    frameon=False,
    columnspacing=0.5,
    handletextpad=0.8
)

ax2.legend(
    fontsize=16,
    loc='upper center',
    bbox_to_anchor=(0.58, -0.20),   # slightly right
    ncol=1,
    frameon=False
)


# ------------------------------------------------
# Panel labels in plots
# ------------------------------------------------

ax1.text(
    0.03, 0.97,
    '(a)',
    transform=ax1.transAxes,
    fontsize=19,
    fontweight='bold',
    va='top',
    ha='left'
)

ax2.text(
    0.03, 0.97,
    '(b)',
    transform=ax2.transAxes,
    fontsize=19,
    fontweight='bold',
    va='top',
    ha='left'
)


# ------------------------------------------------
# Limits / proportions
# ------------------------------------------------

ax1.set_ylim(-0.15, 0.7)
ax2.set_ylim(-0.15, 0.7)

ax1.set_box_aspect(4.5 / 6)
ax2.set_box_aspect(4.5 / 6)


fig.subplots_adjust(
    wspace=0.08,   # space between plots
    bottom=0.30    # room for legends
)

for ax in [ax1, ax2]:
    ax.set_xticks([0, 20, 40, 60, 80, 100])

plt.savefig(out_pth + '/household voltage plots/V_5th_penetration_subplot.pdf',
    bbox_inches='tight'
)
plt.show()