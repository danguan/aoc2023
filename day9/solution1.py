#! /usr/bin/python3.10
import csv
from typing import List


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def extrapolate_value(self, seq: List[int]) -> int:
        """Extrapolates the next value in seq based on the sequence diffs."""
        diffs = [seq]

        while not (diffs[-1][0] == 0 and diffs[-1][-1] == 0):
            curr_diffs = []

            for idx in range(1, len(diffs[-1])):
                curr_diffs.append(diffs[-1][idx] - diffs[-1][idx - 1])

            diffs.append(curr_diffs)
        
        diffs[-1].append(0)
        
        for diff_idx in range(len(diffs) - 2, -1, -1):
            diffs[diff_idx].append(diffs[diff_idx][-1] + diffs[diff_idx + 1][-1])

        return diffs[0][-1]

    def solve(self):
        seqs = []
        extrapolated_value_sum = 0

        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            for row in csv_reader:
                seqs.append([int(num) for num in row[0].split(" ")])

        for seq in seqs:
            extrapolated_value_sum += self.extrapolate_value(seq)

        print(extrapolated_value_sum)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
