# Lucas Calderon
# 14/02/2025
# I want to try and find the ideal altitude for a spacecraft to orbit in orer to find the maximum surplus of air mass flow rate.




# WHAT WAS FOUND:
# As long as Isp*g0*eff_intake > V_orbital, the lower you go the higher surplus you can get.
# No surprise there, but it's good to have a confirmation.




# Import the necessary libraries
import numpy as np
import pymsis as msis

# Problem constants
spacecraft = {
    'A_intake': 9,  # Intake area in m^2
    'eff_intake': 0.6,  # Intake efficiency, unitless
    'C_D': 2.2,  # Drag coefficient, unitless
    'Isp': 4200  # Specific impulse in s
}

earth = {
    'R': 6371,  # Earth radius in km
    'mu': 3.986e5,  # Earth gravitational parameter in km^3/s^2
    'g0': 9.81  # Standard gravity in m/s^2
}


# Calculate the atmospheric density for an array of altitudes
def GetRho(h: np.ndarray) -> np.ndarray:
    """
    This function will return the composition of the atmosphere at the given position points.

    Inputs:
        h: altitudes in km. This is a one dimensional array.

    Returns:
        rho: one dimensional array of air density values (in kg/m^3)
        """

    # Create lists for et, lons, and lats
    et = np.array([np.datetime64('2000-01-01T00:00:00') for _ in range(len(h))])
    lons = np.zeros(len(h))
    lats = np.zeros(len(h))

    # Obtain atmospheric composition (outputs a numpy array of size len(et) x 11)
    print('Calculating atmospheric composition...')
    composition_data = msis.calculate(et, lons, lats, h)  # Adjust solar activity as needed
    print('Composition calculation complete!')

    # Replace nan entries by 0
    composition_data = np.nan_to_num(composition_data)

    # Extract the air density
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

    Inputs:
        h: altitudes in km. This is a one dimensional array.
        sc_parameters: dictionary with the spacecraft parameters.
        earth_parameters: dictionary with the Earth parameters.

    Returns:
        m_gain: the mass flow rate gain in kg/s. This is a one dimensional array.
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
    rho = GetRho(h) # In kg/m^3

    # Calculate the intake mass flow rate
    m_in = A * eff_intake * V * rho

    # Calculate the mass flow rate necessary for sustaining flight
    m_out = 0.5 * rho * V**2 * A * C_D / (Isp * g0)

    # Calculate the mass flow rate gain
    m_gain = m_in - m_out

    return m_gain, m_in, m_out

if __name__ == '__main__':

    # Create an array of altitudes
    h = np.linspace(70, 200, 1000)

    # Calculate the mass flow rate gain
    m_gain, m_in, m_out = Getm_gain(h, spacecraft, earth)

    # Find the maximum mass flow rate gain
    h_max = h[np.argmax(m_gain)]
    m_max = np.max(m_gain)

    print('The maximum mass flow rate gain is:', m_max, 'kg/s')
    print('The altitude at which this occurs is:', h_max, 'km')

    # Plot the results
    import matplotlib.pyplot as plt
    plt.plot(h, m_gain, label='Mass flow rate gain')
    plt.plot(h, m_in, label='Intake mass flow rate')
    plt.plot(h, m_out, label='Thruster mass flow rate')
    plt.yscale('log')
    plt.axhline(0, color='k', linestyle='--')
    plt.axvline(h_max, color='r', linestyle='--', label='Altitude of max gain')
    plt.legend()
    plt.xlabel('Altitude (km)')
    plt.ylabel('Mass flow rate gain (kg/s)')
    plt.title('Mass flow rate gain vs altitude')
    plt.grid()
    plt.show()