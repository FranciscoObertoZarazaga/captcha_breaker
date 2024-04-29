import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

def frontera(function):
    def wrap(*args, **kwargs):
        try:
            return function()
        except:
            return False

    return wrap

def search_black_pixel(image):
    filas, columnas, _ = image.shape
    for j in range(columnas):
        for i in range(filas):
            if is_black(image, i, j):
                return i, j
    return False


def look_around(image, pixeles, i, j):
    add_pixel(pixeles, i, j)
    if search_up(image, i, j):
        add_pixel(pixeles, i+1, j)
    if search_left(image, i, j):
        add_pixel(pixeles, i, j-1)
    if search_down(image, i, j):
        add_pixel(pixeles, i-1, j)
    if search_right(image, i, j):
        add_pixel(pixeles, i, j+1)

    # Busca en las diagonales
    '''if search_up(image, i, j+1):
        add_pixel(pixeles, i+1, j+1)
    if search_up(image, i, j-1):
        add_pixel(pixeles, i+1, j-1)
    if search_down(image, i, j+1):
        add_pixel(pixeles, i-1, j+1)
    if search_down(image, i, j-1):
        add_pixel(pixeles, i-1, j-1)'''


def get_letter(img):
    i, j = search_black_pixel(img)
    n_pixeles = 0
    pixeles = []
    look_around(img, pixeles, i, j)
    while n_pixeles != len(pixeles):
        n_pixeles = len(pixeles)
        for pixel in pixeles:
            i, j = pixel
            look_around(img, pixeles, i, j)
    pixeles = np.array(pixeles)

    return pixeles


def search_up(image, i, j):
    return is_black(image, i+1, j)


def search_left(image, i, j):
    return is_black(image, i, j-1)


def search_down(image, i, j):
    return is_black(image, i-1, j)


def search_right(image, i, j):
    return is_black(image, i, j+1)


def is_black(image, i, j):
    return not image[i][j][0]


def add_pixel(pixeles, i, j):
    if tuple([i, j]) not in pixeles:
        pixeles.append((i, j))


def delete_background(img, limit=125):
    img_array = np.array(img)
    img_array[img_array > limit] = 255
    img_array[img_array < limit] = 0
    return img_array


def blanquear(img, pixeles):
    for pixel in pixeles:
        i, j = pixel
        img[i][j] = np.array([1, 1, 1])


def graficar(img):
    plt.imshow(img)
    plt.show()


def preprocess_captcha(src, graf=0, limit=125):
    img = Image.open(src)
    img = np.array(img)
    img = delete_background(img,limit)
    img = img / img.max()
    if graf:
        graficar(img)
    letras = list()

    while search_black_pixel(img):
        letter = get_letter(img)
        blanquear(img, letter)

        y_min = np.min(letter[:, 0])
        x_min = np.min(letter[:, 1])
        y_max = np.max(letter[:, 0])
        x_max = np.max(letter[:, 1])
        letter[:, 0] = letter[:, 0] - y_min + 5
        letter[:, 1] = letter[:, 1] - x_min + 5
        letra = np.ones((y_max - y_min + 10, x_max - x_min + 10, 4))

        for pixel in letter:
            i, j = pixel
            letra[i][j] = np.array([0, 0, 0, 1])

        letras.append(letra)
    return letras
