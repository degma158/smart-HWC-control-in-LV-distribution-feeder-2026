import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import sys
import os

sys.path.append(r"C:\Users\Max de Groot\Git\Honours-Project-2026\My Code")
os.chdir(r"C:\Users\Max de Groot\Git\Honours-Project-2026\My Code")

import load_results

import re

plt.rcParams['font.family'] = 'Times New Roman'

# -----------------------------
# Load results
# -----------------------------

controls = ['thermo', 'price', 'price_rand', 'current','voltage', 'voltage_prob']
penetrations = [0,50,60,80,100]

results, trial = load_results.load_results(controls, penetrations)

# -----------------------------
# Define objects
# -----------------------------

Circuit = trial['thermo'][0]['Circuit']
Circuit[0]

ActiveBus = Circuit[4]
Lines = Circuit[5]

ActiveBus
Lines

# -----------------------------
# Spatial plot
# -----------------------------

bus_coords = {
    str(row['ActiveBus']): (row['x'], row['y'])
    for _, row in ActiveBus.iterrows()
}

fig, ax = plt.subplots(figsize=(8, 5))

# Plot feeder lines ONLY
for _, line in Lines.iterrows():

    bus1 = str(line['Bus1'])
    bus2 = str(line['Bus2'])

    if bus1 in bus_coords and bus2 in bus_coords:

        x1, y1 = bus_coords[bus1]
        x2, y2 = bus_coords[bus2]

        ax.plot([x1, x2],[y1, y2],color='0.5',linewidth=1.5,solid_capstyle='round',zorder=1)


# Find household load buses
def get_load_name(load_list):
    if isinstance(load_list, list):
        for item in load_list:
            if str(item).upper().startswith('LOAD.LOAD'):
                return str(item)
    return None

load_buses = ActiveBus.copy()
load_buses['LoadName'] = load_buses['LoadList'].apply(get_load_name)
load_buses = load_buses[load_buses['LoadName'].notna()]
load_buses = load_buses.drop_duplicates(subset='LoadName')

print(f'Number of household loads: {len(load_buses)}')

# Plot household locations
house_colour = {0: "#E4F529",
                20: 'blue',
                54: 'red'}

house_label = {0: 'Household A',
               20: 'Household B',
               54: 'Household C'}

ax.scatter(load_buses['x'],load_buses['y'],s=50,color='grey',alpha=1,linewidth=1.2,zorder=5,label='Other\nHouseholds')

for h in [0,20,54]:
    ax.scatter(load_buses['x'].iloc[h], load_buses['y'].iloc[h], s=50,color=house_colour[h],alpha=1,linewidth=1.2,zorder=5,label=house_label[h])

# # Add load numbers inside household markers
# for _, row in load_buses.iterrows():
#     match = re.search(r'\d+', row['LoadName'])

#     if match:
#         ax.text(row['x'],
#             row['y'],
#             match.group(),
#             fontsize=14,
#             color='black',
#             ha='center',
#             va='center',
#             zorder=6
#         )

# Plot source
source = ActiveBus[ActiveBus['ActiveBus'].astype(str) == 'sourcebus']
ax.scatter(    source['x'],source['y'],s=180,marker='s',color='black',zorder=7,label='Feeder source')

# Formatting
ax.set_xlabel('Easting (m)', fontsize=19)
ax.set_ylabel('Northing (m)', fontsize=19)
ax.set_aspect('equal', adjustable='box')
ax.tick_params(    axis='both',    labelsize=16)
ax.grid(    True,    alpha=0.25)


handles, labels = ax.get_legend_handles_labels()

order = [
    labels.index('Household A'),
    labels.index('Household B'),
    labels.index('Household C'),
    labels.index('Other Households'),
    labels.index('Feeder source')
]

ax.legend(
    [handles[i] for i in order],
    [labels[i] for i in order],
    fontsize=16,
    loc='center right',
    bbox_to_anchor=(1.45, 0.5),
    ncol=1,
    frameon=False
)

# ax.legend(fontsize=16,loc='best')
plt.tight_layout()
plt.savefig(
    r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\methodology' + '/feeder_spatial_plot.pdf')
plt.show()



# -------------------------------------------------------
# Load distance from source
# ---------------------------------------------------------

# # Convert bus names to strings so indexing is consistent
# lines = Lines.copy()
# lines['Bus1'] = lines['Bus1'].astype(str)
# lines['Bus2'] = lines['Bus2'].astype(str)

# # Distance from source
# bus_distance = {
#     'sourcebus': 0.0,
#     '1': 0.0
# }

# # Keep finding buses whose upstream bus is already known
# remaining = lines.copy()

# while len(remaining) > 0:

#     found = []

#     for idx, line in remaining.iterrows():

#         bus1 = line['Bus1']
#         bus2 = line['Bus2']
#         length = line['Length']

#         # If upstream bus distance is known,
#         # calculate distance to downstream bus
#         if bus1 in bus_distance:
#             bus_distance[bus2] = bus_distance[bus1] + length
#             found.append(idx)

#     # Remove lines that have been processed
#     remaining = remaining.drop(found)

#     # Safety check
#     if len(found) == 0:
#         print("Could not connect remaining lines:")
#         print(remaining[['Bus1', 'Bus2', 'Length']])
#         break

# load_distance = []

# for _, row in ActiveBus.iterrows():

#     if len(row['LoadList']) > 0:

#         load_name = str(row['LoadList'][0])

#         # Extract the number from the load name
#         match = re.search(r'\d+', load_name)

#         if match:
#             load_number = int(match.group())

#             bus = str(row['ActiveBus'])

#             load_distance.append({
#                 'Load': load_number,
#                 'Bus': bus,
#                 'Distance': bus_distance[bus]
#             })

# load_distance = pd.DataFrame(load_distance)
# load_distance['Distance'] = load_distance['Distance']/1000

# load_distance.to_csv(
#     os.path.join(r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs', 'load_distance.csv'),
#     index=False
# )

