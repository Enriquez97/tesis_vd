from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import numpy as np
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
service = Service(executable_path='chromedriver.exe')




def descarga_lista_last(wait = 30, usuario = '', password = ''):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(wait)
    options.add_argument("--start-maximized")
    driver.get("http://seaap.minsa.gob.pe/web/login")  
    input_usuario=driver.find_element("xpath",'/html/body/div/main/div/form/div[1]/input')
    input_usuario.send_keys(usuario)
    input_password=driver.find_element("xpath",'/html/body/div/main/div/form/div[2]/input')
    input_password.send_keys(password)
    driver.find_element("xpath",'/html/body/div/main/div/form/div[3]/button').click()
    time.sleep(1)
    driver.find_element("xpath",'/html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[7]/a').click()
    time.sleep(1)
    driver.find_element("xpath",'/html/body/header/nav[2]/div/div[2]/div[1]/div/ul[1]/li[7]/ul/li/a').click()
    time.sleep(1)
    driver.find_element("xpath",'/html/body/div[1]/div/div[2]/div/div/div[1]/div[1]/div/div[1]/a').click()
    time.sleep(2)
    driver.find_element("xpath",'/html/body/div[1]/div/div[1]/div[1]/div/span').click()
    time.sleep(1)
    driver.find_element("xpath",'/html/body/div[1]/div/div[1]/div[3]/div[1]/div[2]/button').click()
    time.sleep(1)   
   #/html/body/div[1]/div/div[1]/div[1]/div/span
    #time.sleep(1)
    driver.find_element("xpath",'/html/body/div[1]/div/div[1]/div[3]/div[1]/div[2]/ul/li[2]/a').click()
    time.sleep(1)
    driver.find_element("xpath",'/html/body/div[1]/div/div[1]/div[3]/div[1]/div[2]/ul/li[3]/a').click()
    time.sleep(1)
    driver.find_element("xpath",'/html/body/div[1]/div/div[1]/div[3]/div[1]/div[2]/button').click()
    time.sleep(1)
    driver.find_element("xpath",'/html/body/div[1]/div/div[2]/div/div/div/table/tbody/tr[1]').click()
    time.sleep(2)
    span = driver.find_element("xpath",'/html/body/div[1]/div/div[2]/div/div/div/table/tbody[1]/tr/td[21]/div/span[1]')
    #time.sleep(1)
    max_rows=driver.find_element("xpath",'/html/body/div[1]/div/div[2]/div/div/div/table/tbody[1]/tr/td[21]/div/span[2]').text
    #time.sleep(1)
    driver.execute_script(f"arguments[0].innerText = '1-{max_rows}'", span)
    #driver.execute_script(f"arguments[0].innerText = '1-100", span)
    #time.sleep(1)
    span.click()
    driver.find_element("xpath",'/html/body/div[1]/div/div[2]/div/div/div/table/tbody[1]/tr/td[21]').click()

    time.sleep(wait)
    #time.sleep(20)
    size_rows = len(driver.find_elements("xpath",'/html/body/div[1]/div/div[2]/div/div/div/table/tbody[2]/tr'))       
    print(size_rows)
    for i in range(size_rows):
        print(i)
        driver.find_element("xpath",f'/html/body/div[1]/div/div[2]/div/div/div/table/tbody[2]/tr[{i+1}]/td[2]/div/input').click()
    time.sleep(1)
    driver.find_element("xpath",f'/html/body/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/button').click()
    time.sleep(1)
    driver.find_element("xpath",f'/html/body/div[1]/div/div[1]/div[2]/div[2]/div/div[2]/ul/li[1]/a').click()
    time.sleep(1)
    driver.find_element("xpath",f'/html/body/div[6]/div/div/div[2]/div[1]/div[1]/div/div[2]/input').click()
    time.sleep(1)
    driver.find_element("xpath",f'/html/body/div[6]/div/div/div[2]/div[1]/div[2]/div/div[2]/input').click()
    time.sleep(1)
    driver.find_element("xpath",f'/html/body/div[6]/div/div/div[2]/div[2]/div[3]/div[2]/select/option[97]').click()
    time.sleep(1)
    driver.find_element("xpath",'/html/body/div[6]/div/div/div[3]/button[1]').click()