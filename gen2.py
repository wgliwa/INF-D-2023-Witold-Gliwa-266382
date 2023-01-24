import time
from math import e, pow

import numpy as np
import pandas as pd
import pygad


def run_gen(size, strength, times):
    def calc3d(x):
        return np.linalg.norm(np.array([x[0], x[1], x[2]])
                              - np.array([x[3], x[4], x[5]]))

    def fitness_func(x, solution_idx=0):
        x = np.array_split(x, len(x) / 3)
        sum = 0
        for i in range(0, len(x)):
            for j in range(i + 1, len(x)):
                sum += pow(e, strength *
                           (1 - calc3d(np.append(x[i], x[j])))) \
                       * (pow(e, strength *
                              (1 - calc3d(np.append(x[i], x[j])))) - 2)
        return -sum

    def crossover(parents, offspring_size, pygad):
        offspring = []
        idx = 0
        while len(offspring) != offspring_size[0]:
            parent1 = parents[idx % parents.shape[0], :].copy()
            parent2 = parents[(idx + 1) % parents.shape[0], :].copy()
            random_split_point = 3 * round(np.random.choice(range(offspring_size[1])) / 3)
            parent1[random_split_point:] = parent2[random_split_point:]
            offspring.append(parent1)
            idx += 1
        return np.array(offspring)

    gene_space = {'low': -2.0, 'high': 2.0}
    sol_per_pop = 150
    num_genes = size * 3
    mean_times = []
    best_pred = 0.0
    best_solution = []
    for i in range(0, times):
        print(size, strength, i)
        start = time.time()
        ga_instance = pygad.GA(gene_space=gene_space,
                               num_generations=150,
                               num_parents_mating=int(sol_per_pop / 2),
                               fitness_func=fitness_func,
                               sol_per_pop=sol_per_pop,
                               num_genes=num_genes,
                               parent_selection_type="tournament",
                               keep_parents=int(sol_per_pop / 10),
                               crossover_type=crossover,
                               mutation_type="random",
                               mutation_percent_genes=20,
                               )

        ga_instance.run()
        end = time.time()
        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        prediction = -fitness_func(solution)
        mean_times.append(end - start)
        if prediction < best_pred:
            best_pred = prediction
            best_solution = solution
    return [size, strength, best_pred, np.mean(mean_times), np.min(mean_times), np.max(mean_times), best_solution]


n_particles = list(range(5, 12))
strengths = [3, 6, 10, 14]
res = pd.DataFrame(columns=['size', 'strength', 'best_pred', 'mean_time', 'min_time', 'max_time', 'best_pos'])
for i in n_particles:
    for j in strengths:
        res.loc[len(res)] = run_gen(i, j, 10)
res.to_csv("gen2.csv")
