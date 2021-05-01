#!/usr/bin/env python3
from typing import List

import numpy as np
import cv2
import webbrowser

from create_label import analyze_bar


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


def main():
    url_encoding = get_webcam_values()
    url_str = ""
    url_str = url_str.join(url_encoding)
    url = "https://youtu.be/" + url_str
    webbrowser.get("google-chrome").open(url)


if __name__ == "__main__":
    main()
