import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv
from Similaridade import *
from bic import *


def get_frames(path, window):
    cap = cv.VideoCapture(path)  # open a video
    frame_list = []

    if cap.isOpened():

        total_of_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))  #

        print(total_of_frames)

        for x in range(1, total_of_frames, window):

            cap.set(cv.CAP_PROP_POS_FRAMES, x)

            ret, frame = cap.read()

            data = {
                'frame': frame,
                'time': cap.get(cv.CAP_PROP_POS_MSEC),
            }

            frame_list.append(data)

    return frame_list



if __name__ == '__main__':
    frames = get_frames("/home/taigo/Documents/2018.2/ebagens/Ebagens/TP2/The Last Night on Xbox One - 4K Trailer.mp4", 20)
    # printing
    # print(frames)
    # print(len(frames))

    # writes each frame in a image

    # for i in range(0, len(frames)):
    #     cv.imwrite("frames/"+str(i)+".jpg", frames[i]['frame'])

    shotsFramesInterval = [0]
    shotsMSecsInterval = [0]
    limiar = 70000
    for i in range(1, len(frames)):
        previousFrame = frames[i-1]['frame']
        curFrame = frames[i]['frame']

        borderHistsPrevious, innerHistsPrevious = bic(previousFrame)
        borderHistsCur, innerHistsCur = bic(curFrame)

        borderHistRsim = Similarity.euclidean_distance(borderHistsPrevious[0], borderHistsCur[0])
        borderHistGsim = Similarity.euclidean_distance(borderHistsPrevious[1], borderHistsCur[1])
        borderHistBsim = Similarity.euclidean_distance(borderHistsPrevious[2], borderHistsCur[2])

        innerHistRsim = Similarity.euclidean_distance(innerHistsPrevious[0], innerHistsCur[0])
        innerHistGsim = Similarity.euclidean_distance(innerHistsPrevious[1], innerHistsCur[1])
        innerHistBsim = Similarity.euclidean_distance(innerHistsPrevious[2], innerHistsCur[2])

        meanHistBorder = sum([borderHistRsim, borderHistGsim, borderHistBsim]) / 3
        meanHistInner = sum([innerHistRsim, innerHistGsim, innerHistBsim]) / 3

        if meanHistBorder > limiar or meanHistInner > limiar:
            print('shot transition detected at frame', i)
            print(meanHistBorder, meanHistInner)
            shotsFramesInterval.append(i)
            shotsMSecsInterval.append(frames[i]['time'])

    print(shotsFramesInterval)
    print(shotsMSecsInterval)












