import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv

img = cv.imread('aventura.jpg')
cv.imshow('press any key to close 1111', img)
cv.waitKey(0)
cv.destroyAllWindows()


def histogram(image, cord):  # histograma global rgb
    histR = np.zeros(256)
    histG = np.zeros(256)
    histB = np.zeros(256)
    rHist = []  # para plotar
    gHist = []  # para plotar
    bHist = []  # para plotar
    for i in range(cord['iInit'], cord['iEnd']):
        for j in range(cord['jInit'], cord['jEnd']):
            blue = image[i][j][0]
            green = image[i][j][1]
            red = image[i][j][2]
            rHist.append(red)
            gHist.append(green)
            bHist.append(blue)
            histR[red] += 1
            histG[green] += 1
            histB[blue] += 1

    return (histR, histG, histB, rHist, gHist, bHist)


if __name__ == '__main__':

    cordenadas = {
        'iInit': 0,
        'iEnd': len(img),
        'jInit': 0,

        'jEnd': len(img[0])
    }

    # histogramas globais para cada canal de cor
    R, G, B, rHist, gHist, bHist = histogram(img, cordenadas)
    print(R,G,B)
    plt.hist(rHist, bins=256, facecolor='r')
    plt.show()
    plt.hist(gHist, bins=256, facecolor='g')
    plt.show()
    plt.hist(bHist, bins=256, facecolor='b')
    plt.show()