import sys
import RPi.GPIO as GPIO
from led_controller import *


def main(path, red_pin, green_pin, blue_pin):
    print("PI Revision: " + str(GPIO.RPI_INFO['P1_REVISION']))
    file = open(path, 'r')
    control_string = file.read()
    file.close()
    led_controller = LedController(red_pin, green_pin, blue_pin, control_string)
    led_controller.runControlList()


if __name__ == '__main__':
    path = sys.argv[1]
    red_gpio = int(sys.argv[2])
    green_gpio = int(sys.argv[3])
    blue_gpio = int(sys.argv[4])
    main(path, red_gpio, green_gpio, blue_gpio)
