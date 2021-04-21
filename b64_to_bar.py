#!/usr/bin/env python3
from typing import List
from string import ascii_lowercase, ascii_uppercase

import cv2
import numpy as np

lookup_table = {}
for index, letter in enumerate(ascii_uppercase):
    lookup_table[letter] = index

for index, letter in enumerate(ascii_lowercase):
    lookup_table[letter] = index + 26

for i in range(1, 10):
    lookup_table[str(i)] = i + 52

lookup_table["+"] = 62
lookup_table["/"] = 63

inv_lookup = {v: k for k, v in lookup_table.items()}


def b64_to_int(code: str) -> List[int]:
    int_conversion = []
    for letter in code:
        int_conversion.append(lookup_table[letter])
    return int_conversion


def b10_to_bar(code: List[int]) -> List[int]:
    bars = []
    for number in code:
        int_val = str(oct(number))[2:]
        if len(int_val) == 2:
            bars.append(int(int_val[0]))
            bars.append(int(int_val[1]))
        else:
            bars.append(0)
            bars.append(int(int_val[0]))
    return bars


def bar_to_b10(code: List[int]) -> List[int]:
    b10_list = []
    print(code)
    for i in range(0, len(code), 2):
        b10 = int(str(code[i])+str(code[i+1]), 8)
        b10_list.append(inv_lookup[b10])
    print(b10_list)



def main():
    code = b64_to_int("LC254Hk")
    bars = b10_to_bar(code)
    bar_to_b10(bars)


if __name__ == "__main__":
    main()
