from django.db import models
from model_utils.models import TimeStampedModel

import numpy as np
import cv2
import glob
import time
#import picamera

WHITE_VALUE = 255
SCALE_VALUE_CM = 2.29

class Payment(TimeStampedModel):
    value = models.FloatField(verbose_name="Valor da Compra")
    token = models.CharField('Token', max_length=200)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.value


class Key():
    def __init__(self):
        self.key = 0
        self.templates = []
        self.match = 0
        self.contour = 0
        self.scale = 0
        self.serial = 0

    def load_key(self):
        # TODO Alterar quando estiver com a estrutura pronta
        # TODO Tirar a foto usando o PiCamera e salvar nesse path abaixo
        # camera = picamera.PiCamera()
        # camera.capture('media/chave.jpg')
        # camera.close()
        #Código acima retirado, pois só irá funcinar na RaspberryPi
        img = cv2.imread('media/a2.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('media/loadgray.jpg', gray)
        self.key = gray
	

    def load_templates(self):
        key_models = glob.glob('media/templates/*.jpg')
        for path in key_models:
            self.templates.append(path)

    def verify_key_model(self):
        match = False
        for template in self.templates:
            img_template = cv2.imread(template, 0)
            w, h = img_template.shape[::-1]
            res = cv2.matchTemplate(self.key, img_template,
                                    cv2.TM_CCOEFF_NORMED)
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
        key = self.key[132:270, 350:410]
        blured = cv2.GaussianBlur(key, (5, 5), 0)
        midpoint = (blured.max() - blured.min())//2 + blured.min()
        _, key_limit = cv2.threshold(blured, midpoint, WHITE_VALUE,
                                     cv2.THRESH_BINARY_INV)
        self.contour = key_limit
        cv2.imwrite('media/contorno.jpg', key_limit)
	

    def define_scale(self):
        # TODO quando tivermos a scale definitiva, descomentamos isso daqui
        # transformações para imagem da scale
        scale = self.key[85:240, 470:490]
        #scale = cv2.imread('media/testescale.jpg')
        # scale = cv2.cvtColor(scale, cv2.COLOR_BGR2GRAY)
        midpoint = (scale.max() - scale.min())//2 + scale.min()
        _, scale_limit = cv2.threshold(scale, midpoint, WHITE_VALUE,
                                        cv2.THRESH_BINARY_INV)
        scale_final = scale_limit.transpose()
        cv2.imwrite('media/escala_scale.jpg', scale) 
        cv2.imwrite('media/escala.jpg', scale_limit)

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
        self.scale = SCALE_VALUE_CM/size

    def gcode(self):
        f = open('media/gcode.nc', 'w')
        f.write(self.g0(0, 0.365))

        for x, row in enumerate(self.contour):
            for y, pixel in enumerate(row):
                if pixel == 255:
                    reference = (x, y)
                    break
            if pixel == 255:
                break
        for x, row in enumerate(self.contour):
            for y, pixel in enumerate(row):
                if pixel == 255:
                    f.write(self.g1(reference, (x,y), self.scale))
                    break
        f.write('M2')
        f.close()

    def g0(self, x, y):
        return 'G0 X{} Y{}\n'.format(y, x)

    def g1(self, reference, pixel, scale):
        difx = reference[0] - pixel[0]
        dify = reference[1] - pixel[1]
        return 'G1 X{} Y{}\n'.format(dify * scale , difx * scale)
