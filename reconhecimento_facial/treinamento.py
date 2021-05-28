import cv2
import os
import numpy as np
from PIL import Image  

LBPHFace = cv2.face.LBPHFaceRecognizer_create()
EigenFace = cv2.face.EigenFaceRecognizer_create()
FisherFace = cv2.face.FisherFaceRecognizer_create()




def getImagemComId():
    caminhos = [os.path.join('/home/pi/projeto/fotos', f) for f in os.listdir('/home/pi/projeto/fotos')]
    #print(caminhos)
    FaceList = []
    IDs = []
    
    for caminhoImagem in caminhos:
        imagemLida = cv2.cvtColor(cv2.imread(caminhoImagem), cv2.COLOR_BGR2GRAY)
        id = int(os.path.split(caminhoImagem)[-1].split('.')[2])
        #print(caminhoImagem)
        IDs.append(id)
        FaceList.append(imagemLida)
        #print(caminhoImagem)
        #cv2.imshow("face", imagemLida)
        #cv2.waitKey(500)
    return np.array(IDs), FaceList

    
IDs, FaceList = getImagemComId()
#print(ids)


print('TRAINING......')
EigenFace.train(FaceList, IDs)                          # The recongniser is trained using the images
print('EIGEN FACE RECOGNISER COMPLETE...')
EigenFace.save('/home/pi/projeto/reconhecedores/trainingDataEigan_v2.xml')
print('FILE SAVED..')
FisherFace.train(FaceList, IDs)
print('FISHER FACE RECOGNISER COMPLETE...')
FisherFace.save('/home/pi/projeto/reconhecedores/trainingDataFisher_v2.xml')
print('Fisher Face XML saved... ')
LBPHFace.train(FaceList, IDs)
print('LBPH FACE RECOGNISER COMPLETE...')
LBPHFace.save('/home/pi/projeto/reconhecedores/trainingDataLBPH_v2.xml')
print ('ALL XML FILES SAVED...')

print("treinamento realizado")

