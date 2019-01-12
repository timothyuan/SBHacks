import os
from PIL import Image #pip install Pillow
import numpy as np
import cv2 # pip install opencv-python
#also need pip install opencv-contrib-python
import pickle

face_cascade = cv2.CascadeClassifier('C:/Users/Toby/Desktop/whatiscs/cascades/data/haarcascade_frontalface_alt.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
y_labels = []
x_train = []

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "trainingfaces")

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg") or file.endswith("JPG"):
            path = os.path.join(root, file) #finds path of all images
            label = os.path.basename(root)
            #print(label, path)
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
                
            id_ = label_ids[label]
            #print(label_ids)
            pil_image = Image.open(path).convert("L") #converts image to grayscale
            image_array = np.array(pil_image, "uint8") #convert image to numpy array for training
            #print(image_array)
            faces = face_cascade.detectMultiScale(image_array, scaleFactor = 1.5, minNeighbors = 5)

            for (x,y,w,h) in faces:
                roi = image_array[y:y+h, x:x+h]
                x_train.append(roi)
                y_labels.append(id_)

print(y_labels)
print(x_train)

with open("labels.pickle", 'wb') as f:
    pickle.dump(label_ids, f)

recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainer.yml")
