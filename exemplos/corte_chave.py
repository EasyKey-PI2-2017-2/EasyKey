import numpy as np
import cv2
import matplotlib.pyplot as plt
import subprocess
import os

from math import pow, sqrt


def load():
    im = cv2.imread('a3.jpg')
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    escala = imgray[140:190, 45:55]
    chave = imgray[114:433, 190:260]

    blur = cv2.GaussianBlur(chave, (5,5), 0)

    ret,thresh_chave_antes = cv2.threshold(blur,127,255,0)
    ret,thresh_escala = cv2.threshold(escala,127,255,0)

    thresh_chave_depois = cv2.erode(thresh_chave_antes, None, iterations=1)

    return (thresh_chave_antes, thresh_chave_depois, thresh_escala)


def gcode(img, escala):
    f = open('gcode.nc', 'w')
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
                f.write(g1(referencia, (x,y), escala))
                break

    f.write('M2')

def set_escala(efinal):
    primeiro = 0
    ultimo = 0
    for y, linha in enumerate(efinal):
        for x, pixel in enumerate(linha):
            if pixel == 255 and primeiro == 0:
                primeiro = x
            elif pixel == 255 and x < primeiro:
                primeiro = x
            elif pixel == 255 and x > ultimo:
                ultimo = x
    import ipdb
    ipdb.set_trace()
    tamanho = ultimo-primeiro
    return 1/tamanho*3


# define a posição inicial
def g0(x, y):
    return 'G0 X{} Y{}\n'.format(x, y)

# movimentação do corte
def g1(referencia, pixel, escala):
    difx = referencia[0] - pixel[0]
    dify = referencia[1] - pixel[1]

    return 'G1 X{} Y{}\n'.format(difx * escala , dify * escala)

if __name__ == '__main__':
    t_antes, t_depois, t_escala = load()
    cfinal = (t_antes - t_depois)
    cfinal = (255-cfinal)
    efinal = (255-t_escala)
    efinal = efinal.transpose()

    cv2.imwrite('dilate-erode.jpg', cfinal)
    escala = set_escala(efinal)
