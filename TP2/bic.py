import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv

# img = cv.imread('balo.jpg')
# cv.imshow('press any key to close 1111', img)
# cv.waitKey(0)
# cv.destroyAllWindows()


def _reduceColor(pixel): # funcao responsavel por mapear uma cor do padrao rgb (255) para um padrao com 64 cores
    if pixel < 64:
        return 0
    elif 64 <= pixel < 128:
        return 64
    elif 128 <= pixel < 192:
        return 128
    else:
        return 255


def _mapColor(pixel):
    if pixel == 0: return 0
    elif pixel == 64: return 1
    elif pixel == 128: return 2
    elif pixel == 255: return 3
    else: return -1


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


def check_neighbors(image, i, j, grey=False):
    if grey:
        color = image[i][j]
        if image[i][j + 1] != color:
            return True
        if image[i][j - 1] != color:
            return True
        if image[i + 1][j] != color:
            return True
        if image[i - 1][j] != color:
            return True

        return False
    else:
        for c in range(3):
            color = image[i][j][c]
            if image[i][j+1][c] != color: return True
            if image[i][j-1][c] != color: return True
            if image[i+1][j][c] != color: return True
            if image[i-1][j][c] != color: return True

        return False


def bic(image):
    linhas = len(image)
    colunas = len(image[0])

    image = colorQuantization(image)

    histBorderR = np.zeros(4)
    histBorderG = np.zeros(4)
    histBorderB = np.zeros(4)

    histInnerR = np.zeros(4)
    histInnerG = np.zeros(4)
    histInnerB = np.zeros(4)

    # bicImg = np.zeros((linhas, colunas))

    for i in range(1, linhas-1):
        for j in range(1, colunas-1):
            is_border = check_neighbors(image, i, j)

            red = _mapColor(image[i][j][2])
            green = _mapColor(image[i][j][1])
            blue = _mapColor(image[i][j][0])

            if is_border:
                histBorderR[red] += 1
                histBorderG[green] += 1
                histBorderB[blue] += 1
            else:
                histInnerR[red] += 1
                histInnerG[green] += 1
                histInnerB[blue] += 1
                # bicImg[i][j] = 255

    # cv.imwrite('bic.jpg', bicImg)

    return [histBorderR, histBorderG, histBorderB], [histInnerR, histInnerG, histInnerB]


def bicGrey(image):
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    linhas = len(image)
    colunas = len(image[0])

    image = colorQuantizationGrey(image)

    histBorder = np.zeros(4)

    histInner = np.zeros(4)

    # bicImg = np.zeros((linhas, colunas))

    for i in range(1, linhas-1):
        for j in range(1, colunas-1):
            is_border = check_neighbors(image, i, j, grey=True)

            color = _mapColor(image[i][j])

            if is_border:
                histBorder[color] += 1
            else:
                histInner[color] += 1
                # bicImg[i][j] = 255

    # cv.imwrite('bic.jpg', bicImg)

    return histBorder, histInner

# if __name__ == '__main__':
#     print(bic(img))