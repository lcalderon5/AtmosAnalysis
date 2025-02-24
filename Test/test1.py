import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import pytest
import numpy as np
from AltitudeAnalysis.altitude_analysis import Getm_gain

class MockRegime:
    def __init__(self, h, earth_params):
        self.h = h
        self.earth_params = earth_params

    def v_circ(self):
        return np.full_like(self.h, 7800)  # Mock circular velocity in m/s

    def atmos(self):
        return np.full_like(self.h, 1e-4)  # Mock atmospheric density in kg/m^3

def test_getm_gain():
    # Define mock spacecraft parameters
    spacecraft = {
        'A_intake': 9,
        'eff_intake': 0.6,
        'C_D': 2.2,
        'Isp': 4200,
        'T_max': 5,
        'Q_rejection': 1e6,
        'P_max': 1000,
        'eff_solar': 0.2,
        'Tank_load': 2000
    }

    # Define mock Earth parameters
    earth = {
        'R': 6371,
        'mu': 3.986e5,
        'g0': 9.81,
        'SolarFlux': 1361
    }

    # Create a mock Regime object
    h = np.linspace(70, 200, 1000)
    regime = MockRegime(h, earth)

    # Call the Getm_gain function
    m_gain, m_in, m_out = Getm_gain(regime, spacecraft)

    # Define expected results (these values are just examples, adjust as needed)
    expected_m_gain = np.full_like(h, 0.00054)
    expected_m_in = np.full_like(h, 0.0006)
    expected_m_out = np.full_like(h, 0.00006)

    # Assert that the results are as expected
    np.testing.assert_allclose(m_gain, expected_m_gain, rtol=1e-5)
    np.testing.assert_allclose(m_in, expected_m_in, rtol=1e-5)
    np.testing.assert_allclose(m_out, expected_m_out, rtol=1e-5)

if __name__ == "__main__":
    pytest.main()