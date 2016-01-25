import os, time

pipePath = "./motorL"
if not os.path.exists(pipePath):
    os.mkfifo(pipePath)

message="works"
i=0
wp = os.open(pipePath, os.O_WRONLY)


while True:
	i+=1
	os.write(wp, "left 5")
	os.write(wp, "right 5")
	#wp = open(pipePath,'w')
	#wp.write(message+str(i))
	print message+str(i)
	time.sleep(.1)


#wp.close()
print message+str(i)

