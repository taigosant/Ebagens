import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv

img = cv.imread('aventura.jpg')
greyImga = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('press any key to close 1111', greyImga)
cv.waitKey(0)
cv.destroyAllWindows()


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

def generateRuidPepperSalt(image, value):  # gerador de imagens com ruido tipo sal/pimenta
    colunas = len(image[0])
    percent = int(colunas * value)
    tamImg = len(image) * len(image[0])
    quantiRuid = len(image) * len(image[0]) * value
    print(tamImg, quantiRuid)
    for i in range(0, len(image)):
        randomPositions= np.random.randint(colunas, size=percent)
        for pos in randomPositions:
            if np.random.randint(0, 2, size=1)[0] == 1:
                image[i][pos] = 255
            else:
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


if __name__ == '__main__':

    cordenadas = {
        'iInit': 0,
        'iEnd': len(img),
        'jInit': 0,
        'jEnd': len(img[0])
    }

    neoImage = generateRuidPepperSalt(greyImga, 0.2) # gerando ruido

    cv.imshow('press any key to close 2222', neoImage)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # aplicando filtro  em iteracoes

    for i in range(3):
        neoImage2 = transfRadioMedianaGrey(neoImage)
        cv.imshow('press any key to close 3333', neoImage2)
        cv.waitKey(0)
        cv.destroyAllWindows()
        neoImage = neoImage2
        cv.imwrite('result' + str(i) + '.jpg', neoImage2)
