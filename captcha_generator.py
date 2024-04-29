from threading import Thread
import threading
from captcha.image import ImageCaptcha
from captcha_preprocessing import preprocess_captcha, graficar
from save_letters import save_letters
from random import choice

options = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz.'

def generate():
    name = choice(options)
    image = ImageCaptcha()
    src = f'aux_letters/{threading.current_thread().name}.png'
    image.write(name, src)
    result = preprocess_captcha(src, limit=255)

    if name == '.':
        name = '-'
    if name == 'i' or name == 'j':
        result = [result[1]] if len(result[1]) > len(result[0]) else [result[0]]
    return result, name


def loop():
    for i in range(100000):
        try:
            result, name = generate()
            save_letters(result, [name])
        except:
            continue


threads = list()
for i in range(100):
    thread = Thread(target=loop)
    thread.start()
