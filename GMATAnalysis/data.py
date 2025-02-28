# Lucas Calderon
# 02/02/2025

# This file is dedicated to reading and processing the data from GMAT simulations.

import numpy as np
from datetime import datetime

# ----------- DATA READING FUNCTIONS ------------

def ReadState(filepath:str) -> np.ndarray:
    """
    This function reads the state vector data from a GMAT simulation file and returns it as a numpy array.
    Inputs:
        filepath: path to the GMAT simulation file. The file contains the state vector data, including mass and time.
    Returns:
        data: numpy array with the data from the GMAT simulation ordered as [x, y, z, vx, vy, vz, m, t].
    """
    data = np.loadtxt(filepath, skiprows=1)
    return data


def ReadGeoPos(filepath: str='GMAT_Data/GeoPosData.txt') -> tuple[dict, dict]:
    """
    This function reads the altitude data from a GMAT simulation file and stores it in a dictionary.

    Inputs:
        filepath: path to the GMAT simulation file. 
                The file contains altitude, latitude, longitude, date, velocity magnitude and elapsed seconds data.

    Returns:
        States: dictionary with keys ['altitude', 'latitude', 'longitude', 'date', 'velocity', 'elapsed_seconds'].
                Each key maps to a pre-allocated list of corresponding data.
    """
    # Determine the number of lines in the file (excluding the header)
    with open(filepath, 'r') as file:
        num_lines = sum(1 for _ in file) - 1  # Subtract 1 for the header line

    # Pre-allocate lists
    altitude = [0.0] * num_lines
    latitude = [0.0] * num_lines
    longitude = [0.0] * num_lines
    date = [None] * num_lines  # Pre-allocate for datetime objects
    velocity = [0.0] * num_lines
    elapsed_seconds = [0.0] * num_lines

    # Read the file and populate the lists
    with open(filepath, 'r') as file:
        next(file)  # Skip the header

        for i, line in enumerate(file):
            parts = line.split()
            altitude[i] = float(parts[0])
            latitude[i] = float(parts[1])
            longitude[i] = float(parts[2])

            # Parse the date string into a datetime object
            date_str = " ".join(parts[3:7])
            date[i] = datetime.strptime(date_str, "%d %b %Y %H:%M:%S.%f")
            
            velocity[i] = float(parts[7]) * 1000  # Convert from km/s to m/s
            elapsed_seconds[i] = float(parts[8])

    # Store all lists in a dictionary
    States = {
        "altitude": np.array(altitude),
        "latitude": np.array(latitude),
        "longitude": np.array(longitude),
        "date": np.array(date),
        "velocity": np.array(velocity),
        "elapsed_seconds": np.array(elapsed_seconds)
    }

    return States


# ----------- DATA PROCESSING FUNCTIONS ------------
def CropData(GeoPos:dict, VelHist:dict, max_alt:float) -> dict:
    """
    This function removes data above a certain altitude.

    Inputs:
        GeoPos: dictionary with keys ['altitude', 'latitude', 'longitude', 'date'].
        max_alt: maximum altitude to keep in the data.

    Returns:
        GeoPos: dictionary with the data cropped above the maximum altitude.
        VelHist: dictionary with the velocity data above below the maximum altitude.
    """
    # Find the indices where the altitude is above the minimum
    indices = [i for i, alt in enumerate(GeoPos['altitude']) if alt <= max_alt]

    # Create a new dictionary with the cropped GeoPos data
    New_GeoPos = {
        'altitude': [GeoPos['altitude'][i] for i in indices],
        'latitude': [GeoPos['latitude'][i] for i in indices],
        'longitude': [GeoPos['longitude'][i] for i in indices],
        'date': [GeoPos['date'][i] for i in indices]
    }

    # Create a new dictionary with the cropped velocity data
    New_VelHist = {
        'velocity': [VelHist['velocity'][i] for i in indices],
        'elapsed_seconds': [VelHist['elapsed_seconds'][i] for i in indices]
    }


    return New_GeoPos, New_VelHist




# ----------- TESTING ------------
if __name__ == '__main__':

    geodata, velhist = ReadGeoPos('GMAT_Data/GeoPosData.txt')

    # Test cropping
    h_max = 150
    geodata, velhist = CropData(geodata, velhist, h_max)

    # Plot the data
    import matplotlib.pyplot as plt
    plt.plot(velhist['elapsed_seconds'], geodata['altitude'])
    plt.xlabel('Elapsed seconds')
    plt.ylabel('Altitude (km)')
    plt.title('Altitude vs. Time')
    plt.show()
    