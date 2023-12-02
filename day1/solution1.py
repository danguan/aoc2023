#! /usr/bin/python3.10
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            total_calibration_value = 0

            for row in csv_reader:
                first_number = -1
                last_number = -1

                for ch in row[0]:
                    if ch.isnumeric():
                        if first_number == -1:
                            first_number = int(ch)
                        last_number = int(ch)
                
                total_calibration_value += first_number * 10 + last_number

        print(total_calibration_value)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
