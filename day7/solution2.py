#! /usr/bin/python3.10
import csv
from typing import List, Tuple
from collections import defaultdict
from enum import Enum

card_values = ["T", "Q", "K", "A"]


class HandType(Enum):
    HIGH = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7


class Hand:
    def __init__(self, hand: str):
        self.hand = hand

    def get_hand_type(self) -> HandType:
        """Identifies the poker hand type of the current hand."""
        freq = defaultdict(int)
        sorted_hand = [c for c in self.hand]
        sorted_hand.sort(key=ord)
        max_freq = 0
        jokers = 0

        for c in sorted_hand:
            if c == "J":
                jokers += 1
            else:
                freq[c] += 1
                max_freq = max(max_freq, freq[c])

        if max_freq + jokers == 5:
            return HandType.FIVE_OF_A_KIND
        elif max_freq + jokers == 4:
            return HandType.FOUR_OF_A_KIND
        elif max_freq + jokers == 3:
            if len(freq.keys()) == 2:
                return HandType.FULL_HOUSE
            else:
                return HandType.THREE_OF_A_KIND
        elif max_freq + jokers == 2:
            if len(freq.keys()) == 3:
                return HandType.TWO_PAIR
            else:
                return HandType.ONE_PAIR
        else:
            return HandType.HIGH

    def get_hand_strength(self) -> Tuple[HandType, List[int]]:
        """Returns hand type and relative hand strength."""
        value = []

        for c in self.hand:
            if c == "J":
                value.append(1)
            elif c.isnumeric():
                value.append(int(c))
            else:
                value.append(10 + card_values.index(c))
        if self.get_hand_type() == None:
            print(self.hand)
        return (self.get_hand_type().value, value)


class Solution(object):
    def __init__(self, filename):
        self.filename = filename

    def solve(self):
        hand_bids = []

        with open(self.filename) as f:
            csv_reader = csv.reader(f)

            for row in csv_reader:
                hand, bid = row[0].split(" ")
                hand_bids.append((Hand(hand), int(bid)))

        hand_bids.sort(key=lambda hand_bid: hand_bid[0].get_hand_strength())

        total_winnings = 0

        for idx in range(len(hand_bids)):
            _, bid = hand_bids[idx]
            total_winnings += bid * (idx + 1)

        print(total_winnings)


if __name__ == "__main__":
    sol = Solution("input.csv")
    sol.solve()
