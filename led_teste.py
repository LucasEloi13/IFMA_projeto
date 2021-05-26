import RPi.GPIO as GPIO
import time

led = 24
led2 = 23

GPIO.setwarnings(False)

while True: 

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led, GPIO.OUT)
    GPIO.setup(led2, GPIO.OUT)

    GPIO.output(led, GPIO.HIGH)
    GPIO.output(led2, GPIO.HIGH)

    time.sleep(1)

    GPIO.output(led, GPIO.LOW)
    GPIO.output(led2, GPIO.LOW)

    time.sleep(1)

