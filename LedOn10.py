import RPi.GPIO as GPIO
import time
import sys


def main(gpios):
    print("Turning on LED for 10 seconds")
    pins = [int(s) for s in gpios]
    GPIO.setup(pins, GPIO.OUT, initial = GPIO.HIGH)
    time.sleep(10)
    GPIO.output(pins, GPIO.LOW)
    GPIO.cleanup()

if __name__ == "main":
    main(sys.argv[1:])