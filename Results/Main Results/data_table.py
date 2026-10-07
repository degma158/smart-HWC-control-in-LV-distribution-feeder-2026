
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

out_pth = r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs'

# -----------------------------
# Load results
# -----------------------------

controls = ['thermo', 'price','price_rand', 'current','voltage', 'voltage_prob']
penetrations = [60,100]

results, trial = load_results.load_results(controls, penetrations)

# ------------------------------
# Generate data
# ------------------------------

# Electricity prices ($/kWh)
high_price = 0.42
low_price = 0.255

results['thermo'][60]['E_on_peak_house'].shape


for p in penetrations:
    if p == 60:
        ctrls = controls
    else:
        ctrls = [control for control in controls if control != 'price']

    P_sum_base = results['thermo'][p]['P_sum']
    V_house_base = results['thermo'][p]['V_house']
    I_house_base = results['thermo'][p]['I_house']
    E_on_house_base = results['thermo'][p]['E_on_peak_house']
    E_off_house_base =results['thermo'][p]['E_off_peak_house']

    P_95_base = np.percentile(P_sum_base, 95)
    P_max_base = np.max(P_sum_base)
    V_5_base = np.percentile(V_house_base, 5)
    V_min_base = np.min(V_house_base)
    I_95_base = np.percentile(I_house_base, 95)
    I_max_base = np.max(I_house_base)
    E_on_base = np.mean(E_on_house_base)
    E_off_base = np.mean(E_off_house_base)
    E_tot_base = E_off_base + E_on_base
    C_base = high_price*E_on_base + low_price*E_off_base

    for ctrl in ctrls:
        P_sum = results[ctrl][p]['P_sum']
        V_house = results[ctrl][p]['V_house']
        I_house = results[ctrl][p]['I_house']
        E_on_house = results[ctrl][p]['E_on_peak_house']
        E_off_house =results[ctrl][p]['E_off_peak_house']

        P_95 = np.percentile(P_sum, 95)
        P_max = np.max(P_sum)
        V_5 = np.percentile(V_house, 5)
        V_min = np.min(V_house)
        I_95 = np.percentile(I_house, 95)
        I_max = np.max(I_house)
        E_on = np.mean(E_on_house)
        E_off = np.mean(E_off_house)
        E_tot = E_off + E_on
        C = high_price*E_on + low_price*E_off

        print(f'{p}% {ctrl}:')
        print(f'=> P max = {P_max:.3g} kW')
        print(f'=> P 95th = {P_95:.3g} kW')

        print(
            f'=> change P 95th = '
            f'{100*(P_95-P_95_base)/P_95_base:.3g} %'
        )

        print(f'=> V min = {V_min:.3g} V')

        print(f'=> V 5th = {V_5:.3g} V')

        print(
            f'=> change V_5th = '
            f'{100*(V_5-V_5_base)/V_5_base:.3g} %'
        )

        print(f'=> I max = {I_max:.3g} A')

        print(f'=> I 95 = {I_95:.3g} A')

        print(
            f'=> change E_tot = '
            f'{E_tot-E_tot_base:.3g} kWh/day'
        )

        print(
            f'=> change C = '
            f'{C-C_base:.3g} $/day'
        )

        print('----------------------------')




import pandas as pd
import numpy as np


# ============================================================
# Helper: round to 3 significant figures
# ============================================================

def round_sig(x, sig=3):
    if x == 0:
        return 0
    return round(x, sig - int(np.floor(np.log10(abs(x)))) - 1)


# ============================================================
# Clear controller names for thesis table
# ============================================================

table_control_label = {
    'thermo': 'Baseline',
    'price': 'Price (Original)',
    'price_rand': 'Price (Randomised)',
    'current': 'Current',
    'voltage': 'Voltage (Original)',
    'voltage_prob': 'Voltage (Probabilistic)'
}


# ============================================================
# Create tables
# ============================================================

tables = {}

for p in [60, 100]:

    # Original price only exists at 60%
    ctrls = controls if p == 60 else [
        control for control in controls
        if control != 'price'
    ]

    # --------------------------------------------------------
    # Baseline
    # --------------------------------------------------------

    P_sum_base = results['thermo'][p]['P_sum']
    V_house_base = results['thermo'][p]['V_house']
    I_house_base = results['thermo'][p]['I_house']

    E_on_house_base = results['thermo'][p]['E_on_peak_house']
    E_off_house_base = results['thermo'][p]['E_off_peak_house']

    P_95_base = np.percentile(P_sum_base, 95)
    V_5_base = np.percentile(V_house_base, 5)

    E_on_base = np.mean(E_on_house_base)
    E_off_base = np.mean(E_off_house_base)
    E_tot_base = E_on_base + E_off_base

    C_base = (
        high_price * E_on_base +
        low_price * E_off_base
    )


    # --------------------------------------------------------
    # Table data
    # --------------------------------------------------------

    table_data = {}

    for ctrl in ctrls:

        P_sum = results[ctrl][p]['P_sum']
        V_house = results[ctrl][p]['V_house']
        I_house = results[ctrl][p]['I_house']

        E_on_house = results[ctrl][p]['E_on_peak_house']
        E_off_house = results[ctrl][p]['E_off_peak_house']

        # Metrics
        P_max = np.max(P_sum)
        P_95 = np.percentile(P_sum, 95)

        V_min = np.min(V_house)
        V_5 = np.percentile(V_house, 5)

        I_max = np.max(I_house)
        I_95 = np.percentile(I_house, 95)

        E_on = np.mean(E_on_house)
        E_off = np.mean(E_off_house)
        E_tot = E_on + E_off

        C = (
            high_price * E_on +
            low_price * E_off
        )


        # ----------------------------------------------------
        # Store under clear controller name
        # ----------------------------------------------------

        table_data[table_control_label[ctrl]] = [

            P_max,

            P_95,

            100 * (
                P_95 - P_95_base
            ) / P_95_base,

            V_min,

            V_5,

            100 * (
                V_5 - V_5_base
            ) / V_5_base,

            I_max,

            I_95,

            E_tot - E_tot_base,

            C - C_base
        ]


    # --------------------------------------------------------
    # Metric names
    # --------------------------------------------------------

    metric_names = [
        'P max (kW)',
        'P 95th (kW)',
        'ΔP 95th (%)',
        'V min (V)',
        'V 5th (V)',
        'ΔV 5th (%)',
        'I max (A)',
        'I 95th (A)',
        'ΔE total (kWh/day)',
        'ΔC ($/day)'
    ]


    # --------------------------------------------------------
    # DataFrame
    # --------------------------------------------------------

    table = pd.DataFrame(
        table_data,
        index=metric_names
    )

    table = table.map(
        lambda x: round_sig(x, 3)
    )

    tables[p] = table


# ============================================================
# Write to Excel
# ============================================================

excel_path = (
    out_pth +
    '/results_summary_tables.xlsx'
)

with pd.ExcelWriter(excel_path) as writer:

    tables[60].to_excel(
        writer,
        sheet_name='60% Penetration'
    )

    tables[100].to_excel(
        writer,
        sheet_name='100% Penetration'
    )


print(f'Saved to: {excel_path}')