from math import e, pow

import numpy as np
import pygad

from plot import xd

gene_space = {'low': -1.5, 'high': 1.5}
strength = 6
size = 5


def calc3d(x):
    return np.linalg.norm(np.array([x[0], x[1], x[2]]) - np.array([x[3], x[4], x[5]]))


def fitness_func(x, solution_idx=0):
    x = np.array_split(x, len(x) / 3)
    sum = 0
    for i in range(0, len(x)):
        for j in range(i + 1, len(x)):
            sum += pow(e, strength * (1 - calc3d(np.append(x[i], x[j])))) * (
                    pow(e, strength * (1 - calc3d(np.append(x[i], x[j])))) - 2)
    return -sum


sol_per_pop = 200
num_genes = size * 3
ga_instance = pygad.GA(gene_space=gene_space,
                       num_generations=400,
                       num_parents_mating=int(sol_per_pop / 2),
                       fitness_func=fitness_func,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       parent_selection_type="rws",
                       keep_parents=int(sol_per_pop / 10),
                       crossover_type="scattered",
                       mutation_type="swap",
                       mutation_percent_genes=20,
                       crossover_probability=0.5)

ga_instance.run()
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
prediction = -fitness_func(solution)
print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))
ga_instance.plot_fitness(save_dir=f"A_PLOT_Size{size}strength{strength}")
xd(solution, f"A_FIGURE_Size{size}strength{strength}")
