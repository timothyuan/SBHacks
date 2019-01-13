# following https://www.superdatascience.com/opencv-face-detection/
# import opencv
import cv2
import time
import numpy as np
import requests
# import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import dlib

#convert between BGR (used by opencv?) and RGB (used by matplotlib)

def xywh_to_dlibrect(xywh):
    x,y,w,h = xywh
    return dlib.rectangle(x,y,x+w,y+h)

def dlibrect_to_xywh(d):
    return (d.left(), d.top(), d.width(), d.height())


def convertToRGB(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def extract_face(f_cascade, colored_img, scaleFactor=1.1):
    # make copy of given image so it isnt modified
    img_copy = colored_img.copy()
    # convert to grayscale
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    # find faces
    faces = f_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5, minSize=(100,100))
    # do stuff with faces
    #for (x,y,w,h) in faces:
    #    cv2.rectangle(img_copy, (x,y), (x+w,y+h), (0,255,0), 2)
    # print(faces);
    # assume one face
    if (len(faces) == 0):
        #print("No face found")
        return None
    return faces[0]

pose_predictor_68_point = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')

pose_predictor_5_point = dlib.shape_predictor('data/shape_predictor_5_face_landmarks.dat')

face_encoder = dlib.face_recognition_model_v1('data/dlib_face_recognition_resnet_model_v1.dat')

def get_face_landmarks(img, loc):
    return pose_predictor_5_point(img,xywh_to_dlibrect(loc))

def get_face_encoding(img, loc):
    # img: image
    # loc: bounding box for face
    face_landmarks = get_face_landmarks(img,loc)

    enc10 = np.array(face_encoder.compute_face_descriptor(img, face_landmarks, 10))
    #print(np.linalg.norm(enc10-np.array(face_encoder.compute_face_descriptor(img, face_landmarks, 1))))
    return enc10

test3 = cv2.imread('lucas.jpg')
test2 = cv2.imread('navid.jpg')
test1 = cv2.imread('jacob.jpg')
test4 = cv2.imread('zucc.jpg')
test5 = cv2.imread('zucc2.jpg')
test6 = cv2.imread('jacob2.jpg')
test7 = cv2.imread('human04.jpg')
names = ["jacob", "navid", "lucas", "mark", 'timothy']
test = [test1, test2, test3, test4, test6]

haar_face_cascade = cv2.CascadeClassifier('dat/haarcascade_frontalface_alt.xml')
lbp_face_cascade = cv2.CascadeClassifier('dat/lbpcascade_frontalface.xml')

ex1 = extract_face(lbp_face_cascade, test1)
enc1 = get_face_encoding(test1,ex1 )
enc2 = get_face_encoding(test2, extract_face(lbp_face_cascade, test2))
enc3 = get_face_encoding(test3, extract_face(lbp_face_cascade, test3))
enc4 = get_face_encoding(test4, extract_face(lbp_face_cascade, test4))
enc5 = get_face_encoding(test5, extract_face(lbp_face_cascade, test5))
enc6 = get_face_encoding(test6, extract_face(lbp_face_cascade, test6))
enc7 = get_face_encoding(test7, extract_face(lbp_face_cascade, test7))
enc = [enc1, enc2, enc3, enc4, enc6]

rect = patches.Rectangle(ex1[0:2],ex1[2],ex1[3],linewidth=1,edgecolor='r',facecolor='none')

fig,ax = plt.subplots(1)

#print('jacob-navid: ',np.linalg.norm(enc1-enc2))
#print('lucas-navid: ',np.linalg.norm(enc2-enc3))
#print('jacob-lucas: ',np.linalg.norm(enc1-enc3))
#print('zucc-tim: ',np.linalg.norm(enc4-enc6))

ax.imshow(test1, cmap='gray')
ax.add_patch(rect)
#plt.show()

cap = cv2.VideoCapture(0)

finalframe = None
finalfacerect = None;
parity = True
facerect = (0,0,0,0)
start = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        start = time.time()
        finalframe = frame
        finalfacerect = facerect
        break
    else:
        cv2.putText(frame, "Press Q to Take Picture", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255))
    facerect = extract_face(lbp_face_cascade, frame)

    if facerect is None:
        cv2.imshow('vid', frame)
        # print(frame)
        parity = not parity
        continue

    x,y,w,h = facerect

    cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),2)

    cv2.imshow('vid', frame)

    parity = not parity
cv2.imshow('final image', finalframe)
finalenc = get_face_encoding(finalframe, finalfacerect)
minNorm = 0.45
minIndex = -1;
for i in range(5):
    print(names[i] + '-image: ',np.linalg.norm(enc[i]-finalenc))
    if np.linalg.norm(enc[i]-finalenc) < minNorm:
        minNorm = np.linalg.norm(enc[i]-finalenc)
        minIndex = i
if minIndex == -1: print("No match")
else: print("Match: ", names[minIndex])

url = 'http://35.235.88.148:3000/check'
files = {'file': finalenc}
r = requests.post(url, files = files)
data = r.json()['isAllowed']
print(data)
