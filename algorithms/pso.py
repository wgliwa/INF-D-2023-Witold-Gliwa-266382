import time
from math import e, pow

import numpy as np
import pyswarms as ps


def run_pso(size, strength, times):
    def calc3d(x):
        return np.linalg.norm(np.array([x[0], x[1], x[2]]) - np.array([x[3], x[4], x[5]]))

    def help2(x):
        x = np.array_split(x, len(x) / 3)
        sum = 0
        for i in range(0, len(x)):
            for j in range(i + 1, len(x)):
                sum += pow(e, strength * (1 - calc3d(np.append(x[i], x[j])))) * (
                        pow(e, strength * (1 - calc3d(np.append(x[i], x[j])))) - 2)
        return sum

    def f(x):
        n_particles = x.shape[0]
        j = [help2(x[i]) for i in range(n_particles)]
        return np.array(j)

    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
    my_bounds = ([-2.0] * (size * 3), [2.0] * (size * 3))
    mean_times = []
    best_pred = 0.0
    best_solution = []
    for i in range(0, times):
        print(size, strength, i)
        start = time.time()
        optimizer = ps.single.GlobalBestPSO(n_particles=150, dimensions=size * 3, options=options, bounds=my_bounds)
        cost, pos = optimizer.optimize(f, iters=150, )
        end = time.time()
        mean_times.append(end - start)
        if cost < best_pred:
            best_pred = cost
            best_solution = pos

    return [size, strength, best_pred, np.mean(mean_times), np.min(mean_times), np.max(mean_times), best_solution]


n_particles = list(range(5, 12))
strengths = [3, 6, 10, 14]
for i in n_particles:
    for j in strengths:
        open('results/pso_results.txt', 'a').write(';'.join(str(i) for i in run_pso(i, j, 10)))
        open('results/pso_results.txt', 'a').write("\n")
