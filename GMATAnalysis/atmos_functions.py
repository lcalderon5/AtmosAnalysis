# Lucas Calderon
# 02/02/2025

import os
import sys

# Add the parent directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import numpy as np
import pymsis as msis
from datetime import datetime

from spacecraft import spacecraft

# ----------- ATMOSPHERE FUNCTIONS ------------
def GetComposition(data: dict) -> dict:
    """
    This function will return the composition of the atmosphere at the given position points.

    Inputs:
        data: dictionary with the input data for the atmosphere model, containing at least the following:
            - 'altitude': list of altitudes (in km)
            - 'latitude': list of latitudes (in degrees)
            - 'longitude': list of longitudes (in degrees)
            - 'date': list of datetime objects

    Returns:
        composition: dictionary with the composition of the atmosphere at the given positions, containing numpy arrays:
            - 'rho': list of air density values (in kg/m^3)
            - 'N2': list of N2 number density values (in m^-3)
            - 'O2': list of O2 number density values (in m^-3)
            - 'O': list of O number density values (in m^-3)  
            - 'He': list of He number density values (in m^-3)
            - 'H': list of H number density values (in m^-3)
            - 'Ar': list of Ar number density values (in m^-3)
            - 'N': list of N number density values (in m^-3)
            - 'AnomalousO': list of Anomalous O number density values (in m^-3)
            - 'NO': list of NO number density values (in m^-3)
            - 'T': list of temperature values (in K)
        """

    # Extract relevant data from the dictionary, converting lists to NumPy arrays
    alts = np.array(data['altitude'])
    lats = np.array(data['latitude'])
    lons = np.array(data['longitude'])
    et = np.array(data['date'])

    # Obtain atmospheric composition (outputs a numpy array of size len(et) x 11)
    print('Calculating atmospheric composition...')
    composition_data = msis.calculate(et, lons, lats, alts)  # Adjust solar activity as needed
    print('Composition calculation complete!')

    # Replace nan entries by 0
    composition_data = np.nan_to_num(composition_data)

    # Create a dictionary with the composition of the atmosphere
    composition = {
        'rho':        composition_data[:, 0],  # In kg/m^3
        'N2':         composition_data[:, 1],  # Number density in m^-3
        'O2':         composition_data[:, 2],  # Number density in m^-3
        'O':          composition_data[:, 3],   # Number density in m^-3
        'He':         composition_data[:, 4],  # Number density in m^-3
        'H':          composition_data[:, 5],   # Number density in m^-3
        'Ar':         composition_data[:, 6],  # Number density in m^-3
        'N':          composition_data[:, 7],   # Number density in m^-3
        'AnomalousO': composition_data[:, 8],  # Number density in m^-3
        'NO':         composition_data[:, 9],  # Number density in m^-3
        'T':          composition_data[:, 10]   # In K
    }      

    return composition


# ----------- MASS FLOW FUNCTIONS ------------
def GetMassFlow(states:dict, composition:dict, h_max:float=None) -> tuple[dict, dict]:
    """
    This function calculates the mass flow rate and total mass captured by the spacecraft.

    Inputs:
        states: dictionary with the data from the spacecraft simulation.
        composition: dictionary with the composition of the atmosphere at the spacecraft positions.
        h_max: maximum altitude for the intake to be active (in km). If None, the intake is always active. 
            This is basically equivalent to turning off the intake at a certain altitude.

    Returns:
        m_dot: dictionary with the mass flow rates of each component at each location.
        m_total: dictionay with the total mass captured by the spacecraft of each component.
    """

    # Extract data
    altitudes = states['altitude']  # In km
    velocities = states['velocity']  # In m/s
    elapsed_seconds = states['elapsed_seconds'] # In seconds

    # Create effective area array based on altitude, this is like turning on and off the intake at a certain altitude
    if h_max is None:
        A_intake_eff = spacecraft['A_intake']
    elif h_max < 70:
        raise ValueError('The maximum altitude for the intake to be active must be above 70 km to be realistic.')
    else:
        A_intake_eff = np.where(altitudes < h_max, spacecraft['A_intake'], 0)

    # Calculate the mass flow rate for each component
    m_dot = {
        'rho':        composition['rho'] *        A_intake_eff * spacecraft['eff_intake'] * velocities,  # In kg/s
        'N2':         composition['N2']  *        A_intake_eff * spacecraft['eff_intake'] * velocities,  # In particles/s
        'O2':         composition['O2']  *        A_intake_eff * spacecraft['eff_intake'] * velocities,  # In particles/s
        'O':          composition['O']   *        A_intake_eff * spacecraft['eff_intake'] * velocities,  # In particles/s
        'He':         composition['He']  *        A_intake_eff * spacecraft['eff_intake'] * velocities,  # In particles/s
        'H':          composition['H']   *        A_intake_eff * spacecraft['eff_intake'] * velocities,  # In particles/s
        'Ar':         composition['Ar']  *        A_intake_eff * spacecraft['eff_intake'] * velocities,  # In particles/s
        'N':          composition['N']   *        A_intake_eff * spacecraft['eff_intake'] * velocities,  # In particles/s
        'AnomalousO': composition['AnomalousO'] * A_intake_eff * spacecraft['eff_intake'] * velocities,  # In particles/s
        'NO':         composition['NO']  *        A_intake_eff * spacecraft['eff_intake'] * velocities   # In particles/s
    }

    # Calculate the total mass captured for each component by integrating the mass flow rate over time
    m_total = {
        'rho':        np.trapz(m_dot['rho'], x=elapsed_seconds),  # In kg
        'N2':         np.trapz(m_dot['N2'], x=elapsed_seconds),   # In particles
        'O2':         np.trapz(m_dot['O2'], x=elapsed_seconds),   # In particles
        'O':          np.trapz(m_dot['O'], x=elapsed_seconds),    # In particles
        'He':         np.trapz(m_dot['He'], x=elapsed_seconds),   # In particles
        'H':          np.trapz(m_dot['H'], x=elapsed_seconds),    # In particles
        'Ar':         np.trapz(m_dot['Ar'], x=elapsed_seconds),   # In particles
        'N':          np.trapz(m_dot['N'], x=elapsed_seconds),    # In particles
        'AnomalousO': np.trapz(m_dot['AnomalousO'], x=elapsed_seconds),  # In particles
        'NO':         np.trapz(m_dot['NO'], x=elapsed_seconds)    # In particles
    }

    return m_dot, m_total


# ----------- TESTING ------------
if __name__ == '__main__':

    # Test the atmosphere functions
    date = datetime(2025, 1, 1, 0, 0, 0)
    test_data = {
        'altitude': np.arange(0, 1000, 1),  # In km
        'latitude': np.zeros((1000)),  # In degrees
        'longitude': np.zeros((1000)),  # In degrees
        'date': [date] * 1000  # Dummy date
    }

    composition = GetComposition(test_data)

    # Reference exponential model for air density
    control = 1.225 * np.exp(-test_data['altitude'] / 8)  # kg/m^3

    # Plot density vs altitude
    import matplotlib.pyplot as plt
    plt.plot(composition['rho'], test_data['altitude'])
    plt.plot(control, test_data['altitude'])
    plt.axhline(y=100, color='r', linestyle='--')
    plt.xscale('log')
    plt.xlabel('Air Density (kg/m^3)')
    plt.ylabel('Altitude (km)')
    plt.title('Air Density vs. Altitude')
    plt.show()