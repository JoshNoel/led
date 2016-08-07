from enum import Enum
import RPIO
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
        print(self.control_list)
        for i in range(len(self.control_list)):
            self.control_list[i] = self.control_list[i].split('-')
            if self.control_list[i][0] == "Red":
                self.control_list[i][0] == self.LED_COLOR.RED
            if self.control_list[i][0] == "Green":
                self.control_list[i][0] == self.LED_COLOR.GREEN
            if self.control_list[i][0] == "Blue":
                self.control_list[i][0] == self.LED_COLOR.BLUE

        RPIO.setmode(RPIO.BCM)
        RPIO.setwarnings(False)

        if red_GPIO != -1:
            RPIO.setup(red_GPIO, RPIO.OUT, initial=RPIO.LOW)
        if green_GPIO != -1:
            RPIO.setup(green_GPIO, RPIO.OUT, initial=RPIO.LOW)
        if blue_GPIO != -1:
            RPIO.setup(blue_GPIO, RPIO.OUT, initial=RPIO.LOW)

    def __del__(self):
        RPIO.cleanup()

    def __toggleLED(self, LED_COLOR):
        if self.led_map[LED_COLOR][0] != -1:
            RPIO.output(self.led_map[LED_COLOR][0], not self.led_map[LED_COLOR][1])

    def runControlList(self):
        it = 0
        start = time.clock()
        while it < len(self.control_list):
            if time.clock() - start > self.control_list[it][1]:
                it += 1
                self.toggleLED(self.control_list[it][0])

