#! /usr/bin/python3.10
from typing import List, Set, Tuple
from queue import deque
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def get_gear_ratio(self, grid: List[List[str]], row: int, col: int) -> int:
        """Gets the gear ratio for the given row/col coord.

        Returns 0 if the given rol/col starting point is not a valid gear."""
        adj = [
            (row - 1, col - 1),
            (row - 1, col),
            (row - 1, col + 1),
            (row, col + 1),
            (row + 1, col + 1),
            (row + 1, col),
            (row + 1, col - 1),
            (row, col - 1),
        ]

        def parse_num_and_mark_seen(
            num_row: int, num_col: int, seen_adj: Set[Tuple[int, int]]
        ) -> int:
            """Parses a num from the given row/col and mark any seen row/cols.

            Will traverse left and right of the starting `num_row`/`num_col` to
            identify a full integer.
            """
            left_col = num_col
            right_col = num_col + 1
            num_deque = deque()

            while left_col >= 0 and grid[num_row][left_col].isnumeric():
                num_deque.appendleft(grid[num_row][left_col])
                if (num_row, left_col) in seen_adj:
                    seen_adj.remove((num_row, left_col))
                left_col -= 1

            while (
                right_col < len(grid[0])
                and grid[num_row][right_col].isnumeric()
            ):
                num_deque.append(grid[num_row][right_col])
                if (num_row, right_col) in seen_adj:
                    seen_adj.remove((num_row, right_col))
                right_col += 1
            return int("".join(num_deque))

        adj_part_nums = []
        # Maintain a set of adjacent part numbers that have already been seen
        seen_adj = set(adj)

        for new_r, new_c in adj:
            if (
                0 <= new_r < len(grid)
                and 0 <= new_c < len(grid[0])
                and grid[new_r][new_c].isnumeric()
            ):
                if (new_r, new_c) not in seen_adj:
                    continue

                adj_part_nums.append(
                    parse_num_and_mark_seen(new_r, new_c, seen_adj)
                )
                if len(adj_part_nums) > 2:
                    break
        return (
            adj_part_nums[0] * adj_part_nums[1]
            if len(adj_part_nums) == 2
            else 0
        )

    def sum_gear_ratios(self, grid: List[List[str]]) -> int:
        """Sums gear ratios adjacent to symbols in the given grid."""
        gear_ratio_sum = 0

        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == "*":
                    gear_ratio_sum += self.get_gear_ratio(grid, row, col)
        return gear_ratio_sum

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            gear_ratio_sum = 0
            grid = []

            for row in csv_reader:
                grid.append([c for c in row[0]])

        gear_ratio_sum = self.sum_gear_ratios(grid)
        print(gear_ratio_sum)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
