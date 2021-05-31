import re
import cv2
import util as ut
import numpy as np
import tf_func as tff
import RPi.GPIO as GPIO
import tflite_runtime.interpreter as tflite

from PIL import Image
from time import sleep

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(18, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

pin18 = GPIO.PWM(18, 100)   
pin19 = GPIO.PWM(19, 100) 

val=100     #VELOCIDADE DO MOTOR
pin18.start(val)              
pin19.start(val)

def track_person(result, labels):
    
    global x_deviation, y_max, tolerance
    
    if result == []:
        ut.red_light('OFF')
        ut.stop()
        
    else:
        for obj in result:
            _id = obj['_id']
            
            if _id == 0:
                pos = obj['pos']           
            
                x1 = int(pos[1] * CAMERA_WIDTH)
                x2 = int(pos[3] * CAMERA_WIDTH)
                y1 = int(pos[0] * CAMERA_HEIGHT)
                y2 = int(pos[2] * CAMERA_HEIGHT)
                
               
                Xm = int((x1+x2)/2)
                Ym = int((y1+y2)/2)      
                mid = (Xm, Ym)
                
                x_tolerance1 = 240
                x_tolerance2 = 400
                y_max = (CAMERA_HEIGHT - 80)
                
                if y2 < y_max:
                    ut.forward()
                    
                    if Xm < x_tolerance1:
                        deviation = Xm
                        delay = get_delay(deviation)
                        print(delay)
                        
                        ut.left()
                        sleep(delay)
                        ut.stop()
                    
                    elif Xm > x_tolerance2:
                        deviation = Xm - x_tolerance2
                        delay = get_delay(deviation)
                        print(delay)
                        
                        ut.right()
                        sleep(delay)
                        ut.stop()
                    
                    ut.red_light('ON')
                
                else: 
                    ut.red_light('OFF')
                    ut.stop()

                    
            else:
                ut.red_light('OFF')
                ut.stop()
            
def get_delay(deviation):
    deviation = abs(deviation)
    
    if(deviation>=180):
        d=0.080
    elif(deviation>=120 and deviation<180):
        d=0.060
    elif(deviation>=60 and deviation<120):
        d=0.050
    else:
        d=0.040
    
    return d

def display_result(result, frame, labels):
    font = cv2.FONT_HERSHEY_SIMPLEX
    size = 0.6
    color = (0, 0, 255)  
    thickness = 1
    medium = 2
    radius = 5
    line = -1

    for obj in result:
        _id = obj['_id']
        if _id == 0:
            pos = obj['pos']           
            
            x1 = int(pos[1] * CAMERA_WIDTH)
            x2 = int(pos[3] * CAMERA_WIDTH)
            y1 = int(pos[0] * CAMERA_HEIGHT)
            y2 = int(pos[2] * CAMERA_HEIGHT)
            
            Xm = int((x1+x2)/2)
            Ym = int((y1+y2)/2)      
            mid = (Xm, Ym)

            cv2.circle(frame, mid, radius, color, line)               
            cv2.putText(frame, 'person', (x1, y1), font, size, color, thickness)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, medium)

    cv2.imshow('Object Detection', frame)
    
if __name__ == "__main__":
    ut.init_gpio()

    model_path = '/home/pi/IFMA_projeto/human_follower_try/TFlite_models/detect.tflite'
    label_path = '/home/pi/IFMA_projeto/human_follower_try/TFlite_models/labelmap.txt'
    
    cap = cv2.VideoCapture(0)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, 15)

    interpreter = tff.load_model(model_path)
    labels = tff.load_labels(label_path)

    input_details = interpreter.get_input_details()

    input_shape = input_details[0]['shape']
    height = input_shape[1]
    width = input_shape[2]

    input_index = input_details[0]['index']

    while True:
        ret, frame = cap.read()

        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image = image.resize((width, height))

        top_result = tff.process_image(interpreter, image, input_index)
        track_person(top_result, labels)
        display_result(top_result, frame, labels)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            ut.stop()
            pin18.stop()
            pin19.stop()
            GPIO.cleanup()
            break

    cap.release()
    cv2.destroyAllWindows()