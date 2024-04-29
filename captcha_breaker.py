from selenium import webdriver
from captcha_preprocessing import preprocess_captcha
from captcha_solver import solve_captcha
from save_letters import save_letters

url = os.environ.get('URL')
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)

def submit(captcha):
    cuil_container = driver.find_element('id', 'CuilTitular')
    captcha_container = driver.find_element('id', 'InputCaptcha')
    boton_submit = driver.find_element('class name', 'ButtonBody')
    cuil_container.send_keys(os.environ.get('CUIL'))
    captcha_container.send_keys(captcha)
    boton_submit.click()



def break_captcha():
    driver.get(url)
    container = driver.find_element('id', 'containeruno')
    src = 'captcha.png'
    container.find_element('tag name', 'img').screenshot(src)
    letras = preprocess_captcha(src)
    captcha = solve_captcha(letras)
    if len(captcha) == 6:
        submit(captcha)
    else:
        break_captcha()

    return letras, captcha

