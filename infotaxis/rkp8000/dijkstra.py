from ast import literal_eval
import numpy as np
from obstacle import get_mask
from config import *

"""
Get the nearest cell index to the agent
"""
def get_index(pos):
    dx = x_grid - pos[0]
    dy = y_grid - pos[1]
    dist = np.sqrt(np.square(dx) + np.square(dy))
    flat_idex = np.argmin(dist)
    index = np.unravel_index(flat_idex, grid_shape)
    return index


"""
Get index of valid neigbor cells
"""
def get_neighbor_id(index, dead_map):
    neighbor_list = []

    for shift in [(0,1), (0,-1), (1,0), (-1,0)]:
        idx = np.array(index) + np.array(shift)
        if idx[0] < 0 or idx[0] >= grid[0] or idx[1] < 0 or idx[1] >= grid[1]:
            continue
        elif dead_map[idx[0], idx[1]] is True:
            continue
        else:
            neighbor_list.append(tuple(idx))

    return neighbor_list


"""
Path planning using Djkstra
"""
def find_path(pos, goal):
    # initialize some matrix of value
    cost_map = np.full(grid_shape, np.inf)
    parent_map = np.full(grid_shape, "no_parent")
    dead = np.full(grid_shape, False)

    # add obstacles
    mask = get_mask()
    dead[mask] = True

    goal_index = get_index(goal)
    start_index = get_index(pos)

    id = start_index
    cost_map[id] = 0

    reach_goal = False
    while not reach_goal :
        dead[id] = True   # Examinated node
        neighbor_list = get_neighbor_id(id, dead)

        for n_idex in neighbor_list:
            current_cost = cost_map.item(n_idex)
            estimate_cost = cost_map[id] + speed*dt

            if estimate_cost < current_cost:
                cost_map[n_idex] = estimate_cost
                parent_map[n_idex] = str(id)

        visit_index = np.argmin(np.ma.MaskedArray(cost_map, dead))
        id = np.unravel_index(visit_index, grid_shape)
        
        if (id == goal_index):
            reach_goal = True  

    route = []
    parent = parent_map[id]

    while parent != "no_parent":
        id = literal_eval(parent)
        route.append((x_grid[id], y_grid[id]))
        parent = parent_map[id]
        
    return(route)