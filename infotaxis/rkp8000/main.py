import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from infotaxis import simulate
from plume_processing import IdealPlume
from obstacle import get_mask

agent_pt    = []
seed        = 8
grid        =(101, 51)
src_pos     =(.1, .5)
start_pos   =(1.9, 0.9)
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



fps = 30
nSeconds = 5
snapshots = []
im = []


def animate(i):
    # if hs[i] == 1:
    #     agent_pt.set_color('y')
    #     agent_pt.set_fillstyle('none')
    # else:
    #     agent_pt.set_color('b')
    #     agent_pt.set_fillstyle('full')

    if mode[i] == True:
        agent_pt.set_color('y')
    else:
        agent_pt.set_color('b')
        
    agent_pt.set_data(traj[:, 0][i], traj[:, 1][i])
    return agent_pt,


def animate_func(i):
    if i % fps == 0:
        print( '.', end ='' )

    im.set_array(snapshots[i].T)
    im.set_cmap('hot')
    return [im]


def visualize():
    # global agent_pt
    conc, extent = plume.get_profile(grid)
    # mask = get_mask(conc)
    # conc[mask] =  0


    # fig, ax_main = plt.subplots()
    # ax_main.imshow(conc.T, origin='lower', extent=extent, cmap='hot', zorder=0)
    
    # x = list(traj[:, 0])
    # y = list(traj[:, 1])
    # agent_pt, = ax_main.plot(x, y, 'bo')
    # ani = animation.FuncAnimation(fig, animate, frames=len(x), interval=20, blit=True, save_count=50,repeat=False)

    # # mark source location
    # ax_main.scatter(*plume.src_pos, marker='*', s=100, c='k', zorder=2)

    # # set figure axis limits, figure labels
    # ax_main.set_xlim(extent[:2])
    # ax_main.set_ylim(extent[2:])
    # ax_main.set_xlabel('x (m)')
    # ax_main.set_ylabel('y (m)')
    # plt.show()

    # ani.save('myAnimation.gif', writer='imagemagick', fps=30)



    global im 
    global snapshots
    fps = 30
    nSeconds = 5
    snapshots = log_p_srcs

    # First set up the figure, the axis, and the plot element we want to animate
    fig = plt.figure( figsize=(8,8) )

    a = snapshots[0]
    im = plt.imshow(a.T, origin='lower', extent=extent, cmap='hot', zorder=0)

    

    anim = animation.FuncAnimation(fig, animate_func, 
                                frames = nSeconds * fps,
                                interval = 1000 / fps, )

    print('Done!')
    plt.show()  # Not required, it seems!



if  __name__ == "__main__":
    # Generate a random ideal gas distribution
    np.random.seed(seed)                            
    plume = IdealPlume(src_pos=src_pos, w=w, d=d, r=r, a=a, tau=tau, dt=dt)

    # Running the infotaxis simulation
    traj, hs, src_found, log_p_srcs, mode = simulate(
        plume=plume, grid=grid, start_pos=start_pos, speed=speed, dt=dt, 
        max_dur=max_dur, th=th, src_radius=src_radius, w=w, d=d, r=r, a=a, tau=tau)

    if src_found:
        print('Source found after {} time steps ({} s)'.format(
            len(traj), len(traj) * dt))
    else:
        print('Source not found after {} time steps ({} s)'.format(
            len(traj), len(traj) * dt))

    visualize()