#! /usr/bin/python3.10
import csv
import math
import re


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def find_ways(self, time: int, dist: int) -> int:
        """Finds the number of ways to beat the record `dist` in `time`.
        
        Original formula:
            dist = (time - idx) * idx
            dist = time * idx - idx ^ 2
            idx ^ 2 - time * idx + dist = 0

        Methodology uses quadratic equation:
            Find roots where 0 = (idx ^ 2) - (time * idx) + dist

            idx = time +- sqrt(time ^ 2 - 4(1 * dist)) / 2
        
        where idx is the lower and upper roots.
        """
        radical = math.sqrt(time ** 2 - 4 * dist)

        roots = [(time + radical) / 2, (time - radical) / 2]
        roots.sort()
        
        # Exclude exact roots, as these do not "beat the record"
        return (math.ceil(roots[1]) - 1) - (math.floor(roots[0]) + 1) + 1
        

    def solve(self):
        times = []
        dists = []
        ways = 1

        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            for row in csv_reader:
                if re.match("Time.*", row[0]):
                    times.extend([int(s) for s in row[0].split(" ") if s.isnumeric()])
                else:
                    dists.extend([int(s) for s in row[0].split(" ") if s.isnumeric()])
        
        for idx in range(len(times)):
            ways *= self.find_ways(times[idx], dists[idx])
        
        print(ways)
        

if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
