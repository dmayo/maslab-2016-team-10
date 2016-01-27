from tamproxy.devices import AnalogInput

class Ir_sensor(AnalogInput):
    """Represents a short-range IR sensor"""
    def __init__(self,tamp,pin):
        super(self.__class__,self).__init__(tamp,pin)

    def get_distance(self):
        '''Min: 1.75in -- Max:12in. We are placing the sensors so that it is impossible to detect distances below the minimum. If we detect a distance above the maximum, we will return a Not a Number'''
        max_dist = 24
        v = self.val
        d = 1.0656*10**5/(v+633.328)
        print 'Voltage: ' + str(v)
        if d > max_dist:
            return float('inf')
        else:
            return d
