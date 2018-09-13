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


def histogramEqualization(image, histograma):
    linhas = len(image)
    colunas = len(image[0])
    tamImg = linhas * colunas
    nColors = len(histograma)
    probabilities = np.zeros(nColors)
    cumulativeProbs = np.zeros(nColors)

    for i in range(len(histograma)):
        probabilities[i] = histograma[i] / tamImg

    cumulativeProbs[0] = probabilities[0]

    for i in range(1, len(probabilities)):
        cumulativeProbs[i] = cumulativeProbs[i-1] + probabilities[i]

    for i in range(linhas):
        for j in range(colunas):
            currentColor = image[i][j]
            neoColor = int((nColors - 1) * cumulativeProbs[currentColor])
            image[i][j] = neoColor

    return image


def transfRadioBW(image): # transformada radiometrica fatiamento: duas fatias: preto e branco
    for i in range(0, len(image)):
        for j in range(0, len(image[0])):
            pixel = image[i][j]
            if pixel > 127:
                image[i][j] = 255
            else:
                image[i][j] = 0
    return image


if __name__ == '__main__':
    cordenadas = {
        'iInit': 0,
        'iEnd': len(img),
        'jInit': 0,
        'jEnd': len(img[0])
    }

    #fatiamento
    # neoImage = transfRadioBW(greyImga)
    # cv.imshow('press any key to close 2222', neoImage)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    # histograma de imagem em tons de cinza
    GreyHist, listFreq = histogramGrey(greyImga, cordenadas)
    print(GreyHist, listFreq)
    plt.hist(listFreq, bins=256, facecolor='g')
    plt.show()

    neoImage = histogramEqualization(greyImga, GreyHist)

    GreyHist, listFreq = histogramGrey(neoImage, cordenadas)
    print(GreyHist, listFreq)
    plt.hist(listFreq, bins=256, facecolor='b')
    plt.show()

    cv.imshow('press any key to close 2222', neoImage)
    cv.waitKey(0)
    cv.destroyAllWindows()