import RPi.GPIO as GPIO
from time import sleep

class Stepper:
    def __init__(self):
        self.seq_pointer = 0
        self.arrSeq = [
                [0, 0, 0, 1],
                [0, 0, 1, 1],
                [0, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 1, 0, 0],
                [1, 1, 0, 0],
                [1, 0, 0, 0],
                [1, 0, 0, 1]
            ]

    def move(self, direction):
        self.seq_pointer = (self.seq_pointer + direction) % len(self.arrSeq)
        return self.arrSeq[self.seq_pointer]
    
    def getPos(self):
        return self.arrSeq[self.seq_pointer]

class ShiftReg:
    def __init__(self, data_0, data_1, clock, latch):
        GPIO.setmode(GPIO.BCM)
        self.data_pin_0 = data_0
        self.data_pin_1 = data_1
        self.clock_pin = clock
        self.latch_pin = latch

        GPIO.setup(self.data_pin_0, GPIO.OUT)
        GPIO.setup(self.data_pin_1, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)
        GPIO.setup(self.latch_pin, GPIO.OUT)
        
        self.stepper_x = Stepper()
        self.stepper_y = Stepper()
        self.stepper_z = Stepper()
        self.stepper_a = Stepper()
        self.stepper_x_value = [0]*4
        self.stepper_y_value = [0]*4
        self.stepper_z_value = [0]*4
        self.stepper_a_value = [0]*4
        
    def _shift_out(self, value_0, value_1):
        for i in range(0, 8):
            GPIO.output(self.data_pin_0, value_0[i])
            GPIO.output(self.data_pin_1, value_1[i])
            GPIO.output(self.clock_pin, 1)
            GPIO.output(self.clock_pin, 0)
        GPIO.output(self.latch_pin, 1)
        GPIO.output(self.latch_pin, 0)
#         print(f"Shift Register Value: x= {value_0[:4]} y= {value_0[4:]} z= {value_1[:4]} a= {value_1[4:]}")
        
    def move(self, x=0, y=0, a=0):
        z = y 
        xDir = 1 if x > 0 else -1
        yDir = 1 if y > 0 else -1
        zDir = 1 if z > 0 else -1
        aDir = 1 if a > 0 else -1
        x = abs(x)
        y = abs(y)
        z = abs(z)
        a = abs(a)
        
        for i in range(max(x, y, z, a)):
            self.stepper_x_value = self.stepper_x.getPos() if x == 0 or x <= i else self.stepper_x.move(xDir)
            self.stepper_y_value = self.stepper_y.getPos() if y == 0 or y <= i else self.stepper_y.move(yDir)
            self.stepper_z_value = self.stepper_z.getPos() if z == 0 or z <= i else self.stepper_z.move(zDir)
            self.stepper_a_value = self.stepper_a.getPos() if a == 0 or a <= i else self.stepper_a.move(aDir)
            self._shift_out(value_0=self.stepper_a_value+self.stepper_y_value, value_1=self.stepper_z_value+self.stepper_x_value)
            sleep(0.001)

    def cleanup(self):
        GPIO.cleanup()

# cnc = ShiftReg(data_0=24, data_1=25, clock=4, latch=23)
# cnc.move(x=-10000, y=50000, a=10000)
# cnc.cleanup()
