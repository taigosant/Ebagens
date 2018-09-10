import numpy as np
import cv2 as cv

img = cv.imread('teste1.jpg')

print "showing the original image... press any key to close"
cv.imshow('image1', img)
cv.waitKey(0)
cv.destroyAllWindows()


def toNegative(image):
    for i in range(0, len(image)):
        for j in range(0, len(image[0])):
            blue = image[i][j][0]
            green = image[i][j][1]
            red = image[i][j][2]
            image[i][j][0] = abs(blue - 255)
            image[i][j][1] = abs(green - 255)
            image[i][j][2] = abs(red - 255)

    return image


if __name__ == '__main__':
    neoImage = toNegative(img)
    cv.imshow('press any key to close', neoImage)
    cv.waitKey(0)
    cv.destroyAllWindows()


