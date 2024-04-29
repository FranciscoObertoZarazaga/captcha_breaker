import pytesseract
from PIL import Image
import cv2
import numpy as np
from easyocr import Reader
from save_letters import graficar
from save_letters import save_letters

reader = Reader(["en"])

def blur(img, param=3):
    return cv2.medianBlur(img, param)


def predict_letter(letter):
    alfabeto = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz."
    prediction = pytesseract.image_to_string(letter, config=f'--psm 10 --oem 1 -c tessedit_char_whitelist={alfabeto}')
    '''prediction2 = reader.readtext(letter, allowlist=alfabeto)[0][1]
    print(prediction2, prediction[0])'''
    try:
        return prediction[0]
    except:
        return prediction


def solve_captcha(letras):
    captcha = ''
    is_point = False
    for letra in letras:
        img = Image.fromarray((letra*255).astype('uint8'), mode='RGBA')
        img = np.array(img)
        prediction = predict_letter(blur(img))
        if is_point and prediction == 'i' or prediction == 'l':
            captcha += 'i'
        elif is_point and prediction == 'j':
            captcha += prediction
        elif prediction == '.':
            is_point = True
            #save_letters([img/255], ['-'])
            continue
        else:
            is_point = False
            captcha += prediction
        #graficar(img)

    return captcha
