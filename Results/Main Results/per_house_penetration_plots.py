# Code for plotting all per-house metrics against control

import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import sys
import os

sys.path.append(r"C:\Users\Max de Groot\Git\Honours-Project-2026\My Code")
os.chdir(r"C:\Users\Max de Groot\Git\Honours-Project-2026\My Code")

import load_results

out_pth = rf"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\penetration plots"

out_pths = {"feeder power": rf"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\feeder power\penetration plots",
            "household voltage": rf"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\household voltage\penetration plots",
            "household metrics":  rf"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\household metrics\penetration plots"
}

# -----------------------------
# Load results
# -----------------------------

controls = ['thermo', 'price_rand', 'current','voltage', 'voltage_prob']
penetrations = [0,20,40,60,80,100]

results, trial = load_results.load_results(controls, penetrations)

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
# Per House Metrics
# -----------------------------

# All calculated metrics
all_possible_metrics = ['V_min_house',
                    'V_5th_house', 
                    'V_mean_house', 
                    'V_std_house', 
                    'temp_mean_house', 
                    'temp_min_house', 
                    'time_below_temp_min', 
                    'E_hwc_house', 
                    'E_on_peak_house', 
                    'E_off_peak_house', 
                    'P_mean_house', 
                    'P_peak_house', 
                    'P_95th_house', 
                    'switching_events_house'
                    ]

# All metrics to plot
possible_metrics = [
                    'V_5th_house', 
                    'E_hwc_house', 
                    'E_on_peak_house', 
                    'E_off_peak_house', 
                    'P_95th_house'
                    ]

ylabels = {
    'V_min_house': 'Change in Minimum Household Voltage\n(V)',
    'V_5th_house': 'Change in Average 5th Percentile \n Household Voltage (V)',
    'V_mean_house': 'Change in Mean Household\nVoltage (V)',
    'V_std_house': 'Change in Average Household Voltage\n Standard Deviation (V)',
    'temp_mean_house': 'Change in Mean HWC\nTemperature (°C)',
    'temp_min_house': 'Change in Minimum HWC\nTemperature (°C)',
    'time_below_temp_min': 'Change in Time Below Minimum\nHWC Temperature (h)',
    'E_hwc_house': 'Change in Average HWC Energy\n Consumption (kWh)',
    'E_on_peak_house': 'Change in Average On-Peak HWC \n Energy Consumption (kWh)',
    'E_off_peak_house': 'Change in Averagem Off-Peak HWC \n Energy Consumption (kWh)',
    'P_mean_house': 'Change in Mean Household\n Power (kW)',
    'P_peak_house': 'Change in Peak Household\nPower (kW)',
    'P_95th_house': 'Change in Average 95th Percentile \n Household Power (kW)',
    'switching_events_house': 'Change in Switching Events\nper Household'
}


# Create summary dataframe and plot for each metric
for metric in possible_metrics:

    # Create summary dataframe off all metrics
    summary = {}
    for control in controls:
        rows = []
        datasets = {}
        datasets.update({
            p: results[control][p][metric]
            for p in penetrations
        })

        for p, data in datasets.items():

            mean_house = np.mean(data, axis=1)

            rows.append({
                'percentile': p,
                'number_of_houses': int(np.ceil(55 * p / 100)),
                'penetration': 100*int(np.ceil(55 * p / 100))/55,
                'mean': np.mean(mean_house),
                'min': np.min(mean_house),
                'max': np.max(mean_house)
            })
        summary[control] = pd.DataFrame(rows)


    # Comparison plots
    plt.figure(figsize=(9,6))
    if metric in ['E_hwc_house', 'P_95th_house', 'E_on_peak_house', 'E_off_peak_house']:
        controls_to_plot = ['price_rand', 'current', 'voltage_prob']
    else:
        controls_to_plot = controls

    for control in controls_to_plot:
        if control != 'thermo':
            df = summary[control]
            y = summary[control]['mean']-summary['thermo']['mean']
            # yerr = np.vstack([df['mean'] - df['min'], df['max'] - df['mean']])
            # plt.errorbar(
            #     df['penetration'],
            #     df['mean'],
            #     yerr=yerr,
            #     marker='o',
            #     capsize=4,
            #     label=control.capitalize()+' Control'
            # )
            plt.plot(df['penetration'], y, label=control_label[control], color=colours[control], linestyle=line_styles[control], marker=marker_styles[control])

    plt.axhline(y=0, color=colours['thermo'], linestyle='--', linewidth=1)

    plt.xlabel('Control Penetration (%)', fontsize=18)
    plt.ylabel(ylabels[metric], fontsize=19)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.grid(True)
    plt.legend(fontsize=16)
    plt.tight_layout()
    plt.savefig(
        out_pth + f'/per_house_{metric}_comparison.png',
        dpi=600
    )

    if metric in ('V_5th_house', 'V_std_house'):
         plt.savefig(
        out_pths['household voltage'] + f'/{metric}_vs_penetration.png',
        dpi=600
        )

    if metric in ('P_95th_house', 'E_hwc_house', 'E_on_peak_house', 'E_off_peak_house'):
         plt.savefig(
        out_pths['household metrics'] + f'/{metric}_vs_penetration.png',
        dpi=600
        )
    plt.show()


# ----------------------------------------------------------------
# Feeder power metrics
# ----------------------------------------------------------------