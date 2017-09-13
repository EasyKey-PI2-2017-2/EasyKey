import numpy as np
import cv2
import matplotlib.pyplot as plt
import subprocess
import os

def load():
    im = cv2.imread('a2.jpg')
    os.system('convert a2.jpg -crop 150x315+185+118 +repage cp.jpg')
    img = cv2.imread('cp.jpg')
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(imgray, (5,5), 1)
    ret,thresh = cv2.threshold(blur,127,255,0)
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,
                                                  cv2.CHAIN_APPROX_SIMPLE)
    return cv2.drawContours(img, contours, -1, (255,255,255), 1), im

if __name__ == '__main__':
    img, im = load()

