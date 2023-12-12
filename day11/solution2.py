#! /usr/bin/python3.10
import csv
from typing import List, Tuple


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def get_empty_rows_cols(self, grid: List[List[str]]) -> Tuple[List[int], List[int]]:
        """Finds all empty row and col indexes."""
        empty_rows = []
        empty_cols = []
        for r_idx, r in enumerate(grid):
            is_empty = True
            for c_idx, rc in enumerate(r):
                if rc == "#":
                    is_empty = False

            if is_empty:
                empty_rows.append(r_idx)

        for c_idx, _ in enumerate(grid[0]):
            is_empty = True
            for r_idx, _ in enumerate(grid):
                if grid[r_idx][c_idx] == "#":
                    is_empty = False

            if is_empty:
                empty_cols.append(c_idx)

        return empty_rows, empty_cols

    def count_expanded_space(
        self,
        grid: List[List[str]],
        galaxies: List[Tuple[int, int]],
        expansion_mult: int,
    ) -> int:
        """Find extra amount of traversal space is needed per galaxy pair."""
        expanded_space = 0
        empty_rows, empty_cols = self.get_empty_rows_cols(grid)
        g_idx = 0

        for empty_row in empty_rows:
            if g_idx == len(galaxies):
                break

            while g_idx < len(galaxies) and galaxies[g_idx][0] < empty_row:
                g_idx += 1

            expanded_space += g_idx * (len(galaxies) - g_idx) * expansion_mult

        galaxies.sort(key=lambda rc: rc[1])
        g_idx = 0

        for empty_col in empty_cols:
            if g_idx == len(galaxies):
                break

            while g_idx < len(galaxies) and galaxies[g_idx][1] < empty_col:
                g_idx += 1

            expanded_space += g_idx * (len(galaxies) - g_idx) * expansion_mult

        return expanded_space

    def solve(self):
        grid = []
        galaxies = []
        distance_sum = 0

        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            for row in csv_reader:
                grid.append([c for c in row[0]])

        for r_idx, r in enumerate(grid):
            for c_idx, rc in enumerate(r):
                if rc == "#":
                    galaxies.append((r_idx, c_idx))

        EXPANSION_MULT = 1000000
        distance_sum += self.count_expanded_space(grid, galaxies, EXPANSION_MULT - 1)

        for g_idx in range(len(galaxies) - 1):
            g = galaxies[g_idx]

            for g_pair_idx in range(g_idx + 1, len(galaxies)):
                g_pair = galaxies[g_pair_idx]

                distance_sum += abs(g_pair[0] - g[0]) + abs(g_pair[1] - g[1])

        print(distance_sum)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
