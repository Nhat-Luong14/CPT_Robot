import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt

from infotaxis import simulate
from plume_processing import IdealPlume
from obstacle import get_mask
from config import *

def animate(i):
    # if hs[i] == 1:
    #     agent_pt.set_color('y')
    #     agent_pt.set_fillstyle('none')
    # else:
    #     agent_pt.set_color('b')
    #     agent_pt.set_fillstyle('full')

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
    conc, extent = plume.get_profile(grid)
    mask = get_mask(conc.shape)
    conc[mask] =  0

    fig, ax_main = plt.subplots()
    ax_main.imshow(conc.T, origin='lower', extent=extent, cmap='hot', zorder=0)
    
    # x = list(traj[:, 0])
    # y = list(traj[:, 1])
    # agent_pt, = ax_main.plot(x, y, 'bo')
    # ani = animation.FuncAnimation(fig, animate, frames=len(x), interval=20, blit=True, save_count=50,repeat=False)

    # mark source location
    ax_main.scatter(*plume.src_pos, marker='*', s=100, c='k', zorder=2)

    # set figure axis limits, figure labels
    ax_main.set_xlim(extent[:2])
    ax_main.set_ylim(extent[2:])
    ax_main.set_xlabel('x (m)')
    ax_main.set_ylabel('y (m)')


    x = np.array([1.02,1.32,1.02,1.02,1.02,1.02,1.02,1.02,1.02,1.32,1.02,1.02,1.26])
    y = np.array([0.12,0.02,0,1,0.96,1,0.94,0.14,0.94,0.02,1,0.72,0.04])
    area = 100  # 0 to 15 point radii

    plt.scatter(x, y, s=area, alpha=0.5)
    plt.show()

    # ani.save('myAnimation.gif', writer='imagemagick', fps=30)


if  __name__ == "__main__":
    for i in range(20):
       
        # Generate a random ideal gas distribution
        np.random.seed(i+1)                            
        plume = IdealPlume(src_pos=src_pos, w=w, d=d, r=r, a=a, tau=tau, dt=dt)

        # Running the infotaxis simulation
        traj, hs, src_found, log_p_srcs, mode = simulate(
            plume=plume, grid=grid, start_pos=start_pos, speed=speed, dt=dt, 
            max_dur=max_dur, th=th, src_radius=src_radius, w=w, d=d, r=r, a=a, tau=tau)

        if src_found:
            print(i+1)
            print('Source found after {} time steps ({} s)'.format(
                len(traj), len(traj) * dt))
        else:
            print(i+1)
            print('Source not found after {} time steps ({} s)'.format(
                len(traj), len(traj) * dt))

        visualize()