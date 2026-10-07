# Code for initial simulation with HWC and only load (no other load profiles) to find average HWC electrical load and voltage/current changes from HWC switching

# Import dependencies
import pandas as pd
from dss import dss
from altdss import altdss
from dss import SolveModes
from importlib import reload
import matplotlib.pyplot as plt
import os
import numpy as np
import pickle
import random

import importlib.util
import sys

# Import custom modules
sys.path.append(r"C:\Users\Max de Groot\Git\Honours-Project-2026\My Code")
os.chdir(r"C:\Users\Max de Groot\Git\Honours-Project-2026\My Code")
import Py_OpenDSS_circuit
import Py_OpenDSS_set
import Py_OpenDSS_get
import load_profiles
import hot_water_cylinder
import plots

# Set path to the test feeder
pth = r"C:\Users\Max de Groot\Git\Honours-Project-2026\LVTestCase"

# Set true to determine control signals
initial_run = True

no_ctrl_house = 0

# Set output path
output_pth = rf"C:\Users\Max de Groot\Git\Honours-Project-2026\Outputs\HWC energy"

# Run the master.dss
dss.Text.Command = 'redirect "' + pth + '/master.dss"'

# Set active circuit and solve
AC = dss.ActiveCircuit
AC.Solution.Mode = 0 # Set to snapshot mode for initialisation
AC.Solution.Solve()

# Get the circuit from OpenDSS
[Circuit,dss_names] = Py_OpenDSS_circuit.new() # Creates dataframe structure
Circuit = Py_OpenDSS_get.circuit(AC,Circuit,dss_names) # Gets circuit information from AC
Circuit = Py_OpenDSS_circuit.bus_loadlist_2_load_buses(Circuit) #Get the bus for each load from the bus loadlist


# Creating indices for the different components in the circuit dataframe
b = Circuit[0].index('LoadShapes')
c = Circuit[0].index('Loads')
txs = Circuit[0].index('Transformers')

# Correct error in the first loadshape data
Circuit[b].loc[0,'LoadShapes'] = 'shape_1'
Circuit[b].loc[0,'Npts']=1440

# Fix source bus at bus 1 co
Circuit[4].loc[0,'x'] = Circuit[4]['x'][1]
Circuit[4].loc[0,'y'] = Circuit[4]['y'][1]

#----------------------------------------------------
# Generate hot water cylinder flows
#----------------------------------------------------

flows_pth = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Hot water model\Final Data\real\synthetic_profile[0].csv"
flow_data = pd.read_csv(flows_pth)
flow_vector = flow_data['Winter[undifferentiated_days]'] # in L/min
flow_vector = flow_vector*0.000016667 # convert from L/min to m3/s

n = 1440 # number of time steps in a day (1 minute resolution)

# Create flow matrix (1440 time steps, 55 houses, 100 trials)
flow_matrix = np.zeros((n, len(Circuit[c]), 100))
for t in range(100): # for each trial
    for l in range(len(Circuit[c])): # for each house

        start = t*n*len(Circuit[c]) + l*n
        end = start + n

        flow_matrix[:,l,t] = flow_vector.iloc[start:end].values

#pd.Series(flow_matrix[:, 0]).describe()

#---------------------------------------------------
# HWC constants
#---------------------------------------------------

constants = {
    "Cv": 4.2,  # kJ/kg.K
    "rho": 1000,  # kg/m3
    "Volume": 0.18, # cylinder volume m3
    "T_in": 20,  # degC
    "Q": 3,  # Element load kW
    "U": 0.0009,  # Heat loss coefficient kW/m2.K
    "A": 2.83,  # Surface area m2
    "T_amb": 20,  # degC
    "T_min": 40,  # degC
    "T_std": 63,  # degC
    "T_max": 73,  # degC
    "del_t": 60,  # s
}

# Unpack constants
Cv, rho, Volume, T_in, Q, U, A, T_amb, T_min, T_std, T_max, del_t = [
constants[k]
for k in ["Cv","rho","Volume", "T_in","Q","U","A","T_amb","T_min","T_std","T_max","del_t"]]


#-----------------------------------------
# Import previous price signal and other controls
#-----------------------------------------

if initial_run == False:

    with open(r'C:\Users\Max de Groot\Git\Honours-Project-2026\Outputs\Initial\control_signals.dat', 'rb') as f:
        Control_signals = pickle.load(f)
    # Control_signals.keys()

    price_signal = Control_signals['price_signal']
    current_thresh_low = Control_signals['current_thresh_low']
    current_thresh_high = Control_signals['current_thresh_high']
    voltage_thresh_low = Control_signals['voltage_thresh_low']
    voltage_thresh_high = Control_signals['voltage_thresh_high']
    delta_V_est = Control_signals['delta_V_est']
    delta_I_est = Control_signals['delta_I_est']
    V_tolerance = Control_signals['V_tolerance']

    price = price_signal[:,None]






#---------------------------------------------------
# MONTE CARLO SIMULATION
#---------------------------------------------------

scenarios = ['thermo']

scenarios_to_run = scenarios

trials = 1

    # Sets all loads to 1 kW but keeps pf, kVar etc
for ci in range(len(Circuit[c])):
    Circuit[c].loc[ci,'kW'] = 1

# Changes daily mode to yearly
Circuit[7]['daily'] = Circuit[7]['yearly']
Py_OpenDSS_set.Loads(AC,Circuit)

# Sets simulation mode in OpenDSS to daily with 1 minute steps
dss.Text.Command = "set mode=daily stepsize=1m number=1 hour=0.016666"

# Generates synthetic load profiles to monte carlo simulate with
profiles = load_profiles.bootstrap_REFIT(300)

#profiles = np.zeros(profiles)

profiles_all = np.zeros((trials, 1440, len(Circuit[b])))
for t in range(trials):
    profiles_all[t, :, :] = load_profiles.bootstrap_REFIT(len(Circuit[b]))

#profiles_all = np.zeros(profiles_all)

# Generate random control houses and mask true/false
count_control_houses = no_ctrl_house
control_houses = np.zeros((count_control_houses,trials))
control_houses = np.array([
    np.random.choice(55, size=count_control_houses, replace=False)
    for _ in range(trials)
]).T

control_mask_all = np.zeros((55, trials), dtype=bool)

for t in range(trials):
    control_mask_all[control_houses[:, t], t] = True

# Percentile array for voltage PDF
P = np.arange(0,100,1)

# Time vector for one day at 1 minute resolution (for graphing)
time_vector = np.arange(0,1440,1)

# Network storage arrays
volt_PDF = np.zeros((len(P),len(Circuit[c]),trials)) # Voltage percentiles for each house/trial
current_PDF = np.zeros((len(P),len(Circuit[c]),trials)) # Current percentiles for each house/trial
losses = np.zeros((len(profiles),trials)) # Not operational
I_sum = np.zeros((len(profiles),trials)) # Feeder current over time for each trial
P_sum = np.zeros((len(profiles),trials)) # Feeder power over time for each trial
V_mean_time = np.zeros((len(profiles),trials)) # Mean household voltage over time for each trial

# Household voltage and current
V_house = np.zeros((len(profiles),len(Circuit[c]),trials)) 
I_house = np.zeros((len(profiles),len(Circuit[c]),trials))
P_house = np.zeros((len(profiles),len(Circuit[c]),trials)) # Household power demand over time for each trial

# Synchronisation
on_fraction = np.zeros((len(profiles),trials)) # Fraction of HWC on over time for each trial

# # Base volt/curr change from HWC switching # not being used for results
delta_V_tot = np.zeros((len(Circuit[c]))) 
delta_I_tot = np.zeros((len(Circuit[c])))
count_switch = np.zeros((len(Circuit[c])))

## Per house metrics
# Voltage
V_min_house = np.zeros((len(Circuit[c]),trials)) # Min voltage for each house/trial
V_5th_house = np.zeros((len(Circuit[c]),trials)) # 5th percentile voltage for each house/trial
V_mean_house = np.zeros((len(Circuit[c]),trials)) # Mean voltage for each house/trial
V_std_house = np.zeros((len(Circuit[c]),trials)) # Standard dev of voltage for each house over each trial
# HWC temp performance
temp_mean_house = np.zeros((len(Circuit[c]),trials)) # Mean HWC temp for each house/trial
temp_min_house = np.zeros((len(Circuit[c]),trials)) # Min HWC temp for each house/trial
time_below_temp_min = np.zeros((len(Circuit[c]),trials)) # Duration HWC temp below min for each house/trial
# Electrical load contribution
E_hwc_house = np.zeros((len(Circuit[c]),trials)) # Total energy consumed by HWC for each house/trial in kWh
P_mean_house = np.zeros((len(Circuit[c]),trials)) # Mean household power demand for each house/trial
P_peak_house = np.zeros((len(Circuit[c]),trials)) # Peak household power demand for each house/trial
P_95th_house = np.zeros((len(Circuit[c]),trials)) # 95th percentile household power demand for each house/trial
# Off peak vs on peak
E_on_peak_house = np.zeros((len(Circuit[c]),trials)) # Total energy consumed on peak for each house/trial
E_off_peak_house = np.zeros((len(Circuit[c]),trials)) # Total energy consumed off peak for each house/trial
# Control mechanism
switching_events_house = np.zeros((len(Circuit[c]),trials)) # Count of HWC switching (ON/OFF) events for each house/trial






#----------------------------------------------------------------------------------------------------------
# Thermo-controlled hot water cylinder simulation
#----------------------------------------------------------------------------------------------------------

if 'thermo' in scenarios_to_run:
    for t in range(trials):
        print('Thermo trial: ' + str(t))

        if t != 0:
            initial_temps = temp_vector[-1,:].copy()
            initial_states = element_state_log[-1,:].copy()

        # Network storage arrays for trial
        Current = np.zeros((1440,len(Circuit[c])))
        Voltage = np.zeros((1440,len(Circuit[c])))

        # Household/HWC storage arrays for trial
        temp_vector = np.zeros((len(profiles), len(Circuit[c])))
        element_state_log = np.zeros((len(profiles),len(Circuit[c])))
        power_demand = np.zeros((len(profiles), len(Circuit[c])))
        cummulative_energy_out = np.zeros((len(profiles),len(Circuit[c])))
        cummulative_energy_in = np.zeros((len(profiles),len(Circuit[c])))

        # Initialise start temp and state
        if t == 0:
            temp_vector[0,:] = np.random.uniform(T_std-3, T_std, size=temp_vector[0,:].shape)
            # only 0.05 of the elements on initially
            n_on = int(0.05 * element_state_log[0, :].size)
            on_indices = np.random.choice(element_state_log[0, :].size,size=n_on,replace=False)
            element_state_log[0, on_indices] = 1
        else:
            temp_vector[0,:] = initial_temps
            element_state_log[0,:] = initial_states

        # add initial temp difference energy
        cummulative_energy_out[0,:] = Cv*rho*Volume*(T_std - temp_vector[0,:])
        
        # Assigns synthetic load profiles     
        profiles = np.asfortranarray(profiles_all[t], dtype=np.float64)

        # Set load shapes from bootstrapped profiles
        for l in range(len(Circuit[b])):
            Circuit[b].at[l,'Pmult'] = profiles[:,l]
            Circuit[b].at[l,'Qmult'] = 0*profiles[:,l] 
            
        Circuit[7]['daily'] = Circuit[7]['yearly']
        Py_OpenDSS_set.LoadShapes(AC,Circuit)

        # Determine load index for each loadshape
        loadshape_map = np.array([
            np.where(Circuit[b]['LoadShapes'] == Circuit[c].loc[l,'daily'])[0][0]
            for l in range(len(Circuit[c]))
            ])
        
        # Time series simulation loop
        for i in range(len(profiles)):
            #print('Time step: ' + str(i))
            
            #dss.Text.Command = "set time=("+str(int(i/60))+","+str(60*np.mod(i,60))+")"
            #AC.Solution.Solve() # does one step in Daily mode
        
            if i == 0:
                temp_prev = temp_vector[0,:]
                state_prev = element_state_log[0,:]
                flow_prev = flow_matrix[0,:,t]
                enrg_in_prev = cummulative_energy_in[0,:]
                enrg_out_prev = cummulative_energy_out[0,:]
            else:
                temp_prev = temp_vector[i-1,:]
                state_prev = element_state_log[i-1,:]
                flow_prev = flow_matrix[i-1,:,t]
                enrg_in_prev = cummulative_energy_in[i-1,:]
                enrg_out_prev = cummulative_energy_out[i-1,:]
                
            # Household loop (for HWC simulation)
            for l in range(len(Circuit[c])):
                #print('House: ' + str(l))
                # Loop through each house, determine if HWC on/off, calc temp enrg etc., add load to household profile, solve Circuit

                # Identify correct loadshape for the house (important)
                ls = loadshape_map[l]

                prev_temp = temp_prev[l]
                prev_state = state_prev[l]
                prev_flow = flow_prev[l]
                prev_enrg_in = enrg_in_prev[l]
                prev_enrg_out = enrg_out_prev[l]
            
                cummulative_energy_out[i,l] = U*A*(prev_temp - T_amb)*del_t - Cv*rho*prev_flow*(T_in - prev_temp)*del_t + prev_enrg_out
                cummulative_energy_in[i,l] = Q*prev_state*del_t + prev_enrg_in

                # New state
                new_temp, new_state = hot_water_cylinder.thermo_ctrl(prev_temp, prev_flow, prev_state, Cv, rho, Volume, T_in, Q, U, A, T_amb, T_min, T_std, T_max, del_t)
                                                                    
                # Log new state
                temp_vector[i,l] = new_temp
                element_state_log[i,l] = new_state

                # Log household power demand
                power_demand[i,l] = Q*new_state + profiles[i,l] # kW

                # Set loadshape  
                Circuit[b].at[ls,'Pmult'] = power_demand[:,l].copy()

            # Set load shapes and solve at time step
            Py_OpenDSS_set.LoadShapes(AC,Circuit)
            dss.Text.Command = "set time=("+str(int(i/60))+","+str(60*np.mod(i,60))+")" # seems to be important to reset time before solve
            AC.Solution.Solve()
            Circuit = Py_OpenDSS_get.voltage(AC,Circuit)
            Circuit = Py_OpenDSS_get.current(AC,Circuit)

            for l in range(len(Circuit[c])):
                
                # Identify phase for each load
                phase = int(Circuit[c]['phase'][l][-1]) - 1

                # Calculate current magnitude for each load
                Current[i, l] = np.sqrt(
                    Circuit[c]['Current'][l][0]**2 +
                    Circuit[c]['Current'][l][1]**2
                )
                
                # Get voltage magnitude for each load
                Voltage[i, l] = Circuit[c]['Volts'][l][phase]

                if i !=0:
                    if element_state_log[i,l] != element_state_log[i-1,l]:
                        delta_V_tot[l] = delta_V_tot[l] + abs(Voltage[i,l]-Voltage[i-1,l])
                        delta_I_tot[l] = delta_I_tot[l] + abs(Current[i,l] - Current[i-1,l])
                        count_switch[l] = count_switch[l] + 1
                
            # Get losses for each transformer
            Circuit = Py_OpenDSS_get.current(AC,Circuit,'Transformers')
            losses[i,t] = np.sum(AC.AllElementLosses)

        for l in range(len(Circuit[c])):
            # percentiles
            volt_PDF[:,l,t] = np.percentile(Voltage[:,l],P)
            current_PDF[:,l,t] = np.percentile(Current[:,l],P)
            
        V_house[:,:,t] = Voltage
        I_house[:,:,t] = Current
        P_house[:,:,t] = power_demand

        # Network results   
        I_sum[:,t] = np.sum(Current,1)
        P_sum[:,t] = np.sum(power_demand, axis=1)
        V_mean_time[:,t] = np.mean(Voltage, axis=1)        
        
        # Frac HWC on
        on_fraction[:, t] = np.mean(element_state_log, axis=1)

        # per house metrics
        V_min_house[:,t] = np.min(Voltage, axis=0)
        V_5th_house[:,t] = np.percentile(Voltage, 5, axis=0)
        V_mean_house[:,t] = np.mean(Voltage, axis=0)
        V_std_house[:,t] = np.std(Voltage, axis=0)

        temp_mean_house[:,t] = np.mean(temp_vector, axis=0)
        temp_min_house[:,t] = np.min(temp_vector, axis=0)
        time_below_temp_min[:,t] = np.sum(temp_vector < T_min, axis=0)

        E_hwc_house[:,t] = np.sum(element_state_log, axis=0)*Q/60 # in kWh
        P_mean_house[:,t] = np.mean(power_demand, axis=0)
        P_peak_house[:,t] = np.max(power_demand, axis=0)
        P_95th_house[:,t] = np.percentile(power_demand, 95, axis=0)

        # if initial_run == False:
        #     E_on_peak_house[:,t] = np.sum(power_demand*price, axis=0)/60 # on peak price signal = 1
        #     E_off_peak_house[:,t] = np.sum(power_demand*(1-price), axis=0)/60

        switching_events_house[:, t] = np.sum(np.abs(np.diff(element_state_log[:, :], axis=0)), axis=0)

        # Save one example trail (e.g. for graphing)
        if t == 1:
            category = np.zeros(1440)
            tx_current = Circuit[6]['Current2']
            low_voltage = np.percentile(Voltage,1,1)

            Trial_res = {'Circuit':Circuit,
                        'Current':Current,
                        'Voltage':Voltage,
                        'volt_PDF':volt_PDF,
                        'temp_vector':temp_vector,
                        'flow_matrix':flow_matrix[:,:,t],
                        'element_state_log':element_state_log,
                        'cummulative_energy_out':cummulative_energy_out,
                        'cummulative_energy_in':cummulative_energy_in,
                        'power_demand':power_demand,
                        'profiles':profiles,
                        'switching_events':switching_events_house[:,t],
                        'control_mask':control_mask_all[:,t],
                        'category':category
                        }
            
            with open(output_pth + '/' + 'thermo_trial.dat', 'wb') as f:
                pickle.dump(Trial_res, f)

        if t == trials-1:
            print('All trials complete')

        # Check physicality of results for one house in 1st trial
        if t == -1: 
            for h in [10,20,30,40,50]: #range(1,56): # House
                V = Voltage[:, h]
                I = Current[:, h]
                state = element_state_log[:, h]
                T = temp_vector[:, h]
                enrg_in = cummulative_energy_in[:, h]
                enrg_out = cummulative_energy_out[:, h]
                F = flow_matrix[:, h, t]
                P_supply = V*I/1000 # kW
                P_demand = power_demand[:, h]
                plots.single_house_ctrl_check_plot(f'Thermo Control: House {h}', h, time_vector, V, I, state, T, enrg_in, enrg_out, F, P_supply, P_demand,
                                                0, 0, 0, 0, 0)

    # - Post processing and saving result -

    # Calculate mean voltage and current percentiles across trials
    volt_PDF_mu = np.zeros((len(P),len(Circuit[c])))
    current_PDF_mu = np.zeros((len(P),len(Circuit[c])))
    for l in range(len(Circuit[c])):
            volt_PDF_mu[:,l] = np.mean(volt_PDF[:,l,:],1)
            current_PDF_mu[:,l] = np.mean(current_PDF[:,l,:],1)

    # Calculate mean losses across trials
    losses_mu = np.mean(np.sum(losses,1))

    # On peak vs off peak energy

    # Save results to file by saving a data dictionary
    Results = {'volt_PDF_mu':volt_PDF_mu,
                'current_PDF_mu':current_PDF_mu,
                'tx_current':tx_current,
                'low_voltage':low_voltage,
                'losses':losses,
                'I_sum':I_sum,
                'P_sum':P_sum,
                'V_mean_time':V_mean_time,
                'on_fraction':on_fraction,
                'V_min_house':V_min_house,
                'V_5th_house':V_5th_house,
                'V_mean_house':V_mean_house,
                'V_std_house':V_std_house,
                'temp_mean_house':temp_mean_house,
                'temp_min_house':temp_min_house,
                'time_below_temp_min':time_below_temp_min,
                'E_hwc_house':E_hwc_house,
                'E_on_peak_house':E_on_peak_house,
                'E_off_peak_house':E_off_peak_house,
                'P_mean_house':P_mean_house,
                'P_peak_house':P_peak_house,
                'P_95th_house':P_95th_house,
                'switching_events_house':switching_events_house,
                'control_mask_all':control_mask_all,
                'V_house':V_house,
                'I_house':I_house,
                'P_house':P_house
                }
        
    # Save the 'Results' dictionary to a file using pickle
    with open(output_pth + '/' + 'thermo_mean.dat', 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(Results, f)




