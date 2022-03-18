import cv2
from matplotlib import pyplot as plt
import numpy as np
import math


def image_da_webcam(img):
    """
    ->>> !!!! FECHE A JANELA COM A TECLA ESC !!!! <<<<-
        deve receber a imagem da camera e retornar uma imagems filtrada.
    """

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cimg = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2RGB)

    circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, dp=3,
                               minDist=100, param1=100, param2=200, minRadius=50, maxRadius=70)

    areas = []

    circulos = []

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:

            # desenha o contorno do circulo
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 4)

            # desenha no centro do circulo
            cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 5)
            area = math.pi * math.pow(i[2], 2)

            areas.append(area)
            circulos.append((i[0], i[1]))

    if len(circulos) == 2:

        cv2.line(cimg, (circulos[0]), (circulos[1]), (254, 0, 0), 3)

    return cimg


cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

# configura o tamanho da janela
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:

    img = image_da_webcam(frame)

    cv2.imshow("preview", img)
    cv2.imshow("original", frame)

    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break
cv2.destroyWindow("original")
cv2.destroyWindow("preview")
vc.release()
