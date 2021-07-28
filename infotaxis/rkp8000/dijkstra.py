import numpy as np
from plume_processing import IdealPlume
from obstacle import get_mask
import matplotlib.pyplot as plt
import sys

agent_pt    = []
seed        =8 
grid        =(101, 51)
src_pos     =(.1, .5)
dt          =.1
speed       =.2
max_dur     =40
th          =.5
src_radius  =.02
w           =.5
d           =.05
r           =5
a           =.003
tau         =100
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




def find_path(xs, ys, pos):
    x_grid, y_grid = np.meshgrid(xs, ys, indexing='ij')
    shape = x_grid.shape

    dist_from_pos = np.full(shape, np.inf)
    parent = np.full(shape, "none")
    dead = np.full(shape, False)

    goal_index = get_nearest_index(x_grid, y_grid, src_pos)
    start_index = get_nearest_index(x_grid, y_grid, pos)

    id1, id2 = np.unravel_index(start_index, shape)

    dist_from_pos[id1, id2] = 0
    parent[id1, id2] = str([-1, -1])
    
    reach_goal = False

    # for i in range(100):
    while not reach_goal :
        dead[id1, id2] = True
        near_list = get_neighbor_id(id1, id2, dead)

        for i in range(len(near_list)):
            near_id = near_list[i]
            current_cost = dist_from_pos[near_id[0], near_id[1]]
            estimate_cost = dist_from_pos[id1, id2] + step

            if estimate_cost < current_cost:
                dist_from_pos[near_id[0], near_id[1]] = estimate_cost
                parent[near_id[0], near_id[1]] = str([id1, id2])

        visit_index = np.argmin(np.ma.MaskedArray(dist_from_pos, dead))
        if (visit_index == goal_index):
            reach_goal = True  
            print("dmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")

        id1, id2 = np.unravel_index(visit_index, shape)
        print(id1, id2)















    #     x = x_grid.item(visit_index)
    #     y = y_grid.item(visit_index)








    #     dist = get_distance(x_grid, y_grid, (x,y))

    #     alive.flat[visit_index] = False
        
    #     new_dist = dist_from_pos.item(visit_index) + dist
    #     mask = (new_dist < dist_from_pos)*alive

    #     dist_from_pos[mask] = new_dist[mask]
    #     parent[mask] = visit_index

    #     tmp_gid = dist_from_pos
    #     tmp_gid[~alive] = np.inf
    #     visit_index = np.argmin(tmp_gid)
    #     if (visit_index == goal_index):
    #         reach_goal = True    

    # # list_index = []
    # # parent_id = parent.item(visit_index)




    # # for i in range(30):
    # #     list_index.append(parent_id)
    # #     parent_id = parent.item(int(parent_id))
    # #     if parent_id == -1:
    # #         break

    
    
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



        









np.set_printoptions(threshold=sys.maxsize)

plume = IdealPlume(src_pos=src_pos, w=w, d=d, r=r, a=a, tau=tau, dt=dt)
xbs_ = plume.x_bounds
ybs_ = plume.y_bounds
xs = np.linspace(xbs_[0], xbs_[1], grid[0])
ys = np.linspace(ybs_[0], ybs_[1], grid[1])
pos = (1.6, 0.6)
find_path(xs, ys, pos)