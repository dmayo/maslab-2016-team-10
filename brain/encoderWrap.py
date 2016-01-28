from tamproxy.devices import Encoder

class EncoderWrap:
	def __init__(self):
        self.encoderL = Encoder(self.tamp, 22, 23)
        self.encoderR = Encoder(self.tamp, 21, 20)
        self.isRobotMoving=False
        self.prevEncoderL=0
        self.pervEncoderR=0
        self.NOT_MOVING_DIST=100

    def resetEncoders(self):
		self.encoderL.write(0)
		self.encoderR.write(0)

	def update():
		if(abs(self.encoderL.val-self.prevEncoderL)<self.NOT_MOVING_DIST and abs(self.encoderL.val-self.prevEncoderL)<self.NOT_MOVING_DIST):
			self.isRobotMoving=False
		else:
			self.isRobotMoving=True
		self.prevEncoderL=self.encoderL.val
		self.prevEncoderR=self.encoderR.val
