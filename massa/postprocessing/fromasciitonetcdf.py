import os
import sys
import numpy as np
import pandas as pd
import xarray as xr

# if len(sys.argv) > 1 and sys.argv[1] != "-f":
if getattr(sys, "ps1", None) is None:
    if len(sys.argv) == 3:
        run = sys.argv[1]
        var = sys.argv[2]
    else:
        exit("Missing arguments (run, var or both)")
else:
    run = input("Enter the run name")
    var = input("Enter the var name")

# Config
base_dir = rf"/OCEANASTORE/progetti/funwave/output_massa/output_files"
ascii_dir = "/".join([base_dir, run])
output_nc = "/".join([ascii_dir, f"{var}_masked.nc"])

file_pattern_var = f"{var}_{{:05d}}"                # Pattern eta files
file_pattern_mask = "mask_{:05d}"                   # Pattern mask files

start_index = 0                                     # Start index (e.g. 1 for eta_00001)

# Select files whose filename starts with prefix
prefix = f"{var}_"
num_files_var = len([of for of in sorted(os.listdir(ascii_dir), key=str.casefold ) if of.startswith(prefix) and "." not in of])

# Opzionale: informazioni sulla griglia
# Se hai coordinate spaziali specifiche, definiscile qui
# Ad esempio:
# x_coords = np.linspace(inizio_x, fine_x, numero_x)
# y_coords = np.linspace(inizio_y, fine_y, numero_y)

data_list = []
time_steps = []

for i in range(start_index, start_index + num_files_var):
    
    # Build u file path
    filename_var = os.path.join(ascii_dir, file_pattern_var.format(i))
    print(f"Reading {filename_var}...")
    # Build mask file path
    filename_mask = os.path.join(ascii_dir, file_pattern_mask.format(i))
    print(f"Reading {filename_mask}...")

    
    try:
        # Read output files
        data_var = np.loadtxt(filename_var)
        data_mask = np.loadtxt(filename_mask)
        
        # Replace 0s in mask file with np.nan
        data_mask[data_mask == 0] = np.nan
        masked_var = data_var * data_mask
        data_list.append(masked_var)

        # Generate a time step, either incremental or based on a real time interval
        time_steps.append(pd.to_timedelta(i * 30, unit="s"))
    except Exception as e:
        print(f"Error in file reading or manipulation: {e}")

# Convert list into 3D array (time, y, x)
data_array = np.stack(data_list, axis=0)

# Create xarray object Dataset
ds = xr.Dataset(
    {
        f"{var}_masked": (["time", "y", "x"], data_array)
    },
    coords={
        "time": time_steps,
        "y": np.arange(data_array.shape[1]),  # Replace with real y coordinate values if available
        "x": np.arange(data_array.shape[2])   # Replace with real x coordinate values if available
    }
)

# Add global attributes (optional)
ds.attrs["description"] = f"{var} converted from ASCII file into NetCDF."
ds.attrs["source"] = "Python script conversion."

# Add attributes for the variable (optional)
ds[f"{var}_masked"].attrs["_FillValue"] = np.nan  # Define NoData value
match var:
    case "eta":
        ds["eta_masked"].attrs["units"] = "m"
        ds["eta_masked"].attrs["long_name"] = "Water Level"
    case "u":
        ds["u_masked"].attrs["units"] = "m/s"
        ds["u_masked"].attrs["long_name"] = "U velocity"
    case "v":
        ds["v_masked"].attrs["units"] = "m/s"
        ds["v_masked"].attrs["long_name"] = "V velocity"

# Save the Dataset in NetCDF format
ds.to_netcdf(output_nc, format="NETCDF4")
print(f"File NetCDF saved in {output_nc}")
