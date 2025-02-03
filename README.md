# Introduction
This is a little package intended to help in designing an atmospheric refueling space tug, a vehicle that ca refuel by dipping into the upper layers of the atmosphere.

So far the capabilities are:

Calculating the atmospheric composition at different positions,
Calculating the mass flows in the intake of a spacecraft aerobraking
Calculating the total air mass collected by a spacecraft aerobraking
Plotting the composition of captured air

To do this, a file containing state data for a spacecraft is needed, usually generated through Nasa's General Mission Analysis Tool (GMAT): https://software.nasa.gov/software/GSC-17177-1 

# Dependencies
Numpy

Matplotlib

Datetime

pysmis
