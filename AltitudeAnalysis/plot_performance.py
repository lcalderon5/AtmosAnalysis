import matplotlib.pyplot as plt
import numpy as np

# Plot the results

def plot_time_vs_massflow(h, m_gain, m_in, m_out, time, h_drag, h_heat):
    # Create the plot
    fig, ax1 = plt.subplots(figsize=(12, 7))

    colors = {
    "m_gain": "#1f77b4",  # Muted blue
    "m_in": "#2ca02c",    # Deep green
    "m_out": "#d62728",   # Deep red
    "time": "#e5a46c",    # Orange
    "h_drag": "#9467bd",  # Purple for altitude limit
    "h_heat": "#8c564b",  # Brown for overheating limit
    }

    # Plot mass flow rates on the left y-axis
    ax1.plot(h, m_gain, label='Mass flow rate gain'    , color=colors['m_gain'], linewidth=1.5)
    ax1.plot(h, m_in  , label='Intake mass flow rate'  , color=colors['m_in']  , linewidth=1.5)
    ax1.plot(h, m_out , label='Thruster mass flow rate', color=colors['m_out'] , linewidth=1.5)
 
    ax1.set_yscale('log')
    ax1.set_xlabel('Altitude ($km$)', fontsize=16)
    ax1.set_ylabel('Mass flow rate ($kg/hour/m^2$)', fontsize=16)
    ax1.tick_params(axis='y', labelsize=16)
    ax1.tick_params(axis='x', labelsize=16)

    # Create the second y-axis
    ax2 = ax1.twinx()
    ax2.plot(h, time, label='Refueling time', color=colors['time'], linewidth=1.5)
    ax2.set_yscale('log')

    ax2.set_ylabel('Time to refuel ($days/m^2$)', fontsize=16)
    ax2.tick_params(axis='y', labelsize=16)

    # Add vertical lines for the minimum altitudes
    # ax1.axvline(h_drag, color='magenta', linestyle='--', label='Altitude limit due to Thrust < Drag')
    # ax1.axvline(h_heat, color='lime', linestyle='--', label='Min altitude due to overheating')
    # ax1.axvline(h_max, color='k', linestyle='--', label='Altitude of max gain')

    # Legends
    ax1.legend(loc='upper left', bbox_to_anchor=(0.6, 0.7), fontsize=16)
    ax2.legend(loc='upper left', bbox_to_anchor=(0.6, 0.48), fontsize=16)

    ax1.grid(axis='both')
    # plt.title('Mass Flow Rate Per Intake Unit Area and Refueling Time vs Altitude')
    plt.show()


def plot_power_vs_altitude(h, P_req, A_solar, h_drag, h_heat):
# Create the plot for the power requirements
    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Plot mass flow rates on the left y-axis
    ax1.plot(h, P_req, label='Minimum required power', color='r')

    ax1.set_yscale('log')
    ax1.set_xlabel('Altitude (km)')
    ax1.set_ylabel('Required power (W)')
    ax1.tick_params(axis='y')

    # Create the second y-axis
    ax2 = ax1.twinx()
    ax2.plot(h, A_solar, label='Required solar panel area', color='r')
    ax2.set_yscale('log')

    ax2.set_ylabel('Required solar panel area (m^2)')
    ax2.tick_params(axis='y')

    # Add lines for the minimum altitudes
    ax1.axvline(h_drag, color='magenta', linestyle='--', label='Altitude limit due to Thrust < Drag')
    ax1.axvline(h_heat, color='lime', linestyle='--', label='Min altitude due to overheating')
    # ax1.axvline(h_max, color='k', linestyle='--', label='Altitude of max gain')

    # Legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.title('Power Requirements vs Altitude')
    plt.grid()
    plt.show()
