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
def plot_time_vs_massflow(states:dict, m_dot:dict, h_max:float=150):

    """
    This function will plot the altitude against the mass flow rate of the spacecraft.
    Inputs:
        states: dictionary with the spacecraft states.
        m_dot: dictionary with the mass flow rates of each component at each location.
    
    Returns:
    - None
    """
    # Extract data
    time = states['elapsed_seconds']
    m_dot_values = m_dot['rho']
    altitude = states['altitude']

    # Plot the data
    # Create the figure and axis
    fig, ax1 = plt.subplots()

    # Plot mass flow vs time on the left y-axis
    ax1.plot(time, m_dot_values, 'g-', label='Mass Flow')
    ax1.set_yscale('log')  # Set the left y-axis to logarithmic scale
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Mass Flow (kg/s)', color='g')
    ax1.tick_params(axis='y', labelcolor='g')

    # Create a second y-axis sharing the same x-axis
    ax2 = ax1.twinx()

    # Plot altitude vs time on the right y-axis
    ax2.plot(time, altitude, 'b-', label='Altitude')
    ax2.set_ylabel('Altitude(km)', color='b')
    ax2.set_yscale('log')  # Set the right y-axis to logarithmic scale
    ax2.tick_params(axis='y', labelcolor='b')

    # Add horizontal line to indicate the maximum altitude
    if h_max:
        ax2.axhline(y=h_max, color='r', linestyle='--', label='Max Altitude')

    # Title and display the plot
    plt.title('Mass Flow and Altitude vs Time')
    plt.show()