#!/usr/bin/env python3
from typing import List

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


def calculate_ratios(scale: float, heights: List[float]):
    """
    Given a list of floats representing the height of the bars, these values are converted to their
    original base-64 encoding.
    Args:
        scale (float): Maximum height of a data bar
        heights (List[float]): List of heights of bars

    Returns:

    """
    ratios = []
    new_scale = 0.4
    for height in heights:
        ratio = height / new_scale
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
    gray = cv2.cvtColor(src.img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, 1)
    contours, h = cv2.findContours(thresh, 1, 2)
    bar_heights = []
    x_vals = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            x, y1, w, y2 = cv2.boundingRect(cnt)
            height = round(y2 / src.height, 2)
            org = (x, 310)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(src.img, str(height), org, font, 0.30, (0, 0, 0))
            bar_heights.append(height)
            # This is stored so that we can sort bar heights based on their respective x value
            x_vals.append(x)
    # This sorts the bar heights based on their respective x position as the contours do not
    # automatically sort from left to right
    sorted_bars = zip(x_vals, bar_heights)
    sorted_bars = sorted(sorted_bars)
    sorted_bars_final = [bar for _, bar in sorted_bars]
    b64_values = calculate_ratios(sorted_bars_final[0], sorted_bars_final[1:-2])
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
    nums = b64_to_bar("OcHuxFJvKmI")
    bars = BarGenerator()
    bars.draw_bar(0, 0.9)
    bars.draw_bar(len(nums) + 1, 0.9)
    bars.draw_bar(len(nums) + 2, 0.9)
    for index, x in enumerate(nums):
        bars.draw_bar(index + 1, 0.05 * (x + 1))
    analyze_bar(bars)


def main():
    generate_bar_from_code("OcHuxFJvKmI")


if __name__ == "__main__":
    main()
