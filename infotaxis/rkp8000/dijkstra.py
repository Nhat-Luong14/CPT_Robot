import numpy as np
from obstacle import get_mask

agent_pt    = []
# grid        =(101, 51)
# src_pos     =(.1, .5)
# dt          =.1
# speed       =.2
# max_dur     =40
# th          =.5
# src_radius  =.02
# w           =.5
# d           =.05
# r           =5
# a           =.003
# tau         =100
step        =0.02


# def is_goal_found(pos_index):
#     dist = get_distance(x_grid, y_grid, src_pos)
#     if (dis < src_radius):
#         return True
#     else:
#         return False


def get_distance(x_grid, y_grid, pos):
    dx = x_grid - pos[0]
    dy = y_grid - pos[1]
    dist = np.sqrt(np.square(dx) + np.square(dy))
    return dist


def get_nearest_index(x_grid, y_grid, pos):
    dist = get_distance(x_grid, y_grid, pos)
    return np.argmin(dist)


def get_neighbor_id(id1, id2, alive):
    id = np.array([id1, id2])
    neighbor_list = []

    for shift in [(0,1), (0,-1), (1,0), (-1,0)]:
        neighbor_id = id + np.array(shift)
        if neighbor_id[0] < 0 or neighbor_id[0] > 100 or neighbor_id[1] < 0 or neighbor_id[1] > 50:
            pass
        elif alive[neighbor_id[0], neighbor_id[1]] is False:
            pass
        else:
            neighbor_list.append(neighbor_id)
    return neighbor_list


def get_mask(x_grid):
    map = np.zeros(x_grid.shape)
    map[40:50, 0:40] = 1 #add obstacle
    map[40:80, 30:40] = 1 #add obstacle
    mask = (map==1)
    return mask



def find_path(xs, ys, pos, goal):
    x_grid, y_grid = np.meshgrid(xs, ys, indexing='ij')
    shape = x_grid.shape

    dist_from_pos = np.full(shape, np.inf)
    parent = np.full(shape, "null_value")
    dead = np.full(shape, False)



    obs_mask = get_mask(x_grid)
    dead[obs_mask] = True


    goal_index = get_nearest_index(x_grid, y_grid, goal)
    start_index = get_nearest_index(x_grid, y_grid, pos)

    id1, id2 = np.unravel_index(start_index, shape)
    dist_from_pos[id1, id2] = 0
    parent[id1, id2] = str(-1) + ',' + str(-1)
    
    reach_goal = False

    while not reach_goal :
        dead[id1, id2] = True
        near_list = get_neighbor_id(id1, id2, dead)

        for i in range(len(near_list)):
            near_id = near_list[i]
            current_cost = dist_from_pos[near_id[0], near_id[1]]
            estimate_cost = dist_from_pos[id1, id2] + step

            if estimate_cost < current_cost:
                dist_from_pos[near_id[0], near_id[1]] = estimate_cost
                parent[near_id[0], near_id[1]] = str(id1) + ',' + str(id2) 

        visit_index = np.argmin(np.ma.MaskedArray(dist_from_pos, dead))
        id1, id2 = np.unravel_index(visit_index, shape)
        
        if (visit_index == goal_index):
            reach_goal = True  

    route = []
    last_parent_str = parent[id1, id2]

    while last_parent_str != "-1,-1":
        id1, id2 = [int(s) for s in last_parent_str.split(',')]
        route.append([x_grid[id1, id2], y_grid[id1, id2]])
        last_parent_str = parent[id1, id2]
        
    return(route)
    route.reverse()
    return np.array(route)
    
    # # # x = list(traj[:, 0])
    # # # y = list(traj[:, 1])
    # # # agent_pt, = ax_main.plot(x, y, 'bo')
    # # # ani = animation.F1plume.src_pos, marker='*', s=100, c='k', zorder=2)

    # # # # set figure axis limits
    # # # ax_main.set_xlim(extent[:2])
    # # # ax_main.set_ylim(extent[2:])

    # # # # make figure labels
    # # # ax_main.set_xlabel('x (m)')
    # # # ax_main.set_ylabel('y (m)')
    # # # plt.show()



        









# np.set_printoptions(threshold=sys.maxsize)

# plume = IdealPlume(src_pos=src_pos, w=w, d=d, r=r, a=a, tau=tau, dt=dt)
# xbs_ = plume.x_bounds
# ybs_ = plume.y_bounds
# xs = np.linspace(xbs_[0], xbs_[1], grid[0])
# ys = np.linspace(ybs_[0], ybs_[1], grid[1])
# pos = (1.6, 0.6)
# find_path(xs, ys, pos, src_pos)