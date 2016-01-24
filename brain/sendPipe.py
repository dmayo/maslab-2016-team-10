import os, time

pipePath = "./vision7"
if not os.path.exists(pipePath):
    os.mkfifo(pipePath)

message="works"
i=0
wp = os.open(pipePath, os.O_WRONLY| os.O_NONBLOCK)

while True:
	i+=1
	#wp = open(pipePath,'w')
	#wp.write(message+str(i))
	os.write(wp, message+str(i))
	print message+str(i)
	time.sleep(1)

#wp.close()

