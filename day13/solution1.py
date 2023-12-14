#! /usr/bin/python3.10
import csv
import math
from typing import List


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def find_horiz_value(self, pattern: List[str]) -> int:
        """Finds the horizontal value of the given pattern or 0 if N/A."""

        def is_horiz_mirror(row: int, mirror_row: int) -> bool:
            if row < 0 or mirror_row >= len(pattern):
                return True

            for c in range(len(pattern[row])):
                if pattern[row][c] != pattern[mirror_row][c]:
                    return False

            if is_horiz_mirror(row - 1, mirror_row + 1):
                return True

            return False

        # Check each starting row for possible mirrored rows
        for r in range(len(pattern) - 1):
            if is_horiz_mirror(r, r + 1):
                return (r + 1) * 100

        return 0

    def find_vert_value(self, pattern: List[str]) -> int:
        """Finds the vertical value of the given pattern or 0 if N/A."""

        def is_vert_mirror(col: int, mirror_col: int) -> bool:
            if col < 0 or mirror_col >= len(pattern[0]):
                return True

            for r in range(len(pattern)):
                if pattern[r][col] != pattern[r][mirror_col]:
                    return False

            if is_vert_mirror(col - 1, mirror_col + 1):
                return True

            return False

        # Check each starting col for possible mirrored cols
        for c in range(len(pattern[0]) - 1):
            if is_vert_mirror(c, c + 1):
                return c + 1

        return 0

    def get_pattern_value(self, pattern: List[str]) -> int:
        """Finds the value of the given pattern.

        Value can be found by multiplying the number of rows above a horizontal
        line of reflection by 100, or multiplying the number of columns to the
        left of a vertical line of reflection by 1.
        """
        return self.find_horiz_value(pattern) + self.find_vert_value(pattern)

    def solve(self):
        total = 0
        patterns = []

        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            curr_pattern = []

            for row in csv_reader:
                if not row:
                    patterns.append(curr_pattern)
                    curr_pattern = []
                else:
                    curr_pattern.append(row[0])

            patterns.append(curr_pattern)

        for p in patterns:
            total += self.get_pattern_value(p)

        print(total)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
