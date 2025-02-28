# Lucas Calderon
# 03/02/2025

from GMATAnalysis.atmos_functions import GetComposition, GetMassFlow
from GMATAnalysis.plotting import plot_atmos_data, plot_time_vs_massflow
from GMATAnalysis.data import ReadGeoPos, CropData


if __name__ == '__main__':

    # Read the data
    states = ReadGeoPos('GMAT_Data/GeoPosData.txt')

    # Get the composition of the atmosphere for the spacecraft flythrough
    composition = GetComposition(states)

    # Get mass flow and total captured mass
    h_max = None
    print('Calculating mass flow...')
    m_dot, m_total = GetMassFlow(states, composition, h_max=h_max)
    print('Mass flow calculation complete!')

    # Print the total captured mass
    print('Total captured mass:', m_total['rho'], 'kg')

    # Plot the composition of the atmosphere
    plot_atmos_data(m_total)
    # plot_time_vs_massflow(states, m_dot)
