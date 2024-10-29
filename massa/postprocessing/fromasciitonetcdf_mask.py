import os
import sys
import numpy as np
import pandas as pd
import xarray as xr

if len(sys.argv) > 1:
    run = sys.argv[1]
else:
    print('No run parameter passed')
    exit()

# Config
base_dir = rf'/OCEANASTORE/progetti/funwave/output_massa/output_files'
ascii_dir = "/".join([base_dir, run])
output_nc = "/".join([ascii_dir, 'eta_masked.nc'])

file_pattern_eta = 'eta_{:05d}'                  # Pattern eta files
file_pattern_mask = 'mask_{:05d}'                # Pattern mask files
start_index = 0                                  # Start index (e.g. 1 for eta_00001)

# Select files whose filename starts with prefix
prefix = "eta_"
num_files_eta = len([of for of in sorted(os.listdir(ascii_dir), key=str.casefold ) if of.startswith(prefix) and '.' not in of])

# Opzionale: informazioni sulla griglia
# Se hai coordinate spaziali specifiche, definiscile qui
# Ad esempio:
# x_coords = np.linspace(inizio_x, fine_x, numero_x)
# y_coords = np.linspace(inizio_y, fine_y, numero_y)

data_list = []
time_steps = []

for i in range(start_index, start_index + num_files_eta):
    
    # Build eta file path
    eta_filename = os.path.join(ascii_dir, file_pattern_eta.format(i))
    print(f"Reading {eta_filename}...")
    
    # Build mask file path
    mask_filename = os.path.join(ascii_dir, file_pattern_mask.format(i))
    print(f"Reading {mask_filename}...")
    
    try:
        # Read files eta and mask
        eta_data = np.loadtxt(eta_filename)
        mask_data = np.loadtxt(mask_filename)
        # Replace 0s in mask file with np.nan
        mask_data[mask_data == 0] = np.nan
        eta_masked = eta_data * mask_data
        data_list.append(eta_masked)

        # Generate a time step, either incremental or based on a real time interval
        time_steps.append(pd.to_timedelta(i * 30, unit='s'))
    except Exception as e:
        print(f"Error in file reading or manipulation: {e}")

# Convert list into 3D array (time, y, x)
data_array = np.stack(data_list, axis=0)

# Create xarray object Dataset
ds = xr.Dataset(
    {
        "eta_masked": (["time", "y", "x"], data_array)
    },
    coords={
        "time": time_steps,
        "y": np.arange(data_array.shape[1]),  # Replace with real y coordinate values if available
        "x": np.arange(data_array.shape[2])   # Replace with real x coordinate values if available
    }
)

# Add global attributes (optional)
ds.attrs['description'] = 'Water levels converted from ASCII file into NetCDF.'
ds.attrs['source'] = 'Python script conversion.'

# Add attributes for the variable (optional)
ds['eta_masked'].attrs['_FillValue'] = np.nan  # Define NoData value
ds['eta_masked'].attrs['units'] = 'meters'  # Replace with correct units of measure
ds['eta_masked'].attrs['long_name'] = 'Water Level'

# Save the Dataset in NetCDF format
ds.to_netcdf(output_nc, format='NETCDF4')
print(f"File NetCDF saved in {output_nc}")
