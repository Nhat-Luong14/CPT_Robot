import numpy as np
from config import obs_shape, grid_shape

"""
check collision by checking if agent is really near the obstacle
"""
def is_collision(xs, ys, pos):
    x_grid, y_grid = np.meshgrid(xs, ys, indexing='ij')
    mask, blind_zone, bound_zone = get_region()
    dx = x_grid[mask] - pos[0]
    dy = y_grid[mask] - pos[1]
    dis = np.sqrt(np.square(dx) + np.square(dy))

    if np.any(dis < 0.02):
        return True
    else:
        return False


"""
Created obstacle shape and return a boolean matrix
"""
def get_region():
    mask = np.full(grid_shape, False)
    blind_zone = np.full(grid_shape, False)
    bound_zone = np.full(grid_shape, False)
    

    if obs_shape == "corner":
        mask[40:50, 0:40] = True #add obstacle
        mask[40:80, 30:40] = True 
        blind_zone[50:101, 0:40] = True
        # bound_zone[40:101, 22:23] = True
        # bound_zone[40:101, 27:28] = True
        bound_zone[38:40, 0:41] = True
        bound_zone[38:101, 40:42] = True


    if obs_shape == "tunnel":
        mask[40:50, 0:22] = True #add obstacle
        mask[40:50, 28:51] = True 
        blind_zone[50:101, 0:22] = True
        blind_zone[50:101, 28:51] = True
        bound_zone[40:101, 22:24] = True
        bound_zone[40:101, 26:28] = True
        bound_zone[38:40, 0:24] = True
        bound_zone[38:40, 26:51] = True

    if obs_shape == "central":
        mask[40:50, 11:39] = True #add obstacle
        blind_zone[50:101, 11:39] = True
        bound_zone[40:101, 39:41] = True
        bound_zone[40:101, 9:11] = True
        bound_zone[38:40, 9:41] = True

    return mask, blind_zone, bound_zone