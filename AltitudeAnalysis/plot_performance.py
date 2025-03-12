import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import mpl_style


# Plotting functions

def plot_time_vs_massflow(h:np.ndarray, m_gain:np.ndarray, m_in:np.ndarray, m_out:np.ndarray, time:np.ndarray,
                           h_drag:float, h_heat:float, SAVEPATH:str=None):
    # Create the plot
    fig, ax1 = plt.subplots()


    # Plot mass flow rates on the left y-axis
    ax1.plot(h, m_gain, label='Mass flow rate gain'    )
    ax1.plot(h, m_in  , label='Intake mass flow rate'  )
    ax1.plot(h, m_out , label='Thruster mass flow rate')
 
    ax1.set_yscale('log')
    ax1.set_xlabel('Altitude ($km$)')
    ax1.set_ylabel('Mass flow rate ($kg/hour$)')
    ax1.tick_params(axis='y')
    ax1.tick_params(axis='x')

    # Create the second y-axis
    ax2 = ax1.twinx()
    ax2.plot(h, time, label='Refueling time', color='#FE6100', linestyle=':')
    ax2.set_yscale('log')
    ax2.set_ylabel('Time to refuel ($days$)')
    ax2.tick_params(axis='y')

    # Add vertical lines for the minimum altitudes
    ax1.axvline(h_drag, color='magenta', linestyle='--', label='Limit: T < D')
    ax1.axvline(h_heat, color='lime', linestyle='--', label='Limit: Overheating')

    # Legends
    ax1.legend(loc='upper left', bbox_to_anchor=(0.6, 0.75))
    ax2.legend(loc='upper left', bbox_to_anchor=(0.6, 0.45))

    plt.title('Mass Flow Rate Per Intake Unit Area and Refueling Time vs Altitude')

    if SAVEPATH is not None:
        plt.savefig(SAVEPATH)

    else:
        plt.show()


def plot_power_vs_altitude(h:np.ndarray, P_req:np.ndarray, A_solar:np.ndarray,
                            h_drag:float, h_heat:float, SAVEPATH:str=None):
    # Create the plot for the power requirements
    fig, ax1 = plt.subplots()

    # Plot mass flow rates on the left y-axis
    ax1.plot(h, P_req, label='Minimum required power')

    ax1.set_yscale('log')
    ax1.set_xlabel('Altitude (km)')
    ax1.set_ylabel('Required power $(W)$')
    ax1.tick_params(axis='y')

    # Create the second y-axis
    ax2 = ax1.twinx()
    ax2.plot(h, A_solar, label='Required solar panel area')
    ax2.set_yscale('log')

    ax2.set_ylabel('Required solar panel area $(m^2)$')
    ax2.tick_params(axis='y')

    # Add lines for the minimum altitudes
    ax1.axvline(h_drag, color='magenta', linestyle='--', label='Limit: T < D')
    ax1.axvline(h_heat, color='lime', linestyle='--', label='Limit: Overheating')
    # ax1.axvline(h_max, color='k', linestyle='--', label='Altitude of max gain')

    # Legends
    ax1.legend(loc='upper left', bbox_to_anchor=(0.55, 0.95))
    ax2.legend(loc='upper left', bbox_to_anchor=(0.55, 0.75))

    plt.title('Power Requirements vs Altitude')
    plt.grid()

    if SAVEPATH is not None:
        plt.savefig(SAVEPATH)
    
    else:
        plt.show()


def plot_power_vs_time(P_req:np.ndarray, time:np.ndarray,
                        t_min:float, SAVEPATH=None):
    # Create the plot for the power requirements
    fig, ax1 = plt.subplots()

    # Plot time
    ax1.plot(time, P_req, label='Power vs Time')

    ax1.set_yscale('log')
    ax1.set_xscale('log')
    ax1.set_xlabel('Time $(days)$')
    ax1.set_ylabel('Required power $(W)$')
    ax1.tick_params(axis='y')
    ax1.tick_params(axis='x')

    # Add lines for the minimum altitudes
    # ax1.axvline(t_min, color='magenta', linestyle='--', label='Minimum refueling time')

    # Legends
    ax1.legend(loc='upper left', bbox_to_anchor=(0.55, 0.95))

    plt.title('Power Requirements vs Time')

    if SAVEPATH is not None:
        plt.savefig(SAVEPATH)
    
    else:
        plt.show()

