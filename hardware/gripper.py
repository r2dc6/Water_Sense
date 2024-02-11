import RPi.GPIO as GPIO
import time

class Gripper:
    def __init__(self, pin1, pin2, pin3, pin4):
        GPIO.setmode(GPIO.BCM)
        self.stepper_pins = [pin1, pin2, pin3, pin4]
        for pin in self.stepper_pins:
            GPIO.setup(pin, GPIO.OUT)
        self.step_sequence = [
            [1, 0, 0, 1],
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 1],
        ]
        self.step_index = 0

    def step(self, direction, steps, delay):
        for i in range(steps):
            self.step_index = (self.step_index + direction) % len(self.step_sequence)
            for pin_index in range(len(self.stepper_pins)):
                pin_value = self.step_sequence[self.step_index][pin_index]
                GPIO.output(self.stepper_pins[pin_index], pin_value)
            time.sleep(delay)

# Example usage:
# gripper = Gripper(5, 6, 13, 26)
# gripper.step(-1, 2000, 0.009)  # Take 500 steps in the anticlockwise direction with a delay of 0.009 seconds between steps
# gripper.step(-1, 500, 0.009)  # Take 500 steps in the clockwise direction with a delay of 0.009 seconds between steps

# Clean up GPIO after usage
# GPIO.cleanup()
