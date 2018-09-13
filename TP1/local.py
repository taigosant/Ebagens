import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv

img = cv.imread('aventura.jpg')
cv.imshow('press any key to close 1111', img)
cv.waitKey(0)
cv.destroyAllWindows()


def __ninePartitions(image):
    linhas = len(image)
    colunas = len(image[0])
    xPart = np.linspace(0, linhas, num=4, dtype=int)
    yPart = np.linspace(0, colunas, num=4, dtype=int)
    return xPart, yPart


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


if __name__ == '__main__':

    cordenadas = {
        'iInit': 0,
        'iEnd': len(img),
        'jInit': 0,
        'jEnd': len(img[0])
    }

    histsR, histsG, histsB = histogramLocal(img)



    print(histsR, histsG, histsB)

    with open("histLocalRed.txt", 'w') as file:
        file.write(str(histsR))

    with open("histLocalGreen.txt", 'w') as file:
        file.write(str(histsG))

    with open("histLocalBlue.txt", 'w') as file:
        file.write(str(histsB))

    for freq in histsR:
        frequencies = freq
        labels = range(256)
        pos = np.arange(256)
        width = 1.0  # gives histogram aspect to the bar diagram

        ax = plt.axes()
        ax.set_xticks(pos)
        ax.set_xticklabels(labels)

        plt.bar(pos, frequencies, width, color='r')
        plt.show()