import util as ut
import RPi.GPIO as GPIO
import os, time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

pin18 = GPIO.PWM(18, 100)   
pin19 = GPIO.PWM(19, 100) 

val=100 
pin18.start(val)              
pin19.start(val)

print("speed set to: ", val)


def move_robot(cmd):
    if cmd == '1':
        ut.forward()
    elif cmd == '0':
        ut.stop()
        
        
def main():
    ut.init_gpio()
    
    while True:
    
        x = input('Digite 1 para LIGAR o motor e 0  par DESLIGAR: ')
        move_robot(x)
    
if __name__ == '__main__':
    main()