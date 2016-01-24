import os, time

pipePath = "./vision7"
#print "ok1"
#time.sleep(1)
try:
    os.mkfifo(pipePath)
except OSError:
    print "error"
#print "ok"
rp = open(pipePath, 'r')
while True:
	
	response = rp.read()
	print response
	#rp.close()