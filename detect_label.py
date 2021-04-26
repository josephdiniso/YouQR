import numpy as np
import cv2

# Read a test image
img = cv2.imread('test.jpg',0)
# Adding a digital rectangle to the test image
start_point = (100,300)
end_point = (300,400)
black = (0,0,0)
white = (255,255,255)
cv2.rectangle(img, start_point, end_point, white, -1)
cv2.rectangle(img, start_point, end_point, black, 0)
cv2.putText(img, 'TEST', (120, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.30, (0, 0, 0))

# Detect label rectangle in the image
ret,thresh = cv2.threshold(img,127,255,1)
contours,h = cv2.findContours(thresh,1,2)
detected = 0
for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt,True),True)
        if len(approx)==4:
            x,y1,w,y2 = cv2.boundingRect(cnt)
            # Check for correct ratio
            if w/y2 > 1.8 and w/y2 < 2.2:
                detected+=1
                cropped = img [y1:y1+y2,x:x+w]
                # This cropped section will be sent to the detect bars function
                cv2.imshow("cropped", cropped)
print ("Detected: ", detected)
cv2.imshow("original", img)
cv2.waitKey(0)