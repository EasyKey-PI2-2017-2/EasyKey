import numpy as np
import cv2
import matplotlib.pyplot as plt
import subprocess
import os
import glob

from math import pow, sqrt
from django.shortcuts import render


class Chave():
    def __init__(self):
        self.chave = 0
        self.templates = []
        self.match = 0
        self.contorno = 0
        self.escala = 0

    def carregar_chave(self):
        # TODO Alterar quando estiver com a estrutura pronta
        # TODO Tirar a foto usando o PiCamera e salvar nesse path abaixo
        # img = cv2.imread('media/chave.jpg')
        img = cv2.imread('media/a2.jpg')
        cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.chave = cinza

    def carregar_templates(self):
        modelos = glob.glob('media/templates/*.jpg')
        for path in modelos:
            self.templates.append(path)

    def verificar_modelo(self):
        match = False
        for template in self.templates:
            img_template = cv2.imread(template, 0)
            w, h = img_template.shape[::-1]
            res = cv2.matchTemplate(self.chave, img_template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.85
            loc = np.where(res >= threshold)
            if len(loc[0]) > 0:
                match = True
                break
            else:
                match = False
        return match

    def definir_contorno(self):
        # transformações para imagem da chave
        # TODO verificar tamanho da chave pra cortar do tamanho certo
        chave = self.chave[114:433, 190:260]
        borrado = cv2.GaussianBlur(chave, (5, 5), 0)
        _, chave_limite_antes = cv2.threshold(borrado, 127, 255, 0)
        chave_limite_depois = cv2.erode(chave_limite_antes, None, iterations=1)
        chave_contorno = (chave_limite_antes - chave_limite_depois)
        chave_final = (255 - chave_contorno)
        self.contorno = chave_final

    def definir_escala(self):
        # TODO quando tivermos a escala definitiva, descomentamos isso daqui
        # transformações para imagem da escala
        #escala = self.chave[140:190, 45:55]
        #_, escala_limite = cv2.threshold(escala, 127, 255, 0)
        #escala_inversa = (255 - escala_limite)
        #escala_final = escala_inversa.transpose()

        # TODO retirar isso quando tivermos escala
        return 1

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

        # esse 1 no retorno é 1cm, valor conhecido de referência
        self.escala = 1/tamanho

    def gcode(self):
        f = open('media/gcode.nc', 'w')
        f.write(self.g0(0, -2))

        for x, linha in enumerate(self.contorno):
            for y, pixel in enumerate(linha):
                if pixel == 0:
                    referencia = (x, y)
                    break
            if pixel == 0:
                break
        for x, linha in enumerate(self.contorno):
            for y, pixel in enumerate(linha):
                if pixel == 0:
                    f.write(self.g1(referencia, (x,y), self.escala))
                    break
        f.write('M2')
        f.close()

    def g0(self, x, y):
        return 'G0 X{} Y{}\n'.format(x, y)

    def g1(self, referencia, pixel, escala):
        difx = referencia[0] - pixel[0]
        dify = referencia[1] - pixel[1]
        return 'G1 X{} Y{}\n'.format(difx * escala , dify * escala)
