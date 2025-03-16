# Introduction
This is a little package intended to help in designing an atmospheric refueling space tug, a reusable vehicle concept that can refuel by diving into the upper layers of the atmosphere, capturing air, and subsequently using it as propellant. It includes two packages (for now). The first one is meant to analyze a specified altitude range given by the user. The second is mean to interface with GMAT and analyze orbit paths produced inside GMAT.


# Capabilities

## For the Gmat Analysis Package
Calculating the atmospheric composition at different positions,
Calculating the mass flows in the intake of a spacecraft aerobraking
Calculating the total air mass collected by a spacecraft aerobraking
Plotting the composition of captured air

To do this, a file containing state data for a spacecraft is needed, usually generated through Nasa's General Mission Analysis Tool (GMAT): https://software.nasa.gov/software/GSC-17177-1 


## For the AltitudeAnalysis Package
Given an altitude range it will analyze refueling at the input altitudes assuming a circular orbit

It does so by:
Calculating orbital velocity, atmospheric composition and drag at every altitude
Calculating the mass flow in, out and gained at each altitude
Calculating the spacecrafts altitude limits based on thrust and power estimations
Calculating the refueling time given a tank volume


## Virtual Environment Creation and install
To create a virtual environment and download the dependencies run the following commands on your terminal.
#TODO: Finish explanations


python -m venv .venv

.venv\Scripts\activate 

pip install -r requirements.txt


To update requirements list:
pip freeze > requirements.txt

