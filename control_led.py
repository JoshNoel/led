import sys
import RPi.GPIO as GPIO
from led_controller import *


def main(path):
    print("PI Revision: " + str(GPIO.RPI_INFO['P1_REVISION']))
    file = open(path, 'r')
    control_string = file.read()
    file.close()
    led_controller = LedController(17, -1, -1, control_string)
    led_controller.runControlList()


if __name__ == '__main__':
    main(sys.argv[1])
