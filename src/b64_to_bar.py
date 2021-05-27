#!/usr/bin/env python3
from typing import List, Optional
from string import ascii_lowercase, ascii_uppercase


def make_lookup():
    """
    Called always, generates global lookup and inverse to convert from base64 to int
    Returns:
        None
    """
    global lookup_table
    global inv_lookup
    if "lookup_table" not in globals():
        lookup_table = {}
    if "inv_lookup" not in globals():
        inv_lookup = {}
    for index, letter in enumerate(ascii_uppercase):
        lookup_table[letter] = index

    for index, letter in enumerate(ascii_lowercase):
        lookup_table[letter] = index + 26

    for i in range(1, 10):
        lookup_table[str(i)] = i + 52
    lookup_table["-"] = 62
    lookup_table["/"] = 63
    # Generates inverse lookup
    inv_lookup = {v: k for k, v in lookup_table.items()}
    inv_lookup[52] = "0"


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


def bar_to_b64(code: List[int]) -> Optional[List[str]]:
    """
    Takes in a list of octal integers and converts them in pairs of two to b64
    values
    Args:
        code (List[int]): List of octal integers, each pair of two being a single
        number

    Returns:
        (List[str]) List of b64 converted values or None if the list of integers is invalid
    """
    b64_list = []
    if len(code) % 2 != 0:
        return None
    for i in range(0, len(code), 2):
        if code[i] < 0 or code[i] > 7 or code[i + 1] < 0 or code[i + 1] > 7:
            return None
        try:
            b10 = int((str(code[i]) + str(code[i + 1])), 8)
            b64_list.append(inv_lookup[b10])
        except ValueError:
            pass
    return b64_list


def main():
    bar_rev = b64_to_bar("LC254Hk")
    bar_to_b64(bar_rev)


if __name__ == "__main__":
    make_lookup()
    main()
else:
    make_lookup()
