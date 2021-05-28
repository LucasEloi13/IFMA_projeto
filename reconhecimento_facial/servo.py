from gpiozero import Servo
from time import sleep

myGPIO=17

servo = Servo(myGPIO)


while True:
    servo.min()
    print('min')
    sleep(1)
    servo.mid()
    print('mid')
    sleep(1)
    servo.max()
    print('max')
    sleep(1)
    servo.mid()
    print('mid')
    sleep(1)
    
    