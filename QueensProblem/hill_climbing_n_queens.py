import random
import time
import tracemalloc


def random_permutation(n):
    return random.sample(range(n), n)


def count_conflicts(board, row, col):
    conflicts = 0
    for r in range(len(board)):
        if r == row:
            continue
        c = board[r]
        if c == col or abs(r - row) == abs(c - col):
            conflicts += 1
    return conflicts


def get_conflicted_rows(board):
    return [row for row in range(len(board)) if count_conflicts(board, row, board[row]) > 0]


def solve(n, max_steps=100000):
    board = random_permutation(n)

    for step in range(max_steps):
        conflicted = get_conflicted_rows(board)
        if not conflicted:
            print(f"Solution found at step {step}")
            return board

        row = random.choice(conflicted)
        min_conflicts = n
        best_cols = []
        for col in range(n):
            conflicts = count_conflicts(board, row, col)
            if conflicts < min_conflicts:
                min_conflicts = conflicts
                best_cols = [col]
            elif conflicts == min_conflicts:
                best_cols.append(col)

        board[row] = random.choice(best_cols)

    return None  # Failed to find a solution


if __name__ == "__main__":
    N = 50  # Change this to 30, 50, 100, or 200 as needed

    print(f"Running Min-Conflicts Hill Climbing for N = {N}")
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
