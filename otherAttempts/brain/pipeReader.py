import os
class PipeReader:
	def __init__(self, pipe_path):
	    if not os.path.exists(pipe_path):
	        os.mkfifo(pipe_path)
	    self.pipe = os.open(pipe_path, os.O_RDONLY)

	def read(self,numBytes):
		return os.read(self.pipe, numBytes)