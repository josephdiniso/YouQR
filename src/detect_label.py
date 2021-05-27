#!/usr/bin/env python3
from typing import List

import numpy as np
import cv2
import webbrowser

from b64_to_bar import bar_to_b64


def analyze_contours(frame: np.array, contours: List) -> List:
    """
    Iterates through the list of contours and determined if they are a viable code
    Args:
        frame (np.array): Image to analyze for eligible code
        contours (List): List of contours to receive rectangles from

    Returns:
        List of b64 coded values if a eligible code is found, otherwise None
    """
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            x, y1, w, h = cv2.boundingRect(cnt)
            # Check for correct ratio
            if 1.8 < w / h < 2.2 and frame.size * 0.01 < w * h < frame.size * 0.8:
                cv2.drawContours(frame, [cnt], 0, (0, 255, 0), 3)
                cropped = frame[y1:y1 + h, x:x + w]
                b64_values = analyze_bar(cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY))
                return b64_values


def get_webcam_values():
    """
    Opens webcam and displays live webcam image to the user. If contours are found after
    thresholding and passed to the analyze_contours() function along with the current frame.
    If analyze_contours() returns a non NoneType value then it breaks its loop and returns
    the list of b64 values to open a browser with.

    Returns:
        (List) b64 values as a list of strings
    """
    cap = cv2.VideoCapture(0)
    failure = False
    b64_values = None
    while not failure:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        th3 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        contours, h = cv2.findContours(th3, 1, 2)
        b64_values = analyze_contours(frame, contours)
        if b64_values is not None:
            break
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return b64_values


def calculate_ratios(heights: List[float]) -> List[int]:
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
        val = round(ratio * 8) - 1
        ratios.append(int(val))
    b64_values = bar_to_b64(ratios)
    return b64_values


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
    # Cuts edges of image
    src = src[10:-10, 10:-10]
    thresh = cv2.adaptiveThreshold(src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 5)
    contours, h = cv2.findContours(thresh, 1, 2)
    bar_heights = []
    img_height, img_width = src.shape
    x_vals = []
    for cnt in contours:
        top = (cnt[cnt[:, :, 1].argmin()])[0][1]
        bottom = (cnt[cnt[:, :, 1].argmax()])[0][1]
        x = (cnt[cnt[:, :, 0].argmax()][0])[0]
        height = round((bottom - top) / img_height, 5)
        bar_heights.append(height)
        # This is stored so that we can sort bar heights based on their respective x value
        x_vals.append(x)
    # This sorts the bar heights based on their respective x position as the contours do not
    # automatically sort from left to right
    sorted_bars = zip(x_vals, bar_heights)
    sorted_bars = sorted(sorted_bars)
    sorted_bars_final = [bar for _, bar in sorted_bars]
    b64_values = calculate_ratios(sorted_bars_final[1:-3])
    return b64_values


def main():
    url_encoding = get_webcam_values()
    url_str = ""
    url_str = url_str.join(url_encoding)
    url = "https://youtu.be/" + url_str
    webbrowser.get().open(url)


if __name__ == "__main__":
    main()
