# Lucas Calderon
# 15/03/2025
# This file will do an analysis of time and power needed to refuel and based on spacecraft parameters.
# It can be run as a standalone script or imported as a module.
# It can be used to produce qualitative plots or to analyze an actual spacecraft.

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


# Refueling analysis
def time_analysis(Regime:Regime, spacecraft:dict, Isp:np.ndarray, T_max:np.ndarray, PLOT:bool=False) -> np.ndarray:

    # Unpack constants
    m_tank = spacecraft['Tank_load']
    eff_intake = spacecraft['eff_intake']
    A_intake = spacecraft['A_intake']
    ve = Isp * spacecraft['g0']

    # Calculate atmospheric properties
    D = Get_Drag(Regime, spacecraft) # Shape (k, ) k being the ln(h) of the regime object
    rho = Regime.atmos()
    V = Regime.v_circ()

    # Vectorized calculation
    # Indices where the thrust is higher than the drag
    idxs = np.argmax(D[None, :] <= T_max[:, None], axis=1)

    # Get the corresponding rho and V
    rho = rho[idxs]
    V = V[idxs]

    # Calculate the time to refuel
    V_rho = V * rho
    thrust_ve = T_max[None, :] / ve[:, None]

    time = m_tank / (A_intake * eff_intake * V_rho - thrust_ve) / 3600 / 24 # In days

    if PLOT:

        # Calculate countour lines
        contour_levels = [40, 50, 60, 80, 100, 150, 300, 500, 800, 1500, 4000]

        fig, ax1 = plt.subplots()

        # Use filled contour plot for smoother appearance
        c = ax1.imshow(time, extent=[T_max.min(), T_max.max(), Isp.min(), Isp.max()],
               origin='lower', cmap='viridis', aspect='auto', 
               norm=mcolors.LogNorm(vmin=40, vmax=2000))

        # Add contour lines on top for readability
        contours = ax1.contour(T_max, Isp, time, levels=contour_levels, colors='black', linewidths=1)
        ax1.clabel(contours, fmt='%d days', inline=True, fontsize=8, inline_spacing=10, colors='black', manual=True)

        # Labels and formatting
        ax1.set_ylabel('Specific Impulse (s)')
        ax1.set_xlabel('Thrust (N)')
        fig.colorbar(c, ax=ax1, label='Time to Refuel (days)')

        plt.title('Refueling Time vs Isp and Thrust')
        plt.show()

    return time


# Power analysis
def power_analysis(spacecraft:dict, Isp:np.ndarray, T_max:np.ndarray, PLOT:bool=False) -> np.ndarray:

    # Unpack constants
    n_prop = spacecraft['n_prop']
    g0 = spacecraft['g0']
    ve = Isp * g0

    # Calculate the power
    power = T_max[None, :] * ve[:, None] / (2 * n_prop)

    if PLOT:

        # Convert to kW
        power = power / 1000

        # Calculate countour lines
        contour_levels = [1, 5, 10, 15, 20, 30, 50, 70, 100, 150, 200, 300, 500, 1000, 1500]

        fig, ax1 = plt.subplots()

        # Use filled contour plot for smoother appearance
        c = ax1.imshow(power, extent=[T_max.min(), T_max.max(), Isp.min(), Isp.max()],
               origin='lower', cmap='viridis', aspect='auto', 
               norm=mcolors.LogNorm(vmin=1, vmax=500))

        # Add contour lines on top for readability
        contours = ax1.contour(T_max, Isp, power, levels=contour_levels, colors='black', linewidths=1)
        ax1.clabel(contours, fmt='%d kW', inline=True, fontsize=8, inline_spacing=10, colors='black', manual=True)

        # Labels and formatting
        ax1.set_ylabel('Specific Impulse (s)')
        ax1.set_xlabel('Thrust (N)')
        fig.colorbar(c, ax=ax1, label='Power (kW)')

        plt.title('Power vs Isp and Thrust')
        plt.show()


    return power


if __name__ == '__main__':
    # Create the regime
    h = np.linspace(70, 500, 50000)
    regime = Regime(h, earth)

    # Analyze the time to refuel
    T_max = np.linspace(0, 10, 1000) # Thrust in N
    Isp = np.linspace(1500, 5000, 1000) # Specific impulse in s
    time = time_analysis(regime, spacecraft, Isp, T_max, PLOT=True)
    power = power_analysis(spacecraft, Isp, T_max, PLOT=True)