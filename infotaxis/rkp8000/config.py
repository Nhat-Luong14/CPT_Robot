import numpy as np

agent_pt    = []
seed        = 2
grid        =(101, 51)
src_pos     =(.1, .5)
start_pos   =(1.9, 0.4)
dt          =.1
speed       =.2
max_dur     =100
th          =.5
src_radius  =.02
w           =.5
d           =.05
r           =5
a           =.003
tau         =100

x_bounds = (0, 2)
y_bounds = (0, 1)
xs = np.linspace(*x_bounds, num=grid[0])
ys = np.linspace(*y_bounds, num=grid[1])
x_grid, y_grid = np.meshgrid(xs, ys, indexing='ij')
grid_shape = x_grid.shape

ps = 30
nSeconds = 5
snapshots = []
im = []


x_grid, y_grid = np.meshgrid(xs, ys, indexing='ij')
shape = x_grid.shape