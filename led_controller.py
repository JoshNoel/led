from enum import Enum
import RPi.GPIO as GPIO
import time


class LedController:
    class LED_COLOR(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3

        ### control_list : [[color, start_time, end_time], ...]
    def __init__(self, red_GPIO, blue_GPIO, green_GPIO, control_list):
        self.led_map = {self.LED_COLOR.RED:[red_GPIO, False],self.LED_COLOR.BLUE:[blue_GPIO, False],
                        self.LED_COLOR.GREEN:[green_GPIO, False]}
        self.control_list = control_list.split(" : ")
        for i in range(len(self.control_list)):
            self.control_list[i] = self.control_list[i].split('-')
            if self.control_list[i][0] == "Red":
                self.control_list[i][0] = self.LED_COLOR.RED
            if self.control_list[i][0] == "Green":
                self.control_list[i][0] = self.LED_COLOR.GREEN
            if self.control_list[i][0] == "Blue":
                self.control_list[i][0] = self.LED_COLOR.BLUE
            self.control_list[i][1] = float(self.control_list[i][1])

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        if red_GPIO != -1:
            GPIO.setup(red_GPIO, GPIO.OUT, initial=GPIO.LOW)
        if green_GPIO != -1:
            GPIO.setup(green_GPIO, GPIO.OUT, initial=GPIO.LOW)
        if blue_GPIO != -1:
            GPIO.setup(blue_GPIO, GPIO.OUT, initial=GPIO.LOW)

    def __del__(self):
        GPIO.cleanup()

    def __outputGPIO(self, channel, state):
        if state == False:
            GPIO.output(channel, GPIO.LOW)
        elif state == True:
            GPIO.output(channel, GPIO.HIGH)

    def __toggleLED(self, LED_COLOR):
        if self.led_map[LED_COLOR][0] != -1:
            self.led_map[LED_COLOR][1] = not self.led_map[LED_COLOR][1]
            self.__outputGPIO(self.led_map[LED_COLOR][0], self.led_map[LED_COLOR][1])
            print(str(self.led_map[LED_COLOR][0]) + ":" + str(self.led_map[LED_COLOR][1]))

    def runControlList(self):
        it = 0
        start = time.clock()
        while it < len(self.control_list):
            if time.clock() - start > self.control_list[it][1]:
                self.__toggleLED(self.control_list[it][0])
                it += 1


