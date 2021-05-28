import RPi.GPIO as GPIO
import os
import time

ena = 18            
in1 = 6
in2 = 17

enb = 19
in3 = 27
in4 = 23

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

GPIO.setup(ena,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

pwm_a = GPIO.PWM(ena,500)
pwm_b = GPIO.PWM(enb,500)

pwm_a.start(0)
pwm_b.start(0)

def  Giro_Favor_Reloj_MotorA():
    GPIO.output(in1,False)
    GPIO.output(in2,True)

def Giro_Contra_Reloj_MotorA():
    GPIO.output(in1,True)
    GPIO.output(in2,False)

def  Giro_Favor_Reloj_MotorB():
    GPIO.output(in3,False)
    GPIO.output(in4,True)

def Giro_Contra_Reloj_MotorB():
    GPIO.output(in3,True)
    GPIO.output(in4,False)

os.system('clear')
print("Motor[A-B], Sentido [F-R], Velocidade [0-100]")
print("exemplo 'AF50' MOTOR A Foward a 50% de velocidade")
print("CTRL-C para sair")
print
try:
    while True:
        cmd = input("Insira o comando: ")
        cmd = cmd.lower()
        motor = cmd[0]
        direccion =cmd[1]
        velocidad =cmd[2:5]

        if motor == "a":
            if direccion == "f":
                Giro_Favor_Reloj_MotorA()
                print("motor A, CW, vel="+velocidad)
            elif direccion== "r":
                Giro_Contra_Reloj_MotorA()
                print("motor A, CCW, vel="+velocidad)
            else:
                print("comando não reconhecido")
            pwm_a.ChangeDutyCycle(int(velocidad))
            print

        elif motor == "b":
            if direccion == "f":
                Giro_Favor_Reloj_MotorB()
                print("motor B, CW, vel="+velocidad)
            elif direccion == "r":
                Giro_Contra_Reloj_MotorB()
            else:
                print("comando não reconhecido")
            pwm_b.ChangeDutyCycle(int(velocidad))
            print
        else:
            print
            print("comando não reconhecido")
            print
except KeyboardInterrupt:
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
    os.system('clear')
    print
    print("Programa finalizado pelo usuário")
    print
    exit()
