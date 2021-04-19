#!/usr/bin/env/ python3

import argparse

import numpy as np
import cv2


class CodeMaker:
    def __init__(self, code: str):
        window = np.zeros((150, 400))
        cv2.imshow("window", window)
        cv2.waitKey(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate code given character set")
    parser.add_argument("--code", type=str,
                        help="String to convert to code")
    args = parser.parse_args()
    CodeMaker(args.code)
