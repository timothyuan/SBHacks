#! /usr/bin/python

import PIL.Image

import dlib

import numpy as np

import sys

# rectangle format conversions

SHAPE_PREDICTOR_DATA_LOC = 'data/shape_predictor_5_face_landmarks.dat'
FACE_REC_DATA_LOC = 'data/dlib_face_recognition_resnet_model_v1.dat'

def xywh_to_dlibrect(xywh):
    x,y,w,h = xywh
    return dlib.rectangle(x,y,x+w,y+h)

def dlibrect_to_xywh(d):
    return (d.left(), d.top(), d.width(), d.height())

dlib_face_detector = dlib.get_frontal_face_detector()
pose_predictor_5_point = dlib.shape_predictor(SHAPE_PREDICTOR_DATA_LOC)
face_encoder = dlib.face_recognition_model_v1(FACE_REC_DATA_LOC)

def dlib_extract_face(img):
    det = dlib_face_detector(img, 1)
    if len(det) == 0:
        return False, None
    return True, dlibrect_to_xywh(det[0])

def get_face_landmarks(img, loc):
    return pose_predictor_5_point(img,xywh_to_dlibrect(loc))

def get_face_encoding(img, loc):
    # img: image
    # loc: bounding box for face
    face_landmarks = get_face_landmarks(img,loc)

    # using jitter 10 for robustness
    enc10 = np.array(face_encoder.compute_face_descriptor(img, face_landmarks, 10))
    return enc10

def read_img_from_file(loc):
    im = PIL.Image.open(loc)
    im.convert('RGB')
    return np.array(im)

if __name__ == "__main__":
    a = sys.argv
    if len(a) >= 2:
        for i in range(1, len(a)):
            filename = a[i]
            img = read_img_from_file(filename)
            success, loc = dlib_extract_face(img)
            if not success:
                print('No face detected')
                exit()
            enc = get_face_encoding(img, loc)
            lastdot = filename.rfind('.')
            outfilename = filename[0:lastdot] + '.dat'

            # open file in binary mode
            f = open(outfilename, 'wb')

            # this is not a string in the sense of str() but a Python bytes sequence
            s = enc.tostring()
            f.write(s)
            f.close()

            # how to read the data back out

            #g = open(outfilename, 'rb')
            #print(enc-np.fromstring(g.read(), dtype='float'))

    else:
        print('Need filename as argument')
