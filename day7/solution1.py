#! /usr/bin/python3.10
import csv
from typing import List, Tuple
from collections import defaultdict
from enum import Enum

card_values = ["T", "J", "Q", "K", "A"]


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

        for c in sorted_hand:
            freq[c] += 1

        if len(freq.keys()) == 1:
            return HandType.FIVE_OF_A_KIND
        elif len(freq.keys()) == 2:
            if freq[sorted_hand[0]] == 4 or freq[sorted_hand[0]] == 1:
                return HandType.FOUR_OF_A_KIND
            else:
                return HandType.FULL_HOUSE
        elif len(freq.keys()) == 3:
            # Middle card must be included if there is a 3 of a kind
            if freq[sorted_hand[2]] == 3:
                return HandType.THREE_OF_A_KIND
            elif freq[sorted_hand[0]] == 2 or freq[sorted_hand[2]] == 2:
                return HandType.TWO_PAIR
        elif len(freq.keys()) == 4:
            return HandType.ONE_PAIR
        else:
            return HandType.HIGH

    def get_hand_strength(self) -> Tuple[HandType, List[int]]:
        """Returns hand type and relative hand strength."""
        value = []

        for c in self.hand:
            if c.isnumeric():
                value.append(int(c))
            else:
                value.append(10 + card_values.index(c))
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
