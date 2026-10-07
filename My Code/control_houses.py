# Code to generate the nested set of control houses for each penetration


import numpy as np
import pickle

# -------------------------------------------------------
# Settings
# -------------------------------------------------------

n_houses = 55

penetrations = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

out_path = r'C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\Outputs\Initial'

# -------------------------------------------------------
# Generate cumulative control-house sets
# -------------------------------------------------------

generate_control_houses = True

if generate_control_houses == True:
    # One random ordering of all houses
    house_order = np.random.permutation(n_houses)

    control_houses = {}

    for p in penetrations:

        n_control = int(n_houses * p / 100)

        # Cumulative selection
        control_houses[p] = house_order[:n_control].copy()

# --------------------------------------------------------
# Check
# --------------------------------------------------------

control_houses.keys()
control_houses[0]
control_houses[10].shape
control_houses[20].shape
control_houses[50].shape

# -------------------------------------------------------
# Save
# -------------------------------------------------------

with open(out_path + '/' + 'control_houses.dat', 'wb') as f:
    pickle.dump(control_houses, f)