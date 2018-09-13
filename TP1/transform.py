import cv2
import numpy as np
from matplotlib import pyplot as plt

if __name__ == '__main__':
    gray_img = cv2.imread('edleno_hexa.jpg', cv2.IMREAD_GRAYSCALE)
    cv2.imshow('Edloiro', gray_img)

    hist = cv2.calcHist([gray_img], [0], None, [256], [0,256])
    plt.hist(gray_img.ravel(), 256, [0,256])
    plt.title('Histograma escala cinza')
    plt.show()


    while True:
        k = cv2.waitKey(0) & 0xFF
        if k == 27: break

    cv2.destroyAllWindows()

