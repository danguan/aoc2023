#! /usr/bin/python3.10
import csv
from typing import List
from queue import deque

PIPES = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(0, -1), (1, 0)],
    "F": [(0, 1), (1, 0)],
}

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def is_pipe_adj(
        self,
        grid: List[List[str]],
        start_r: int,
        start_c: int,
        r_delta: int,
        c_delta: int,
        magnitude: int = 1,
    ) -> bool:
        """Checks whether adj pipe leads into tile at start_r, start_c.

        Magnitude is used to scale down delta values into directional values
        for PIPES lookup only.
        """
        adj_pipe = grid[start_r + r_delta][start_c + c_delta]
        if adj_pipe == "S":
            print(start_r, start_c, r_delta, c_delta)

        if (-1 * r_delta // magnitude, -1 * c_delta // magnitude) in PIPES[adj_pipe]:
            return True

        return False

    def are_pipes_connected(
        self,
        grid: List[List[str]],
        start_r: int,
        start_c: int,
        r_delta: int,
        c_delta: int,
        magnitude: int = 1,
    ) -> bool:
        """Checks whether the current pipe is connected to its neighbor."""
        new_r = start_r + r_delta
        new_c = start_c + c_delta

        connected = False

        if grid[start_r][start_c] == "S":
            connected = self.is_pipe_adj(
                grid, start_r, start_c, r_delta, c_delta, magnitude
            )
        elif grid[new_r][new_c] == "S":
            connected = self.is_pipe_adj(
                grid, new_r, new_c, -r_delta, -c_delta, magnitude
            )
        else:
            connected = self.is_pipe_adj(
                grid, start_r, start_c, r_delta, c_delta, magnitude
            ) and self.is_pipe_adj(grid, new_r, new_c, -r_delta, -c_delta, magnitude)

        return connected

    def flood_island(self, grid: List[List[int]], r: int, c: int):
        """Traverses current island of "."s and mark if it touches the edge.

        If the island touches the edge, mark it with a " " character. If it
        does not, i.e. it is contained in the main loop, mark it with a "@"
        character.
        """
        queue = deque([(r, c)])
        seen = set([(r, c)])
        touches_edge = False

        while queue and not touches_edge:
            curr_r, curr_c = queue.popleft()

            for r_d, c_d in DIRS:
                new_r = curr_r + r_d
                new_c = curr_c + c_d

                if (
                    new_r < 0
                    or new_r >= len(grid)
                    or new_c < 0
                    or new_c >= len(grid[r])
                ):
                    touches_edge = True
                    break

                if grid[new_r][new_c] == "." and (new_r, new_c) not in seen:
                    seen.add((new_r, new_c))
                    queue.append((new_r, new_c))

        flood_char = " " if touches_edge else "@"
        queue = deque([(r, c)])
        seen = set([(r, c)])

        while queue:
            curr_r, curr_c = queue.popleft()
            grid[curr_r][curr_c] = flood_char

            for r_d, c_d in DIRS:
                new_r = curr_r + r_d
                new_c = curr_c + c_d

                if (
                    0 <= new_r < len(grid)
                    and 0 <= new_c < len(grid[r])
                    and grid[new_r][new_c] == "."
                    and (new_r, new_c) not in seen
                ):
                    seen.add((new_r, new_c))
                    queue.append((new_r, new_c))

    def solve(self):
        grid = []
        total_enclosed = 0

        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            for row in csv_reader:
                if grid:
                    grid.append(["." for _ in range(len(grid[-1]))])
                new_row = []
                for c in row[0]:
                    new_row.append(c)
                    new_row.append(".")
                grid.append(new_row[:-1])

        for r in range(0, len(grid), 2):
            for c in range(0, len(grid[r]), 2):
                if grid[r][c] != ".":
                    if (
                        0 <= c + 2 < len(grid[r])
                        and grid[r][c + 2] != "."
                        and self.are_pipes_connected(grid, r, c, 0, 2, 2)
                    ):
                        grid[r][c + 1] = "-"

                    if (
                        0 <= r + 2 < len(grid)
                        and grid[r + 2][c] != "."
                        and self.are_pipes_connected(grid, r, c, 2, 0, 2)
                    ):
                        grid[r + 1][c] = "|"

        for r, _ in enumerate(grid):
            for c, _ in enumerate(grid[r]):
                if grid[r][c] == ".":
                    self.flood_island(grid, r, c)

        found_enclosed = -1

        while found_enclosed != 0:
            found_enclosed = 0

            for r in range(0, len(grid), 2):
                for c in range(0, len(grid[r]), 2):
                    if grid[r][c] != " ":
                        invalid_neighbors = set(DIRS)

                        for r_d, c_d in DIRS:
                            new_r = r + r_d
                            new_c = c + c_d

                            if (
                                0 <= new_r < len(grid)
                                and 0 <= new_c < len(grid[r])
                                and grid[new_r][new_c] == "@"
                            ):
                                invalid_neighbors.remove((r_d, c_d))

                        if len(invalid_neighbors) <= 1:
                            found_enclosed += 1
                            grid[r][c] = " "

                            if len(invalid_neighbors) == 1:
                                inv_r_d, inv_c_d = list(invalid_neighbors)[0]
                                grid[r + inv_r_d][c + inv_c_d] = "@"

            total_enclosed += found_enclosed

        print(total_enclosed)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
