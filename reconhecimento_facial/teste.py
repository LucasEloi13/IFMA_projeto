import cv2
import RPi.GPIO as GPIO


classificador_faces = cv2.CascadeClassifier('/home/pi/projeto/cascades/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture('https://192.168.0.9:8080/video')


led = 24
led2 = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)



while True:
    
    conectado, frame = cap.read()
    
    frameCinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    facesDetectadas = classificador_faces.detectMultiScale(frameCinza, minNeighbors=9, minSize=(50,50))
    
    for(x, y, l, a) in facesDetectadas:
        cv2.rectangle(frame, (x, y), (x + l, y + a), (0,0,255), 2)
        
        print(facesDetectadas)
        
        if facesDetectadas != 0:
            
            GPIO.output(led, GPIO.HIGH)
        
        
    
    cv2.imshow("capturing", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWidows()