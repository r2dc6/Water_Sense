import RPi.GPIO as GPIO
import time

# Define the GPIO pins for the switch
switch_pin1 = 17
switch_pin2 = 22

# Set up GPIO mode and configure pull-up resistors
GPIO.setmode(GPIO.BCM)
GPIO.setup(switch_pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        # Read the status of the switches
        switch1_status = GPIO.input(switch_pin1)
        switch2_status = GPIO.input(switch_pin2)

        # Print the status of the switches
        print(f"Switch 1: {switch1_status}, Switch 2: {switch2_status}")

        # Add your custom logic based on the switch status here

        # Wait for a short duration to avoid high CPU usage
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting program.")
finally:
    # Clean up GPIO settings
    GPIO.cleanup()
