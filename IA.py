import pandas as pd
import cv2
import os
from tqdm import tqdm
from tensorflow import keras
from sklearn.model_selection import train_test_split
from captcha_preprocessing import graficar
from keras.layers import Dense, Flatten
from keras.models import Sequential
from keras import applications


def preprocess(letra, alto_max, ancho_max):
    letter = list()
    alto = len(letra)
    ancho = len(letra[0])
    for i, fila in enumerate(letra):
        fila = [int(pixel[0]/255) for pixel in fila]
        letter += fila + [1] * (ancho_max - ancho)
    return letter + [1] * ancho_max * (alto_max - alto)


def listar(img):
    return [j for i in img for j in i]


def get_size(letra):
    return len(letra), len(letra[0])


def get_max_size(letras):
    max_alto, max_ancho = 0, 0

    for letra in letras:
        alto, ancho = get_size(letra)
        max_ancho = ancho if ancho > max_ancho else max_ancho
        max_alto = alto if alto > max_alto else max_alto

    return max_alto, max_ancho


def import_letters():
    print('Importando imagenes')
    images = list()
    names = list()
    for img in tqdm(os.listdir('letters')):
        letter = cv2.imread(f'letters/{img}')
        #letter = preprocess(letter)
        images.append(letter)
        names.append(img[0])
    return images, names


def img_to_csv():
    letters, names = import_letters()
    max_alto, max_ancho = get_max_size(letters)
    df_letters = pd.DataFrame(columns=['letter', 'name'])
    print('\nProcesando imagenes')
    for i, letra in tqdm(enumerate(letters)):
        letra = preprocess(letra, max_alto, max_ancho)
        exit()
        df_letters = pd.concat([df_letters, pd.DataFrame({'letter': [letra], 'name': names[i]})], ignore_index=True)

    print(df_letters)
    df_letters.to_csv('letters.csv')

print(img_to_csv())
exit()
print('Importando df')
letters = pd.read_csv('letters.csv')

print('Dividiendo datos')
x = letters["letter"]
y = letters['name']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
x_val, x_test, y_val, y_test = train_test_split(x_test, y_test, test_size=.5)

tags = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz.'
tags = [tag for tag in tags]

inception = applications.InceptionV3(include_top=False, input_shape=(324542, 1))

predictor = Sequential([
    Flatten(),
    Dense(128, activation='relu'),
    Dense(2, activation='softmax')
])

model = Sequential([inception, predictor])
