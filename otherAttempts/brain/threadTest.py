import time
from threading import Thread

def findBlock():
    print "hi"
    '''
    cap = cv2.VideoCapture(0)
    while 1:

        _, im = cap.read()
        height, width, channels = im.shape #todo: dont recalculate each time
        hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        COLOR_MIN = np.array([100,150,0])
        COLOR_MAX = np.array([200,220,360])
        frame_threshed = cv2.inRange(hsv_img, COLOR_MIN, COLOR_MAX)
        imgray = frame_threshed
        ret,thresh = cv2.threshold(frame_threshed,127,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        # Find the index of the largest contour
        if(len(contours)>0):
            areas = [cv2.contourArea(c) for c in contours]
            max_index = np.argmax(areas)
            cnt=contours[max_index]
            if(cv2.contourArea(cnt)>=150):
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)

                #blockLocation = [(x+w/2.0)-(width/2),(y+h/2.0)-(height/2)]
            else:
                pass
                #blockLocation = None
        else:
            pass
            #blockLocation = None
    '''

#global blockLocation
#start opencv thread
t = Thread(target=findBlock(), args=None)
t.start()