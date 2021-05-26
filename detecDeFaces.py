import cv2

classificador = cv2.CascadeClassifier('/home/pi/projeto/cascades/haarcascade_frontalface_default.xml')

imagem = cv2.imread('/home/pi/projeto/pessoas/IMG-20171223-WA0037-1.jpg')

imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

facesDetectadas = classificador.detectMultiScale(imagemCinza, scaleFactor=1.2, minNeighbors=11)

print(len(facesDetectadas))

for(x, y, l, a) in facesDetectadas:
    print(x, y, l, a)
    cv2.rectangle(imagem, (x, y), (x + l, y + a), (0,0,255), 2)

cv2.imshow("Faces econtradas", imagem)

cv2.waitKey()