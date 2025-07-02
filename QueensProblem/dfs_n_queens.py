import sys
import time
import tracemalloc


def is_safe(board, row, col):
    # Check column
    for i in range(row):
        if board[i] == col:
            return False
    # Check diagonals
    for i in range(row):
        if abs(board[i] - col) == row - i:
            return False
    return True


def dfs_backtrack(n, row, board, solutions):
    if row == n:
        solutions.append(board.copy())
        return True
    found = False
    for col in range(n):
        if is_safe(board, row, col):
            board[row] = col
            if dfs_backtrack(n, row + 1, board, solutions):
                found = True
    return found


def solve(n):
    board = [-1] * n
    solutions = []
    dfs_backtrack(n, 0, board, solutions)
    return solutions


if __name__ == "__main__":
    N = 15  #Change value of N for board size.

    print(f"Running DFS for N = {N}")
    tracemalloc.start()
    start_time = time.perf_counter()
    solutions = solve(N)
    elapsed = time.perf_counter() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"{len(solutions)} solutions were found")
    print(f"Execution time: {elapsed:.6f} seconds")
    print(f"Max. memory usage: {peak / 1024:.2f} KiB")
