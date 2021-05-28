import cv2

detectorFace = cv2.CascadeClassifier('/home/pi/projeto/cascades/haarcascade_frontalface_default.xml')
reconhecedor = cv2.face.FisherFaceRecognizer_create()
reconhecedor.read('/home/pi/projeto/reconhecedores/TreinamentoDataFisher2.xml')
largura, altura = 220, 200
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
camera = cv2.VideoCapture('https://192.168.0.9:8080/video')

while (True):
    conectado, imagem = camera.read()
    imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    facesDetectadas = detectorFace.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(30,30))
    
    
    for (x, y, l, a) in facesDetectadas:
        imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
        cv2.rectangle(imagem, (x, y), (x + l, y + a), (0,0,255), 2)
        id, confianca = reconhecedor.predict(imagemFace)       
        cv2.putText(imagem, str(id), (x,y + (a+30)), font, 2, (0,0,255))
    
    cv2.imshow("face", imagem)
    
    print(id)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
camera.release()
cv2.destroyAllWidows()    
