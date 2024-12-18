### PLOT WAVE for inlet_shoal CASE ###

# import necessary modules
import numpy as np               
import matplotlib.pyplot as plt
import os

# write your OWN PC folder path for fdir and dep.
# Remember that we use for Mac & Linux machines '/', while on windows '\'
#fdir = rf'/home/mare/funwave/output_massa/output_files/'
fdir = rf'/OCEANASTORE/progetti/funwave/output_massa/output_files/tide_abs_1bc_c_1/'
dep=np.loadtxt(os.path.join(fdir,'dep.out'))


# define bathy location
n,m = np.shape(dep)
dx = 1.0
dy = 1.0

x = np.asarray([float(xa)*dx for xa in range(m)])  
y = np.asarray([float(ya)*dy for ya in range(n)])

# define wavemaker and sponge location
x_sponge = [1, 100, 100, 1, 1]
y_sponge = [y[len(y)-1], y[len(y)-1], 1, 1, y[len(y)-1]]

x_wavemaker = [249, 251, 251, 249, 249 ]
y_wavemaker = [y[len(y)-1], y[len(y)-1], 1, 1, y[len(y)-1] ]


nfile = [5, 11]      # range of eta files you want to plot   
min = ['150','900']  # time  you want to plot

# figure size option 
# wid=20   # width
# length=8 # length
wid=4*1.26   # width
length=4 # length


# Plot Figure
fig = plt.figure(figsize=(wid,length),dpi=300)

for num in range(len(nfile)):
    fnum= '%.5d' % nfile[num]
    eta = np.loadtxt(fdir+'eta_'+fnum)
    mask = np.loadtxt(fdir+'mask_'+fnum)

    eta_masked = np.ma.masked_where(mask==0,eta)  # do not plot where mask = 0

    ax = fig.add_subplot(1,len(nfile),num+1)
    fig.subplots_adjust(hspace=1,wspace=.25)
    plt.pcolor(x, y, eta_masked,cmap='coolwarm')
    plt.axis('tight')
    title = 'Time = '+min[num]+ ' sec'
    plt.title(title)
    #plt.hold(True)

    # plot sponge and wavemaker
    plt.plot(x_sponge,y_sponge,'k--',linewidth=3)
    plt.text(40, 500, 'Sponge',color='k', rotation=90)
    plt.plot(x_wavemaker,y_wavemaker,'k-',linewidth=3)
    plt.text(200,500,'Wavemaker',color='k', rotation=90)
   
    if num == 0:
        plt.ylabel('Y (m)')
        plt.xlabel('X (m)')
    else:
        plt.xlabel('X (m)')
        cbar=plt.colorbar()
        cbar.set_label(r'$\eta$'+' (m)', rotation=90)

# save figure        
fig.savefig(rf'/OCEANASTORE/progetti/funwave/output_massa/output_postprocessed/tide_abs_1bc_c_1/wave_massa.png', dpi=fig.dpi)
