from selenium import webdriver
from time import sleep
import os

url = os.environ.get('URL')

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)


def retry(function):
    def wrapper(*args, **kw_args):
        while True:
            try:
                return function(*args, **kw_args)
            except:
                continue
    return wrapper


@retry
def download(i):
    driver.get(url)
    container = driver.find_element('id', 'containeruno')
    #container.find_element('tag name', 'img').screenshot(f'./captchas/{i}.png')


def run(n):
    for i in range(n):
        download(i)
    driver.close()





