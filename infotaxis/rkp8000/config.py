import numpy as np

#========================== PLUME CHARACTERISTIC===========================
src_pos     = np.array([0.1, 0.5])
start_pos   =(1.9, 0.4) # agent starting position (m)
dt          =.1         # simulation time step (s) , sampling interval
speed       =.2         # agent movement speed (m/s)
max_dur     =100        # maximum simulation duration (s)
src_radius  =.02        # how close agent must be to source to detect it (m)
w           =.5         # wind speed (m/s)w: wind speed (m/s)
d           =.05        # diffusivity coefficient (m^2/s)
r           =5          # source emission rate (Hz)
a           =.003       # searcher size (m)
tau         =100        # particle lifetime (s)

#====================== turbulence length constant =========================
# This is given by Eq. 5 in the infotaxis paper
num     = d * tau
denom   = 1 + (tau * w**2) / (4 * d)
lam     = np.sqrt(num / denom)

#========================== ENVIRONMENT CONFIG =============================
grid            =(101, 51)  # number of (x, y) points in grid spanning plume environment
x_bounds        = (0, 2)
y_bounds        = (0, 1)
safe_bound      = 0.01 #m
xs              = np.linspace(*x_bounds, num=grid[0])
ys              = np.linspace(*y_bounds, num=grid[1])
x_grid, y_grid  = np.meshgrid(xs, ys, indexing='ij')
grid_shape      = (len(xs), len(ys))
obs_shape       = "tunnel"