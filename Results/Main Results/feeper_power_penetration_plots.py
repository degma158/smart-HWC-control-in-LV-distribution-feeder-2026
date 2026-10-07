
import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import sys
import os

sys.path.append(r"C:\Users\Max de Groot\Git\Honours-Project-2026\Results")
os.chdir(r"C:\Users\Max de Groot\Git\Honours-Project-2026\Results")

import load_results

from plotting_customisation import colours, control_label, marker_styles, line_styles

out_pths = {"feeder power": rf"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\feeder power",
            "household voltage": rf"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\household voltage\penetration plots",
            "household metrics":  rf"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\household metrics\penetration plots"
}

# -----------------------------
# Load results
# -----------------------------

controls = ['thermo', 'price_rand', 'current','voltage', 'voltage_prob']
penetrations = [0,20,40,60,80,100]

results, trial = load_results.load_results(controls, penetrations)

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Times New Roman'
plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
plt.rcParams['mathtext.bf'] = 'Times New Roman:bold'


# --------------------------------------------------
# Penetration data frame
# --------------------------------------------------

results['thermo'][0].keys()

summary = {}

for control in controls:
    summary[control] = []
    for p in penetrations:
        if p == 0:
            P_sum = results['thermo'][0]['P_sum']
        else:
            P_sum = results[control][p]['P_sum']

        # P_95th_day = np.percentile(P_sum, 95, axis=0)
        P_std_day = np.std(P_sum, axis=0)     

        # P_sum_95th = np.mean(P_95th_day)
        P_sum_std = np.mean(P_std_day)

        P_sum_95th = np.percentile(P_sum, 95)

        summary[control].append({
            'Penetration': p,
            'P_sum_95th': P_sum_95th,
            'P_sum_std': P_sum_std
        })

    summary[control] = pd.DataFrame(summary[control])





















# -----------------------------------------------------------------------
# Plots
# -----------------------------------------------------------------------

pen_control_label = {
    "thermo": "Baseline",
    "price": "Price Control\n(Origional)",
    "price_rand": "Price Control\n(Randomised)",
    "current": "Current\nControl",
    "voltage": "Voltage Control\n(Origional)",
    "voltage_prob": "Voltage Control\n(Probabilistic)"
}

metrics = ['P_sum_95th'] #, 'P_sum_std']

y_label = {'P_sum_95th': r'$\Delta P_{95\mathrm{th}}$ (%)', #'Change in 95th Percentile Feeder Power (kW)', 
           'P_sum_std': 'Change in Feeder Power Standard Deviation (kW)'}

thermo = summary["thermo"]

for metric in metrics:

    fig, ax = plt.subplots(
        figsize=(8, 4)
    )

    # --------------------------------------------------------
    # Controllers
    # --------------------------------------------------------

    for control in controls:

        if control != 'thermo':

            df = summary[control]

            delta_metric = (
                100 *
                (df[metric] - thermo[metric]) /
                thermo[metric]
            )

            ax.plot(
                df['Penetration'],
                delta_metric,
                label=pen_control_label[control],
                color=colours[control],
                linestyle=line_styles[control],
                marker=marker_styles[control],
                linewidth=2,
                markersize=7,
                alpha=0.8
            )


    # --------------------------------------------------------
    # Baseline reference
    # --------------------------------------------------------

    ax.axhline(
        y=0,
        color=colours['thermo'],
        linestyle='--',
        linewidth=1.5,
        alpha=0.8
    )


    # --------------------------------------------------------
    # Formatting
    # --------------------------------------------------------

    ax.set_xlabel(
        'Penetration (%)',
        fontsize=19
    )

    ax.set_ylabel(
        y_label[metric],
        fontsize=19
    )

    ax.tick_params(
        axis='both',
        labelsize=16
    )

    ax.set_box_aspect(4.5 / 6)

    ax.grid(
        alpha=0.5
    )


    # --------------------------------------------------------
    # Legend
    # --------------------------------------------------------

    ax.legend(
        fontsize=16,
        loc='center right',
        bbox_to_anchor=(1.6,0.5),
        ncol=1,
        frameon=False
    )


    # --------------------------------------------------------
    # Figure spacing
    # --------------------------------------------------------


    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    plt.savefig(
        out_pths['feeder power'] +
        f'/feeder power plots/{metric}_vs_penetration.pdf',
        bbox_inches='tight'
    )

    plt.show()











# #-------------------------------------
# # Data table summary
# #-------------------------------------

# summary = {}

# pens = [60,100]

# for control in controls:
#     summary[control] = []
#     if control == 'price':
#         pens = [60]
#     else:
#         pens = [60,100]
#     for p in pens:
#         summary[control][p] = {}
#         if p == 0:
#             P_sum = results['thermo'][0]['P_sum']
#         else:
#             P_sum = results[control][p]['P_sum']

#         P_sum_95th = np.percentile(P_sum, 95)

#         summary[control][p].append({
#             'P_sum_95th': P_sum_95th,
#         })

#     summary[control] = pd.DataFrame(summary[control])




# #---------------------------------------------------
# # Data table
# #---------------------------------------------------
# pens = [60,100]

# summary['thermo'].keys()

# for p in pens:
#     P_95th_base = summary['thermo'][p]['P_sum_95th']
#     for control in controls:
#         P_95th = summary[control][p]['P_sum_95th']
#         delta_P_95th = 100*(P_95th-P_95th_base)/P_95th_base

#         print(f'{p}% {control}:')
#         print(f'P 95th = {P_95th} kW')
#         print(f'delta P 95th = {delta_P_95th} %')
       

