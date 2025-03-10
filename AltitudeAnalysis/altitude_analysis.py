# Lucas Calderon
# 14/02/2025
# I want to try and find the ideal altitude for a spacecraft to orbit in orer to get the maximum surplus of air mass flow rate.
# Let's also find the optimal Isp and Thrust values, maybe relating them to power consumption.



# WHAT WAS FOUND:
# As long as 2*Isp*g0*eff_intake > V_orbital*C_D, the lower you go the higher surplus you can get.
# No surprise there, but it's good to have a confirmation.

# Power is probably the biggest limiting factor


# NEXT STEPS: 

# Power limitations
# Implement power requirements as a function of the orbit
# Check if that power is achievable

# Heat limitations
# Implement heat rejection vs intake as a function of the orbit



# Import the necessary libraries
import numpy as np
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from plot_performance import plot_time_vs_massflow, plot_power_vs_altitude
from classes import Regime
from spacecraft import spacecraft

# Problem constants

earth = {
    'R': 6371,  # Earth radius in km
    'mu': 3.986e5,  # Earth gravitational parameter in km^3/s^2
    'g0': 9.81,  # Standard gravity in m/s^2
    'SolarFlux': 1361  # Solar constant in W/m^2
}


# Calculate Drag
def Get_Drag(Regime:Regime, sc_parameters:dict) -> np.ndarray:
    return 0.5 * Regime.atmos() * Regime.v_circ()**2 * sc_parameters['A_ref'] * sc_parameters['C_D']


# Calculate the mass flow rate gain for an array of altitudes
def Getm_gain(Regime:Regime, sc_parameters:dict) -> tuple:

    """
    This function calculates the MASS FLOW gain of the spacecraft at a certain altitude.
    The function assumes a circular orbit for simplicity. 
    It also assumes that the intake area and drag reference area are the same.
    It also assumes that the earth is perfectly spherical.
    It also assumes that the longitude and latitude are 0 degrees.
    It also assumes that the date is 01 Jan 2000.

    INPUTS:
        h: altitudes in km. This is a one dimensional array.
        sc_parameters: dictionary with the spacecraft parameters.
        earth_parameters: dictionary with the Earth parameters.

    OUTPUTS:
        m_gain: the mass flow rate gain in kg/s. This is a one dimensional array.
        m_in: the intake mass flow rate in kg/s. This is a one dimensional array.
        m_out: the thruster mass flow rate in kg/s. This is a one dimensional array.
    """

    # Unpack the spacecraft parameters
    A = sc_parameters['A_intake']
    eff_intake = sc_parameters['eff_intake']
    C_D = sc_parameters['C_D']
    Isp = sc_parameters['Isp']

    # Unpack the Earth parameters
    g0 =  Regime.earth_params['g0']

    # Calculate regime paramters
    V = Regime.v_circ() # In m/s
    rho = Regime.atmos() # In kg/m^3

    # Calculate the intake mass flow rate
    m_in = A * eff_intake * V * rho

    # Calculate the mass flow rate necessary for sustaining flight
    m_out = Get_Drag(Regime, sc_parameters) / (Isp * g0)

    # Calculate the mass flow rate gain
    m_gain = m_in - m_out

    return m_gain, m_in, m_out


# How low can I fly?
def Get_minAlts(Regime:Regime, sc_parameters:dict) -> tuple:
    """
    This function calculates the minimum altitude at which the spacecraft can fly, based on drag and heating.
    It calculates at which altitude the drag force is equal to the thrust force.
    It calculates at which altitude the heating rate is equal to the heat rejection rate.
    It assumes simplified models for drag and heating. It also assumes no lift to help the spacecraft maintian its altitude.
    It also assumes everything assumed by the Getm_gain function.

    INPUTS:
        h: altitudes in km. This is a one dimensional array.
        sc_parameters: dictionary with the spacecraft parameters.
        earth_parameters: dictionary with the Earth parameters.

    OUTPUTS:
        h_drag: the minimum altitude due to drag in km.
        h_heat: the minimum altitude due to heating in km.
    """

    # Unpack the spacecraft parameters
    T = sc_parameters['T_max']
    Q_rejection = sc_parameters['Q_rejection']

    # Extract the point at which the drag force is equal to the thrust force
    h_drag = h[np.argmax(Get_Drag(Regime, sc_parameters) < T)]

    # Calculate the heating rate WORK IN PROGRESS
    Q_heating = 0

    # Extract the point at which the heating rate is equal to the heat rejection rate
    h_heat = h[np.argmax(Q_heating < Q_rejection)]

    return h_drag, h_heat


# Power Thrust and Isp relations
def Get_PowReq(Regime:Regime, sc_parameters:dict) -> np.ndarray:
    """
    This function calculates the propulsive requirements for the spacecraft at a certain altitude.
    It calculates the power required by the propulsion system to maintain the orbit, the solar panel area required, the thrust required and the specific impulse required.
    It assumes everything assumed by the Getm_gain function.
    It assumes that the thruster power is equal to the power of the exhaust gases.

    INPUTS:
        h: altitudes in km. This is a one dimensional array.
        sc_parameters: dictionary with the spacecraft parameters.
        earth_parameters: dictionary with the Earth parameters.

    OUTPUTS:
        P_req_prop: the power required by the propulsion system to maintain the orbit in W.
        A_solar: the solar panel area required in m^2.

    """

    # Unpack the spacecraft parameters
    eff_sol = sc_parameters['eff_solar']

    # Calculate the required mass flow rate
    m_out = Getm_gain(Regime, sc_parameters)[2]

    # Calculate the minimum power required
    P_req_prop = 0.5 * m_out * Regime.v_circ()**2

    # Calculate the solar panel area required
    Flux = Regime.earth_params['SolarFlux']
    A_solar = P_req_prop / eff_sol / Flux / np.cos(67.5)  # cosine comes from average incidence angle over an orbit

    return P_req_prop, A_solar



if __name__ == '__main__':

    # Create an array of altitudes
    h = np.linspace(70, 300, 1000)

    # Create a Regime object
    regime = Regime(h, earth)

    # Calculate the mass flow rate gain
    m_gain, m_in, m_out = Getm_gain(regime, spacecraft)

    # Normalize with respoect to intake area, and convert to kg/hour
    m_gain = m_gain / spacecraft['A_intake'] * 3600
    m_in = m_in / spacecraft['A_intake'] * 3600
    m_out = m_out / spacecraft['A_intake'] * 3600

    # Calculate the minimum altitudes
    h_drag, h_heat = Get_minAlts(regime, spacecraft)

    # Calculate the Power requirements
    P_req, A_solar = Get_PowReq(regime, spacecraft)

    # Calculate the time for refueling
    tank_load = spacecraft['Tank_load']  # Tank load in kg
    time = tank_load / m_gain # Time in seconds
    time = time / 24 # Time in days

    # Apply element-wise logical AND to create a boolean mask
    mask = np.logical_and(h > h_drag, h > h_heat)

    # Filter the m_gain and h arrays using the mask
    m_crop = m_gain[mask]
    h_crop = h[mask]  # Need to filter h too

    # Find the max mass flow rate and corresponding height
    if len(m_crop) > 0:  # Ensure there are valid values
        idx_max = np.argmax(m_crop)
        h_max = h_crop[idx_max]
        m_max = m_crop[idx_max]
    else:
        h_max = None
        m_max = None  # Handle the case where no valid values exist

    # Print the results
    print('The maximum mass flow rate gain is:', m_max * 3600, 'kg/hour')
    print('The altitude at which this occurs is:', h_max, 'km')

    # Plot the results
    plot_time_vs_massflow(h, m_gain, m_in, m_out, time, h_drag, h_heat)
    plot_power_vs_altitude(h, P_req, A_solar, h_drag, h_heat)