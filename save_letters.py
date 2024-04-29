from random import randint
from captcha_preprocessing import preprocess_captcha, graficar
import os
from PIL import Image
import pytesseract
import cv2


def blur(img, param):
    return cv2.medianBlur(img, param)

def save_letters(letras, names):
    for letra, name in zip(letras, names):
        im = Image.fromarray((letra*255).astype('uint8'), mode='RGBA')
        dirs = os.listdir('letters')
        dirs = [int(d[1:-4]) for d in dirs if d[0] == name]
        i = max(dirs) + 1 if len(dirs) > 0 else 0
        src = f"letters/{name}{i}.png"
        while os.path.isfile(src):
            i += 1
            src = f"letters/{name}{i}.png"
        im.save(src)


def run(n):
    for i in range(n):
        n = randint(0, 500)
        src = f'./captchas/{n}.png'
        letras = preprocess_captcha(src)
        save_letters(letras)
