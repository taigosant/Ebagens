import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv


def _reduceColor(pixel):
    if pixel < 64:
        return 0
    elif 64 <= pixel < 128:
        return 64
    elif 128 <= pixel < 192:
        return 128
    else:
        return 255


def colorQuantization(image):
    linhas = len(image)
    colunas = len(image[0])
    for i in range(linhas):
        for j in range(colunas):
            red = image[i][j][2]
            green = image[i][j][1]
            blue = image[i][j][0]
            image[i][j][0] = _reduceColor(blue)
            image[i][j][1] = _reduceColor(green)
            image[i][j][2] = _reduceColor(red)
    return image


def transfRadioMediaRGB(image):
    for i in range(1, len(image) - 1):
        for j in range(1, len(image[0]) - 1):
            convR = 0
            convG = 0
            convB = 0
            for k in range(i - 1, i + 1):
                for l in range(j - 1, j + 1):
                    red = image[k][l][2]
                    green = image[k][l][1]
                    blue = image[k][l][0]
                    print(red,green,blue)
                    convR += red
                    convG += green
                    convB += blue
            print(convB / 9, convG / 9, convR / 9)
            image[i][j][0] = int(convB / 9)
            image[i][j][1] = int(convG / 9)
            image[i][j][2] = int(convR / 9)

    return image

def generateRuidSalt(image, value):
    colunas = len(image[0])
    percent = int(colunas * value)
    tamImg = len(image) * len(image[0])
    quantiRuid = len(image) * len(image[0]) * value
    print(tamImg, quantiRuid)
    for i in range(0, len(image)):
        randomPositions= np.random.randint(colunas, size=percent)
        for pos in randomPositions:
            image[i][pos] = 255
    return image

def generateRuidPepper(image, value):
    colunas = len(image[0])
    percent = int(colunas * value)
    tamImg = len(image) * len(image[0])
    quantiRuid = len(image) * len(image[0]) * value
    print(tamImg, quantiRuid)
    for i in range(0, len(image)):
        randomPositions= np.random.randint(colunas, size=percent)
        for pos in randomPositions:
            image[i][pos] = 0
    return image

def transfRadioMediaGrey(image):
    for i in range(1, len(image) - 1):
        for j in range(1, len(image[0]) - 1):
            sum = 0
            for k in range(i - 1, i + 2):
                for l in range(j - 1, j + 2):
                    pixel = image[k][l]
                    sum += pixel
            image[i][j] = int(sum / 9)

    return image

def transfRadioMedianaGrey(image):
    for i in range(1, len(image) - 1):
        for j in range(1, len(image[0]) - 1):
            pixels = []
            for k in range(i - 1, i + 2):
                for l in range(j - 1, j + 2):
                    pixel = image[k][l]
                    pixels.append(pixel)
            pixels = sorted(pixels)
            print(pixels)
            mediana = int(len(pixels)/2)
            print(mediana, pixels[mediana])
            image[i][j] = pixels[mediana]

    return image


def transfRadioBW(image):
    for i in range(0, len(image)):
        for j in range(0, len(image[0])):
            pixel = image[i][j]
            if pixel > 63:
                image[i][j] = 255
            else:
                image[i][j] = 0
    return image


def histogram(image, cord):
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


def histogramGrey(image, cord):
    histG = np.zeros(256)
    gHist = []  # para plotar
    for i in range(cord['iInit'], cord['iEnd']):
        for j in range(cord['jInit'], cord['jEnd']):
            pixel = image[i][j]
            gHist.append(pixel)
            histG[pixel] += 1

    return histG, gHist


def __ninePartitions(image):
    linhas = len(image)
    colunas = len(image[0])
    xPart = np.linspace(0, linhas, num=4)
    yPart = np.linspace(0, colunas, num=4)
    print(xPart, yPart)
#
# def localHistogram(image, xPartitions, yPartitions):
#     xPartitions = [int(x) for x in xPartitions]
#     yPartitions = [int(y) for y in yPartitions]
#
#     for initX, endX in xPartitions:
#         for initJ, endJ in yPartitions:
#             for()


if __name__ == '__main__':
    img = cv.imread('edleno_hexa.jpg')
    # greyImga = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # cv.imshow('press any key to close 1111', greyImga)
    cv.imshow('press any key to close 1111', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # print(greyImga)
    #
    # neoImage = generateRuidPepper(greyImga, 0.2) # gerando ruido

    # cv.imshow('press any key to close 2222', neoImage)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    # aplicando filtro  em iteracoes

    # for i in range(5):
    #     neoImage2 = transfRadioMedianaGrey(neoImage)
    #     cv.imshow('press any key to close 3333', neoImage2)
    #     cv.waitKey(0)
    #     cv.destroyAllWindows()
    #     neoImage = neoImage2
    #     cv.imwrite('result' + str(i) + '.jpg', neoImage2)

    # coordenadas para o histograma
    cordenadas = {
        'iInit': 0,
        'iEnd': len(img),
        'jInit': 0,
        'jEnd': len(img[0])
    }
    # __ninePartitions(img)

    # histogramas globais para cada canal de cor
    # R, G, B, rHist, gHist, bHist = histogram(img, cordenadas)
    # plt.hist(rHist, bins=256, facecolor='r')
    # plt.show()
    # plt.hist(gHist, bins=256, facecolor='g')
    # plt.show()
    # plt.hist(bHist, bins=256, facecolor='b')
    # plt.show()

    # histograma de imagem em tons de cinza
    # GreyHist, listFreq = histogramGrey(greyImga, cordenadas)
    # print(GreyHist, listFreq)
    # plt.hist(listFreq, bins=256, facecolor='g')
    # plt.show()

    neoImage = colorQuantization(img)
    cv.imshow('press any key to close 2222', neoImage)
    cv.waitKey(0)
    cv.destroyAllWindows()
