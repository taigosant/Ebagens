import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv
import math


def __ninePartitions(image):
    linhas = len(image)
    colunas = len(image[0])
    xPart = np.linspace(0, linhas, num=4, dtype=int)
    yPart = np.linspace(0, colunas, num=4, dtype=int)
    return xPart, yPart


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


def histogramLocal(image):
    partitions = 9

    histsR = []
    histsG = []
    histsB = []

    xPart, yPart = __ninePartitions(image)

    # print(xPart, yPart)
    # print(xPart)

    for i in range(len(xPart) - 1):
        for j in range(len(yPart) - 1):
            left = xPart[i]
            right = xPart[i + 1]
            up = yPart[j]
            down = yPart[j + 1]

            # print(left, right)
            # print(up, down)
            # print()

            histR = np.zeros(256)
            histG = np.zeros(256)
            histB = np.zeros(256)

            for k in range(left, right):
                for l in range(up, down):
                    blue = image[k][l][0]
                    green = image[k][l][1]
                    red = image[k][l][2]
                    histR[red] += 1
                    histG[green] += 1
                    histB[blue] += 1

            histsR.append(histR)
            histsG.append(histG)
            histsB.append(histB)

    return (histsR, histsG, histsB)



def _reduceColor(pixel): # funcao responsavel por mapear uma cor do padrao rgb (255) para um padrao com 64 cores
    if pixel < 64:
        return 0
    elif 64 <= pixel < 128:
        return 64
    elif 128 <= pixel < 192:
        return 128
    else:
        return 255


def colorQuantization(image): # atribui a reducao de cor para cada pixel de uma imagem
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


def colorQuantizationGrey(image): # atribui a reducao de cor para cada pixel de uma imagem
    linhas = len(image)
    colunas = len(image[0])
    for i in range(linhas):
        for j in range(colunas):
            pixel = image[i][j]
            image[i][j] = _reduceColor(pixel)
    return image

def transfRadioMediaRGB(image): # filtro da media para rgb
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


def generateRuidSalt(image, value):  # gerador de imagens com ruido tipo sal
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


def generateRuidPepper(image, value):  # gerador de imagens com ruido tipo pimenta
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


def transfRadioMediaGrey(image):  # filtro da media para imagens em tons de cinza
    for i in range(1, len(image) - 1):
        for j in range(1, len(image[0]) - 1):
            sum = 0
            for k in range(i - 1, i + 2):
                for l in range(j - 1, j + 2):
                    pixel = image[k][l]
                    sum += pixel
            image[i][j] = int(sum / 9)

    return image


def transfRadioMedianaGrey(image): # filtro da mediana para imagens em tons de cinza
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


def transfRadioBW(image): # transformada radiometrica fatiamento: duas fatias: preto e branco
    for i in range(0, len(image)):
        for j in range(0, len(image[0])):
            pixel = image[i][j]
            if pixel > 63:
                image[i][j] = 255
            else:
                image[i][j] = 0
    return image


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



if __name__ == '__main__':
    img = cv.imread('edleno_hexa.jpg')
    greyImga = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cv.imshow('press any key to close 1111', greyImga)
    cv.waitKey(0)
    cv.destroyAllWindows()

    greyImga = colorQuantizationGrey(greyImga)

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
    # print(greyImga)


    # neoImage = generateRuidPepper(greyImga, 0.2) # gerando ruido

    # cv.imshow('press any key to close 2222', neoImage)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    # aplicando filtro  em iteracoes

    # for i in range(5):
    #     neoImage2 = transfRadioBW(neoImage)
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
    #
    # neoImage = histogramEqualization(greyImga, GreyHist)
    #
    # GreyHist, listFreq = histogramGrey(neoImage, cordenadas)
    # print(GreyHist, listFreq)
    # plt.hist(listFreq, bins=256, facecolor='b')
    # plt.show()

    # cv.imshow('press any key to close 2222', neoImage)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    # histsR, histsG, histsB = histogramLocal(img)



    # print(histsR, histsG, histsB)

    # with open("histLocalRed.txt", 'w') as file:
    #     file.write(str(histsR))

    # with open("histLocalGreen.txt", 'w') as file:
    #     file.write(str(histsG))

    # with open("histLocalBlue.txt", 'w') as file:
    #     file.write(str(histsB))


    # for freq in histsR:
    #     frequencies = freq
    #     labels = range(256)
    #     pos = np.arange(256)
    #     width = 1.0  # gives histogram aspect to the bar diagram
    #
    #     ax = plt.axes()
    #     ax.set_xticks(pos)
    #     ax.set_xticklabels(labels)
    #
    #     plt.bar(pos, frequencies, width, color='r')
    #     plt.show()

