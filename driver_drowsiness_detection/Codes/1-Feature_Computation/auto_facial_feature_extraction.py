import argparse
import os
import re
import numpy as np
import math
import csv
import glob
import tensorflow as tf
import h5py as h5py
from keras.preprocessing import image
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.models import Model, load_model

import imageio
import matplotlib.pyplot as plt
from mlxtend.image import extract_face_landmarks
from scipy.spatial import distance
import cv2


def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


def mouth_aspect_ratio(mouth):
    A = distance.euclidean(mouth[14], mouth[18])
    C = distance.euclidean(mouth[12], mouth[16])
    mar = (A) / (C)
    return mar


def circularity(eye):
    A = distance.euclidean(eye[1], eye[4])
    radius = A/2.0
    Area = math.pi * (radius ** 2)
    p = 0
    p += distance.euclidean(eye[0], eye[1])
    p += distance.euclidean(eye[1], eye[2])
    p += distance.euclidean(eye[2], eye[3])
    p += distance.euclidean(eye[3], eye[4])
    p += distance.euclidean(eye[4], eye[5])
    p += distance.euclidean(eye[5], eye[0])
    return 4 * math.pi * Area / (p**2)


def mouth_over_eye(eye):
    ear = eye_aspect_ratio(eye)
    mar = mouth_aspect_ratio(eye)
    mouth_eye = mar/ear
    return mouth_eye


def getFrame(vidcap, sec):
    start = 1800
    vidcap.set(cv2.CAP_PROP_POS_MSEC, start + sec*1000)
    hasFrames, image = vidcap.read()
    return hasFrames, image


def facial_feature_extraction(output_file_name, input_video):
    data = []
    labels = []

    for j in [60]:
        for i in [0]:
            vidcap = cv2.VideoCapture(input_video)
            sec = 0
            frameRate = 1
            success, image = getFrame(vidcap, sec)
            count = 0
            print(success)
            print(image)
            while success and count < 240:
                landmarks = extract_face_landmarks(image)
                if sum(sum(landmarks)) != 0:
                    count += 1
                    data.append(landmarks)
                    labels.append([i])
                    sec = sec + frameRate
                    sec = round(sec, 2)
                    success, image = getFrame(vidcap, sec)
                    print(count)
                else:
                    sec = sec + frameRate
                    sec = round(sec, 2)
                    success, image = getFrame(vidcap, sec)
                    print("not detected")

    data = np.array(data)
    labels = np.array(labels)

    features = []
    for d in data:
        eye = d[36:68]
        ear = eye_aspect_ratio(eye)
        mar = mouth_aspect_ratio(eye)
        cir = circularity(eye)
        mouth_eye = mouth_over_eye(eye)
        features.append([ear, mar, cir, mouth_eye])

    features = np.array(features)

    print(data.shape)
    print(labels.shape)
    print(features.shape)

    # saving landmarks of each frame
    np.save(open(f'{output_file_name}_Data.npy', 'wb'), data)

    # saving the features in .npy file and creating CSV file for that
    np.save(open(f'{output_file_name}_Features.npy', 'wb'), features)
    np.savetxt(f'{output_file_name}_Features.csv', features, delimiter=",")

    # saving the labels in .npy file and creating CSV file for that
    np.save(open(f'{output_file_name}_Labels.npy', 'wb'), labels)
    np.savetxt(f'{output_file_name}_Labels.csv', labels, delimiter=",")


def main(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if(file.endswith(".mp4") or file.endswith(".mov") or file.endswith(".MOV")):
                output_name = ''
                print(f"root: {root}, dirs {dirs}, file {file}")
                if bool(re.search(r"^0.[mov|MOV|mp4]", file)):
                    output_name = 'alert_object'
                elif bool(re.search(r"^10.[mov|MOV|mp4]", file)):
                    output_name = 'sleepy_object'
                else:
                    print("Would not care low vigrillant for now")
                    continue
                facial_feature_extraction(os.path.join(
                    root, output_name), os.path.join(root, file))


def arg_parse():
    parser = argparse.ArgumentParser(description='Blinks detector auto script')
    parser.add_argument('--data_dir', '-d', type=str, required=True,
                        help='Path to data dir')

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = arg_parse()
    main(args.data_dir)
