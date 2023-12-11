#! /usr/bin/python3.10
import csv
from typing import List, Tuple
from queue import deque

PIPES = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(0, -1), (1, 0)],
    "F": [(0, 1), (1, 0)],
}


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def get_connected_tiles(
        self, grid: List[List[str]], r: int, c: int
    ) -> List[Tuple[int, int]]:
        """Finds all valid adjacent tiles to r, c as coord tuples."""
        DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        adj = []

        def is_pipe_adj(start_r: int, start_c: int, r_delta: int, c_delta: int) -> bool:
            """Checks whether adj pipe leads into tile at start_r, start_c."""
            adj_pipe = grid[start_r + r_delta][start_c + c_delta]

            if (-1 * r_delta, -1 * c_delta) in PIPES[adj_pipe]:
                return True

            return False

        for r_d, c_d in DIRS:
            new_r = r + r_d
            new_c = c + c_d

            if 0 <= new_r < len(grid) and 0 <= new_c < len(grid[r]):
                if grid[new_r][new_c] not in PIPES:
                    continue

                # Check if current pipe and adjacent pipes are connected
                if is_pipe_adj(r, c, r_d, c_d) and (
                    grid[r][c] == "S" or is_pipe_adj(new_r, new_c, -r_d, -c_d)
                ):
                    adj.append((new_r, new_c))

                # Each pipe is only connected to 2 tiles
                if len(adj) == 2:
                    break

        return adj

    def solve(self):
        grid = []
        queue = deque()
        seen = set()
        max_dist = 0

        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            for row in csv_reader:
                grid.append([*row[0]])

        for r, _ in enumerate(grid):
            for c, _ in enumerate(grid[r]):
                if grid[r][c] == "S":
                    queue.append((r, c, 0))
                    seen.add((r, c))

        while queue:
            curr_r, curr_c, dist = queue.popleft()

            for adj_r, adj_c in self.get_connected_tiles(grid, curr_r, curr_c):
                if (adj_r, adj_c) not in seen:
                    seen.add((adj_r, adj_c))
                    queue.append((adj_r, adj_c, dist + 1))
                    max_dist = max(max_dist, dist + 1)

        print(max_dist)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
