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


def b64_to_int(code: str) -> List[int]:
    """
    Takes in a b64 string and converts it to a list of integers
    Args:
        code (str): B64 string

    Returns:
        (List[int]) List of integers converted from b64 to b10
    """
    int_conversion = []
    for letter in code:
        int_conversion.append(lookup_table[letter])
    return int_conversion


def b10_to_bar(code: List[int]) -> List[int]:
    """
    Takes in a list of b10 integers and converts it to a list of octal integers
    with a zero padded length of 2
    Args:
        code (List[int]): List of b10 integers

    Returns:
        (List[int]) List of zero padded to length to octal integers
    """
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
    code = b64_to_int("LC254Hk")
    bars = b10_to_bar(code)
    bar_to_b64(bars)


if __name__ == "__main__":
    main()
