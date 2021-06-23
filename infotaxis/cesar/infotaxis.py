import numpy as np
from bombyxsim.utils.geometry import Point
import bombyxsim.controllers.infotaxis_core as core
from collections import namedtuple, deque


class Infotaxis(object):

    def __init__(self, fps, xlim, ylim):

        self.dt = 1 / fps
        self.V = core.V
        self.D = core.D
        self.E = core.E
        self.tau = core.TAU
        self.agent_size = core.AGT_SIZE
        self.src_radius = core.SRC_RADIUS
        self._tblank = 0.0
        # self.xlim = xlim
        # self.ylim = ylim
        self.Ncells_x = core.NCX
        self.Ncells_y = core.NCY
        self.xbs = tuple([i / 1000 for i in xlim])
        # self.ybs = tuple([i / 1000 for i in ylim])
        self.ybs = (0, .720)
        # self.xbs = tuple([i for i in xlim])
        # self.ybs = tuple([i for i in ylim])
        self.xs = np.linspace(*self.xbs, self.Ncells_x)
        self.ys = np.linspace(*self.ybs, self.Ncells_y)
        # self.core = core(V, D, E, tau, agent_size)
        self.log_p_src = core.build_log_src_prior('uniform', self.xs, self.ys)
        self.agent_speed = core.AGT_SPEED
        self.entropy = core.entropy(self.log_p_src)
        self.delta_s_expected = 0
        self.entropies = deque(maxlen=10)
        self.hits = deque(maxlen=2 * fps)
        self.burstiness = 0
        self.hit_transitions = deque(maxlen=2)
        self.tb_on_hits = deque(maxlen=10)
        self.tb_B = 0
        self.dS_B = 0
        self.hit_B = 1
        self.wsum = 0
        # self.entropy_errors = deque(maxlen=fps)
        self.dS_mean = 0
        # self.SRMS = 0
        # self.delta_s_expecteds = []

    # @property
    # def action_space(self):
    #     # lin_v = LinearVel(0.0, 19.0, 0.8, 0.8)
    #     # ang_v = AngularVel(0.0, 0.062, 1.3, -1.3)

    #     u = {
    #         0: (0, 0),
    #         1: (self.agent_speed, 0),
    #         2: (-self.agent_speed, 0),
    #         3: (0, self.agent_speed),
    #         4: (0, -self.agent_speed),
    #     }

    #     return u
    def __str__(self):
        return 'wSum:{}, S:{:.4f}, tb_B:{:.4f}'.format(self.wsum, self.entropy,
                                                       self.tb_B)

    @property
    def log_header(self):
        return 'tblank,entropy,EDS,DSmean,wSum,hit_B,tb_B,ds_B'

    @property
    def log_step(self):
        return [
            self._tblank, self.entropy, self.delta_s_expected, self.dS_mean, self.wsum, self.hit_B, self.tb_B, self.dS_B
        ]

    def get_burstiness(self, x):
        B = (np.std(x) - np.mean(x)) / (np.std(x) + np.mean(x))
        return B

    def control(self, h, pos: Point):

        h = int(h > 0)

        # pos = (pos.x / 1000, pos.y / 1000)
        pos = (pos.x / 1000, ((360 + pos.y) / 1000))
        # pos = (pos.x, pos.y)
        # print(pos)
        # pos *= 1e-3

        self.log_p_src = core.update_log_p_src(
            pos, self.xs, self.ys, self.dt, h,
            self.V, self.D, self.E, self.agent_size, self.tau,
            self.src_radius, self.log_p_src)

        self.hits.append(h)
        self.hit_transitions.append(h)
        self.entropy = core.entropy(self.log_p_src)
        self.entropies.append(self.entropy)
        if len(self.entropies) >= 30:
            self.dS_mean = np.mean(np.diff(self.entropies))
            self.dS_B = self.get_burstiness(np.diff(self.entropies))

        # self.tb_on_hits.append(self._tblank)
        # if len(self.tb_on_hits) >= int(10 / (self.dt)):
        # self.tb_B = self.get_burstiness(self.tb_on_hits)

        if (len(self.hits) >= int(2 / (self.dt))) and (np.sum(self.hits) > 0):
            self.hit_B = self.get_burstiness(self.hits)

        if len(self.hit_transitions) > 1 and np.diff(
                self.hit_transitions)[0] > 0:
            self.tb_on_hits.append(self._tblank)
            self.wsum += 1

        if len(self.tb_on_hits) >= 10:
            self.tb_B = self.get_burstiness(self.tb_on_hits)

        if h:
            # if (self.hit_transitions[1] - self.hit_transitions[0]) > 0:
            self._tblank = .0

        # if (len(self.hits) >= 30) and (np.sum(self.hits) > 0):
        #     self.burstiness = (np.var(self.hits) - np.mean(self.hits)) / (
        #         np.var(self.hits) + np.mean(self.hits))

        moves = core.get_moves(pos, self.xs, self.ys, (self.dt * self.agent_speed))
        delta_s_expecteds = []

        # get entropy decrease given src found
        delta_s_src_found = -self.entropy

        for move in moves:

            # set entropy increase to inf if move is out of bounds
            if not round(self.xbs[0], 6) <= round(move[0], 6) <= round(self.xbs[1], 6):
                delta_s_expecteds.append(np.inf)
                continue
            elif not round(self.ybs[0], 6) <= round(move[1], 6) <= round(self.ybs[1], 6):
                delta_s_expecteds.append(np.inf)
                continue

            # get probability of finding source
            p_src_found = core.get_p_src_found(move, self.xs, self.ys, self.log_p_src, self.src_radius)
            p_src_not_found = 1 - p_src_found

            # loop over probability and expected entropy decrease for each sample
            p_samples = np.nan * np.zeros(len([0, 1]))
            delta_s_given_samples = np.nan * np.zeros(len([0, 1]))

            for ctr, h in enumerate([0, 1]):

                # probability of sampling h at pos
                p_sample = core.get_p_sample(
                    pos=move, xs=self.xs, ys=self.ys, dt=self.dt, h=h,
                    w=self.V, d=self.D, r=self.E, a=self.agent_size, tau=self.tau, log_p_src=self.log_p_src)

                # posterior distribution from sampling h at pos
                log_p_src_ = core.update_log_p_src(
                    pos=move, xs=self.xs, ys=self.ys, dt=self.dt, src_radius=self.src_radius,
                    h=h, w=self.V, d=self.D, r=self.E, a=self.agent_size, tau=self.tau, log_p_src=self.log_p_src)

                # decrease in entropy for this move/sample
                s_ = core.entropy(log_p_src_)
                delta_s_given_sample = s_ - self.entropy

                p_samples[ctr] = p_sample
                delta_s_given_samples[ctr] = delta_s_given_sample

            # get expected entropy decrease given source not found
            delta_s_src_not_found = p_samples.dot(delta_s_given_samples)

            # compute total expected entropy decrease
            delta_s_expected = (p_src_found * delta_s_src_found) + \
                (p_src_not_found * delta_s_src_not_found)

            delta_s_expecteds.append(delta_s_expected)
            self.delta_s_expected = delta_s_expected

        # print(len(self.delta_s_expecteds))
        # print('Length of moves: {}, best action index: {}'.format(
        # len(moves), np.argmin(delta_s_expecteds)))
        # print(moves[np.argmin(self.delta_s_expecteds)])

        # self.entropy_errors.append(self.entropy)
        try:
            best_action = moves[np.argmin(delta_s_expecteds)]
        except:
            best_action = moves[-1]
        return best_action
