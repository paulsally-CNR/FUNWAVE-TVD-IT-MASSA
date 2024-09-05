### PLOT inlet_shoal bathymetry ###

# import necessary modules
import os
import numpy as np               
import matplotlib.pyplot as plt


# write your OWN PC folder path for dep.
# Remember that we use for Mac & Linux machines '/', while on windows '\'

fdir = rf'/home/mare/funwave/output_massa/output_files/reg_2x2/'
dep=np.loadtxt(os.path.join(fdir,'dep.out'))

#fdir = rf'/home/mare/funwave/FUNWAVE-TVD/massa/bathy/'
#dep=np.loadtxt(os.path.join(fdir,'dtm_2x2.txt'))

# define bathy location
n,m = np.shape(dep)
dx = 2.0
dy = 2.0

# print(n,m)
# exit()

x = np.asarray([float(xa)*dx for xa in range(m)])
y = np.asarray([float(ya)*dy for ya in range(n)])

# define wavemaker and sponge location
x_sponge = [1, 100, 100, 1, 1]
y_sponge = [y[len(y)-1], y[len(y)-1], 1, 1, y[len(y)-1]]

x_wavemaker = [249, 251, 251, 249, 249 ]
y_wavemaker = [y[len(y)-1], y[len(y)-1], 1, 1, y[len(y)-1] ]


# figure size option 
wid=5    # width
length=4 # length

# Plot figure
fig = plt.figure(figsize=(wid,length),dpi=500)
ax = fig.add_subplot(1,1,1)
fig.subplots_adjust(hspace=1,wspace=.25)

plt.pcolor(x, y, -1*dep,cmap='terrain')
plt.axis('tight')  
plt.ylabel('Y (m)')
plt.xlabel('X (m)')
# plt.hold(True)

# plot sponge and wavemaker
plt.plot(x_sponge,y_sponge,'k--',linewidth=3)
plt.text(40, 500, 'Sponge',color='k', rotation=90)
plt.plot(x_wavemaker,y_wavemaker,'k-',linewidth=3)
plt.text(200,500,'Wavemaker',color='k', rotation=90)

# figure colorbar
cbar=plt.colorbar()
cbar.set_label('Bathymetry (m)')

# save figure
fig.savefig(rf'/home/mare/funwave/output_massa/images/reg_2x2/bathy_massa.png', dpi=fig.dpi)
