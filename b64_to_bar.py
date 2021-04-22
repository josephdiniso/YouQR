#!/usr/bin/env python3
from typing import List
from string import ascii_lowercase, ascii_uppercase

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


def b64_to_bar(text: str) -> List[int]:
    """
    Takes in a string of b64 values and converts it to a list of octal integers
    with a zero padded length of 2
    Args:
        text (str): b64 text

    Returns:
        (List[int]) List of zero padded to length to octal integers
    """
    code = []
    for letter in text:
        code.append(lookup_table[letter])
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


def bar_to_b64(code: List[int]) -> List[int]:
    """
    Takes in a list of octal integers and converts them in pairs of two to b64
    values
    Args:
        code (List[int]): List of octal integers, each pair of two being a single
        number

    Returns:
        (List[int]) List of b64 converted values
    """
    b10_list = []
    print(code)
    for i in range(0, len(code), 2):
        b10 = int(str(code[i]) + str(code[i + 1]), 8)
        b10_list.append(inv_lookup[b10])
    print(b10_list)


def main():
    bar_rev = b64_to_bar("LC254Hk")
    bar_to_b64(bar_rev)


if __name__ == "__main__":
    main()
