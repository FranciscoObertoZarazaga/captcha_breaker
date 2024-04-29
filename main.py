#import captcha_generator
import IA
exit()
from save_letters import save_letters
import pytesseract
import cv2
from captcha_breaker import break_captcha, driver
pytesseract.pytesseract.tesseract_cmd = os.environ.get('TESSERACT_PATH')


def fuerza_bruta(n, m=0):
    try:
        letras, captcha = break_captcha()
        n += 1
        container = driver.find_element('id', 'Principal').find_element('tag name', 'h6').text
        if container == 'El titular no cumple con los requisitos de edad necesarios para solicitar turno sobre este trámite.':
            m += 1
            print('Exito, intentos', n, ', Total obtenidas: ', m*5)
            save_letters(letras, captcha)
            n = 0
        fuerza_bruta(n, m)
    except:
        fuerza_bruta(0, m)


fuerza_bruta(0)











'''for letra in letras:
    im = Image.fromarray((letra*255).astype('uint8'), mode='RGBA')
    im.save("letra.png")
    im = cv2.imread('letra.png')
    #cv2.imshow('image', im)
    caracter = image_to_string(im, config='--psm 6')
    resultado.append(caracter)
    #graficar(letra)
    #graficar(img)

print(resultado)'''
