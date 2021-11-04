import numpy as np
import sys

#========================== PLUME CHARACTERISTIC===========================
src_pos      = np.array([0.1, 0.5])
dt           =.1         # simulation time step (s) , sampling interval
src_radius   =.02        # how close agent must be to source to detect it (m)
w            =.5         # wind speed (m/s)w: wind speed (m/s)
d            =.05        # diffusivity coefficient (m^2/s)
release_rate =50         # source emission rate (Hz)
a            =.003       # searcher size (m)
tau          =100        # particle lifetime (s)

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
obs_shape       = "corner"

cell_size_x = (x_bounds[1]- x_bounds[0])/(grid[0] - 1)
cell_size_y = (y_bounds[1]- y_bounds[0])/(grid[1] - 1)

#========================== OBSTACLE REGION =============================
decay_param = 0.8
random_walk_param = 1.5

#========================== ANGENT PARAM =============================
# step = dt*speed
start_pos    =(1.1, 0.2) # agent starting position (m)
speed        =.2         # agent movement speed (m/s)
max_dur      =100        # maximum searching duration (s)
if cell_size_x == cell_size_y:
    step = cell_size_x
else:
    print("ERROR!! Cells have different dimension in width and length.")
    sys.exit(0)