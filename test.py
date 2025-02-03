import pymsis as msis
from datetime import datetime

time = [datetime(2025, 2, 2, 0, 0, 0)]
lons = [0]
lats = [0]
alts = [100]

composition = msis.calculate(time, lons, lats, alts)

print(composition)
print(type(composition))