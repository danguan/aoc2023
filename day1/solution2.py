#! /usr/bin/python3.10
import csv


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def num_str_to_calibration(self, s: str) -> int:
        """Converts a calibration document string into a calibration value.

        Interprets ints as ints, and converts string representation of ints to
        int values, in order to determine the final calibration value.
        """
        int_strings_by_len = {
            3: {"one": 1, "two": 2, "six": 6},
            4: {"four": 4, "five": 5, "nine": 9},
            5: {"three": 3, "seven": 7, "eight": 8},
        }

        first_digit = -1
        last_digit = -1
        s_idx = 0

        while s_idx < len(s):
            curr_digit = -1
            if s[s_idx].isnumeric():
                curr_digit = int(s[s_idx])
            else:
                for s_length in int_strings_by_len:
                    if s_idx + s_length > len(s):
                        break

                    curr_num_str = s[s_idx : s_idx + s_length]
                    if curr_num_str in int_strings_by_len[s_length]:
                        curr_digit = int_strings_by_len[s_length][curr_num_str]
                        break

            if curr_digit != -1:
                if first_digit == -1:
                    first_digit = curr_digit
                last_digit = curr_digit
            
            s_idx += 1

        return first_digit * 10 + last_digit

    def solve(self):
        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            total_calibration_value = 0

            for row in csv_reader:
                total_calibration_value += self.num_str_to_calibration(row[0])

        print(total_calibration_value)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
