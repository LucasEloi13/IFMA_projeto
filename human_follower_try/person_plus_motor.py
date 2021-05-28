#--------------------libs----------------------------
import cv2
import numpy as np
from pynput import keyboard
import RPi.GPIO as GPIO
import imutils
import util as ut
import os, time
#----------------------------------------------------

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


KILL = False

def on_press(key):
    if key.char == 'q':
        global KILL
        KILL = True

def main():
    ut.init_gpio()
    
    #Inicialização da Rede Neural utilizando um modelo pré treinado [ALTERAR DIRETÓRIO, CASO NECESSÁRIO]
    net = cv2.dnn.readNetFromCaffe('/home/pi/IFMA_projeto/Pre-traineds SSD/MobileNetSSD_deploy.prototxt.txt', '/home/pi/IFMA_projeto/Pre-traineds SSD/MobileNetSSD_deploy.caffemodel')    
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor"]
    
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    (h, w) = frame.shape[:2]
    
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G') 
    out = cv2.VideoWriter('webcam_tracker.avi',fourcc, 20.0, (w,h))
    
    while True:
        ret, frame = cap.read()
        frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)        
    
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
            0.007843, (300, 300), 127.5)
         
        net.setInput(blob)
        detections = net.forward()
        
        for i in np.arange(0, detections.shape[2]):
            object_type = detections[0,0,i,1]
            confidence = detections[0, 0, i, 2]
            if object_type == 15 and confidence > 0.2: 
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                label = "{}: {:.2f}%".format('person',confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[int(object_type)], 2)
                                                
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[int(object_type)], 2)

                Xi, Yi = startX, startY
                Xf, Yf = endX, endY
                
                Xm = int((Xi+Xf)/2)
                Ym = int((Yi+Yf)/2)      
                ponto_medio = (Xm, Ym)
                cor = (0,0,255)
                raio = 5
                espessura_linha = -1
                cv2.circle(frame, ponto_medio, raio, cor, espessura_linha)        
                
            if int(object_type) == 15:
                ut.forward()
                
                if Xm < 240:
                    ut.left()
                elif Xm > 400:
                    ut.right()
                    
            else:
                ut.stop()
                 
        out.write(frame)
        cv2.imshow('Webcam Tracking', frame)

        if KILL:  #PRESSIONE 'q' PARA FINALIZAR O SCRIPT
            ut.stop()
            pin18.stop()
            pin19.stop()
            GPIO.cleanup()
            os.system('clear')
            print("\nFinished")
            out.release()
            cv2.destroyAllWindows()
            exit()
        cv2.waitKey(1)

if __name__ == '__main__':
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    main()
    exit()                
                