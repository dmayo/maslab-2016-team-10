import os, time



while True:

	pipePath = "./vision"
	print "ok1"
	time.sleep(1)
	try:
	    os.mkfifo(pipePath)
	except OSError:
	    print "error"
	print "ok"
	rp = open(pipePath, 'r')
	response = rp.read()
	print "Got response %s" % response
	rp.close()