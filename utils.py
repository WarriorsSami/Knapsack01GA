import numpy as np
import matplotlib.pyplot as plt


def generate_chromosome(length):
    return np.random.randint(2, size=length)


def generate_population(config):
    return [generate_chromosome(len(config['items'])) for _ in range(config['population_size'])]


def get_fitness(chromosome, config):
    selected_items = list(
        map(lambda x: x[0],
            filter(lambda x: x[1] == 1,
                   zip(config['items'], chromosome),
                   ),
            ),
    )

    total_weight = sum(map(lambda x: x['weight'], selected_items))
    total_value = sum(map(lambda x: x['value'], selected_items))

    if total_weight > config['capacity']:
        return -total_value
    else:
        return total_value


def get_population_avg_fitness(population, config):
    return np.mean([get_fitness(chromosome, config) for chromosome in population])


def select(population, config):
    fitnesses = [get_fitness(chromosome, config) for chromosome in population]
    fitnesses = np.array(fitnesses)

    probabilities = list(map(lambda x: x / fitnesses.sum(), fitnesses))
    partial_probabilities_sum = list(map(lambda x: sum(probabilities[:x]), range(1, len(probabilities) + 1)))

    selections = []
    for _ in range(len(population)):
        r = np.random.uniform()
        chromosome_id = next(x[0] for x in enumerate(partial_probabilities_sum) if x[1] > r)

        selections.append(population[chromosome_id])

    return selections


def crossover(chromosome1, chromosome2):
    length = len(chromosome1)
    crossover_mask = np.random.randint(2, size=length)

    return (
        [chromosome1[i] if crossover_mask[i] == 1 else chromosome2[i] for i in range(length)],
        [chromosome2[i] if crossover_mask[i] == 1 else chromosome1[i] for i in range(length)],
    )


def mutate(chromosome, config):
    length = len(chromosome)
    mutation_rate = config['mutation_rate']
    mutation_probabilities = [np.random.uniform() for _ in range(length)]

    return [chromosome[i] if mutation_probabilities[i] > mutation_rate else 1 - chromosome[i] for i in range(length)]


def get_fittest_chromosome(population, config):
    fitnesses = [get_fitness(chromosome, config) for chromosome in population]
    fitnesses = np.array(fitnesses)

    return population[np.argmax(fitnesses)], np.max(fitnesses)


def get_diversity_rate(population):
    return len(set(map(lambda x: tuple(x), population))) / len(population)


def sort_population_by_fitness_desc(population, config):
    fitnesses = [get_fitness(chromosome, config) for chromosome in population]
    fitnesses = np.array(fitnesses)

    return [population[i] for i in np.argsort(fitnesses)[::-1]]


def evolve(population, config):
    population = select(population, config)
    population = sort_population_by_fitness_desc(population, config)

    print_population(population, config)

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
    print('Population: (len: {})', len(population))
    for chromosome in population:
        fitness = get_fitness(chromosome, config)
        print('Chromosome: {} (fitness: {})'.format(chromosome, fitness))
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

