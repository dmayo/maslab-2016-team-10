from ir_sensor import *
import math

class Ir_array:
    """Ir_array is used to update all IR sensors on the Stack Destroyer robot
    and report the distances in inches between the edge of the robot circular
    profile and the nearest wall.
        If the sensor configuration on the robot is changed, the math/trig in this
    class will have to be updated!
    If 'not a number' is returned, the IR sensor is out of range!
    """
    ir_value = [float('inf'),float('inf'),float('inf'),float('inf'),float('inf'),float('inf')];
    ir_offset = [0.0,0.0,0.0,0.0,0.0,0.0]

    def __init__(self,tamp,pin0,pin1,pin2,pin3,pin4,pin5):
        self.sensors = [Ir_sensor(tamp,pin0),Ir_sensor(tamp,pin1),Ir_sensor(tamp,pin2,"Long"),Ir_sensor(tamp,pin3,"Long"),Ir_sensor(tamp,pin4),Ir_sensor(tamp,pin5)]

        self.ir_offset[0] = 1.1 #error: 1.61-.5 = 1.1
        self.ir_offset[1] = 1.1 #error: 1.61 - .5 = 1.1
        self.ir_offset[2] = 3.735
        self.ir_offset[3] = 3.735
        self.ir_offset[4] = 1.1 #error: 1.61 - .5 = 1.1
        self.ir_offset[5] = 1.1 #error 1.61 - .5 = 1.1

        self.IRs = {'Left': [0, 1, 2], 'Right': [5, 4, 3]}

        self.DISTANCE_EPSILON=1 #in inches

    def update(self):
        for x in xrange(len(self.ir_value)):
            self.ir_value[x] = self.sensors[x].get_distance() - self.ir_offset[x]

    def getAvgDistanceLeftWall(self):
        return (self.ir_value[self.IRs["Left"][0]]+self.ir_value[self.IRs["Left"][1]]*math.cos(math.radians(30)))/2

    def getAvgDistanceRightWall(self):
        return (self.ir_value[self.IRs["Right"][0]]+self.ir_value[self.IRs["Right"][1]]*math.cos(math.radians(30)))/2

    def getMinDistanceLeftWall(self):
        return min(self.ir_value[self.IRs["Left"][0]], self.ir_value[self.IRs["Left"][1]]*math.cos(math.radians(30)))

    def getMinDistanceRightWall(self):
        return min(self.ir_value[self.IRs["Right"][0]], self.ir_value[self.IRs["Right"][1]]*math.cos(math.radians(30)))

    def isCorner(self, side):
        return (self.ir_value[self.IRs[side][0]]-self.ir_value[self.IRs[side][1]]*math.cos(math.radians(30)))<self.DISTANCE_EPSILON

    def isCliff(self, side):
        return (self.ir_value[self.IRs[side][0]]-self.ir_value[self.IRs[side][1]]*math.cos(math.radians(30)))>self.DISTANCE_EPSILON

    def isFlatWall(self, side):
        return abs(self.ir_value[self.IRs[side][0]]-self.ir_value[self.IRs[side][1]]*math.cos(math.radians(30)))<=self.DISTANCE_EPSILON

    def getWallInFrontDistance(self,side):
        return self.ir_value[self.IRs[side][2]]


        
        
