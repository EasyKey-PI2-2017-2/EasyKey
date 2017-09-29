import numpy as np
import cv2
import matplotlib.pyplot as plt
import subprocess
import os

from math import pow, sqrt

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
    im = cv2.imread('rasp.jpg')
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    escala = imgray[60:130, 290:310]
    chave = imgray[25:152, 405:440]

    blur = cv2.GaussianBlur(chave, (5,5), 0)
    

    ret,t_antes = cv2.threshold(blur,204,255,cv2.THRESH_BINARY)
    ret,t_escala = cv2.threshold(escala,188,255,cv2.THRESH_BINARY)
    
    t_depois = cv2.erode(t_antes, None, iterations=1)
    
    cfinal = (t_antes - t_depois)
    cfinal = (255-cfinal)
    efinal = (255-t_escala)
    efinal = efinal.transpose()
    
    #escala = set_escala(efinal)
