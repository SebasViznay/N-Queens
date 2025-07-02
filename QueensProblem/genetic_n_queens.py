import random
import time
import tracemalloc


def generate_individual(n):
    return random.sample(range(n), n)


def fast_conflicts(board):
    n = len(board)
    col_counts = {}
    diag1_counts = {}
    diag2_counts = {}
    for row in range(n):
        col = board[row]
        diag1 = row - col
        diag2 = row + col
        col_counts[col] = col_counts.get(col, 0) + 1
        diag1_counts[diag1] = diag1_counts.get(diag1, 0) + 1
        diag2_counts[diag2] = diag2_counts.get(diag2, 0) + 1

    conflicts = 0
    for counts in (col_counts, diag1_counts, diag2_counts):
        for count in counts.values():
            if count > 1:
                conflicts += count * (count - 1) // 2
    return conflicts


def crossover(parent1, parent2):
    n = len(parent1)
    point = random.randint(1, n - 2)
    child = parent1[:point] + [x for x in parent2 if x not in parent1[:point]]
    return child


def mutate(individual, mutation_rate):
    n = len(individual)
    for _ in range(n):
        if random.random() < mutation_rate:
            i, j = random.sample(range(n), 2)
            individual[i], individual[j] = individual[j], individual[i]
    return individual


def roulette_selection(population, fitnesses):
    max_fit = max(fitnesses)
    adjusted = [max_fit - f + 1 for f in fitnesses]
    total = sum(adjusted)
    probs = [f / total for f in adjusted]
    return population[random.choices(range(len(population)), weights=probs, k=1)[0]]


def solve(n, population_size=200, generations=1000):
    population = [generate_individual(n) for _ in range(population_size)]

    for generation in range(generations):
        fitnesses = [fast_conflicts(ind) for ind in population]
        best_fitness = min(fitnesses)
        if best_fitness == 0:
            best_index = fitnesses.index(0)
            print(f"Solution found at generation {generation}")
            return population[best_index]

        sorted_population = [ind for _, ind in sorted(zip(fitnesses, population))]
        next_generation = sorted_population[:population_size // 5]  # top 20%

        mutation_rate = max(0.05, 0.2 * (1 - generation / generations))

        while len(next_generation) < population_size - 5:
            parent1 = roulette_selection(sorted_population, fitnesses)
            parent2 = roulette_selection(sorted_population, fitnesses)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            next_generation.append(child)

        for _ in range(5):
            next_generation.append(generate_individual(n))

        population = next_generation

    return None


if __name__ == "__main__":
    N = 50
    print(f"Running Optimized Genetic Algorithm for N = {N}")
    tracemalloc.start()
    start = time.perf_counter()
    solution = solve(N)
    elapsed = time.perf_counter() - start
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if solution:
        print("Solution found:", solution)
    else:
        print("Failed to find a solution")
    print(f"Execution time: {elapsed:.6f} seconds")
    print(f"Peak memory usage: {peak / 1024:.2f} KiB")