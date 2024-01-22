import json
import os

from utils import *

input_path = os.environ.get('INPUT_PATH')
mode = os.environ.get('MODE')
evolve_alg = os.environ.get('EVOLVE_ALG')
print_mode = os.environ.get('PRINT_MODE')

print('Input from: {}'.format(input_path))
print('Mode: {}'.format(mode))
print('Evolve algorithm: {}'.format(evolve_alg))

print('Evolving...')

with open(input_path) as f:
    knapsack_config = json.load(f)

evolve = evolve_with_elitism if evolve_alg == 'elitism' else evolve_without_elitism
diversity_threshold = 1 / knapsack_config['population_size']
diversity_rate_diff_cnt = 0

generation = 0
population = generate_population(knapsack_config)
fittest_tuple = population[0], get_fitness(population[0], knapsack_config), 0

fitness_history = []
diversity_history = []

while True:
    population = sort_population_by_fitness(population, knapsack_config)

    if get_fitness(population[0], knapsack_config) > fittest_tuple[1]:
        fittest_tuple = population[0], get_fitness(population[0], knapsack_config), generation

    if print_mode == 'verbose':
        print('Generation: {}'.format(generation))

    avg_fitness = get_population_avg_fitness(population, knapsack_config)
    fitness_history.append(avg_fitness)

    if print_mode == 'verbose':
        print('Average fitness: {}'.format(avg_fitness))

    diversity_rate = get_diversity_rate(population)
    diversity_history.append(diversity_rate)

    if print_mode == 'verbose':
        print('Diversity rate: {}'.format(diversity_rate))

    if print_mode == 'verbose':
        print_population(population, knapsack_config)

    if len(diversity_history) > 1:
        if abs(diversity_history[-1] - diversity_history[-2]) <= knapsack_config['diversity_rate_diff']:
            diversity_rate_diff_cnt += 1
        else:
            diversity_rate_diff_cnt = 0

    match mode:
        case 'convergence':
            if (diversity_rate <= diversity_threshold
                    or diversity_rate_diff_cnt >= knapsack_config['diversity_rate_diff_cnt']):
                print('Converged at generation {}'.format(generation))
                break
        case _:
            if generation == knapsack_config['generations'] - 1:
                break

    population = evolve(population, knapsack_config)
    generation += 1

    if print_mode == 'verbose':
        print()

plot_fitness_history(fitness_history)
plot_diversity_history(diversity_history)

show_possible_solution(fittest_tuple, knapsack_config)
