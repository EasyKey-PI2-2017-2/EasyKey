from django.db import models
from model_utils.models import TimeStampedModel

import numpy as np
import cv2
import glob
import serial
import time


class Payment(TimeStampedModel):
    value = models.FloatField(verbose_name="Valor da Compra")
    token = models.CharField('Token', max_length=200)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.value

class Key:
    def __init__(self):
        self.key = 0
        self.templates = []
        self.match = 0
        self.contour = 0
        self.scale = 0

    def enviar_comandos(self):
        try:
            ser = serial.Serial('/dev/ttyACM1', 9600, timeout=None)
            ser.write('0'.encode('ASCII'))
            time.sleep(1)
            ser.read_all()
            ser.write('g0'.encode('ASCII'))
        except NameError:
            print(NameError)

            # f = open("gcode.nc")
            # for l in f:
            # print(l.strip())
            # ser.write((l.strip() + "\n").encode("ASCII"))
            # ser.read(1)

    def load_key(self):
        # TODO Alterar quando estiver com a estrutura pronta
        # TODO Tirar a foto usando o PiCamera e salvar nesse path abaixo
        # img = cv2.imread('media/chave.jpg')
        img = cv2.imread('media/a2.jpg')
        cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.key = cinza

    def load_templates(self):
        modelos = glob.glob('media/templates/*.jpg')
        for path in modelos:
            self.templates.append(path)

    def verify_key_model(self):
        match = False
        for template in self.templates:
            img_template = cv2.imread(template, 0)
            w, h = img_template.shape[::-1]
            res = cv2.matchTemplate(self.key, img_template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.85
            loc = np.where(res >= threshold)
            if len(loc[0]) > 0:
                match = True
                break
            else:
                match = False
        return match

    def define_contour(self):
        # transformações para imagem da chave
        # TODO verificar size da chave pra cortar do size certo
        key = self.key[114:433, 190:260]
        borrado = cv2.GaussianBlur(key, (5, 5), 0)
        _, key_limite_antes = cv2.threshold(borrado, 127, 255, 0)
        key_limite_depois = cv2.erode(key_limite_antes, None, iterations=1)
        key_contour = (key_limite_antes - key_limite_depois)
        key_final = (255 - key_contour)
        self.contour = key_final

    def define_scale(self):
        # TODO quando tivermos a scale definitiva, descomentamos isso daqui
        # transformações para imagem da scale
        #scale = self.key[140:190, 45:55]
        #_, scale_limite = cv2.threshold(scale, 127, 255, 0)
        #scale_inversa = (255 - scale_limite)
        #scale_final = scale_inversa.transpose()

        # TODO retirar essas 2 linhas quando tivermos scale
        self.scale = 1
        return 1

        first = 0
        last = 0
        for y, row in enumerate(scale_final):
            for x, pixel in enumerate(row):
                if pixel == 255 and first == 0:
                    first = x
                elif pixel == 255 and x < first:
                    first = x
                elif pixel == 255 and x > last:
                    last = x
        size = last-first

        # esse 1 no retorno é 1cm, valor conhecido de referência
        self.scale = 1/size

    def gcode(self):
        f = open('media/gcode.nc', 'w')
        f.write(self.g0(0, -2))

        for x, row in enumerate(self.contour):
            for y, pixel in enumerate(row):
                if pixel == 0:
                    reference= (x, y)
                    break
            if pixel == 0:
                break
        for x, row in enumerate(self.contour):
            for y, pixel in enumerate(row):
                if pixel == 0:
                    f.write(self.g1(reference, (x,y), self.scale))
                    break
        f.write('M2')
        f.close()

    def g0(self, x, y):
        return 'G0 X{} Y{}\n'.format(x, y)

    def g1(self, reference, pixel, scale):
        difx = reference[0] - pixel[0]
        dify = reference[1] - pixel[1]
        return 'G1 X{} Y{}\n'.format(difx * scale , dify * scale)