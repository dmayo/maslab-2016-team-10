from state import state
import turnToBlockState
import lookingForBlocksState
from startState import *
from utils import *

#substates: WallDetect,FindSafeAngle,PickUpBlock,DeChoke

class PickUpBlockState(state):

	timeoutMax = 50 #max timeout of 5 seconds (50 timed loops)
	minSafeFrontDistance = 9 #an approximation of the distance in inches we'd need to read from a 90-degree corner pointing at the middle of the robot to life the block safely

	def __init__(self, sensors, actuators, motorController, timer):
		super(startState, self).__init__(sensors, actuators, motorController, timer)
		print "PickUpBlockState starting..."
		self.substate = "WallDetect"
		self.timeoutCounter = 0

	def run(self):
		while True:
			self.sensors.camera.update()

			if self.timer.millis() > 100:
				self.sensors.update()

				if self.substate == "WallDetect":
					if isItSafeToLiftArm == True:
						self.actuators.arm.pickUpBlock()
						self.substate = "PickUpBlock"
					else:
						self.substate = "FindSafeAngle"
				elif self.substate =="FindSafeAngle":
					#TODO
				elif self.substate == "PickUpBlock":
					isBlockDetected = self.sortBlock()
					if isBlockDetected == True:
						return startState(self.sensors, self.actuators, self.motorController, self.timer)
					else:
						self.timeoutCounter +=1
						if self.timeoutCounter >= self.timeoutMax:
							if self.actuators.sorter.sorterState == "None":
								self.actuators.sorter.jostle()


				self.actuators.update()
				self.motorController.updateMotorSpeeds()
				self.timer.reset()

	def isItSafeToLiftArm(self):
		return (self.sensors.irArray.ir_value[2] < self.minSafeFrontDistance and self.sensors.irArray.ir_value[3] < self.minSafeFrontDistance)

