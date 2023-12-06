#! /usr/bin/python3.10
from typing import List, Tuple
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

    def process_seeds(
        self, seeds: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """Outputs all discrete ranges of seeds that have a mapping."""
        next_seeds = []

        while len(seeds) > 0:
            start, end = seeds.pop()

            for dst, src, range_len in self.ranges:
                overlap_start = max(start, src)
                overlap_end = min(end, src + range_len)

                if overlap_start < overlap_end:
                    next_seeds.append(
                        (overlap_start - src + dst, overlap_end - src + dst)
                    )
                    if overlap_start > start:
                        seeds.append((start, overlap_start))
                    if overlap_end < end:
                        seeds.append((overlap_end, end))
                    break
            else:
                next_seeds.append((start, end))

        return next_seeds


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        seed_ranges = []
        mappers = []

        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            for row in csv_reader:
                if not row:
                    continue
                # First row
                elif re.search("seeds.*", row[0]):
                    parsed_seed_ranges = [
                        int(num) for num in row[0].split(": ")[1].split(" ")
                    ]

                    for idx in range(len(parsed_seed_ranges) // 2):
                        seed_ranges.append(
                            (
                                parsed_seed_ranges[idx * 2],
                                parsed_seed_ranges[idx * 2]
                                + parsed_seed_ranges[idx * 2 + 1],
                            )
                        )
                elif re.search(".*map", row[0]):
                    mappers.append(Mapper())
                else:
                    mappers[-1].add_range(
                        *(int(num) for num in row[0].split(" "))
                    )

        for mapper in mappers:
            seed_ranges = mapper.process_seeds(seed_ranges)

        print(min(seed_ranges)[0])


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
