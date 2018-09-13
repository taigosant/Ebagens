import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv
import math

img = cv.imread('balo.jpg')
greyImga = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('press any key to close 1111', greyImga)
cv.waitKey(0)
cv.destroyAllWindows()

def _reduceColor(pixel): # funcao responsavel por mapear uma cor do padrao rgb (255) para um padrao com 64 cores
    if pixel < 64:
        return 0
    elif 64 <= pixel < 128:
        return 64
    elif 128 <= pixel < 192:
        return 128
    else:
        return 255

def colorQuantizationGrey(image): # atribui a reducao de cor para cada pixel de uma imagem
    linhas = len(image)
    colunas = len(image[0])
    for i in range(linhas):
        for j in range(colunas):
            pixel = image[i][j]
            image[i][j] = _reduceColor(pixel)
    return image

def borderDetectionGrey(image, limiar, convX, convY):
    linhas = len(image)
    colunas = len(image[0])
    mapEdge = np.zeros((linhas, colunas))
    for i in range(1, linhas-1):
        for j in range(1, colunas-1):
            sumX = 0
            sumY = 0
            for ix in range(-1,2):
                for jy in range(-1,2):
                    posX = i + ix
                    posY = j + jy
                    sumX += convX[ix+1][jy+1] * image[posX][posY]
                    sumY += convY[ix+1][jy+1] * image[posX][posY]
            print(sumX, sumY)
            grad = math.sqrt((sumX*sumX) + (sumY*sumY))
            if grad >= limiar:
                mapEdge[i][j] = 255

    return mapEdge


if __name__ == '__main__':



    convX = [[1,1,1],
             [0,0,0],
             [-1,-1,-1]]
    convY = [[1,0,-1],
             [1,0,-1],
             [1,0,-1]]

    neoImage = borderDetectionGrey(greyImga, 100, convX, convY)
    cv.imshow('press any key to close 2222', neoImage)
    cv.waitKey(0)
    cv.destroyAllWindows()

    greyImga = colorQuantizationGrey(greyImga)

    neoImage = borderDetectionGrey(greyImga, 100, convX, convY)
    cv.imshow('press any key to close 2222', neoImage)
    cv.waitKey(0)
    cv.destroyAllWindows()