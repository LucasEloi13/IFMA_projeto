#----------------------libs----------------------
import cv2
import RPi.GPIO as GPIO
import util as ut
import os, time
#------------------------------------------------

#----------------GPIO_configs---------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

pin18 = GPIO.PWM(18, 100)   
pin19 = GPIO.PWM(19, 100) 

val=50     #VELOCIDADE DO MOTOR
pin18.start(val)              
pin19.start(val)
#--------------------------------------------------

#----------------CV2_configs----------------
classificador_faces = cv2.CascadeClassifier('/home/pi/IFMA_projeto/cascades/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
conectado, frame = cap.read()
#--------------------------------------------------

def main():
    ut.init_gpio()
    
    while True:
        conectado, frame = cap.read()
    
        frameCinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        facesDetectadas = classificador_faces.detectMultiScale(frameCinza, minNeighbors=9, minSize=(50,50))
    
        Xm, Ym = 0, 0
        
        for(x, y, l, a) in facesDetectadas:
            Xi, Yi = x, y                                    
            Xf, Yf = x + l,  y + a                          
            Xm = int((Xi+Xf)/2)
            Ym = int((Yi+Yf)/2)      
            ponto_medio = (Xm, Ym)
            cor = (0,0,255)
            raio = 5
            espessura_linha = -1
            cv2.circle(frame, ponto_medio, raio, cor, espessura_linha)
            
        if facesDetectadas == ():
                print('ROBOT STOPPED')
                ut.stop()
          
        else:
                print('ROBOT MOVING!')
                ut.forward()
                
                
                if Xm < 240:
                    ut.left()
                    print('LEFT')
                elif Xm > 400:
                    ut.right()
                    print('RIGHT')
                    
        cv2.imshow("capturing", frame)
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  #PRESSIONE 'q' PARA FINALIZAR O SCRIPT
            ut.stop()
            pin18.stop()
            pin19.stop()
            GPIO.cleanup()
            os.system('clear')
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()