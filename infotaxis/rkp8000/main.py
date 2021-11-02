import numpy as np
import matplotlib.pyplot as plt

from infotaxis import simulate
from plume_processing import IdealPlume
from obstacle import get_mask
from config import *
import matplotlib.animation as animation

agent_pt    = []

def animate(i):
    if hs[i] == 1:
        agent_pt.set_color('y')
        agent_pt.set_fillstyle('none')
    else:
        agent_pt.set_color('b')
        agent_pt.set_fillstyle('full')

    if mode[i] == True:
        agent_pt.set_color('y')
        if hs[i] == 1:
            agent_pt.set_fillstyle('full')
        else:
            agent_pt.set_fillstyle('none')
    else:
        agent_pt.set_color('b')
        if hs[i] == 1:
            agent_pt.set_fillstyle('full')
        else:
            agent_pt.set_fillstyle('none')
        
    agent_pt.set_data(traj[:, 0][i], traj[:, 1][i])
    return agent_pt,


def visualize():
    global agent_pt
    conc, extent = plume.get_profile()
    mask = get_mask()
    conc[mask] = 0

    fig, ax_main = plt.subplots()
    ax_main.imshow(conc.T, origin='lower', extent=extent, cmap='hot', zorder=0)
    
    x = list(traj[:, 0])
    y = list(traj[:, 1])
    agent_pt, = ax_main.plot(x, y, 'bo')
    ani = animation.FuncAnimation(fig, animate, frames=len(x), interval=20, blit=True, save_count=50,repeat=False)

    # mark source location
    ax_main.scatter(*src_pos, marker='*', s=100, c='k', zorder=2)

    # set figure axis limits, figure labels
    ax_main.set_xlim(extent[:2])
    ax_main.set_ylim(extent[2:])
    ax_main.set_xlabel('x (m)')
    ax_main.set_ylabel('y (m)')

    plt.show()

    # ani.save('myAnimation.gif', writer='imagemagick', fps=30)


if  __name__ == "__main__":
    for i in range(2):
        # Generate a random ideal gas distribution
        np.random.seed(i+1)                            
        plume = IdealPlume()
        traj, hs, src_found, log_p_srcs, mode = simulate(plume)


        if src_found:
            print('Trial {}: Source found after {} time steps ({} s)'.format(
                i+1, len(traj), len(traj) * dt))
        else:
            print('Trial {}: Source not found after {} time steps ({} s)'.format(
                i+1, len(traj), len(traj) * dt))
        print('=============================================================')

        visualize()