from state import state
import startState
import time
import pickUpBlockState
import turnToBlockState
import timeout

class CheckForMoreBlocksState(state):
	#substates: moveForward, moveBack
	def __init__(self, sensors, actuators, motorController, timer, utils):
		super(CheckForMoreBlocksState, self).__init__(sensors, actuators, motorController, timer, utils)

		print "starting CheckForMoreBlocksState..."
		self.timeout = timeout.Timeout(5)

		self.substate = "moveForward"
		self.sensors.encoders.resetEncoders()
		self.FORWARD_DISTANCE = 2.5 #move forward 2.5 inches
		self.BACKWARD_DISTANCE = -4 #in inches
		self.backingUpStartTime = 0
		self.DRIVE_SPEED = 40
		self.BACK_UP_SPEED = 20

	#Todo: put code to constantly look for blocks
	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()

				#constantly check to see if our state has timed out
				if self.timeout.isTimeUp() == True:
					print 'State has timed out! Exiting to start state...'
					return startState.StartState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				#constantly check to see if we have acquired a block
				if self.sensors.uIR.val == 0:
					print 'Detected a block captured! Now picking it up...'
					self.driveStraight(0)
					self.turnConstantRate(0)
					return pickUpBlockState.PickUpBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				#constanlty check to see if we have detected a new block
				if self.sensors.camera.detectBlock == True:
					self.driveStraight(0)
					self.turnConstantRate(0)
					return turnToBlockState.TurnToBlockState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				if self.substate == "moveForward":
					self.driveStraight(self.DRIVE_SPEED)
					if self.sensors.encoders.getDistanceTraveled() >= self.FORWARD_DISTANCE or self.isColliding():
						print 'Either finished moving forward or about to crash. Now moving backwards.'
						self.substate == "backUp"
						self.sensors.encoders.resetEncoders()
				if self.substate == "backUp":
					self.driveStraight(self.BACK_UP_SPEED)
					if self.sensors.encoders.getDistanceTraveled() <= self.BACKWARD_DISTANCE or self.isCollidingOnSides():
						print 'Finished backing up or detecting potential collision with slanted wall. Now exiting state.'
						self.driveStraight(0)
						self.turnConstantRate(0)
						return startState.StartState(self.sensors, self.actuators, self.motorController, self.timer, self.utils)

				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()

	#collision detection avoids 1 inch of space on the sides. Trig was used to determine the lenght of the 30-degree angled sensors.
	#for the front sensors, we seek to avoid the worst case of a 90-degree angle, comes out to 2.9+.59 = about 3.5
	def isColliding(self):
		if self.sensors.irArray.ir_value[0] < 1 or self.sensors.irArray.ir_value[5] < 1:
			return True
		elif self.sensors.irArray.ir_value[1] < 2.32 or self.sensors.irArray.ir_value[4] < 2.32:
			return True
		elif self.sensors.irArray.ir_value[2] < 3.5 or self.sensors.irArray.ir_value[3] < 3.5:
			return True
		return False


	#for the front sensors, we seek to avoid the worst case of a 90-degree angle, comes out to 2.9+.59 = about 3.5
	def isCollidingOnSides(self):
		if self.sensors.irArray.ir_value[0] < 1 or self.sensors.irArray.ir_value[5] < 1:
			return True
		return False