#! /usr/bin/python3.10
import csv
import re
import sys


class Mapper:
    """A generic mapper class from one component type to another."""

    def __init__(self):
        self.ranges = []

    def add_range(self, dst_start: int, src_start: int, range_len: int):
        """Add a new range to this Mapper's ranges."""
        self.ranges.append((dst_start, src_start, range_len))

    def get_mapped_dst_val(self, src_val: int) -> int:
        """Identifies the mapped value of src_val to the dst component.

        Checks all of this Mapper's ranges for a fitting source range to map
        to the appropriate destination value, and if not found, returns the
        input `src_val`.
        """
        for dst_start, src_start, range_len in self.ranges:
            if src_start + range_len > src_val >= src_start:
                diff = src_start - dst_start
                return src_val - diff

        return src_val


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        seeds = []
        mappers = []

        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            for row in csv_reader:
                if not row:
                    continue
                # First row
                elif re.search("seeds.*", row[0]):
                    seeds.extend(
                        int(num) for num in row[0].split(": ")[1].split(" ")
                    )
                elif re.search(".*map", row[0]):
                    mappers.append(Mapper())
                else:
                    mappers[-1].add_range(
                        *(int(num) for num in row[0].split(" "))
                    )

        smallest_location = sys.maxsize

        for seed in seeds:
            curr_val = seed

            for mapper in mappers:
                curr_val = mapper.get_mapped_dst_val(curr_val)

            smallest_location = min(smallest_location, curr_val)

        print(smallest_location)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
