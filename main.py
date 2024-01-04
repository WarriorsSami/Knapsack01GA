import json
import os

from utils import *

input_path = os.environ.get('INPUT_PATH')
mode = os.environ.get('MODE')
evolve_alg = os.environ.get('EVOLVE_ALG')

print('Input from: {}'.format(input_path))
print('Mode: {}'.format(mode))
print('Evolve algorithm: {}'.format(evolve_alg))

with open(input_path) as f:
    knapsack_config = json.load(f)

evolve = evolve_with_elitism if evolve_alg == 'elitism' else evolve_without_elitism
diversity_threshold = 1 / knapsack_config['population_size']

generation = 0
population = generate_population(knapsack_config)
fittest_tuple = population[0], get_fitness(population[0], knapsack_config), 0

fitness_history = []
diversity_history = []

while True:
    population = sort_population_by_fitness(population, knapsack_config)

    if get_fitness(population[0], knapsack_config) > fittest_tuple[1]:
        fittest_tuple = population[0], get_fitness(population[0], knapsack_config), generation

    print('Generation: {}'.format(generation))

    avg_fitness = get_population_avg_fitness(population, knapsack_config)
    fitness_history.append(avg_fitness)
    print('Average fitness: {}'.format(avg_fitness))

    diversity_rate = get_diversity_rate(population)
    diversity_history.append(diversity_rate)
    print('Diversity rate: {}'.format(diversity_rate))

    print_population(population, knapsack_config)

    match mode:
        case 'convergence':
            if diversity_rate <= diversity_threshold:
                print('Converged at generation {}'.format(generation))
                break
        case _:
            if generation == knapsack_config['generations'] - 1:
                break

    population = evolve(population, knapsack_config)
    generation += 1
    print()

plot_fitness_history(fitness_history)
plot_diversity_history(diversity_history)

show_possible_solution(fittest_tuple, knapsack_config)
