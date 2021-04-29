#!/usr/bin/env python3
from math import ceil
from typing import List
import argparse

import numpy as np
import cv2

from b64_to_bar import b64_to_bar, bar_to_b64


class BarGenerator:
    # Configuration
    height = 300
    bar_width = 15
    space_between_bars = 10

    def __init__(self, nums):
        self.img = np.full((self.height, self.bar_width * (len(nums) + 3) +
                            self.space_between_bars * (len(nums) + 3) + 45), 255,
                           dtype=np.uint8)
        self.draw_bar(1, 0.9)
        self.draw_bar(len(nums) + 2, 0.9)
        self.draw_bar(len(nums) + 3, 0.9)
        for index, x in enumerate(nums):
            self.draw_bar(index + 2, 0.05 * (x + 1))

    def draw_bar(self, bar_index, bar_height):
        # Bar height is a percentage of the total height
        bar_height = int(bar_height * self.height)
        start_point = (bar_index * (self.space_between_bars + self.bar_width),
                       self.height // 2 - bar_height // 2)
        end_point = (start_point[0] + self.bar_width, self.height // 2 + bar_height // 2)
        cv2.rectangle(self.img, start_point, end_point, 0, -1)


def calculate_ratios(heights: List[float]):
    """
    Given a list of floats representing the height of the bars, these values are converted to their
    original base-64 encoding.
    Args:
        scale (float): Maximum height of a data bar
        heights (List[float]): List of heights of bars

    Returns:
        List[str]: List of b64 encoded characters
    """
    ratios = []
    for height in heights:
        ratio = height / max(heights)
        ratios.append(round(ratio * 8) - 1)
    return bar_to_b64(ratios)


def analyze_bar(src: np.array) -> List[str]:
    """
    Receives an image of a embedded QR-code. Analyzes the bars in the image to retrieve the b64 data
    encoded in it
    Args:
        src (np.array): Input image

    Returns:
        List[int] List of b64 characters converted from the image
    """
    # Detecting Bar's height

    src = cv2.resize(src, (300, 150))
    src = src[10:-10, 10:-10]
    cv2.imshow("src", src)
    img = src
    thresh = cv2.adaptiveThreshold(src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 5)
    contours, h = cv2.findContours(thresh, 1, 2)
    bar_heights = []
    img_height, img_width = src.shape
    x_vals = []
    count = 0
    for cnt in contours:
        top = (cnt[cnt[:, :, 1].argmin()])[0][1]
        bottom = (cnt[cnt[:, :, 1].argmax()])[0][1]
        x = (cnt[cnt[:, :, 0].argmax()][0])[0]
        height = round((bottom - top) / img_height, 5)
        count += 1
        org = (x, img_height - 40)
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = cv2.putText(img, str(height), org, font, 0.30, 0)
        bar_heights.append(height)
        # This is stored so that we can sort bar heights based on their respective x value
        x_vals.append(x)
    # This sorts the bar heights based on their respective x position as the contours do not
    # automatically sort from left to right
    cv2.waitKey(0)
    sorted_bars = zip(x_vals, bar_heights)
    sorted_bars = sorted(sorted_bars)
    sorted_bars_final = [bar for _, bar in sorted_bars]
    print(sorted_bars_final)
    print(len(sorted_bars_final))
    b64_values = calculate_ratios(sorted_bars_final[1:-3])
    print(b64_values)
    return b64_values


def generate_bar_from_code(text: str):
    """
    Receives a string of b64 characters and generates an image with bars accordingly.
    The image will have one ground truth bar in the beginning and two at the
    end to ensure the image is oriented correctly.
    Args:
        text (str): String of b64 characters

    Returns:
        None
    """
    nums = b64_to_bar(text)
    bars = BarGenerator(nums)
    return bars


def main():
    bars = generate_bar_from_code("-RmGHFRcqAU")
    cv2.imwrite("Bars.png", bars.img)
    # analyze_bar(bars.img)


if __name__ == "__main__":
    main()
