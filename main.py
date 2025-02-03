# Lucas Calderon
# 03/02/2025

from atmos_functions import GetComposition, GetMassFlow
from plotting import plot_atmos_data, plot_time_vs_massflow
from data import ReadGeoPos, CropData


if __name__ == '__main__':

    # Read the data
    states = ReadGeoPos('GMAT_Data/GeoPosData.txt')

    # Get the composition of the atmosphere for the spacecraft flythrough
    composition = GetComposition(states)

    # Get mass flow and total captured mass
    h_max = 150
    print('Calculating mass flow...')
    m_dot, m_total = GetMassFlow(states, composition)
    print('Mass flow calculation complete!')
    print(max(m_dot['rho']), 'kg/s')

    # Print the total captured mass
    print('Total captured mass:', m_total['rho'], 'kg')

    # Plot the composition of the atmosphere
    # plot_atmos_data(m_total)
    plot_time_vs_massflow(states, m_dot)
