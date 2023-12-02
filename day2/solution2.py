#! /usr/bin/python3.10
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def find_power(self, s: str) -> int:
        """Calculates the power of the given game str."""
        max_cubes = {
            "red": 0,
            "green": 0,
            "blue": 0
        }
        
        # Format: " # <color>, # <color>, ..."
        games = s.split(":")[1].split(";")
        for game in games:
            curr_count = -1

            for tok in game.split(" "):
                if not tok:
                    continue
                elif tok.isnumeric():
                    curr_count = int(tok)
                else:
                    color = tok[:-1] if tok[-1] == "," else tok
                    max_cubes[color] = max(max_cubes[color], curr_count)
        
        return max_cubes["red"] * max_cubes["green"] * max_cubes["blue"]


    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            power_sum = 0

            for row in csv_reader:
                joined_str = "".join(row)

                power_sum += self.find_power(joined_str)

        print(power_sum)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
