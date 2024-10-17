### PLOT WAVE for inlet_shoal CASE ###

# import necessary modules
import sys
import numpy as np               
import matplotlib.pyplot as plt
import os
# import cv2 to create a video out of png output images
import cv2

# To execute coode asynchronously
import asyncio

# Import module for passing arguments
#import sys

# import subprocess
# # Run the ffmpeg -codecs command and capture the output
# result = subprocess.run(['ffmpeg', '-codecs'], capture_output=True, text=True)
# # Print the output
# print(result.stdout)
# exit()

if len(sys.argv) == 2:
    run = sys.argv[1]
else:
    print('You need to pass the name of the directory for the specific run.')
    exit(2)

base_output_dir = rf"/OCEANASTORE/progetti/funwave/output_massa/"
output_files_dir = rf"{base_output_dir}output_files/{run}/"
output_pp_video_dir = rf"{base_output_dir}output_postprocessed/{run}/video/"

# Create directory to contain images used to create the video if it doesn't exist
mode = 0o755
output_postoprocessed_dir_path = os.path.join(base_output_dir, output_pp_video_dir)  
os.makedirs(output_postoprocessed_dir_path, mode=mode, exist_ok = True)

dep=np.loadtxt(os.path.join(output_files_dir,'dep.out'))

# define bathy location
n,m = np.shape(dep)
dx = 2.0
dy = 2.0
# print(n,m)
# exit()

# 525 : 4 = 662 : x 
# x = 4*662/525

x = np.asarray([float(xa)*dx for xa in range(m)])  
y = np.asarray([float(ya)*dy for ya in range(n)])

# define wavemaker and sponge location
x_sponge = [1, 100, 100, 1, 1]
y_sponge = [y[len(y)-1], y[len(y)-1], 1, 1, y[len(y)-1]]

x_wavemaker = [249, 251, 251, 249, 249 ]
y_wavemaker = [y[len(y)-1], y[len(y)-1], 1, 1, y[len(y)-1] ]

# figure size options
w = 5.66   # width
h = 4   # height

# Plot Figure
fig = plt.figure(figsize=(w, h), dpi=500)
#fig = plt.figure()

# Select files whose filename starts with prefix
prefix = "eta_"
output_files_x_imgs = [of for of in sorted(os.listdir(output_files_dir), key=str.casefold) if of.startswith(prefix)  and '.' not in of ]

imgs_paths = []

# Determine min and max eta values
# Initialize variables to store global min and max
global_min = float('inf')
global_max = float('-inf')
for index, of in enumerate(output_files_x_imgs):

    eta = np.loadtxt(os.path.join(output_files_dir, of))
    mask = np.loadtxt((os.path.join(output_files_dir, of).replace("eta", "mask")))
    eta_masked = np.ma.masked_where(mask==0,eta)  # do not plot where mask = 0

    # Update global min and max
    file_min = np.min(eta_masked)
    file_max = np.max(eta_masked)
    if file_min < global_min:
        global_min = file_min
    if file_max > global_max:
        global_max = file_max

    # print(f"Global minimum value: {global_min}")
    # print(f"Global maximum value: {global_max}")
    # exit()

for index, of in enumerate(output_files_x_imgs):
    plt.clf()

    eta = np.loadtxt(os.path.join(output_files_dir, of))
    mask = np.loadtxt((os.path.join(output_files_dir, of).replace("eta", "mask")))
    eta_masked = np.ma.masked_where(mask==0,eta)  # do not plot where mask = 0

    #ax = fig.add_subplot(1,len(output_files_x_imgs),index+1)
    ax = fig.add_subplot(1,1,1)
    
    #fig.subplots_adjust(hspace=1,wspace=.25)
    plt.pcolor(x, y, eta_masked, cmap='coolwarm', vmin=global_min, vmax=global_max)
    plt.axis('equal')
    
    title = 'Time = ' + str("{:4d}".format((index  + 1) * 30)) + ' sec'
    plt.title(title, loc='left')
    #plt.hold(True)

    # plot sponge and wavemaker
    plt.plot(x_sponge,y_sponge,'k--',linewidth=3)
    plt.text(40, 500, 'Sponge',color='k', rotation=90)
    plt.plot(x_wavemaker,y_wavemaker,'k-',linewidth=3)
    plt.text(200,500,'Wavemaker',color='k', rotation=90)

    cbar = plt.colorbar(fraction=0.10, pad=0.02)

    #imgs_paths.append(output_pp_video_dir + 'irr_2x2_pt_' + of.lstrip(prefix) + '.png')
    imgs_paths.append(output_pp_video_dir + run + '_' + of.lstrip(prefix) + '.png')

    # save figures
    print("Saving img " + imgs_paths[index])
    fig.savefig(imgs_paths[index], dpi=fig.dpi)



#----------------------- VIDEO -------------------
# -- Build video out of the output pictures

# Define the codec and create a VideoWriter object
output_video_fn = 'video_' + run + '.mp4'

async def save_video(
        par_imgs_paths, 
        par_output_pp_video_dir, 
        par_output_video_fn):
    # Define video parameters
    height, width = None, None  # Initialize dimensions
    out = None  # Initialize VideoWriter object

    # Check if the file exists
    file_path = par_output_pp_video_dir + par_output_video_fn
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
        print(f"File {file_path} has been deleted.")
    else:
        print(f"File {file_path} does not exist.")

    try:
        for img_path in par_imgs_paths:
            frame = cv2.imread(img_path)
            if frame is None:
                print(f"Skipping image file: {img_path}")
                continue
            
            # Initialize VideoWriter lazily to get the frame size
            if height is None or width is None:
                height, width, _ = frame.shape
                size = (width, height)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(par_output_pp_video_dir + par_output_video_fn, fourcc, 1.0, size)

            # Perform operations on frame
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Write frame to video
            out.write(frame)

        if out is not None:
            # Release the VideoWriter object
            out.release()
            print(f'Video saved as {par_output_video_fn}')
        else:
            print("No frames to write, video not saved.")

    except Exception as e:
        print(f"Error occurred: {e}")

# Run the save_video coroutine asynchronously
asyncio.run(save_video(imgs_paths, output_pp_video_dir, output_video_fn))