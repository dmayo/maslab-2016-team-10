#dummy function until I can import Jake's code
#distance is inches
def get_raw_ir_distance(sensor_id)
    return 0


class Ir_array:
    """Ir_array is used to update all IR sensors on the Stack Destroyer robot
and report the distances in inches between the edge of the robot circular
profile and the nearest wall.
    If the sensor configuration on the robot is changed, the math/trig in this
class will have to be updated!
    If 'not a number' is returned, the IR sensor is out of range!
    """
    ir_value = [float('nan'),float('nan'),float('nan'),float('nan'),float('nan'),float('nan')];
    self.ir_offset = [0.0,0.0,0.0,0.0,0.0,0.0]

    def __init__(self):
        self.self.ir_offset[0] = 1.5
        self.ir_offset[1] = 1.5
        self.ir_offset[2] = 1
        self.ir_offset[3] = 1
        self.ir_offset[4] = 1.5
        self.ir_offset[5] = 1

    def update():
        for x in xrange(6):
            self.ir_value[x] = get_raw_ir_distance(x) - self.ir_offset[x]

        
        
