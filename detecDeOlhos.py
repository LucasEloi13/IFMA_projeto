import cv2

classificador_faces = cv2.CascadeClassifier('/home/pi/projeto/cascades/haarcascade_frontalface_default.xml')
classificador_olhos = cv2.CascadeClassifier('/home/pi/projeto/cascades/haarcascade_eye.xml')

imagem = cv2.imread('/home/pi/projeto/pessoas/beatles.jpg')
imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

facesDetectadas = classificador_faces.detectMultiScale(imagemCinza)

for(x, y, l, a) in facesDetectadas:
    imagem = cv2.rectangle(imagem, (x, y), (x + l, y + a), (0,0,255), 2)
    regiao = imagem[y:y + a, x:x + l]
    regiaoCinzaOlho = cv2.cvtColor(regiao, cv2.COLOR_BGR2GRAY)
    olhosDetectados = classificador_olhos.detectMultiScale(regiaoCinzaOlho, scaleFactor=1.1, minNeighbors=4, minSize=(1,1))
    print(olhosDetectados)
    print(facesDetectadas)
    for (ox, oy, ol, oa) in olhosDetectados:
        cv2.rectangle(regiao, (ox, oy), (ox + ol, oy + oa), (0,0,255), 2)
    

cv2.imshow("Faces e Olhos", imagem)
cv2.waitKey()