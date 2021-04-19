import numpy as np
import cv2 as cv

# Configuration
height = 300 #100%
bar_width = 15
space_between_bars = 10
color = (0,0,0)

img = np.zeros((400,1000,3), np.uint8)
img = img+255
def draw_bar(bar_index, bar_height):
    bar_height = int(bar_height*height)
    y = int((height-bar_height)/2)
    start_point = (bar_index*(space_between_bars+bar_width), y)
    end_point = (start_point[0]+bar_width, bar_height+y)
    cv.rectangle(img, start_point, end_point, color, -1)

# Draw Control Bars
draw_bar(0,0.9)
draw_bar(18,0.9)
draw_bar(19,0.9)

# Testing drawing data bars
for x in range(1, 18):
  draw_bar(x,0.05*x) # Draw a larger bar every time

# Display Image
cv.imshow('Generated Label',img)
cv.waitKey(0)
cv.destroyAllWindows()