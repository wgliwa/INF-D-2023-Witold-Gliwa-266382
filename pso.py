from math import e, pow

import numpy as np
import pyswarms as ps
from pyswarms.utils.plotters import plot_cost_history

from plot import xd

strength = 10
size = 7


def calc3d(x):
    return np.linalg.norm(np.array([x[0], x[1], x[2]]) - np.array([x[3], x[4], x[5]]))


def help2(x):
    x = np.array_split(x, len(x) / 3)
    sum = 0
    for i in range(0, len(x)):
        for j in range(i + 1, len(x)):
            sum += pow(e, strength * (1 - calc3d(np.append(x[i], x[j])))) * (
                    pow(e, strength * (1 - calc3d(np.append(x[i], x[j])))) - 2)
    return -sum


def f(x):
    n_particles = x.shape[0]
    j = [help2(x[i]) for i in range(n_particles)]
    return np.array(j)


options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
my_bounds = ([-1.5] * (size * 3), [1.5] * (size * 3))
optimizer = ps.single.GlobalBestPSO(n_particles=100, dimensions=size * 3, options=options, bounds=my_bounds)
cost, pos = optimizer.optimize(f, iters=100, )
cost_history = optimizer.cost_history
final_best_pos = ps.global_best
xd(pos, f"PSO_FIGURE_Size{size}strength{strength}")
plot = plot_cost_history(cost_history)
fig = plot.get_figure()
fig.savefig(f"PSO_PLOT_Size{size}strength{strength}.png")
