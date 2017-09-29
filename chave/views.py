import numpy as np
import cv2
import matplotlib.pyplot as plt
import subprocess
import os

from math import pow, sqrt
from django.shortcuts import render


class GCode():
    def carregar_imagens(self):
        # carregando imagem
        img = cv2.imread('media/chave.jpg')
        cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # transformações para imagem da escala
        escala = cinza[140:190, 45:55]
        _, escala_limite = cv2.threshold(escala, 127, 255, 0)
        escala_inversa = (255 - escala_limite)
        escala_final = escala_inversa.transpose()

        # transformações para imagem da chave
        chave = cinza[114:433, 190:260]
        borrado = cv2.GaussianBlur(chave, (5, 5), 0)
        _, chave_limite_antes = cv2.threshold(borrado, 127, 255, 0)
        chave_limite_depois = cv2.erode(chave_limite_antes, None, iterations=1)
        chave_contorno = (chave_limite_antes - chave_limite_depois)
        chave_final = (255 - chave_contorno)

        escala = self.set_escala(escala_final)
        self.gcode(chave_final, escala)

    def set_escala(self, escala_final):
        primeiro = 0
        ultimo = 0

        for y, linha in enumerate(escala_final):
            for x, pixel in enumerate(linha):
                if pixel == 255 and primeiro == 0:
                    primeiro = x
                elif pixel == 255 and x < primeiro:
                    primeiro = x
                elif pixel == 255 and x > ultimo:
                    ultimo = x

        tamanho = ultimo-primeiro
        return 1/tamanho*3

    def gcode(self, img, escala):
        f = open('media/gcode.nc', 'w')
        f.write(self.g0(0, -2))

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
                    f.write(self.g1(referencia, (x,y), escala))
                    break
        f.write('M2')

    def g0(self, x, y):
        return 'G0 X{} Y{}\n'.format(x, y)

    def g1(self, referencia, pixel, escala):
        difx = referencia[0] - pixel[0]
        dify = referencia[1] - pixel[1]
        return 'G1 X{} Y{}\n'.format(difx * escala , dify * escala)
