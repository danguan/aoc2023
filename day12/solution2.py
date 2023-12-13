#! /usr/bin/python3.10
import csv
import functools
from typing import List


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def get_record_arrangements(self, record: str, criteria: List[int]) -> int:
        """Gets the total number of valid arrangements for the given record."""
        latest_broken = None
        for c_idx in range(len(record) - 1, -1, -1):
            if record[c_idx] == "#":
                latest_broken = c_idx
                break

        @functools.cache
        def recurse(start_idx: int, criteria_idx: int) -> int:
            # All springs in criteria have been placed
            if criteria_idx == len(criteria):
                # All guaranteed broken springs are accounted for
                if latest_broken is None or start_idx > latest_broken:
                    return 1
                # There is an unfulfilled broken spring
                else:
                    return 0
            # Some criteria have not been placed
            elif start_idx >= len(record):
                return 0

            valid_arrangements = 0
            crit_size = criteria[criteria_idx]

            for idx in range(start_idx, len(record) - crit_size + 1):
                # A broken spring was skipped
                if idx > 0 and record[idx - 1] == "#":
                    break

                is_valid = True
                for curr_crit_idx in range(idx, idx + crit_size):
                    # Attempting to place broken spring on unbroken space
                    if record[curr_crit_idx] == ".":
                        is_valid = False
                        break

                # Check if there is an appropriate gap between criteria
                if (
                    idx + crit_size == len(record) and criteria_idx < len(criteria) - 1
                ) or (idx + crit_size < len(record) and record[idx + crit_size] == "#"):
                    is_valid = False

                if is_valid:
                    valid_arrangements += recurse(idx + crit_size + 1, criteria_idx + 1)

            return valid_arrangements

        return recurse(0, 0)

    def solve(self):
        total_arrangements = 0

        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            for row in csv_reader:
                record, crit_0 = row[0].split(" ")
                criteria = [int(crit_0), *[int(num) for num in row[1:]]]

                FOLDS = 5
                unfolded_record = record

                for _ in range(FOLDS - 1):
                    unfolded_record += "?"
                    unfolded_record += record

                total_arrangements += self.get_record_arrangements(
                    unfolded_record, criteria * FOLDS
                )

        print(total_arrangements)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
