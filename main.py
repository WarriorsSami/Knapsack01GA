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
fitness_history = []
diversity_history = []

while generation < knapsack_config['generations']:
    print('Generation: {}'.format(generation))

    avg_fitness = get_population_avg_fitness(population, knapsack_config)
    fitness_history.append(avg_fitness)
    print('Average fitness: {}'.format(avg_fitness))

    diversity_rate = get_diversity_rate(population)
    diversity_history.append(diversity_rate)
    print('Diversity rate: {}'.format(diversity_rate))

    fittest_chromosome, fitness = get_fittest_chromosome(population, knapsack_config)
    print('Fittest chromosome: {} (fitness: {})'.format(fittest_chromosome, fitness))

    population = evolve(population, knapsack_config)

    print()
    generation += 1

plot_fitness_history(fitness_history)
plot_diversity_history(diversity_history)
