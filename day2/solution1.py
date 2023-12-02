#! /usr/bin/python3.10
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def parse_game(self, s: str) -> int:
        """Reads the ID of a game from the given str."""
        game_str = s.split(":")[0]
        return int(game_str.split(" ")[1])

    def is_valid_game(self, s: str) -> bool:
        """Checks whether the input game str is valid.
        
        Valid is defined as being playable with:
            - 12 red cubes
            - 13 green cubes
            - 14 blue cubes
        """
        GAME_LIMITS = {
            "red": 12,
            "green": 13,
            "blue": 14
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

                    if curr_count > GAME_LIMITS[color]:
                        return False
        
        return True


    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)
            id_sum = 0

            for row in csv_reader:
                joined_str = "".join(row)
                game_id = self.parse_game(joined_str)

                if self.is_valid_game(joined_str):
                    id_sum += game_id

        print(id_sum)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
