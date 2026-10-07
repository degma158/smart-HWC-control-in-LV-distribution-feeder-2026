# HOT WATER CYLINDER CONTROL FUNCTIONS
# -------------------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------
# Thermo control function
# -----------------------------------------------------------

# Thermodynamic control function for hot water cylinder
def thermo_ctrl(T, F, h_state, Cv, rho, Volume, T_in, Q, U, A, T_amb, T_min, T_std, T_max, del_t):

    # Cv, rho, Volume, T_in, Q, U, A, T_amb, T_min, T_std, T_max, del_t = [
    # constants[k]
    # for k in ["Cv","rho","Volume","T_in","Q","U","A","T_amb","T_min","T_std","T_max","del_t"]]

    h_state_new = h_state

    # 1. Turn ON if it is OFF and there is flow
    if h_state == 0 and F > 0:
        h_state_new = 1

    # 2. Turn ON if it is OFF and temp drops below T_min
    elif h_state == 0 and T <= T_std - 3:
        h_state_new = 1

    # 3. Turn OFF if it is ON and temp reaches or exceeds T_std
    elif h_state == 1 and T >= T_std:
        h_state_new = 0

    flow_enrg = Cv*rho*F*(T_in - T)
    element_enrg = Q*h_state_new
    conduction_enrg = U*A*(T - T_amb)

    T_new = (del_t/(Cv*rho*Volume))*(flow_enrg + element_enrg - conduction_enrg) + T

    return T_new, h_state_new

# ---------------------------------------------------------
# Price control function
# ---------------------------------------------------------

# Centralised electricity price control function
def price_ctrl(T, F, h_state, price_signal, Cv, rho, Volume, T_in, Q, U, A, T_amb, T_min, T_std, T_max, del_t):

    # Cv, rho, Volume, T_in, Q, U, A, T_amb, T_min, T_std, T_max, del_t = [
    # constants[k]
    # for k in ["Cv","rho","Volume","T_in","Q","U","A","T_amb","T_min","T_std","T_max","del_t"]]

    h_state_new = h_state

    # Define min/max temp thresholds based on price signal
    if price_signal == 1: # High price signal
        T_on = T_std - 3
        T_off = T_std
    elif price_signal == 0: # Low price signal
        T_on = T_max - 3
        T_off = T_max

    # 1. Turn ON if it is OFF and temp below T_on
    if h_state == 0 and T <= T_on:
        h_state_new = 1

    # 2. Turn OFF if it is ON and temp drops below T_off
    elif h_state == 1 and T >= T_off:
        h_state_new = 0

    # # 3. Turn ON if flow and temp below T_std
    # if F > 0 and T < T_std:
    #     h_state_new = 1

    flow_enrg = Cv*rho*F*(T_in - T)
    element_enrg = Q*h_state_new
    conduction_enrg = U*A*(T - T_amb)

    T_new = (del_t/(Cv*rho*Volume))*(flow_enrg + element_enrg - conduction_enrg) + T

    return T_new, h_state_new


# --------------------------------------------------
# Current Control Fuction
# --------------------------------------------------


# Current control function
def current_ctrl(T, F, h_state, h_state_prev, current, current_thresh_high, current_thresh_low, prev_category, 
                 Cv, rho, Volume, T_in, Q, U, A, T_amb, T_min, T_std, T_max, del_t):

    # Cv, rho, Volume, T_in, Q, U, A, T_amb, T_min, T_std, T_max, del_t = [
    #     constants[k]
    #     for k in ["Cv","rho","Volume","T_in","Q",
    #               "U","A","T_amb","T_min",
    #               "T_std","T_max","del_t"]
    # ]

    h_state_new = h_state
    category = prev_category

    # -------------------------------------------------
    # Predictive current impact
    # -------------------------------------------------
    if h_state == 0: # OFF
        I_thresh = current_thresh_low # use low threshold if OFF
    else: # ON
        I_thresh = current_thresh_high # use high threshold if ON

    #------------------------
    # Category switching
    #------------------------

    if prev_category == 0: # Conservative
        if np.all(current <= I_thresh): # Below low threshold for some time
            category = 1 # Switch to liberal
    else: # Liberal
        #if np.any(current >= I_thresh): # Breach high threshold
        if h_state == 0 and h_state_prev == 1:
            if current[-1]>= current_thresh_high:
                category = 0 # switch to conservative
        else:
            if current[-1]>= I_thresh:
                category = 0 
                  

    # -------------------------------------------------
    # Thermal hysteresis bands
    # -------------------------------------------------
    if category == 1:
        # Aggresive (grid relaxed → charge more aggressively)
        T_on = T_max - 3 #T_std + 0.5 * (T_max - T_std)
        T_off = T_max
    else:
        # conservative (grid stressed → restrict charging)
        T_on = T_std - 3
        T_off = T_std # + 0.5 * (T_std - T_min)

    #-----
    # Control actions
    #-----

    # 1. Turn ON if it is OFF and temp below T_on
    if h_state == 0 and T <= T_on:
        h_state_new = 1

    # 2. Turn OFF if it is ON and temp above T_off
    elif h_state == 1 and T >= T_off:
        h_state_new = 0

    # # 3. Turn ON if flow and temp below T_std
    # if F > 0 and T < T_std:
    #     h_state_new = 1

    #-----
    # Thermal model
    #-----

    flow_enrg = Cv*rho*F*(T_in - T)
    element_enrg = Q*h_state_new
    conduction_enrg = U*A*(T - T_amb)

    T_new = (del_t/(Cv*rho*Volume))*(flow_enrg + element_enrg - conduction_enrg) + T

    return T_new, h_state_new, category


# ------------------------------
# Voltage control function
# ------------------------------

# Voltage control function
def voltage_ctrl_prob(T, F, h_state, voltage, voltage_thresh_high, voltage_thresh_low, delta_V_est, V_tolerance, prev_category, 
                 Cv, rho, Volume, T_in, Q, U, A, T_amb, T_min, T_std, T_max, del_t):

    # Cv, rho, Volume, T_in, Q, U, A, T_amb, T_min, T_std, T_max, del_t = [
    # constants[k]
    # for k in ["Cv","rho","Volume","T_in","Q","U","A","T_amb","T_min","T_std","T_max","del_t"]]

    h_state_new = h_state
    category = prev_category

    #-----
    # Predictive voltage impact (want to control agianst what voltage would be if it was on)
    #-----

    if h_state == 0: # Element OFF
        #V_pred = voltage - delta_V_est # Decreased voltage if was switched OFF to ON
        V_pred = np.mean(voltage) - delta_V_est
        #V_pred = voltage - delta_V_est
    else: # Element ON
        #V_pred = voltage # Element already ON
        V_pred = np.mean(voltage)
        # V_pred = voltage

    #-----
    # Category switching
    #-----

    if prev_category == 0: # low volt (conservative)
        #if np.all(V_pred >= voltage_thresh_low): # below low thresh
        if V_pred >= voltage_thresh_high:
            idx = np.abs(V_tolerance - V_pred).argmin()
            if np.random.uniform(0, 100) < idx:
                category = 1 # switch to liberal
    else: # liberal
        #if np.all(V_pred <= voltage_thresh_high): # above high thresh
        if V_pred <= voltage_thresh_low:
            category = 0 # Change from liberal to conservative if volt driops below low threshold

    #-----
    # Thermal histeresis bands
    #-----

    if category == 1: # Agressive
        T_on = T_max - 3 # T_std + 0.5*(T_max-T_std)
        T_off = T_max
    else: # Conservative
        T_on = T_std - 3
        T_off = T_std # T_min + 0.5*(T_std-T_min)

    #-----
    # Control actions
    #-----

    # 1. Turn ON if it is OFF and temp below T_on
    if h_state == 0 and T <= T_on:
        h_state_new = 1

    # 2. Turn OFF if it is ON and temp drops below T_off
    elif h_state == 1 and T >= T_off:
        h_state_new = 0

    # # 3. Turn ON if flow and temp below T_std
    # if F > 0 and T < T_std:
    #     h_state_new = 1

    #-----
    # Thermal model
    #-----

    flow_enrg = Cv*rho*F*(T_in - T)
    element_enrg = Q*h_state_new
    conduction_enrg = U*A*(T - T_amb)

    T_new = (del_t/(Cv*rho*Volume))*(flow_enrg + element_enrg - conduction_enrg) + T

    return T_new, h_state_new, category





def price_ctrl_delay(T, F, h_state, price_signal, prev_price_signal, Cv, rho, Volume, T_in, Q, U, A, T_amb, T_min, T_std, T_max, del_t, delay, max_delay):

    # Cv, rho, Volume, T_in, Q, U, A, T_amb, T_min, T_std, T_max, del_t = [
    # constants[k]
    # for k in ["Cv","rho","Volume","T_in","Q","U","A","T_amb","T_min","T_std","T_max","del_t"]]

    h_state_new = h_state
    delay_new = max(delay - 1, 0)

    # Default operation
    T_on = T_std - 3
    T_off = T_std

    # Define min/max temp thresholds based on price signal
    if price_signal == 1: # High price signal, charge conservative
        T_on = T_std - 3
        T_off = T_std
    if price_signal == 0 and prev_price_signal == 1: # Just switched to low price signal
        delay_new = np.random.randint(0, max_delay)
        if delay_new == 0: # charge aggressive if delay passed
            T_on = T_max - 3
            T_off = T_max
    elif price_signal == 0 and prev_price_signal == 0: # Low price signal
        if delay_new == 0: # charge aggressive if delay passed
            T_on = T_max - 3
            T_off = T_max


    # 1. Turn ON if it is OFF and temp below T_on
    if h_state == 0 and T <= T_on:
        h_state_new = 1

    # 2. Turn OFF if it is ON and temp drops below T_off
    elif h_state == 1 and T >= T_off:
        h_state_new = 0

    # # 3. Turn ON if flow and temp below T_std
    # if F > 0 and T < T_std:
    #     h_state_new = 1

    flow_enrg = Cv*rho*F*(T_in - T)
    element_enrg = Q*h_state_new
    conduction_enrg = U*A*(T - T_amb)

    T_new = (del_t/(Cv*rho*Volume))*(flow_enrg + element_enrg - conduction_enrg) + T

    return T_new, h_state_new, delay_new







# Voltage control function
def voltage_ctrl(T, F, h_state, voltage, voltage_thresh_high, voltage_thresh_low, delta_V_est, prev_category, 
                 Cv, rho, Volume, T_in, Q, U, A, T_amb, T_min, T_std, T_max, del_t):

    # Cv, rho, Volume, T_in, Q, U, A, T_amb, T_min, T_std, T_max, del_t = [
    # constants[k]
    # for k in ["Cv","rho","Volume","T_in","Q","U","A","T_amb","T_min","T_std","T_max","del_t"]]

    h_state_new = h_state
    category = prev_category

    #-----
    # Predictive voltage impact (want to control agianst what voltage would be if it was on)
    #-----

    if h_state == 0: # Element OFF
        #V_pred = voltage - delta_V_est # Decreased voltage if was switched OFF to ON
        #V_pred = np.min(voltage) - delta_V_est
        V_pred = voltage - delta_V_est
    else: # Element ON
        #V_pred = voltage # Element already ON
        #V_pred = np.min(voltage)
        V_pred = voltage

    #-----
    # Category switching
    #-----

    if prev_category == 0: # low volt (conservative)
        #if np.all(V_pred >= voltage_thresh_low): # below low thresh
        if np.mean(V_pred) >= voltage_thresh_high:
            category = 1 # switch to liberal
    else: # liberal
        #if np.all(V_pred <= voltage_thresh_high): # above high thresh
        if np.mean(V_pred) <= voltage_thresh_low:
            category = 0 # Change from liberal to conservative if volt driops below low threshold

    #-----
    # Thermal histeresis bands
    #-----

    if category == 1: # Agressive
        T_on = T_max - 5 # T_std + 0.5*(T_max-T_std)
        T_off = T_max
    else: # Conservative
        T_on = T_std - 5
        T_off = T_std # T_min + 0.5*(T_std-T_min)

    #-----
    # Control actions
    #-----

    # 1. Turn ON if it is OFF and temp below T_on
    if h_state == 0 and T <= T_on:
        h_state_new = 1

    # 2. Turn OFF if it is ON and temp drops below T_off
    elif h_state == 1 and T >= T_off:
        h_state_new = 0

    # # 3. Turn ON if flow and temp below T_std
    # if F > 0 and T < T_std:
    #     h_state_new = 1

    #-----
    # Thermal model
    #-----

    flow_enrg = Cv*rho*F*(T_in - T)
    element_enrg = Q*h_state_new
    conduction_enrg = U*A*(T - T_amb)

    T_new = (del_t/(Cv*rho*Volume))*(flow_enrg + element_enrg - conduction_enrg) + T

    return T_new, h_state_new, category




# V pred running double mean voltage control function
def voltage_ctrl_pred_running_double(T, F, h_state, voltage, voltage_thresh_high, voltage_thresh_low, delta_V_est, prev_category, 
                 Cv, rho, Volume, T_in, Q, U, A, T_amb, T_min, T_std, T_max, del_t):

    h_state_new = h_state
    category = prev_category

    #-----
    # Predictive voltage impact (want to control agianst what voltage would be if it was on)
    #-----

    if h_state == 0: # Element OFF
        V_pred = voltage - delta_V_est
    else: # Element ON
        V_pred = voltage

    #-----
    # Category switching
    #-----

    if prev_category == 0: # low volt (conservative)
        if np.mean(V_pred) >= voltage_thresh_high:
            category = 1 # switch to liberal
    else: # liberal
        if np.mean(V_pred) <= voltage_thresh_low:
            category = 0 # Change from liberal to conservative if volt driops below low threshold

    #-----
    # Thermal histeresis bands
    #-----

    if category == 1: # Agressive
        T_on = T_max - 5 # T_std + 0.5*(T_max-T_std)
        T_off = T_max
    else: # Conservative
        T_on = T_std - 5
        T_off = T_std # T_min + 0.5*(T_std-T_min)

    #-----
    # Control actions
    #-----

    # 1. Turn ON if it is OFF and temp below T_on
    if h_state == 0 and T <= T_on:
        h_state_new = 1

    # 2. Turn OFF if it is ON and temp drops below T_off
    elif h_state == 1 and T >= T_off:
        h_state_new = 0

    # # 3. Turn ON if flow and temp below T_std
    # if F > 0 and T < T_std:
    #     h_state_new = 1

    #-----
    # Thermal model
    #-----

    flow_enrg = Cv*rho*F*(T_in - T)
    element_enrg = Q*h_state_new
    conduction_enrg = U*A*(T - T_amb)

    T_new = (del_t/(Cv*rho*Volume))*(flow_enrg + element_enrg - conduction_enrg) + T

    return T_new, h_state_new, category




# V pred running double mean voltage control function
def voltage_ctrl_running_double(T, F, h_state, voltage, voltage_thresh_high, voltage_thresh_low, delta_V_est, prev_category, 
                 Cv, rho, Volume, T_in, Q, U, A, T_amb, T_min, T_std, T_max, del_t):

    h_state_new = h_state
    category = prev_category

    #-----
    # Predictive voltage impact (want to control agianst what voltage would be if it was on)
    #-----

    if h_state == 0: # Element OFF
        V_pred = voltage
    else: # Element ON
        V_pred = voltage

    #-----
    # Category switching
    #-----

    if prev_category == 0: # low volt (conservative)
        if np.mean(V_pred) >= voltage_thresh_high:
            category = 1 # switch to liberal
    else: # liberal
        if np.mean(V_pred) <= voltage_thresh_low:
            category = 0 # Change from liberal to conservative if volt driops below low threshold

    #-----
    # Thermal histeresis bands
    #-----

    if category == 1: # Agressive
        T_on = T_max - 5 # T_std + 0.5*(T_max-T_std)
        T_off = T_max
    else: # Conservative
        T_on = T_std - 5
        T_off = T_std # T_min + 0.5*(T_std-T_min)

    #-----
    # Control actions
    #-----

    # 1. Turn ON if it is OFF and temp below T_on
    if h_state == 0 and T <= T_on:
        h_state_new = 1

    # 2. Turn OFF if it is ON and temp drops below T_off
    elif h_state == 1 and T >= T_off:
        h_state_new = 0

    # # 3. Turn ON if flow and temp below T_std
    # if F > 0 and T < T_std:
    #     h_state_new = 1

    #-----
    # Thermal model
    #-----

    flow_enrg = Cv*rho*F*(T_in - T)
    element_enrg = Q*h_state_new
    conduction_enrg = U*A*(T - T_amb)

    T_new = (del_t/(Cv*rho*Volume))*(flow_enrg + element_enrg - conduction_enrg) + T

    return T_new, h_state_new, category






# V pred running double mean voltage control function
def voltage_ctrl_single(T, F, h_state, voltage, voltage_thresh_high, voltage_thresh_low, delta_V_est, prev_category, 
                 Cv, rho, Volume, T_in, Q, U, A, T_amb, T_min, T_std, T_max, del_t):

    h_state_new = h_state
    category = prev_category

    #-----
    # Predictive voltage impact (want to control agianst what voltage would be if it was on)
    #-----

    if h_state == 0: # Element OFF
        V_pred = voltage # - delta_V_est
    else: # Element ON
        V_pred = voltage

    #-----
    # Category switching
    #-----

    if prev_category == 0: # low volt (conservative)
        if V_pred[-1] >= voltage_thresh_high:
            category = 1 # switch to liberal
    else: # liberal
        if V_pred[-1] <= voltage_thresh_high:
            category = 0 # Change from liberal to conservative if volt driops below low threshold

    #-----
    # Thermal histeresis bands
    #-----

    if category == 1: # Agressive
        T_on = T_max - 5 # T_std + 0.5*(T_max-T_std)
        T_off = T_max
    else: # Conservative
        T_on = T_std - 5
        T_off = T_std # T_min + 0.5*(T_std-T_min)

    #-----
    # Control actions
    #-----

    # 1. Turn ON if it is OFF and temp below T_on
    if h_state == 0 and T <= T_on:
        h_state_new = 1

    # 2. Turn OFF if it is ON and temp drops below T_off
    elif h_state == 1 and T >= T_off:
        h_state_new = 0

    # # 3. Turn ON if flow and temp below T_std
    # if F > 0 and T < T_std:
    #     h_state_new = 1

    #-----
    # Thermal model
    #-----

    flow_enrg = Cv*rho*F*(T_in - T)
    element_enrg = Q*h_state_new
    conduction_enrg = U*A*(T - T_amb)

    T_new = (del_t/(Cv*rho*Volume))*(flow_enrg + element_enrg - conduction_enrg) + T

    return T_new, h_state_new, category




