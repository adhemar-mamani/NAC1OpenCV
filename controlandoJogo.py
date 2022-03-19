
import cv2
from matplotlib import pyplot as plt

from pynput.keyboard import Controller
import pynput
import time


import numpy as np
import math

keys = [

    pynput.keyboard.KeyCode.from_char('d'),
    pynput.keyboard.KeyCode.from_char('w'),
    pynput.keyboard.KeyCode.from_char('a'),
]

# Inicializa o controle
keyboard = Controller()


def image_da_webcam(img):
    """
    ->>> !!!! FECHE A JANELA COM A TECLA ESC !!!! <<<<-
        deve receber a imagem da camera e retornar uma imagems filtrada.
    """

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cimg = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2RGB)

    circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, dp=2.1,
                               minDist=210, param1=100, param2=100, minRadius=40, maxRadius=60)

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

        def acharAngulo(circulo1, circulo2):
            catetoAdjacente = (circulo1[0]) - (circulo2[0])
            catetoOposto = (circulo1[1]) - (circulo2[1])

            return math.degrees(math.atan2(catetoOposto, catetoAdjacente))

        cv2.line(cimg, (circulos[0]), (circulos[1]), (254, 0, 0), 3)
        angulo = acharAngulo(circulos[0], circulos[1])

        angulo = np.round(angulo)

        # definir a tecla pressionada de acordo com o angulo

        if angulo > 0 and angulo <= 20:

            print('Tecla: ', keys[0])

            keyboard.press(keys[0])
            time.sleep(0.1)
            keyboard.release(keys[0])
        elif angulo > 20 and angulo <= 50:

            print('Tecla: ', keys[1])

            keyboard.press(keys[1])
            time.sleep(0.5)
            keyboard.release(keys[1])
        elif angulo > 50 and angulo <= 80:

            print('Tecla: ', keys[2])

            keyboard.press(keys[2])
            time.sleep(0.1)
            keyboard.release(keys[2])
        elif angulo > 80:

            print('Tecla: ', keys[1])

            keyboard.press(keys[1])
            time.sleep(0.1)
            keyboard.release(keys[1])

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
