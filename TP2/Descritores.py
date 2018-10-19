import numpy as np
import cv2
import math
from numpy.linalg import norm
import os, sys
import Similaridade


def thresholded(center, pixels):
    out = []
    for a in pixels:
        if a >= center:
            out.append(1)
        else:
            out.append(0)
    return out


def get_pixel_else_0(l, idx, idy, default=0):
    try:
        return l[idx, idy]
    except IndexError:
        return default


class Descritores(object):
    def histograma(self, img):
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        return hist

    def bic(self, img):

        transformed_img = img
        for x in range(1, len(img) - 1):
            for y in range(1, len(img[0])):
                center = img[x, y]
                top_left = get_pixel_else_0(img, x - 1, y - 1)
                top_up = get_pixel_else_0(img, x, y - 1)
                top_right = get_pixel_else_0(img, x + 1, y - 1)
                right = get_pixel_else_0(img, x + 1, y)
                left = get_pixel_else_0(img, x - 1, y)
                bottom_left = get_pixel_else_0(img, x - 1, y + 1)
                bottom_right = get_pixel_else_0(img, x + 1, y + 1)
                bottom_down = get_pixel_else_0(img, x, y + 1)

        values = thresholded(center, [top_left, top_up, top_right, right, bottom_right,
                                      bottom_down, bottom_left, left])

        weights = [1, 2, 4, 8, 16, 32, 64, 128]
        res = 0

        for a in range(0, len(values)):
            res += weights[a] * values[a]

        # transformed_img.itemset((x,y), res)

        hist, bins = np.histogram(img.flatten(), 256, [0, 256])

        return bins

    def hog(img):
        gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
        gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
        mag, ang = cv2.cartToPolar(gx, gy)
        bin_n = 16  # Number of bins
        bin = np.int32(bin_n * ang / (2 * np.pi))

        bin_cells = []
        mag_cells = []
        cellx = celly = 8

        for i in range(0, img.shape[0] / celly):
            for j in range(0, img.shape[1] / cellx):
                bin_cells.append(bin[i * celly: i * celly + celly, j * cellx: j * cellx + cellx])
                mag_cells.append(mag[i * celly: i * celly + celly, j * cellx: j * cellx + cellx])

        hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
        hist = np.hstack(hists)

        # transform to Hellinger kernel
        eps = 1e-7
        hist /= hist.sum() + eps
        hist = np.sqrt(hist)
        hist /= norm(hist) + eps

        return hist

    def Sift(self, img):
        sift = cv2.xfeatures2d.SIFT_create()
        kp, des = sift.detectAndCompute(img, None)
        # print(type(kp))
        # print((kp))
        # print(len(des))
        return len(kp)

    def Surf(self, img):
        surf = cv2.xfeatures2d.SURF_create()

        kp, des = surf.detectAndCompute(img, None)
        return len(kp)
