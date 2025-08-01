import random
import math
import time
import tracemalloc


def random_board(n):
    return [random.randint(0, n - 1) for _ in range(n)]


def compute_conflicts(board):
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                conflicts += 1
    return conflicts


def get_smart_neighbor(board):
    n = len(board)
    neighbor = board[:]
    row = random.randint(0, n - 1)
    min_conflicts = None
    best_cols = []
    for col in range(n):
        neighbor[row] = col
        conflicts = compute_conflicts(neighbor)
        if min_conflicts is None or conflicts < min_conflicts:
            min_conflicts = conflicts
            best_cols = [col]
        elif conflicts == min_conflicts:
            best_cols.append(col)

    if not best_cols:
        best_cols = list(range(n))  # fallback to any column

    neighbor[row] = random.choice(best_cols)
    return neighbor


def solve(n, max_iterations=1000000, initial_temp=1000, cooling_rate=0.999):
    current = random_board(n)
    current_conflicts = compute_conflicts(current)
    temperature = initial_temp

    for iteration in range(max_iterations):
        if current_conflicts == 0:
            print(f"Solution found at iteration {iteration}")
            return current

        neighbor = get_smart_neighbor(current)
        neighbor_conflicts = compute_conflicts(neighbor)
        delta = neighbor_conflicts - current_conflicts

        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current = neighbor
            current_conflicts = neighbor_conflicts

        temperature *= cooling_rate
        if temperature < 1e-10:
            break

    return None 


if __name__ == "__main__":
    N = 100 #  Change value of N for board size

    print(f"Running Simulated Annealing for N = {N}")
    tracemalloc.start()
    start_time = time.perf_counter()
    solution = solve(N)
    elapsed = time.perf_counter() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if solution:
        print("Solution found:", solution)
    else:
        print("Failed to find a solution")

    print(f"Execution time: {elapsed:.6f} seconds")
    print(f"Peak memory usage: {peak / 1024:.2f} KiB")
