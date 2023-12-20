import json
import sys

from utils import *

# get input path from command line arguments
input_path = sys.argv[1]
print('Input from: {}'.format(input_path))

with open(input_path) as f:
    knapsack_config = json.load(f)

generation = 0
population = generate_population(knapsack_config)
fittest_tuple = population[0], get_fitness(population[0], knapsack_config), 0

fitness_history = []
diversity_history = []

for generation in range(knapsack_config['generations']):
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

    if generation == knapsack_config['generations'] - 1:
        break

    population = evolve(population, knapsack_config)
    print()

plot_fitness_history(fitness_history)
plot_diversity_history(diversity_history)

show_possible_solution(fittest_tuple, knapsack_config)
