# Lucas Calderon
# 15/03/2025
# This file will do an analysis of time needed to refuel based on spacecraft parameters and altitude.

# Import the necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Import own libraries
from altitude_analysis import Get_Drag
from spacecraft import spacecraft
from classes import Regime

# Constants
earth = {
    'R': 6371,  # Earth radius in km
    'mu': 3.986e5,  # Earth gravitational parameter in km^3/s^2
    'g0': 9.81,  # Standard gravity in m/s^2
    'SolarFlux': 1361  # Solar constant in W/m^2
}

# Refuel time function
def time_refuel(Regime:Regime, spaceraft:dict, PLOT:bool=False) -> np.ndarray:

    # Unpack constants
    m_tank = spacecraft['Tank_load']
    eff_intake = spacecraft['eff_intake']
    A_intake = spacecraft['A_intake']
    T_max = spacecraft['T_max']
    Isp = spacecraft['Isp']
    g0 = spacecraft['g0']
    ve = Isp * g0

    # Calculate the drag over the regime
    D = Get_Drag(Regime, spacecraft)

    # Calculate the T=D point
    h_drag = Regime.h[np.argmax(D < T_max)]

    # Calculate the density
    rho = Regime.atmos()

    # Calculate the orbital velocity
    V = Regime.v_circ()

    # Calculate the time to refuel
    time = m_tank / (A_intake * eff_intake * V * rho - D / ve) / 3600 / 24 # In days

    if PLOT:
        # Create the plot
        fig, ax1 = plt.subplots()

        # Plot the refueling time
        ax1.plot(Regime.h, time, label='Refueling time', color='#FE6100', linestyle=':')
        ax1.set_yscale('log')
        ax1.set_xlabel('Altitude ($km$)')
        ax1.set_ylabel('Time to refuel ($days$)')
        ax1.tick_params(axis='y')
        ax1.tick_params(axis='x')

        # Add vertical lines for the minimum altitudes
        ax1.axvline(h_drag, color='magenta', linestyle='--', label='Limit: T < D')

        # Legends
        ax1.legend(loc='upper left', bbox_to_anchor=(0.6, 0.75))

        plt.title('Refueling Time vs Altitude')

        plt.show()

    return time


# Refueling analysis
def time_analysis(Regime:Regime, spacecraft:dict, Isp:np.ndarray, T_max:np.ndarray, PLOT:bool=False) -> np.ndarray:

    # Unpack constants
    m_tank = spacecraft['Tank_load']
    eff_intake = spacecraft['eff_intake']
    A_intake = spacecraft['A_intake']
    ve = Isp * spacecraft['g0']

    # Calculate atmospheric properties
    Ds = Get_Drag(Regime, spacecraft)
    rhos = Regime.atmos()
    Vs = Regime.v_circ()

    # Store time list
    time = np.zeros((len(Isp), len(T_max)))

    for i, ve in enumerate(ve):
        for j, thrust in enumerate(T_max):

            # Calculate the T=D point
            idx = np.argmax(Ds < thrust)
            h_drag = Regime.h[idx]

            # Get the corresponding rho and V
            rho = rhos[idx]
            V = Vs[idx]

            # Calculate the time to refuel
            time[i, j] = m_tank / (A_intake * eff_intake * V * rho - thrust / ve) / 3600 / 24 # In days

    if PLOT:

        # Create the colormap plot
        fig, ax1 = plt.subplots()

        # Main colormap plot
        c = ax1.pcolormesh(T_max, Isp, time, shading='auto', 
                            norm=mcolors.LogNorm(vmin=10, vmax=1000), cmap='viridis')

        # Define contour levels (equal time lines)
        contour_levels = [50, 75, 100, 150, 200, 300, 500, 800]  # Adjust based on your data range

        # Plot contour lines
        contours = ax1.contour(T_max, Isp, time, levels=contour_levels, colors='red', linewidths=1)

        # Add labels to contour lines
        ax1.clabel(contours, fmt='%d days', inline=True, fontsize=8, inline_spacing=5, colors='white')

        # Labels and formatting
        ax1.set_ylabel('Specific impulse $(s)$')
        ax1.set_xlabel('Thrust $(N)$')
        ax1.tick_params(axis='y')
        ax1.tick_params(axis='x')
        fig.colorbar(c, ax=ax1, label='Time to refuel $(days)$')

        plt.title('Refueling Time vs Isp and Thrust')
        plt.show()

    return time



if __name__ == '__main__':
    # Create the regime
    h = np.linspace(70, 300, 1000)
    regime = Regime(h, earth)

    # Analyze the time to refuel
    T_max = np.linspace(0.5, 10, 2000)
    Isp = np.linspace(1800, 5000, 2000)
    time = time_analysis(regime, spacecraft, Isp, T_max, PLOT=True)