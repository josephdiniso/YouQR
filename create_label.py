#!/usr/bin/env python3
from math import ceil
from typing import List
import argparse

import numpy as np
import cv2

from b64_to_bar import b64_to_bar, bar_to_b64


class BarGenerator:
    # Configuration
    height = 300  # 100%
    bar_width = 15
    space_between_bars = 10
    color = (0, 0, 0)
    img = np.full((400, 1000, 3), 255, dtype=np.uint8)

    def __init__(self):
        pass

    def draw_bar(self, bar_index, bar_height):
        bar_height = int(bar_height * self.height)
        y = int((self.height - bar_height) / 2)
        start_point = (bar_index * (self.space_between_bars + self.bar_width), y)
        end_point = (start_point[0] + self.bar_width, bar_height + y)
        cv2.rectangle(self.img, start_point, end_point, self.color, -1)


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
        ratio = height / 0.4
        if 0 < ratio <= 0.125:
            ratios.append(0)
        elif 0.125 < ratio <= 0.25:
            ratios.append(1)
        elif 0.25 < ratio <= 0.375:
            ratios.append(2)
        elif 0.375 < ratio <= 0.5:
            ratios.append(3)
        elif 0.5 < ratio <= 0.625:
            ratios.append(4)
        elif 0.625 < ratio <= 0.75:
            ratios.append(5)
        elif 0.75 < ratio <= 0.875:
            ratios.append(6)
        elif 0.875 < ratio <= 1:
            ratios.append(7)
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
    img = src
    # _, thresh = cv2.threshold(src, 127, 255, 1)
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
        height = round((bottom - top) / img_height, 2)
        if height > 0.9:
            continue
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
    b64_values = calculate_ratios(sorted_bars_final[1:-2])
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
    print(nums)
    bars = BarGenerator()
    bars.draw_bar(0, 0.9)
    bars.draw_bar(len(nums) + 1, 0.9)
    bars.draw_bar(len(nums) + 2, 0.9)
    for index, x in enumerate(nums):
        bars.draw_bar(index + 1, 0.05 * (x + 1))
    return bars


def main():
    bars = generate_bar_from_code("OcHuxFJvKmI")
    cv2.imwrite("Bars.png", bars.img)
    analyze_bar(cv2.cvtColor(bars.img, cv2.COLOR_BGR2GRAY))


if __name__ == "__main__":
    main()
