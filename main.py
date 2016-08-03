import RPi.GPIO as GPIO

def main():
    print(GPIO.RPI_INFO['P1_REVISION'])
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)

    GPIO.cleanup()

if __name__ == '__main__':
    main()