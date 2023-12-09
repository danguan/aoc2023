#! /usr/bin/python3.10
import csv
from collections import defaultdict
from math import lcm


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        dirs = None
        adj = defaultdict(list)
        nodes = []

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

                    if src_node[-1] == "A":
                        nodes.append(src_node)
        steps = []

        for node in nodes:
            curr = node
            idx = 0

            while curr[-1] != "Z":
                if dirs[idx % len(dirs)] == "L":
                    curr = adj[curr][0]
                else:
                    curr = adj[curr][1]
                idx += 1
            steps.append(idx)

        print(lcm(*steps))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
