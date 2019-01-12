import numpy as np
import cv2
import pickle

face_cascade = cv2.CascadeClassifier('C:/Users/Toby/Desktop/whatiscs/cascades/data/haarcascade_frontalface_alt.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

labels = {} #Person's name : ID

with open("labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}



print(labels)
cap = cv2.VideoCapture(0)
z = 10
xs = []
while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for (x,y,w,h) in faces:
        #print(x,y,w,h)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)

        roi_gray = gray[y:y+h, x:x+h]
        
        id_, conf = recognizer.predict(roi_gray)
        if conf >=85 and conf <=100:
            print(id_, conf) #id_ is the ID of the person identified
            print(labels[id_])
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255,255,255)
            stroke = 2
            cv2.putText(frame, name, (x,y+h+10), font, 0.5, color, stroke, cv2.LINE_AA)
        
        cv2.imshow('frame', frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cap.destroyAllWindows()

