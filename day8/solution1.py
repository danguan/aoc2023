#! /usr/bin/python3.10
import csv
from collections import defaultdict

class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        dirs = None
        adj = defaultdict(list)

        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            for row in csv_reader:
                if dirs is None:
                    dirs = row[0]
                elif not row:
                    continue
                else:
                    src_node = row[0].split(" = ")[0]

                    l_adj = row[0].split("(")[1]
                    r_adj = row[1][1:-1]
                    adj[src_node] = [l_adj, r_adj]
        steps = 0
        curr_idx = 0
        curr = "AAA"

        while curr != "ZZZ":
            if dirs[curr_idx] == "L":
                curr = adj[curr][0]
            else:
                curr = adj[curr][1]

            steps += 1
            curr_idx = (curr_idx + 1) % len(dirs)

        print(steps)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
