import numpy as np
import matplotlib.pyplot as plt


def get_selected_items(chromosome, config):
    return list(
        map(lambda x: x[0],
            filter(lambda x: x[1] == 1,
                   zip(config['items'], chromosome),
                   ),
            ),
    )


def generate_chromosome(length):
    return np.random.randint(2, size=length)


def generate_population(config):
    return [generate_chromosome(len(config['items'])) for _ in range(config['population_size'])]


def get_fitness(chromosome, config):
    selected_items = get_selected_items(chromosome, config)

    total_weight = sum(map(lambda x: x['weight'], selected_items))
    total_value = sum(map(lambda x: x['value'], selected_items))

    if total_weight > config['capacity']:
        return -total_value
    else:
        return total_value


def get_population_avg_fitness(population, config):
    return np.mean([get_fitness(chromosome, config) for chromosome in population])


def select(population, size_rate, config):
    fitnesses = [get_fitness(chromosome, config) for chromosome in population]
    fitnesses = np.array(fitnesses)

    # normalize fitnesses
    min_fitness = abs(min(fitnesses))
    fitnesses = np.array(list(map(lambda x: x + min_fitness, fitnesses)))

    probabilities = list(map(lambda x: x / fitnesses.sum(), fitnesses))
    partial_probabilities_sum = list(map(lambda x: sum(probabilities[:x]), range(1, len(probabilities) + 1)))

    selections = []
    for _ in range(int(len(population) * size_rate)):
        r = np.random.uniform()
        chromosome_id = next(x[0] for x in enumerate(partial_probabilities_sum) if x[1] > r)

        selections.append(population[chromosome_id])

    return selections


def crossover(chromosome1, chromosome2):
    length = len(chromosome1)
    crossover_mask = np.random.randint(2, size=length)

    return (
        np.array([chromosome1[i] if crossover_mask[i] == 1 else chromosome2[i]
                  for i in range(length)]),
        np.array([chromosome2[i] if crossover_mask[i] == 1 else chromosome1[i]
                  for i in range(length)]),
    )


def mutate(chromosome, config):
    length = len(chromosome)
    mutation_rate = config['mutation_rate']
    mutation_probabilities = [np.random.uniform() for _ in range(length)]

    return np.array([chromosome[i] if mutation_probabilities[i] > mutation_rate else 1 - chromosome[i]
                     for i in range(length)])


def get_diversity_rate(population):
    return len(set(map(lambda x: tuple(x), population))) / len(population)


def sort_population_by_fitness(population, config):
    fitnesses = [get_fitness(chromosome, config) for chromosome in population]
    fitnesses = np.array(fitnesses)

    return [population[i] for i in np.argsort(fitnesses)[::-1]]


def evolve_without_elitism(population, config):
    # select parents
    parents = select(population, config['selection_rate'], config)

    # crossover parents to create len(population) children
    children = []
    for i in range(0, len(population), 2):
        parent1, parent2 = parents[np.random.randint(len(parents))], parents[np.random.randint(len(parents))]

        child1, child2 = crossover(parent1, parent2)

        children.append(child1)
        children.append(child2)

    # mutate children
    mutation_partitions = np.array_split(children, int(len(children) * config['mutation_population_rate']))
    mutated_children = mutation_partitions[0]
    non_mutated_children = mutation_partitions[1]

    mutated_children = [mutate(child, config) for child in mutated_children]

    # merge initial population with children
    population = population + list(mutated_children) + list(non_mutated_children)

    # sort population by fitness
    population = sort_population_by_fitness(population, config)

    # select survivors to match initial population size
    population = select(population, 1, config)[:config['population_size']]

    return population


def evolve_with_elitism(population, config):
    population = select(population, config)
    population = sort_population_by_fitness(population, config)

    # apply elitism
    elitism_size = int(config['population_size'] * config['elitism_rate'])
    new_population = population[:elitism_size]

    remaining_population_size = config['population_size'] - elitism_size

    # mating pool
    mating_pool_size = int(remaining_population_size * config['mating_pool_rate'])
    mating_pool = population[elitism_size:elitism_size + mating_pool_size]

    for _ in range(remaining_population_size):
        chromosome1, chromosome2 = (
            mating_pool[np.random.randint(len(mating_pool))],
            mating_pool[np.random.randint(len(mating_pool))]
        )

        chromosome1, chromosome2 = crossover(chromosome1, chromosome2)
        chromosome1 = mutate(chromosome1, config)
        chromosome2 = mutate(chromosome2, config)

        fitness1 = get_fitness(chromosome1, config)
        fitness2 = get_fitness(chromosome2, config)

        new_population.append(chromosome1 if fitness1 > fitness2 else chromosome2)

    return new_population


def print_population(population, config):
    fittest_chromosome, fitness = population[0], get_fitness(population[0], config)
    print('Fittest chromosome: {} (fitness: {})'.format(fittest_chromosome, fitness))

    print('Population: (len: {})'.format(len(population)))
    for chromosome_id, chromosome in enumerate(population):
        fitness = get_fitness(chromosome, config)
        print('Chromosome {}: {} (fitness: {})'.format(chromosome_id, chromosome, fitness))
    print()


def plot_fitness_history(fitness_history):
    plt.plot(fitness_history)
    plt.xlabel('Generation')
    plt.ylabel('Avg Fitness')
    plt.show()


def plot_diversity_history(diversity_history):
    plt.plot(diversity_history)
    plt.xlabel('Generation')
    plt.ylabel('Diversity Rate')
    plt.show()


def show_possible_solution(fittest_tuple, config):
    fittest_chromosome, fitness, generation = fittest_tuple

    selected_items = get_selected_items(fittest_chromosome, config)

    total_weight = sum(map(lambda x: x['weight'], selected_items))
    total_value = sum(map(lambda x: x['value'], selected_items))

    print('Solution found at generation: {}'.format(generation))
    print('Fittest chromosome: {} (fitness: {})'.format(fittest_chromosome, fitness))
    print('Selected items: {}'.format(selected_items))
    print('Total weight: {}'.format(total_weight))
    print('Total value: {}'.format(total_value))
