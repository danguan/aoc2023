#! /usr/bin/python3.10
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            point_sum = 0

            for row in csv_reader:
                all_nums = row[0].split(":")[1].split("|")
                winning_nums = [int(num) for num in all_nums[0].split(" ") if num != ""]
                card_nums = [int(num) for num in all_nums[1].split(" ") if num != ""]

                points = 0.5
                
                for num in card_nums:
                    if num in winning_nums:
                        points *= 2
                
                point_sum += points if points >= 1 else 0

        print(int(point_sum))


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
