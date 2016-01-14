import numpy as np
import cv2

cap = cv2.VideoCapture(0)
while 1:
	_, im = cap.read()
	hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
	COLOR_MIN = np.array([100,150,0])
	COLOR_MAX = np.array([200,220,360])
	frame_threshed = cv2.inRange(hsv_img, COLOR_MIN, COLOR_MAX)
	imgray = frame_threshed
	ret,thresh = cv2.threshold(frame_threshed,127,255,0)
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	# Find the index of the largest contour
	areas = [cv2.contourArea(c) for c in contours]
	max_index = np.argmax(areas)
	cnt=contours[max_index]

	x,y,w,h = cv2.boundingRect(cnt)
	cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)

	cv2.imshow("Show",im)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
	    break

cv2.destroyAllWindows()
