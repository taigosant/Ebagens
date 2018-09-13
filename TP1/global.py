import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv

img = cv.imread('aventura.jpg')
greyImga = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('press any key to close 1111', greyImga)
cv.waitKey(0)
cv.destroyAllWindows()


def histogramGrey(image, cord):  # histograma global cinza
    histG = np.zeros(256)
    gHist = []  # para plotar
    for i in range(cord['iInit'], cord['iEnd']):
        for j in range(cord['jInit'], cord['jEnd']):
            pixel = image[i][j]
            gHist.append(pixel)
            histG[pixel] += 1

    return histG, gHist


if __name__ == '__main__':

    cordenadas = {
        'iInit': 0,
        'iEnd': len(img),
        'jInit': 0,
        'jEnd': len(img[0])
    }

    GreyHist, listFreq = histogramGrey(greyImga, cordenadas)
    print(GreyHist)
    plt.hist(listFreq, bins=256, facecolor='g')
    plt.show()