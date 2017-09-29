import numpy as np
import cv2
import matplotlib.pyplot as plt
import subprocess
import os

from math import pow, sqrt
from django.shortcuts import render


# escala de 1 mm/px
ESCALA = 0.5

def load():
    # TODO mudar este passo quando estiver com RasPi e PiCamera
    # A imagem carregada deve ser a da câmera.

    os.system('convert media/chave.jpg -crop 75x315+185+118 +repage ' +
              'media/cortada.jpg')
    img = cv2.imread('media/cortada.jpg')
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(imgray, (5,5), 0)

    ret, t_antes = cv2.threshold(blur,127,255,0)
    t_depois = cv2.erode(t_antes, None, iterations=1)

    final = (t_antes - t_depois)
    final = (255-final)
    gcode(final)


def gcode(img):
    f = open('media/gcode.nc', 'w')
    f.write(g0(0, -2))

    for x, linha in enumerate(img):
        for y, pixel in enumerate(linha):
            if pixel == 0:
                referencia = (x, y)
                break
        if pixel == 0:
            break

    for x, linha in enumerate(img):
        for y, pixel in enumerate(linha):
            if pixel == 0:
                f.write(g1(referencia, (x,y)))
                break
    f.write('M2')


# define a posição inicial
def g0(x, y):
    return 'G0 X{} Y{}\n'.format(x, y)

# movimentação do corte
def g1(referencia, pixel):
    difx = referencia[0] - pixel[0]
    dify = referencia[1] - pixel[1]
    return 'G1 X{} Y{}\n'.format(difx * ESCALA , dify * ESCALA)
