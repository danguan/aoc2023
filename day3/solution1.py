#! /usr/bin/python3.10
from typing import List
from queue import deque
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def get_adj_nums(self, grid: List[List[str]], row: int, col: int) -> int:
        """Gets the sum of all part numbers adjacent to given row/col coord."""
        ADJ = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
        ]
        part_number_sum = 0

        def parse_and_clear_num(num_row: int, num_col: int) -> int:
            """Parses a num from the given row/col and replaces it with "."s.

            Will traverse left and right of the starting `num_row`/`num_col` to
            identify a full integer.
            """
            left_col = num_col
            right_col = num_col + 1
            num_deque = deque()

            while left_col >= 0 and grid[num_row][left_col].isnumeric():
                num_deque.appendleft(grid[num_row][left_col])
                grid[num_row][left_col] = "."
                left_col -= 1

            while (
                right_col < len(grid[0])
                and grid[num_row][right_col].isnumeric()
            ):
                num_deque.append(grid[num_row][right_col])
                grid[num_row][right_col] = "."
                right_col += 1
            return int("".join(num_deque))

        for adj_r, adj_c in ADJ:
            new_r = row + adj_r
            new_c = col + adj_c

            if 0 <= new_r < len(grid) and 0 <= new_c < len(grid[0]) and grid[new_r][new_c].isnumeric():
                part_number_sum += parse_and_clear_num(new_r, new_c)
        return part_number_sum

    def sum_part_numbers(self, grid: List[List[str]]) -> int:
        """Sums part numbers adjacent to symbols in the given grid."""
        part_number_sum = 0

        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if not (grid[row][col].isnumeric() or grid[row][col] == "."):
                    part_number_sum += self.get_adj_nums(grid, row, col)
        return part_number_sum

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            part_number_sum = 0
            grid = []

            for row in csv_reader:
                grid.append([c for c in row[0]])

        part_number_sum = self.sum_part_numbers(grid)
        print(part_number_sum)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
