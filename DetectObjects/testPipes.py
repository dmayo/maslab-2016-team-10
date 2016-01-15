import os
import cv2
import time
pipePath = "./vision"
while 1:
	time.sleep(1)
	try:
		os.mkfifo(pipePath)
	except OSError:
		pass
	rp = open(pipePath, 'r')
	response = rp.read()
	print "Got response %s" % response
	rp.close()
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

