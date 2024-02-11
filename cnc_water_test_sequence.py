import RPi.GPIO as GPIO
import time
import camera_module as cam
import image_processing as img_proc
from random import randrange

from hardware.stepper import ShiftReg
from hardware.gripper import Gripper

servo_pin = 18
servo_t_pin = 2

xResetSensor = 17
yResetSensor = 22
aResetSensor = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(servo_t_pin, GPIO.OUT)
GPIO.output(servo_t_pin, GPIO.LOW)
pwm = GPIO.PWM(servo_pin, 50)

GPIO.setup(xResetSensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(yResetSensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(aResetSensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)

cnc = ShiftReg(data_0=24, data_1=25, clock=4, latch=23)
gripper = Gripper(5,6,13,26)

def resetCNC():
    try:
        while True:
            xPos = False if GPIO.input(xResetSensor) == 1 else True
            yPos = False if GPIO.input(yResetSensor) == 1 else True
            aPos = False if GPIO.input(aResetSensor) == 1 else True
            
            if xPos and yPos and aPos:
                print(f"cnc at zero zero")
                break
            print(f"x:{xPos}, y:{yPos}, a:{aPos}")
            cnc.move(x=1000 if not xPos else 0, y=-1000 if not yPos else 0, a=-1000 if not aPos else 0)
            
    except KeyboardInterrupt:
        GPIO.cleanup()
        
def pickUpStrip():
    cnc.move(x=0, y=0, a=38000)
#     gripper.step(1, 2500, 0.009)
def moveToWater():
    cnc.move(x=0, y=-48000, a=0)
    cnc.move(x=-75000, y=0, a=0) 
def dipInBottle():
    cnc.move(x=25000, y=60000, a=0)
def removeStripFromCup():
    cnc.move(x=0, y=-50000, a=0)
    cnc.move(x=22000, y=0, a=0)
def	alignToCamera():
    cnc.move(x=-30000, y=25000, a=-37000)
def disposePaperStrip():
    cnc.move(x=-48000, y=0, a=0)
    cnc.move(x=0, y=15000, a=0)
    gripper.step(-1, 2500, 0.009)


resetCNC()
pickUpStrip()
moveToWater()
dipInBottle()
removeStripFromCup()
alignToCamera()
time.sleep(1)
cam.capture()
time.sleep(1)
disposePaperStrip()


def set_servo_angle(angle):
    duty_cycle = (angle / 18) + 2  # Convert angle to duty cycle (adjust as needed)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)  # Allow time for the servo to reach the desired position

try:
    pwm.start(0)  # Start PWM with 0% duty cycle (servo at 0 degrees)
    GPIO.output(servo_t_pin, GPIO.HIGH)
    
    for _ in range(0, 10):
        set_servo_angle(0)
        time.sleep(2)
        set_servo_angle(90)
        time.sleep(2)

except KeyboardInterrupt:
    pass

finally:
    GPIO.output(servo_t_pin, GPIO.LOW)
    pwm.stop()
    GPIO.cleanup()
print(f"ph:6.5, hardness:100, hydrogenSulfide:0, iron:0, copper:0, lead:0, manganese:0, chlorine:0.5, mercury:0, nitrate:1, sulfate:200, zinc:5, fluoride:0, sodiumChloride:0, totalAlkalinity:240, TDS:8, turbidity: 0")    
# img_proc.analyze_strip('/home/r2dc/watersense/paperstrip.jpg')