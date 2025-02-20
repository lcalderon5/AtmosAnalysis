# Lucas Calderon
# 14/02/2025
# I want to try and find the ideal altitude for a spacecraft to orbit in orer to find the maximum surplus of air mass flow rate.
# Let's also find the optimal Isp and Thrust values, maybe relating them to power consumption.



# WHAT WAS FOUND:
# As long as Isp*g0*eff_intake > V_orbital, the lower you go the higher surplus you can get.
# No surprise there, but it's good to have a confirmation.

# Thrust is probably the biggest limiting factor

# NEXT STEPS: 

# Power limitations
# Implement power requirements as a function of the orbit
# Check if that power is achievable

# Heat limitations
# Implement heat rejection vs intake as a function of the orbit



# Import the necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import pymsis as msis

from plotting import plot_time_vs_massflow, plot_power_vs_altitude

# Problem constants
spacecraft = {
    'A_intake': 9,  # Intake area in m^2
    'eff_intake': 0.6,  # Intake efficiency, unitless
    'C_D': 2.2,  # Drag coefficient, unitless
    'Isp': 4200,  # Specific impulse in s
    'T_max': 5,  # Thrust in N
    'Q_rejection': 1e6,  # Heat rejection rate in W (I HAVE NO IDEA WHAT THIS VALUE SHOULD BE)
    'P_max': 1000,  # Maximum power consumption in W
    'eff_solar': 0.2,  # Solar panel efficiency, unitless
    'Tank_load': 2000  # Tank load in kg
}

earth = {
    'R': 6371,  # Earth radius in km
    'mu': 3.986e5,  # Earth gravitational parameter in km^3/s^2
    'g0': 9.81  # Standard gravity in m/s^2
}


# Calculate the atmospheric density for an array of altitudes
def Get_Rho(h: np.ndarray, full=False) -> np.ndarray:
    """
    This function will return the composition of the atmosphere at the given position points.
    It uses the NRLMSIS model to calculate the atmospheric density at the given altitudes.

    Inputs:
        h: altitudes in km. This is a one dimensional array.
        full: boolean flag to return the full composition or just the air density. Default is False.

    Outputs:
        rho: one dimensional array of air density values (in kg/m^3)
        OR
        composition_data: dictionary of atmospheric composition values (in kg/m^3)
        """

    # Create lists for et, lons, and lats
    et = np.array([np.datetime64('2000-01-01T00:00:00') for _ in range(len(h))])
    lons = np.zeros(len(h))
    lats = np.zeros(len(h))

    # Obtain atmospheric composition (outputs a numpy array of size len(et) x 11)
    composition_data = msis.calculate(et, lons, lats, h)  # Adjust solar activity as needed

    # Replace nan entries by 0
    composition_data = np.nan_to_num(composition_data)

    # Full composition?
    if full:
        return composition_data
    
    else:
        # Return only the air density
        rho = composition_data[:, 0]
        return rho


# Calculate the mass flow rate gain for an array of altitudes
def Getm_gain(h:np.ndarray, sc_parameters:dict, earth_parameters:dict) -> np.ndarray:

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
    mu = earth_parameters['mu']
    R_e = earth_parameters['R']
    g0 = earth_parameters['g0']

    # Calculate the orbital velocity
    V = np.sqrt(mu / (h + R_e)) * 1e3  # In m/s

    # Calculate the atmospheric density
    rho = Get_Rho(h) # In kg/m^3

    # Calculate the intake mass flow rate
    m_in = A * eff_intake * V * rho

    # Calculate the mass flow rate necessary for sustaining flight
    m_out = 0.5 * rho * V**2 * A * C_D / (Isp * g0)

    # Calculate the mass flow rate gain
    m_gain = m_in - m_out

    return m_gain, m_in, m_out


# How low can I fly?
def Get_minAlts(h:np.ndarray, sc_parameters:dict, earth_parameters:dict) -> tuple:
    """
    This function calculates the minimum altitude at which the spacecraft can fly, based on drag and heating.
    It calculates at which altitude the drag force is equal to the thrust force.
    It calculates at which altitude the heating rate is equal to the heat rejection rate.
    It assumes simplified models for drag and heating. It also assumes no lift to help the spacecraft maintian its altitude.
    It also assumes everything assumed by the Getm_gain function.

    Inputs:
        h: altitudes in km. This is a one dimensional array.
        sc_parameters: dictionary with the spacecraft parameters.
        earth_parameters: dictionary with the Earth parameters.

    Returns:
        h_drag: the minimum altitude due to drag in km.
        h_heat: the minimum altitude due to heating in km.
    """

    # Unpack the spacecraft parameters
    A = sc_parameters['A_intake']
    C_D = sc_parameters['C_D']
    T = sc_parameters['T_max']
    Q_rejection = sc_parameters['Q_rejection']

    # Unpack the Earth parameters
    mu = earth_parameters['mu']
    R_e = earth_parameters['R']

    # Calculate the density at the different altitudes
    rho = Get_Rho(h) # In kg/m^3

    # Calculate the orbital velocities
    V = np.sqrt(mu / (h + R_e)) * 1e3  # In m/s

    # Calculate the drag force
    F_drag = 0.5 * rho * V**2 * A * C_D

    # Extract the point at which the drag force is equal to the thrust force
    h_drag = h[np.argmax(F_drag < T)]

    # Calculate the heating rate WORK IN PROGRESS
    Q_heating = 0

    # Extract the point at which the heating rate is equal to the heat rejection rate
    h_heat = h[np.argmax(Q_heating < Q_rejection)]

    return h_drag, h_heat


# Power Thrust and Isp relations
def Get_PowReq(h:np.ndarray, sc_parameters:dict, earth_parameters:dict) -> np.ndarray:
    """
    This function calculates the propulsive requirements for the spacecraft at a certain altitude.
    It calculates the power required by the propulsion system to maintain the orbit, the solar panel area required, the thrust required and the specific impulse required.
    It assumes everything assumed by the Getm_gain function.
    I assumes singly charged ions inside the thruster only

    Inputs:
        h: altitudes in km. This is a one dimensional array.
        sc_parameters: dictionary with the spacecraft parameters.
        earth_parameters: dictionary with the Earth parameters.

    Returns:
        P_req_prop: the power required by the propulsion system to maintain the orbit in W.
        A_solar: the solar panel area required in m^2.

    """

    # Unpack the spacecraft parameters
    A_intake = sc_parameters['A_intake']
    C_D = sc_parameters['C_D']
    eff_sol = sc_parameters['eff_solar']
    Isp = sc_parameters['Isp']

    # Calculate drag for all altitudes
    v = np.sqrt(earth_parameters['mu'] / (h + earth_parameters['R'])) * 1e3 # In m/s
    rho = Get_Rho(h) # In kg/m^3
    D = 0.5 * rho * v**2 * A_intake * C_D # Drag force in N

    # Calculate the required mass flow rate
    m_dot = D / (Isp * earth_parameters['g0']) # Thruster mass flow rate in kg/s

    # Calculate the minimum power required
    P_req_prop = 0.5 * m_dot * v**2

    # Calculate the solar panel area required
    Flux = 1361 # Solar constant in W/m^2
    A_solar = P_req_prop / eff_sol / Flux * 2  # *2 because the solar panels are not always facing the sun (kinda accountig for day and night)

    return P_req_prop, A_solar



if __name__ == '__main__':

    # Create an array of altitudes
    h = np.linspace(70, 200, 1000)

    # Calculate the mass flow rate gain
    m_gain, m_in, m_out = Getm_gain(h, spacecraft, earth)

    # Calculate the minimum altitudes
    h_drag, h_heat = Get_minAlts(h, spacecraft, earth)

    # Calculate the Power requirements
    P_req, A_solar = Get_PowReq(h, spacecraft, earth)

    # Calculate the time for refueling
    tank_load = spacecraft['Tank_load']  # Tank load in kg
    time = tank_load / m_gain # Time in seconds
    time = time / 3600 / 24 # Time in days

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

    print('The maximum mass flow rate gain is:', m_max * 3600, 'kg/hour')
    print('The altitude at which this occurs is:', h_max, 'km')

    plot_time_vs_massflow(h, m_gain, m_in, m_out, time, h_drag, h_heat)
    plot_power_vs_altitude(h, P_req, A_solar, h_drag, h_heat, h_max)