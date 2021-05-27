#!/usr/bin/env python3
from typing import List

import numpy as np
import cv2
import argparse
import requests
import sys
import re

from b64_to_bar import b64_to_bar


class BarGenerator:
    """
    BarGenerator object which takes in a list of numbers, which are the octal representations
    of a YouTube embedded URL
    """
    height = 300
    bar_width = 15
    space_between_bars = 10

    def __init__(self, nums: List[int]):
        """
        Draws the corresponding bars according to the constructors list of nums
        Args:
            nums (List[int]): List of octal integers to draw corresponding bars from
        """
        self.img = np.full((self.height, self.bar_width * (len(nums) + 3) +
                            self.space_between_bars * (len(nums) + 3) + 45), 255,
                           dtype=np.uint8)
        self.draw_bar(1, 0.9)
        self.draw_bar(len(nums) + 2, 0.9)
        self.draw_bar(len(nums) + 3, 0.9)
        for index, x in enumerate(nums):
            self.draw_bar(index + 2, 0.05 * (x + 1))

        # Draw outer rectangle
        x1 = 0
        y1 = 0
        x2 = self.img.shape[1]
        y2 = self.img.shape[0]
        cv2.rectangle(self.img, (x1, y1), (x2, y2), 1, 10)

    def draw_bar(self, bar_index, bar_height) -> None:
        """
        Draws a bar on the self.img
        Args:
            bar_index (int): Represents which bar to draw (corresponds to width of image)
            bar_height (float): Percentage of total image height

        Returns:
            None
        """
        # Bar height is a percentage of the total height
        bar_height = int(bar_height * self.height)
        start_point = (bar_index * (self.space_between_bars + self.bar_width),
                       self.height // 2 - bar_height // 2)
        end_point = (start_point[0] + self.bar_width, self.height // 2 + bar_height // 2)
        cv2.rectangle(self.img, start_point, end_point, 0, -1)


def generate_bar_from_code(text: str) -> BarGenerator:
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


def eval_args(video_id: str):
    resp = requests.get('https://wnewsome.com/youtube_api/?id=' + video_id)
    if resp.json()["valid"]:
        # At this point, the video Id has been validated from the API
        video_title = resp.json()["title"]
        print("Video title: " + video_title)
        bars = generate_bar_from_code(video_id)
        font = cv2.FONT_HERSHEY_SIMPLEX
        video_title = re.sub(r"[^a-zA-Z0-9]", "_", video_title)
        video_title = video_title[0:20]
        cv2.imwrite(video_title + ".png", bars.img)
    else:
        print("Video ID: " + video_id + " is not valid.")


def main():
    parser = argparse.ArgumentParser(description="Generate a custom QR code from a URL embedded URL")
    parser.add_argument("encoding", type=str, required=True)
    args = parser.parse_args()
    video_id = args.encoding
    eval_args(video_id)


if __name__ == "__main__":
    main()
