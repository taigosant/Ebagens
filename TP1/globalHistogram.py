import numpy as np
import matplotlib as plt
import cv2 as cv


def histogram(image):
    histR = np.zeros(256)
    histG = np.zeros(256)
    histB = np.zeros(256)
    for i in range(0, len(image)):
        for j in range(0, len(image[0])):
            blue = image[i][j][0]
            green = image[i][j][1]
            red = image[i][j][2]
            histR[red] += 1
            histG[green] += 1
            histB[blue] += 1

    return (histR, histG, histB)


# def localHistogram(image):
#     init = 0
#     for i in range(3):
#         for j in range(3):
#             for k in range(init, len(image[0])/ 3):
#                 for


if __name__ == '__main__':
    img = cv.imread('teste1.jpg')
    R, G , B = histogram(img)
    print(R,G,B)



