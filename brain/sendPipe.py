import os, time

pipePath = "./robot"
if not os.path.exists(pipePath):
    os.mkfifo(pipePath)

message="works"
i=0
wp = os.open(pipePath, os.O_WRONLY)


while True:
	i+=1
	os.write(wp, "UP")
	os.write(wp, "STOP")
	#wp = open(pipePath,'w')
	#wp.write(message+str(i))
	os.write(wp, message+str(i))
	print message+str(i)
	time.sleep(.1)


#wp.close()
print message+str(i)

