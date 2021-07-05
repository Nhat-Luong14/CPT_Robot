import config
import numpy as np
from copy import copy
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from utilities import build_log_src_prior, update_log_p_src
from utilities import entropy, get_moves, get_p_src_found, get_p_sample
from plume_processing import IdealInfotaxisPlume

if __name__ == "__main__":
    xs = np.linspace(config.x_bounds[0], config.x_bounds[1], config.grid[0])
    ys = np.linspace(config.y_bounds[0], config.y_bounds[1], config.grid[1])    
    
    # initialize source distribution and position
    log_p_src = build_log_src_prior('uniform', xs=xs, ys=ys)
    
    pos = config.start_pos
    traj = [copy(pos)]  # position sequence
    hs = []  # hit sequence

    
    np.random.seed(config.seed)
    plume = IdealInfotaxisPlume(src_pos=config.src_pos)

    # while True: #for in searching time
    for t_ctr, t in enumerate(np.arange(0, config.max_dur, config.dt)):
        # check if source has been found
        if np.linalg.norm(np.array(pos) - config.src_pos) < config.src_radius:
            src_found = True
            break

        ###################################################################################
        # sample hit or miss from plume
        # c = plume.sample(pos, t)
        # h = int(c >= th)    
        
        c = plume.sample(pos, t)        #read value from ARX
        h = int(c >= config.th)
        hs.append(h)
        #########################################################


        # update source posterior
        log_p_src = update_log_p_src(pos=pos, xs=xs, ys=ys, h=h, log_p_src=log_p_src)
        s = entropy(log_p_src)

        # pick next move so as to maximally decrease expected entropy
        # moves = get_moves(pos, xs, ys, step=speed*dt)
        moves = get_moves(pos, step=config.step_size)
        delta_s_expecteds = []

        # estimate expected decrease in p_source entropy for each possible move
        for move in moves:
            # set entropy increase to inf if move is out of bounds
            if not round(config.x_bounds[0], 6) <= round(move[0], 6) <= round(config.x_bounds[1], 6):
                delta_s_expecteds.append(np.inf)
                continue
            elif not round(config.y_bounds[0], 6) <= round(move[1], 6) <= round(config.y_bounds[1], 6):
                delta_s_expecteds.append(np.inf)
                continue

            # get probability of finding source
            p_src_found = get_p_src_found(pos=move, xs=xs, ys=ys, log_p_src=log_p_src)
            p_src_not_found = 1 - p_src_found

            # loop over probability and expected entropy decrease for each sample
            sample_domain = [0, 1]  # miss and hit
            p_samples = np.nan * np.zeros(len(sample_domain))
            delta_s_given_samples = np.nan * np.zeros(len(sample_domain))

            for ctr, h in enumerate(sample_domain):
                # probability of sampling h at pos
                p_sample = get_p_sample(pos=move, xs=xs, ys=ys, h=h, log_p_src=log_p_src)

                # posterior distribution from sampling h at pos
                log_p_src_ = update_log_p_src(pos=pos, xs=xs, ys=ys, h=h, log_p_src=log_p_src)

                # decrease in entropy for this move/sample
                s_ = entropy(log_p_src_)
                delta_s_given_sample = s_ - s

                p_samples[ctr] = p_sample
                delta_s_given_samples[ctr] = delta_s_given_sample

            # get expected entropy decrease given source not found
            delta_s_src_not_found = p_samples.dot(delta_s_given_samples)

            # get entropy decrease given src found
            delta_s_src_found = -s

            # compute total expected entropy decrease
            delta_s_expected = (p_src_found * delta_s_src_found) + (p_src_not_found * delta_s_src_not_found)

            delta_s_expecteds.append(delta_s_expected)

       # choose move that decreases p_source entropy the most
        pos = moves[np.argmin(delta_s_expecteds)]
        traj.append(copy(pos))
    else:
        src_found = False

    if src_found:
        print('Source found after {} time steps ({} s)'.format(
            len(traj), len(traj) * config.dt))
    else:
        print('Source not found after {} time steps ({} s)'.format(
            len(traj), len(traj) * config.dt))

    # convert results to arrays
    traj = np.array(traj)
    hs = np.array(hs)
    # remove last position so that traj and hs are same length
    traj = traj[:-1]



    
    # plot full trajectory overlaid on plume profile
    conc, extent = plume.get_profile(config.grid)
    fig, ax_main = plt.subplots()
    # ax_main = fig.add_subplot(gs[:2, :])
    ax_main.imshow(conc.T, origin='lower', extent=extent, cmap='hot', zorder=0)
    
    # plot trajectory and hits
    ax_main.plot(traj[:, 0], traj[:, 1], lw=2, color='w', zorder=1)
    ax_main.scatter(traj[hs > 0, 0], traj[hs > 0, 1], marker='D', s=50, c='c', zorder=2)
    ax_main.scatter(*config.start_pos, s=30, c='b', zorder=2)           # mark starting position
    ax_main.scatter(*plume.src_pos, marker='*', s=100, c='k', zorder=2) # mark source location
    ax_main.set_xlim(extent[:2])        # set figure axis limits
    ax_main.set_ylim(extent[2:])

    ax_main.set_xlabel('x (m)')
    ax_main.set_ylabel('y (m)')

    plt.show()