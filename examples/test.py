

ANGLE_MAX = 30
ANGLERATE_MAX = 160

def constrain(val, minval, maxval):
    if val>maxval :return maxval
    if val<minval :return minval
    return val

""" Angle = [-180, 180] , range = [-1, 1] """
def calculateGyr(angle,range_axis):
    target = range_axis - (angle/ANGLE_MAX)
    target *= ANGLERATE_MAX
    return target
    return constrain(target, -ANGLERATE_MAX, ANGLERATE_MAX)

class pid:

    MAX_INTEGRAL = 300

    def __init__(self,kp,ki,kd) -> None:
        self.kp=kp
        self.ki=ki
        self.kd=kd
        self.lasterror = 0
        self.integral = 0

    def pidUpdate(self,desired,measured,dt):
        output = 0
        error = desired - measured
        output += error * self.kp

        self.integral += self.ki * error * dt
        self.integral = constrain(self.integral,-self.MAX_INTEGRAL,self.MAX_INTEGRAL)
        output += self.integral

        derivative = ( self.lasterror - error ) / dt
        self.lasterror = error
        output += derivative * self.kd
        return constrain(output,-self.MAX_INTEGRAL,self.MAX_INTEGRAL)

range_axis = 0
angle = 15

print("Target deg/s:")
print(calculateGyr(angle,range_axis))

iteration = 0
axispid = pid(4,0,1)
pidoutput = 0 

measurment = 100
while iteration<100:
    measurment += (pidoutput*0.1)
    #target = calculateGyr(angle,range_axis)
    pidoutput = axispid.pidUpdate(0,measurment,1)
    print("PID:target " + str(pidoutput) + " : " + str(measurment))
    iteration+=1    