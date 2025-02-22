# Lucas Calderon
# 20/02/2025
import numpy as np
import pymsis as msis
import matplotlib.pyplot as plt


class Regime:
    """"
    This class takes an altitude regime and calculates parameters associated with it.
    It calculates the atmospheric density, composition, orbital velocity.
    The class assumes a circular equatorial orbit for simplicity.
    It also assumes that the earth is perfectly spherical.
    For atmospheric calculations it also assumes that the longitude and latitude are 0 degrees, and the date is 2000-01-01.

    INPUTS:
        h: altitudes in km. This is a one dimensional array.
        earth_params: dictionary with the Earth parameters.
    
    PARAMETERS:
        h: the altitudes in km. This is a one dimensional array that you provided.
        earth_params: the Earth parameters. This is a dictionary you provided.
        v_circ: the circular velocity in m/s. This is a one dimensional array.
        rho: the atmospheric density in kg/m^3. This is a one dimensional array.
        atmosphere: the atmospheric composition. This is a dictionary.
    """
    def __init__(self, h:np.ndarray, earth_params:dict):

        # Initialize the class
        self.h = h
        self.earth_params = earth_params

    # Velocity
    def v_circ(self):
        return np.sqrt(self.earth_params['mu'] / (self.earth_params['R'] + self.h)) * 1e3  # Circular velocity in m/s

    # Create lists for et, lons, and lats
    def atmos(self, Composition:bool=False):
        # Create lists for et, lons, and lats
        et = np.array([np.datetime64('2000-01-01T00:00:00') for _ in range(len(self.h))])
        lons = np.zeros(len(self.h))
        lats = np.zeros(len(self.h))

        # Obtain atmospheric composition (outputs a numpy array of size len(et) x 11)
        composition_data = msis.calculate(et, lons, lats, self.h)

        # Replace nan entries by 0
        composition_data = np.nan_to_num(composition_data)

        # Define atmos properties
        rho = composition_data[:, 0]
        atmosphere = composition_data

        if Composition:
            return atmosphere 
        else:
            return rho # Atmospheric density in kg/m^3


    # Plotting functions for validation mostly
    def plot_rho(self):
        # Mostly for validation purposes
        plt.plot(self.h, self.atmos())
        plt.yscale('log')
        plt.xlabel('Altitude (km)')
        plt.ylabel('Density (kg/m^3)')
        plt.title('Atmospheric Density vs Altitude')
        plt.show()

    def plot_T(self):
        # Mostly for validation purposes
        plt.plot(self.h, self.atmos(Composition=True)[:, -1])
        plt.xlabel('Altitude (km)')
        plt.ylabel('Temperature (K)')
        plt.title('Temperature vs Altitude')
        plt.show()

    def plot_v_circ(self):
        # Mostly for validation purposes
        plt.plot(self.h, self.v_circ())
        plt.xlabel('Altitude (km)')
        plt.ylabel('Velocity (m/s)')
        plt.title('Circular Velocity vs Altitude')
        plt.show()



class Spacecraft:
    """
    This class takes a spacecraft and calculates parameters associated with it.
    It calculates the mass flow rate gain of the spacecraft at a certain altitude.
    The class assumes a circular orbit for simplicity.
    It also assumes that the intake area and drag reference area are the same.
    It also assumes a simplified drag model, with constant C_D.

    INPUTS:
        Regime: the altitude regime. This is a Regime object.
        sc_parameters: dictionary with the spacecraft parameters.
    
    PARAMETERS:
        sc_parameters: the spacecraft parameters. This is a dictionary you provided.
        earth_parameters: the Earth parameters. This is a dictionary you provided.
        m_gain: the mass flow rate gain in kg/s. This is a one dimensional array.
        m_in: the intake mass flow rate in kg/s. This is a one dimensional array.
        m_out: the thruster mass flow rate in kg/s. This is a one dimensional array.
    """
    def __init__(self, Regime:Regime, sc_parameters:dict):

        # Initialize the class
        self.sc_parameters = sc_parameters
        
        # Unpack the spacecraft parameters by system
        self.thruster = sc_parameters['Thruster']
        self.intake = sc_parameters['Intake']
        self.drag = sc_parameters['Drag']
        self.heat = sc_parameters['Heat']
        self.power = sc_parameters['Power']
        self.tank = sc_parameters['Tank']
