from infotaxis import get_hit_rate
import numpy as np
from config import *

class IdealPlume(object):
    def __init__(self):
        pass


    def sample(self, pos):
        hit_rate = get_hit_rate(src_pos[0], src_pos[1], pos)[0, 0] #1x1 matrix only
        mean_hits = hit_rate * dt
        sample = int(np.random.poisson(lam=mean_hits) > 0)
        return sample


    def get_profile(self):
        conc = np.nan * np.zeros((len(xs), len(ys)))
        for x_ctr, x in enumerate(xs):
            for y_ctr, y in enumerate(ys):
                hit_rate = get_hit_rate(src_pos[0], src_pos[1], pos=(x, y))[0, 0]
                conc[x_ctr, y_ctr] = hit_rate

        dx = np.mean(np.diff(xs))
        dy = np.mean(np.diff(ys))
        x_lim = [xs[0] - dx/2, xs[-1] + dx/2]
        y_lim = [ys[0] - dy/2, ys[-1] + dy/2]
        extent = x_lim + y_lim

        return conc, extent