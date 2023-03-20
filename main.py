"""
本程序可以自动化登录canvas
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
import os


def screenshot(wd):
    wd.find_element(By.XPATH, "/html/body[@class='full-width ic-Login-Body no-headers  primary-nav-expanded "
                              "full-width webkit chrome no-touch']/div[@id='application']/div[@id='wrapper']/div["
                              "@id='main']/div[@id='not_right_side']/div[@id='content-wrapper']/div["
                              "@id='content']/div[@class='ic-Login']/div[@class='ic-Login__container']/div["
                              "@class='ic-Login__content']/footer[@id='footer']/a[2]/span").click()
    t = time.time()
    pictureName1 = str(t) + '.png'
    wd.save_screenshot(pictureName1)
    
    ce = wd.find_element(By.ID, 'captcha-img')
    print(ce.location)
    left = ce.location['x']
    top = ce.location['y']
    right = ce.size['width'] + left
    height = ce.size['height'] + top
    
    im = Image.open(pictureName1)
    img = im.crop((left, top, right, height))
    
    t = time.time()
    pictureName2 = str(t) + '.png'
    
    img.save(pictureName2)
    os.remove(pictureName1)
    return pictureName2


def captcha(name):
    image1 = Image.open(name)
    te = pytesseract.image_to_string(image1)
    print(te)
    return te
    
    
def login():
    wd = webdriver.Chrome()
    wd.implicitly_wait(5)

    while True:
        wd.get('https://jicanvas.com/login/canvas')
        name = screenshot(wd)
        code = captcha(str(name))
        wd.find_element(By.XPATH, '//*[@id="user"]').send_keys('lh20020727')
        wd.find_element(By.XPATH, '//*[@id="pass"]').send_keys('kobebryant19780823')
        wd.find_element(By.XPATH, '//*[@id="captcha"]').send_keys(code)
        os.remove(name)
        if wd.title == 'Dashboard':
            break
        else:
            continue
    input()


login()

