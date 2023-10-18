from django_plotly_dash import DjangoDash
from apps.vd.constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS
from dash import dcc,html,dash_table, Output, Input, State
import dash_mantine_components as dmc
import pandas as pd
import numpy as np
from apps.vd.utils.frames import Container,Div, Row ,Column, Store
from apps.vd.utils.components import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time


def dash_extraer_padron():
    
    app = DjangoDash('extraer-padron',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
        Row([
            Column([title(content='Extraer Datos de Padrón Nominal',order=1)])
        ]),
        Row([
            Column([dmc.Center(button(id='btn',text='webdriver'))],size=4),
            Column([dmc.NumberInput(label="Tiempo de espera maximo",value=40,min=5,step=1,id='input_tiempo_espera')],size=4)
        ]),
        
        Div(id='notifications-update-data'),
    ])
    @app.callback(
                    Output('notifications-update-data','children'),
                    Input('btn','n_clicks'),
                    State('input_tiempo_espera',"value"),
                   # Input('btn-click-checkbox','n_clicks'),
    )
    def update_r(n_clicks,wait_time):
        tiempo_espera_maxima =int(wait_time)
        docs_madres= ['71603603', '46219030','74764897']
        data=[]
        lista = []
        try:
            if n_clicks:
                options = webdriver.ChromeOptions()
                options.add_experimental_option("detach", True)  
                driver = webdriver.Chrome(options=options,service=Service(executable_path='chromedriver.exe'))
                driver.implicitly_wait(tiempo_espera_maxima)
                driver.get("https://padronnominal.reniec.gob.pe/padronn/")
                time.sleep(tiempo_espera_maxima)
                #
                driver.find_element("xpath",'/html/body/div[1]/div[3]/div/div/div/div/ul/li[1]').click()
                #/html/body/div[1]/div[3]/div/div/div[2]/div[2]/form/ul/li[4]/a   
                driver.find_element("xpath",'/html/body/div[1]/div[3]/div/div/div[2]/div[2]/form/ul/li[4]/a').click()
                for dni_madre in docs_madres:
    
                    #selecciona el tipo de doc DNI
                    driver.find_element("xpath",'/html/body/div[1]/div[3]/div/div/div[2]/div[2]/form/div[1]/div[4]/div[1]/div[1]/select/option[2]').click()
                    input_doc =driver.find_element("xpath","/html/body/div[1]/div[3]/div/div/div[2]/div[2]/form/div[1]/div[4]/div[1]/div[2]/input")
                    
                    input_doc.send_keys(dni_madre)
                    #click para buscar datos del doc
                    driver.find_element("xpath","/html/body/div[1]/div[3]/div/div/div[2]/div[2]/form/div[2]/button[1]").click()
                    
                    try:
                        
                        driver.find_element("xpath","/html/body/div[1]/div[3]/div/div/div[3]/div/fieldset/div[1]/div[2]/div[2]/a").click()
                        #extrayendo
                        
                        dni = dni_madre
                        datos_madre = driver.find_element("xpath","/html/body/div[1]/div[3]/div/div/div[3]/div/fieldset/div[1]/div[1]").text
                        ubigeo = driver.find_element("xpath","/html/body/div[1]/div[3]/div/div/div[3]/div/fieldset/div[1]/div[2]/div[2]/div[1]/p[1]/strong").text
                        reniec_direccion = driver.find_element("xpath","/html/body/div[1]/div[3]/div/div/div[3]/div/fieldset/div[1]/div[2]/div[2]/div[1]/p[2]/strong").text
                        num_hijos = driver.find_element("xpath","/html/body/div[1]/div[3]/div/div/div[3]/div/fieldset/div[1]/div[2]/div[2]/div[1]/p[3]").text
                    except:
                        dni = dni_madre
                        datos_madre =''
                        ubigeo = ''
                        reniec_direccion = ''
                        num_hijos = ''
                    data=np.array([dni,datos_madre,ubigeo,reniec_direccion,num_hijos])
                    print(data)
                    lista.append(data)
                    matriz_scraping_reniec_=np.vstack([lista])
                    
                    input_doc.clear()
                    time.sleep(1)
                print(matriz_scraping_reniec_)
                return notification(text=f'La descarga finalizó',title='Bien')    
        except:
           return notification(text=f'Se cargaron mal',title='Error')