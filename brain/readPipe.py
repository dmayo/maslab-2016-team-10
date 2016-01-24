import os, time
import signal

pipe_path = "./vision7"
if not os.path.exists(pipe_path):
    os.mkfifo(pipe_path)
# Open the fifo. We need to open in non-blocking mode or it will stalls until
# someone opens it for writting
pipe_fd = os.open(pipe_path, os.O_RDONLY)

while True:
    #signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    message = os.read(pipe_fd,100)
    if message:
        print("Received: '%s'" % message)
    print("Doing other stuff")
    time.sleep(1)
