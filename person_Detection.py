
import cv2
import numpy as np
from pynput import keyboard
import imutils

KILL = False


def on_press(key):
	if key.char == 'q':
		global KILL
		KILL = True
		#print('Killing now')

def main():
	
	net = cv2.dnn.readNetFromCaffe('Projeto_IFMA_2020\Pre-traineds SSD/MobileNetSSD_deploy.prototxt.txt', 'Projeto_IFMA_2020\Pre-traineds SSD/MobileNetSSD_deploy.caffemodel')


	CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
		"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		"sofa", "train", "tvmonitor"]
	COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
	

	cap = cv2.VideoCapture(0)


	ret, frame = cap.read()
	(h, w) = frame.shape[:2]


	fourcc = cv2.VideoWriter_fourcc('M','J','P','G') #Define the codec and create VideoWriter object
	out = cv2.VideoWriter('webcam_tracker.avi',fourcc, 20.0, (w,h))

	while 1:
		
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

				# draw the prediction on the frame
				label = "{}: {:.2f}%".format('person',confidence * 100)
				cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[int(object_type)], 2)
				y = startY - 15 if startY - 15 > 15 else startY + 15
				cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[int(object_type)], 2)

			
		out.write(frame)
		cv2.imshow('Webcam Tracking', frame)

		if KILL:
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