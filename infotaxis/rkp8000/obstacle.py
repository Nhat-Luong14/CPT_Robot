import numpy as np

def is_collision(xs, ys, px, py):
    x_grid, y_grid = np.meshgrid(xs, ys, indexing='ij')
    mask = get_mask(x_grid)
    dx = x_grid[mask] - px
    dy = y_grid[mask] - py
    dis = np.sqrt(np.square(dx) + np.square(dy))

    # if np.any((dis > 0) and (dis < 0.1)):
    if np.any((dis < 0.02) & (dis > 0 )):
        return True
    else:
        return False

def get_mask(x_grid):
    map = np.zeros(x_grid.shape)
    map[40:50, 0:40] = 1 #add obstacle
    map[40:80, 30:40] = 1 #add obstacle
    mask = (map==1)
    return mask