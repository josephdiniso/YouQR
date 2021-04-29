#!/usr/bin/env python3
from typing import List

import numpy as np
import cv2
import webbrowser

from create_label import analyze_bar


def add_rectangle(src: np.array):
    # Adding a digital rectangle to the test image
    start_point = (100, 300)
    end_point = (300, 400)
    black = (0, 0, 0)
    white = (255, 255, 255)
    cv2.rectangle(src, start_point, end_point, white, -1)
    # cv2.rectangle(src, (50, 250), (350, 450), white, -1)
    cv2.rectangle(src, start_point, end_point, black, 0)

    cv2.putText(src, 'TEST', (120, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.30, (0, 0, 0))
    return src


def max_crop(crops: List) -> np.array:
    """
    Gets the largest crop in a list of images
    Args:
        crops (List): List of np.arrays (images)

    Returns:
        np.array: Largest crop
    """
    max_size = 0
    biggest_crop = None
    for crop in crops:
        if crop.size > max_size:
            max_size = crop.size
            biggest_crop = crop
    return biggest_crop


def analyze_contours(frame: np.array, contours: List):
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            failure = False
            x, y1, w, h = cv2.boundingRect(cnt)
            # Check for correct ratio
            if 1.8 < w / h < 2.2 and frame.size * 0.01 < w * h < frame.size * 0.8:
                cv2.drawContours(frame, [cnt], 0, (0, 255, 0), 3)
                cropped = frame[y1:y1 + h, x:x + w]
                b64_values = None
                try:
                    b64_values = analyze_bar(cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY))
                except KeyError:
                    failure = True
                except ValueError:
                    failure = True
                except IndexError:
                    failure = True
                return b64_values


def get_webcam_values():
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
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return b64_values


def main():
    url_encoding = get_webcam_values()
    url_str = ""
    url_str = url_str.join(url_encoding)
    url = "https://youtu.be/" + url_str
    webbrowser.get("google-chrome").open(url)


if __name__ == "__main__":
    main()
