import cv2
import numpy as np

classificador_faces = cv2.CascadeClassifier('/home/pi/projeto/cascades/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture('https://192.168.0.9:8080/video')
amostra = 1
numeroAmostras = 25
id = input('Digite seu nome: ')
largura, altura = 220, 200
print('Capturando as faces...')

 
while True:
    
    conectado, frame = cap.read()
    
    frameCinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    facesDetectadas = classificador_faces.detectMultiScale(frameCinza, minNeighbors=9, minSize=(50,50))
    
    for(x, y, l, a) in facesDetectadas:
        cv2.rectangle(frame, (x, y), (x + l, y + a), (0,0,255), 2)
    
    cv2.imshow("capturing", frame) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        imagemFace = cv2.resize(frameCinza[y:y + a, x:x + l], (largura, altura))
        cv2.imwrite("/home/pi/projeto/fotos/pessoa." + str(id) + "." + str(amostra) + ".jpg", imagemFace)
        print("[foto" + str(amostra) + "capturada com  sucesso]")
        amostra += 1
              
    if (amostra >= numeroAmostras + 1):
        break
              
print("fotos tiradas com sucesso")              
cap.release()
cv2.destroyAllWidows()