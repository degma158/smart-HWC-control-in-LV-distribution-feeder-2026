import matplotlib.pyplot as plt
import numpy as np

# HWC physicallity check plot function
def single_house_check_plot(h, time_vector, V, I, state, T, enrg_in, enrg_out, F, P_supply, P_demand):
    plt.figure(figsize=(12,8))

    plt.subplot(3,3,1)
    plt.plot(time_vector, V)
    plt.xlabel('Time (min)')
    plt.ylabel('Voltage (V)')
    plt.title('HouseholdVoltage Profile')
    plt.grid(True)

    plt.subplot(3,3,2)
    plt.plot(time_vector, I)
    plt.xlabel('Time (min)')
    plt.ylabel('Current (A)')
    plt.title('Household Current')
    plt.grid(True)

    plt.subplot(3,3,3)
    plt.plot(time_vector, F)
    plt.xlabel('Time (min)')
    plt.ylabel('Flow (m3/s)')
    plt.title('Hot Water Demand Flow')
    plt.grid(True)

    plt.subplot(3,3,4)
    plt.plot(time_vector, T)
    plt.xlabel('Time (min)')
    plt.ylabel('Temperature (°C)')
    plt.title('Cylinder Temperature')
    plt.grid(True)

    plt.subplot(3,3,5)
    plt.plot(time_vector, state)
    plt.xlabel('Time (min)')
    plt.ylabel('Heater State (0/1)')
    plt.title('Element State')
    plt.grid(True)

    plt.subplot(3,3,6)
    plt.plot(time_vector, enrg_in, label='In')
    plt.plot(time_vector, enrg_out, label='Out')
    plt.xlabel('Time (min)')
    plt.ylabel('Energy (kJ)')
    plt.title('Energy Balance')
    plt.legend()
    plt.grid(True)

    plt.subplot(3,3,8)
    plt.plot(time_vector[:], P_supply, label='Supply')
    plt.plot(time_vector[:], P_demand[:], label='Demand')
    plt.xlabel('Time (min)')
    plt.ylabel('Power (kW)')
    plt.title('Household Load Profile')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def single_house_ctrl_check_plot(title, 
    h, time_vector, V, I, state, T,
    enrg_in, enrg_out, F,
    P_supply, P_demand, ctrl_signal, volt_thresh_high, 
    volt_thresh_low, curr_thresh_high, curr_thresh_low
):

    plt.figure(figsize=(12, 12))
    plt.suptitle(str(title))

    plt.subplot(4, 2, 1)
    plt.plot(time_vector, V)
    if volt_thresh_high != 0:
        plt.axhline(y=volt_thresh_high, color='r', linestyle='--', label='High voltage threshold')
    if volt_thresh_low != 0:
        plt.axhline(y=volt_thresh_low, color='r', linestyle='--', label='Low voltage threshold')
    plt.xlabel('Time (min)')
    plt.ylabel('Voltage (V)')
    plt.title('Household Voltage Profile')
    plt.grid(True)
    plt.legend()   

    plt.subplot(4, 2, 3)
    plt.plot(time_vector, I)
    if curr_thresh_low != 0:
        plt.axhline(y=curr_thresh_low, color='r', linestyle='--', label='Low current threshold')
    if curr_thresh_high != 0:
        plt.axhline(y=curr_thresh_high, color='r', linestyle='--', label='High current threshold')
    plt.xlabel('Time (min)')
    plt.ylabel('Current (A)')
    plt.title('Household Current')
    plt.legend()
    plt.grid(True)

    plt.subplot(4, 2, 7)
    plt.plot(time_vector, F)
    plt.xlabel('Time (min)')
    plt.ylabel('Flow (m³/s)')
    plt.title('Hot Water Demand Flow')
    plt.grid(True)

    plt.subplot(4, 2, 2)
    plt.plot(time_vector, T)
    plt.xlabel('Time (min)')
    plt.ylabel('Temperature (°C)')
    plt.title('Cylinder Temperature')
    plt.grid(True)

    plt.subplot(4, 2, 6)
    plt.plot(time_vector, state)
    plt.xlabel('Time (min)')
    plt.ylabel('Heater State (0/1)')
    plt.title('Element State')
    plt.grid(True)

    plt.subplot(4, 2, 4)
    plt.plot(time_vector, enrg_in, label='In')
    plt.plot(time_vector, enrg_out, label='Out')
    plt.xlabel('Time (min)')
    plt.ylabel('Energy (kJ)')
    plt.title('Energy Balance')
    plt.legend()
    plt.grid(True)

    plt.subplot(4, 2, 5)
    plt.plot(time_vector, P_supply, label='Supply')
    plt.plot(time_vector, P_demand, label='Demand')
    plt.xlabel('Time (min)')
    plt.ylabel('Power (kW)')
    plt.title('Household Load Profile')
    plt.legend()
    plt.grid(True)

    if np.any(ctrl_signal != 0):
        plt.subplot(4, 2, 8)
        plt.plot(time_vector, ctrl_signal)
        plt.xlabel('Time (min)')
        plt.ylabel('Signal')
        plt.title('Conservative vs liberal signal')
        plt.grid(True)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.6, wspace=0.4)
    plt.show()