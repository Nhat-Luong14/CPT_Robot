import numpy as np

obs_shape = "tunnel"


"""
check collision by checking if agent is really near the obstacle
"""
def is_collision(xs, ys, pos):
    x_grid, y_grid = np.meshgrid(xs, ys, indexing='ij')
    mask = get_mask(x_grid.shape)
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
def get_mask(shape):
    mask = np.full(shape, False)
    if obs_shape == "corner":
        mask[40:50, 0:40] = True #add obstacle
        mask[40:80, 30:40] = True 
    if obs_shape == "tunnel":
        mask[40:50, 0:24] = True #add obstacle
        mask[40:50, 26:51] = True 
    
    return mask