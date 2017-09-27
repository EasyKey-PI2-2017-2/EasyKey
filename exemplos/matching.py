import cv2
import numpy as np

img = cv2.imread('a2.jpg')
template = cv2.imread('pado_cabeca.jpg',0)
# template = cv2.imread('formatch.jpg',0)

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
w, h = template.shape[::-1]
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.85
loc = np.where( res >= threshold)
if len(loc[0]) > 0:
    print("Chave bate com o template")
else:
    print("Chave não bate com o template")