import re
import numpy as np
import tflite_runtime.interpreter as tflite


def load_labels(label_path):
    with open(label_path) as f:
        labels = {}
        for line in f.readlines():
            m = re.match(r"(\d+)\s+(\w+)", line.strip())
            labels[int(m.group(1))] = m.group(2)
        return labels

def output_tensor(interpreter, i):
    output_details = interpreter.get_output_details()[i]
    output_data = np.squeeze(interpreter.tensor(output_details['index'])())
    if 'quantization' not in output_details:
        return output_data
    scale, zero_point = output_details['quantization']
    if scale == 0:
        return output_data - zero_point
    return scale * (output_data - zero_point)

def get_output(interpreter, score_threshold, top_k, image_scale=1.0):
    boxes = output_tensor(interpreter, 0)
    class_ids = output_tensor(interpreter, 1)
    scores = output_tensor(interpreter, 2)
    
    def make(i):
        ymin, xmin, ymax, xmax = boxes[i]
        return Object(
            id=int(class_ids[i]),
            score=scores[i],
            bbox=BBox(xmin=np.maximum(0.0, xmin),
                      ymin=np.maximum(0.0, ymin),
                      xmax=np.minimum(1.0, xmax),
                      ymax=np.minimum(1.0, ymax)))

    return [make(i) for i in range(top_k) if scores[i] >= score_threshold]

def load_model(model_path):
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

def process_image(interpreter, image, input_index):
    input_data = np.expand_dims(image, axis=0)  

    interpreter.set_tensor(input_index, input_data)
    interpreter.invoke()

    output_details = interpreter.get_output_details()
    # output_details[0] - position
    # output_details[1] - class id
    # output_details[2] - score
    # output_details[3] - count


    positions = np.squeeze(interpreter.get_tensor(output_details[0]['index']))
    classes = np.squeeze(interpreter.get_tensor(output_details[1]['index']))
    scores = np.squeeze(interpreter.get_tensor(output_details[2]['index']))
       
    result = []

    for idx, score in enumerate(scores):
        if score > 0.6:
            result.append({'pos': positions[idx], '_id': classes[idx]})
    return result