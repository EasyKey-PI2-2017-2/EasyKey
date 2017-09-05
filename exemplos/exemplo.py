import numpy as np
import cv2
import matplotlib.pyplot as plt

im = cv2.imread('2.jpg')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(imgray, (53,53), 0)
ret,thresh = cv2.threshold(blur,127,255,0)
image, contours, hierarchy = cv2.findContours(
    thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
img = cv2.drawContours(im, contours, -1, (255,255,255), 3)
plt.imshow(img)
