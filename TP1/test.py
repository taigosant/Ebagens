import numpy as np
import cv2 as cv

img = cv.imread('teste1.jpg')


print("showing the original image... press any key to close")
cv.imshow('image1', img)
cv.waitKey(0)
cv.destroyAllWindows()


def __getInput():
    raw = input("Enter the percent of brightness desired to apply and the operator."
                    " Ex: \"+ 30\" to increase the brightness or \"- 30\" to decrease.\n> ")
    params = raw.split()
    return params[0], int(params[1])


def __percent(value):
    percent = (255*value)/100
    # print(percent)
    return percent


def __editPixel(pixel, value, op):
    if op == '+':
        sum = pixel + value
        if sum <= 255:
            return sum
        else:
            return 255
    elif op == '-':
        sum = pixel - value
        if sum >= 0:
            return sum
        else:
            return 0


def brightness(image, value, op='+'):
    toSum = __percent(value)
    for i in range(0, len(image)):
        for j in range(0, len(image[0])):
            blue = image[i][j][0]
            green = image[i][j][1]
            red = image[i][j][2]
            image[i][j][0] = __editPixel(blue, toSum, op)
            image[i][j][1] = __editPixel(green, toSum, op)
            image[i][j][2] = __editPixel(red, toSum, op)

    return img


if __name__ == '__main__':
    while True:
        ope, value = __getInput()
        neoImage = brightness(img, value, op=ope)
        cv.imshow('press any key to close', neoImage)
        cv.waitKey(0)
        cv.destroyAllWindows()
        img = neoImage







