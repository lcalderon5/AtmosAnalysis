# Lucas Calderon
# 02/02/2025

import matplotlib.pyplot as plt
import matplotlib.cm as cm


# ----------- AIR COMPOSITION PLOTTING FUNCTIONS ------------

def plot_atmos_data(composition:dict, savepath=None):

    """
    This function will plot a pie chart with the composition of the air captured by the space tug.
    Inputs:
        composition: dictionary with the composition of the air captured by the device.
        savepath: path to save the plot. If None, the plot is shown instead of saved.

    Returns:
    - None
    """

    # Extract data
    labels = [key for key in composition if key not in ('rho', 'name')]
    data = [composition[key] for key in composition if key not in ('rho', 'name')]

    # Dynamically generate colors based on the number of data points
    cmap = cm.get_cmap('tab10')  # Use 'tab10' for distinct colors, or try 'viridis', 'plasma', etc.
    colors = [cmap(i / len(labels)) for i in range(len(labels))]

    # Create the pie chart without labels
    wedges, texts, autotexts = plt.pie(
        data, autopct='%1.1f%%', startangle=140, colors=colors
    )
    plt.axis('equal')  # Ensures the pie chart is a circle

    # Add a legend to the right
    legend_labels = [f"{label} ({autotext.get_text()})" for label, autotext in zip(labels, autotexts)]
    plt.legend(wedges, legend_labels, title="Components", loc="center left", bbox_to_anchor=(1, 0.5))

    # Add a title
    plt.title('Captured Air Composition (By Particle Number Percentage)')

    # Adjust layout to accommodate legend
    plt.tight_layout()

    # Save or show the chart
    if savepath:
        plt.savefig(savepath)
    else:
        plt.show()


# ----------- OTHER PLOTTING FUNCTIONS ------------
def plot_altitude_vs_massflow(states:dict, m_dot:dict):

    """
    This function will plot the altitude against the mass flow rate of the spacecraft.
    Inputs:
        states: dictionary with the spacecraft states.
        m_dot: dictionary with the mass flow rates of each component at each location.
    
    Returns:
    - None
    """
    # Extract data
    alts = states['altitude']
    m_dot_values = m_dot['rho']  # Mass flow rate of air

    # Plot the data
    plt.plot(alts, m_dot_values)
    plt.xlabel('Altitude (km)')
    plt.ylabel('Air Mass Flow Rate (kg/s)')
    plt.title('Altitude vs. Air Mass Flow Rate')
    plt.show()