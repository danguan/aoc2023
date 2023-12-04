#! /usr/bin/python3.10
from queue import deque
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            card_sum = 0
            extra_cards = deque()

            for row in csv_reader:
                all_nums = row[0].split(":")[1].split("|")
                winning_nums = [int(num) for num in all_nums[0].split(" ") if num != ""]
                card_nums = [int(num) for num in all_nums[1].split(" ") if num != ""]

                curr_cards = 1

                if extra_cards:
                    curr_cards += extra_cards.popleft()

                curr_winning_num = 0
                
                for num in card_nums:
                    if num in winning_nums:
                        if curr_winning_num >= len(extra_cards):
                            extra_cards.append(0)
                        extra_cards[curr_winning_num] += curr_cards
                        curr_winning_num += 1
                
                card_sum += curr_cards

        print(card_sum)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
