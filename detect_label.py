#!/usr/bin/env python3
from typing import List

import numpy as np
import cv2

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
    max_size = 0
    biggest_crop = None
    for crop in crops:
        if crop.size > max_size:
            biggest_crop = crop
    return biggest_crop


def detect_rectangle(src: np.array):
    # Detect label rectangle in the image
    th3 = cv2.adaptiveThreshold(src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imshow("th3", th3)
    contours, h = cv2.findContours(th3, 1, 2)
    detected = 0
    crops = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            x, y1, w, y2 = cv2.boundingRect(cnt)

            # Check for correct ratio
            if 1.8 < w / y2 < 2.2:
                detected += 1
                cropped = src[y1:y1 + y2, x:x + w]
                crops.append(cropped)
                # This cropped section will be sent to the detect bars function
                # cv2.imshow("cropped", cropped)
                # cv2.waitKey(0)
    print("Detected: ", detected)
    crop = max_crop(crops)
    cv2.imshow("Crop", crop)
    return crop


def get_webcam_img():
    cap = cv2.VideoCapture(0)
    while True:
        # Capture frame-by-frame
        _, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame


def main():
    # img = get_webcam_img()
    img = cv2.imread("test2.jpg", 0)
    # img = add_rectangle(img)
    cv2.imshow("Original", img)
    res = detect_rectangle(img)
    analyze_bar(res)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()