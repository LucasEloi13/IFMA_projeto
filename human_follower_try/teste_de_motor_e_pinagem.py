import util as ut
import RPi.GPIO as GPIO



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

pin18 = GPIO.PWM(18, 100)   
pin19 = GPIO.PWM(19, 100)

val=100     #VELOCIDADE DO MOTOR
pin18.start(val)              
pin19.start(val)

ut.init_gpio()

while(1):
    x =  input('digite 1 ou 0: ')
    
    if x == '1':
        ut.forward()
        
    elif x == '0':
        ut.stop()



