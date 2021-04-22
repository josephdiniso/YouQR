#!/usr/bin/env python3

import numpy as np
import cv2


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
        print(bar_index, bar_height)
        bar_height = int(bar_height * self.height)
        y = int((self.height - bar_height) / 2)
        start_point = (bar_index * (self.space_between_bars + self.bar_width), y)
        end_point = (start_point[0] + self.bar_width, bar_height + y)
        cv2.rectangle(self.img, start_point, end_point, self.color, -1)


if __name__ == "__main__":
    bars = BarGenerator()
    bars.draw_bar(0, 0.9)
    bars.draw_bar(18, 0.9)
    bars.draw_bar(19, 0.9)
    for x in range(1, 18):
        bars.draw_bar(x, 0.05 * x)
    
    # Detecting Bar's height
    gray = cv2.cvtColor(bars.img, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,127,255,1)
    contours,h = cv2.findContours(thresh,1,2)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt,True),True)
        if len(approx)==4:
            x,y1,w,y2 = cv2.boundingRect(cnt)
            height = round(y2/bars.height,2)
            org = (x,310)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(bars.img,str(height),org, font, 0.30, (0,0,0))

    cv2.imshow('Generated Label', bars.img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
