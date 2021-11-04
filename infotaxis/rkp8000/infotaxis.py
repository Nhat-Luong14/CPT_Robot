from copy import copy
import numpy as np
from scipy.special import k0
from scipy.stats import entropy as entropy_
from dijkstra import find_path
from obstacle import get_region, is_collision
from collections import deque
from config import *

"""
Calculate entropy. Wrapper around scipy.stats entropy function 
that takes in a 2D log probability distribution.
log_p_src: 2D array of log probabilities
"""
def entropy(log_p_src):
    p_src = np.exp(log_p_src)
    p_src /= p_src.sum()    # normalizes to 1
    return entropy_(p_src.flatten())


"""Logarithm of modified bessel function of the second kind of order 0.
Infinite values may still be returned if argument is too close to zero.
"""
def log_k0(x):
    y = k0(x)
    try:    # if array
        logy = np.zeros(x.shape, dtype=float)

        # attempt to calculate bessel function for all elements in x
        logy[y!=0] = np.log(y[y!=0])

        # for zero-valued elements use approximation
        logy[y==0] = -x[y==0] - np.log(x[y==0]) + np.log(np.sqrt(np.pi/2))
        return logy
    except:
        if y == 0:
            return -x - np.log(x) + np.log(np.sqrt(np.pi/2))
        else:
            return np.log(y)


"""
Construct a log-probability distribution from a prior type specifier.
Units are probability per area. (Not cell area but map area)    
"""
def build_log_src_prior(prior_type, xs, ys):
    dx = np.mean(np.diff(xs))
    dy = np.mean(np.diff(ys))
    
    if prior_type == 'uniform':
        log_p_unnormalized = np.ones(grid_shape)
        norm_factor = np.sum(np.exp(log_p_unnormalized) * dx * dy)  # e*dS*Ncell
        log_norm_factor = np.log(norm_factor)                       # 1+log(S)
        log_src_prior = log_p_unnormalized - log_norm_factor        # -logS (S > x*y beacuse it contains the boundary)
    else:
        raise NotImplementedError
    
    # Add obstacles
    mask, blind_zone, bound_zone = get_region()
    log_src_prior[mask] = -np.inf
    return log_src_prior                     


"""
Get the possible moves from a position given a constant speed.
"""
def get_moves(pos, step):
    moves = []
    for dx, dy in [(-step, 0), (step, 0), (0, -step), (0, step), (0, 0)]:
        x = pos[0] + dx
        y = pos[1] + dy
        next_pos = (x, y)
        if not is_collision(xs, ys, next_pos):
            moves.append(next_pos)
    return moves


"""
Return the probability that a position is within source radius
:param pos: position to calc prob that you are close to source
:param log_p_src: log probability distribution over source position
"""
def get_p_src_found(pos,log_p_src):
    
    # get mask containing only points within radius of pos
    dxs = pos[0] - x_grid                                          #distance to x,y matrix of cells to point
    dys = pos[1] - y_grid

    # sum probabilities contained in mask
    mask = (dxs**2 + dys**2 < src_radius**2)                        #cell has distance inside the radius is set true
    p_src = np.exp(log_p_src)                                   #return back to the probability map before logarith
    p_src /= p_src.sum()                                        #? chia cho 1?
    p_src_found = p_src[mask].sum()                             #total probabity the soucre inside the radius area
    return p_src_found


def coor2cell(pos):
    x_cell = round((pos[0] - x_bounds[0])/step)
    y_cell = round((pos[1] - y_bounds[0])/step)
    return(x_cell, y_cell)


"""
Calculate hit rate at specified position for grid of possible source locations.
This is given by Eq. 7 in the infotaxis paper
:param pos: position where hit rate is calculated (m)
:return: grid of hit rates, with one value per source location
"""
def get_hit_rate(xs_src, ys_src, pos):
    mask, blind_zone, bound_zone = get_region()
    xs_src_, ys_src_ = np.meshgrid(xs_src, ys_src, indexing='ij')   #create matrix of x and y
    dx = pos[0] - xs_src_               # matrix of distance form a postion to each cells
    dy = pos[1] - ys_src_

    pos_cell = coor2cell(pos)

    # round dx's and dy's less than resolution down to zero
    resolution=0.00001
    dx[np.abs(dx) < resolution] = 0
    dy[np.abs(dy) < resolution] = 0

    ry = np.exp( -2* np.square(dy/(lam+dx*d)) )

    mask_1 = dx >= 1/np.sqrt(decay_param)
    mask_2 = dx < 0
    rx = 1 - decay_param*(np.square(dx) + np.square(dy))
    rx[mask_1]= 0
    rx[mask_2] = 0

    rm = 1/(random_walk_param*(np.square(dx) + np.square(dy) + 1))
    
    # if blind_zone[pos_cell] == True:
    #     first_term = 0
    # else: 
    #     first_term = rx*ry





    scale_factor = release_rate / np.log(lam/a)
    exp_term = np.exp((w/(2*d))*dx)
    abs_dist = np.sqrt(dx**2 + dy**2)
    bessel_term = np.exp(log_k0(abs_dist / lam))

    if blind_zone[pos_cell] == True:
        first_term = 0
    else: 
        first_term = scale_factor * exp_term * bessel_term


    

    if bound_zone[pos_cell] == True:
        second_term = rx/2
    else: 
        second_term = 0
        
    # hit_rate = release_rate*(first_term + second_term + rm)
    hit_rate = release_rate*(rm + second_term + first_term)

    
    if hit_rate.shape != (1,1):
        
        hit_rate[mask] = 0.000000000001 #advoid devide by zero
    return hit_rate


"""
Get the probability of sampling h at position pos.
:param log_p_src: log probability distribution over source position
:return: probability
"""
def get_p_sample(pos, h, log_p_src):
    
    # poisson probability of no hit given mean hit rate
    hit_rate = get_hit_rate(xs, ys, pos)       #matrix form (hit/ miss rate at a position given a matrix of possible src)
    p_no_hits = np.exp(-dt * hit_rate)

    if h == 0:
        p_samples = p_no_hits
    elif h == 1:
        p_samples = 1 - p_no_hits
    else:
        raise Exception('h must be either 0 (no hit) or 1 (hit)')

    # get source distribution
    p_src = np.exp(log_p_src)
    p_src /= p_src.sum()            #normalize the distribution

    # make sure p_src being 0 wins over p_sample being nan/inf
    p_samples[p_src == 0] = 0

    # average over all source positions
    p_sample = np.sum(p_samples * p_src)
    return p_sample


"""
Update the log posterior over the src given sample h at position pos.
    :param pos: position
    :param log_p_src: previous estimate of log src posterior
    :return: new (unnormalized) log src posterior
"""
def update_log_p_src(pos, h, log_p_src):
    # get mean number of hits at pos given different src positions
    mean_hits = dt * get_hit_rate(xs, ys, pos)

    # calculate log-likelihood (prob of h at pos given src position [Poisson])
    if h == 0:
        log_like = -mean_hits
    else:
        log_like = np.log(1 - np.exp(-mean_hits))

    # compute the new log src posterior
    log_p_src = log_like + log_p_src

    # set log prob to -inf: area around the agent (r = radius source) has posibility = 0
    mask = ((pos[0]-x_grid)**2 + (pos[1]-y_grid)**2 < src_radius**2)
    log_p_src[mask] = -np.inf

    # if we've exhausted the search space start over
    if np.all(np.isinf(log_p_src)):
        log_p_src = np.ones(log_p_src.shape)
    return log_p_src


def get_entropy_gain(moves, s, log_p_src):
    # estimate expected decrease in p_source entropy for each possible move
    delta_s_expecteds = []
    delta_s_src_found = -s      # entropy decrease given src found
    sample_domain = [0, 1]
    
    for move in moves:
        # set entropy increase to inf if out of bounds
        if not round(x_bounds[0], 6) <= round(move[0], 6) <= round(x_bounds[1], 6):
            delta_s_expecteds.append(np.inf)
            continue
        elif not round(y_bounds[0], 6) <= round(move[1], 6) <= round(y_bounds[1], 6):
            delta_s_expecteds.append(np.inf)
            continue

        # get probability of finding source
        p_src_found = get_p_src_found(move,log_p_src)
        p_src_not_found = 1 - p_src_found

        # loop over probability and expected entropy decrease for each sample
        p_samples = np.nan * np.zeros(len(sample_domain))
        delta_s_given_samples = np.nan * np.zeros(len(sample_domain))

        for ctr, h in enumerate(sample_domain):
            p_sample = get_p_sample(move, h, log_p_src)         # probability of sampling h at pos
            log_p_src_ = update_log_p_src(move, h, log_p_src)   # posterior distribution from sampling h at pos                       
            delta_s_given_sample = entropy(log_p_src_) - s    # decrease in entropy for this move/sample

            p_samples[ctr] = p_sample
            delta_s_given_samples[ctr] = delta_s_given_sample

        # get expected entropy decrease given source not found
        delta_s_src_not_found = p_samples.dot(delta_s_given_samples)

        # compute total expected entropy decrease
        delta_s_expected = (p_src_found * delta_s_src_found) + \
            (p_src_not_found * delta_s_src_not_found)

        delta_s_expecteds.append(delta_s_expected)
    return delta_s_expecteds



"""
Run the infotaxis simulation.
:param plume: plume object
:return: trajectory, hit array, src_found flag, [list of source posteriors]
"""
def simulate(plume):
    if lam <= a:
        raise Exception('lambda must be greater than a')

    djkstra_mode  = False
    log_p_src  = build_log_src_prior('uniform', xs, ys)    # initialize source distribution
    pos        = start_pos
    traj       = [copy(start_pos)]   # position sequence
    h_seq      = []            # hit sequence
    s_seq      = []            # entropy sequence
    mode_seq   = [djkstra_mode]            # path generated by Djkstra
    path       = []    
    log_p_src_seq = [log_p_src]         # log src posterior sequence
    duplicate_list = deque(maxlen=10)

    for t in np.arange(0, max_dur, dt):
        # check if source has been found
        if np.linalg.norm(np.array(pos) - src_pos) < src_radius:
            src_found = True
            break
        
        mode_seq.append(djkstra_mode)

        # sample hit or miss at pos from plume
        h = plume.sample(pos)   
        h_seq.append(h)
        
        # update source posterior
        log_p_src = update_log_p_src(pos, h, log_p_src)
        s = entropy(log_p_src)
        log_p_src_seq.append(log_p_src)
        s_seq.append(s)

        # Getting possible moves base on the planning mode
        if djkstra_mode:
            moves = [path.pop()]
            if len(path) == 0:
                print("Switch to Infotaxis " + str(pos))
                djkstra_mode = False
        else:
            path.clear()
            moves = get_moves(pos, step)


        delta_s_expecteds = get_entropy_gain(moves, s, log_p_src)

        # choose move that decreases p_source entropy the most
        pos = moves[np.argmin(delta_s_expecteds)]

        # if traj.count(pos):
        #     duplicate_list.append(True)
        # else:
        #     duplicate_list.append(False)

        # if duplicate_list.count(True) > 5 and djkstra_mode == False:
        #     print("Switch to Djkstra at " + str(pos))
        #     djkstra_mode = True
        #     goal_id = np.unravel_index(np.argmax(log_p_src), log_p_src.shape)
        #     goal =(x_grid[goal_id], y_grid[goal_id])
        #     path = find_path(pos, goal)

        traj.append(copy(pos))
    else:
        src_found = False

    # remove last position so that traj and h_seq are same length
    # convert results to arrays
    traj = np.array(traj[:-1])
    h_seq = np.array(h_seq)
    return traj, h_seq, src_found, log_p_src_seq, mode_seq