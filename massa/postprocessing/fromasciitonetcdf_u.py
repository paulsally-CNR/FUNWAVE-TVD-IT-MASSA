import os
import sys
import numpy as np
import pandas as pd
import xarray as xr

# if len(sys.argv) > 1 and sys.argv[1] != "-f":
if getattr(sys, "ps1", None) is None:
    if len(sys.argv) > 1:
        run = sys.argv[1]
    else:
        exit("No run argument passed")
else:
    run = input("No run argument passed: Enter the run name")

# Config
base_dir = rf'/OCEANASTORE/progetti/funwave/output_massa/output_files'
ascii_dir = "/".join([base_dir, run])
output_nc = "/".join([ascii_dir, 'u_masked.nc'])

file_pattern_u = 'u_{:05d}'                         # Pattern eta files
file_pattern_mask = 'mask_{:05d}'                   # Pattern mask files

start_index = 0                                     # Start index (e.g. 1 for eta_00001)

# Select files whose filename starts with prefix
prefix = "u_"
num_files_u = len([of for of in sorted(os.listdir(ascii_dir), key=str.casefold ) if of.startswith(prefix) and '.' not in of])

# Opzionale: informazioni sulla griglia
# Se hai coordinate spaziali specifiche, definiscile qui
# Ad esempio:
# x_coords = np.linspace(inizio_x, fine_x, numero_x)
# y_coords = np.linspace(inizio_y, fine_y, numero_y)

data_list = []
time_steps = []

for i in range(start_index, start_index + num_files_u):
    
    # Build u file path
    filename_u = os.path.join(ascii_dir, file_pattern_u.format(i))
    print(f"Reading {filename_u}...")
    # Build mask file path
    filename_mask = os.path.join(ascii_dir, file_pattern_mask.format(i))
    print(f"Reading {filename_mask}...")

    
    try:
        # Read output files
        data_u = np.loadtxt(filename_u)
        data_mask = np.loadtxt(filename_mask)
        
        # Replace 0s in mask file with np.nan
        data_mask[data_mask == 0] = np.nan
        masked_u = data_u * data_mask
        data_list.append(masked_u)

        # Generate a time step, either incremental or based on a real time interval
        time_steps.append(pd.to_timedelta(i * 30, unit='s'))
    except Exception as e:
        print(f"Error in file reading or manipulation: {e}")

# Convert list into 3D array (time, y, x)
data_array = np.stack(data_list, axis=0)

# Create xarray object Dataset
ds = xr.Dataset(
    {
        "masked_u": (["time", "y", "x"], data_array)
    },
    coords={
        "time": time_steps,
        "y": np.arange(data_array.shape[1]),  # Replace with real y coordinate values if available
        "x": np.arange(data_array.shape[2])   # Replace with real x coordinate values if available
    }
)

# Add global attributes (optional)
ds.attrs['description'] = 'U velocities converted from ASCII file into NetCDF.'
ds.attrs['source'] = 'Python script conversion.'

# Add attributes for the variable (optional)
ds['masked_u'].attrs['_FillValue'] = np.nan  # Define NoData value
ds['masked_u'].attrs['units'] = 'm/s'  # Replace with correct units of measure
ds['masked_u'].attrs['long_name'] = 'U Velocity'

# Save the Dataset in NetCDF format
ds.to_netcdf(output_nc, format='NETCDF4')
print(f"File NetCDF saved in {output_nc}")
