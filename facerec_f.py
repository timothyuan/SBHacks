# following https://www.superdatascience.com/opencv-face-detection/
# import opencv
import cv2
import argparse
import glob

import numpy as np
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
    if (len(faces) == 0): return None
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
    print(np.linalg.norm(enc10-np.array(face_encoder.compute_face_descriptor(img, face_landmarks, 1))))
    return enc10

names = glob.glob("dat/*.dat")
enc = []
haar_face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
lbp_face_cascade = cv2.CascadeClassifier('data/lbpcascade_frontalface.xml')
i = 0
for name in names:
    g = open(name, 'rb')
    test = np.fromstring(g.read(), dtype='float')
    #test = cv2.imread(name)
    #print(name)
    #print(test)
    #enc.append(get_face_encoding(test, extract_face(lbp_face_cascade, test)))
    enc.append(test)

    # extracting just the name
    lastdot = names[i].rfind('.')
    firstslash = names[i].find('/')
    names[i] = names[i][firstslash + 1:lastdot]
    i = i + 1

g = open("image.dat", 'rb')
test = np.fromstring(g.read(), dtype='float')
#test = cv2.imread("image.png")
#finalenc = get_face_encoding(test, extract_face(lbp_face_cascade, test))
finalenc = test
minNorm = 0.45
minIndex = -1;

for i in range(len(enc)):
    print(names[i] + '-image: ',np.linalg.norm(enc[i]-finalenc))
    if np.linalg.norm(enc[i]-finalenc) < minNorm:
        minNorm = np.linalg.norm(enc[i]-finalenc)
        minIndex = i
if minIndex == -1: print("No match")
else: print("Match: ", names[minIndex])
