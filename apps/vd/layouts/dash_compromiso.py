from django_plotly_dash import DjangoDash
from apps.vd.constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS
from dash import dcc,html,dash_table, Output, Input, State
import dash_mantine_components as dmc
import base64
import datetime
import io
import pandas as pd
from google.cloud import bigquery
from apps.vd.utils.transforms import clean_padron
from apps.vd.utils.components import *
from apps.vd.utils.frames import Container,Div, Row ,Column, Store,Content
from apps.vd.utils.data import padron_df_dash, padron_anio_list
from apps.vd.utils.functions import dataframe_filtro, validar_all_none
from apps.vd.utils.cards import cardGraph
from apps.vd.utils.figures import line_figure,pie_figure, bar_go_figure
from apps.vd.utils.scraping import descarga_lista_last
import dash_ag_grid as dag
from apps.vd.constans import COLUMNAS_COMPROMISO_1
from apps.vd.utils.transforms import clean_compromiso1_data
    
def dash_carga_compromiso():
    app = DjangoDash('carga-compromiso',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
        Row([Column([title(content='Importar datos del Compromiso 1',order=1)],size=12)]),
        
        
        Row([Column(upload(upload_id='upload-compromiso-1',stack_id='content-compromiso-1'))]),
        Row([Column(Div(id='output-data-upload-1'))]),
    ])
    @app.callback(
                Output('output-data-upload-1', 'children'),
                
                Input('upload-compromiso-1', 'contents'),
                
                
                )
    def cargar_data_compromiso(upload):
        if upload == None :
            return dmc.Text(f"Sin carga")
        else:
            content_string_1 = upload.split(',')[1]
            first_decoded = base64.b64decode(content_string_1)
            df = pd.read_excel(io.BytesIO(first_decoded),names = COLUMNAS_COMPROMISO_1)
            dff = clean_compromiso1_data(df)
            return dag.AgGrid(
            id="get-started-example-basic-df",
            rowData=dff.to_dict("records"),
            columnDefs=[{"field": i} for i in dff.columns],
        )
       
    

def dash_descarga_data_compromiso():
    app = DjangoDash('descarga-compromiso',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Content([
        Row([Column([title(content='Descargar Data del Compromiso 1',order=1)],size=12)]),
        Row([
            #43601728
            #   
            Column([dmc.TextInput(id='input-usuario',label="Usuario", placeholder='Ingresa tu usuario',icon=DashIconify(icon="mdi:user"),value='43601728')],size=4),
            Column([
                dmc.PasswordInput(id='input-password',label="Contraseña", placeholder="Ingresa tu contraseña",icon=DashIconify(icon="bi:shield-lock"),value='123456'),
            ],size=4),
            Column([
                #inputNumber(id='inputn_tiempo_espera',label="Tiempo de espera maximo",value=40)
                dmc.NumberInput(label="Tiempo de espera maximo",value=40,min=5,step=1,id='input_tiempo_espera')
            
            ],size=4),

        
        ]),
        Row([Column([dmc.Center(button(id='btn',text='webdriver'))])]),
        Div(id='notifications-update-data'),
    ])
    @app.callback(
                    Output('notifications-update-data','children'),
                    Input('btn','n_clicks'),
                    State('input-usuario',"value"),
                    State('input-password',"value"),
                    State('input_tiempo_espera',"value"),
                   # Input('btn-click-checkbox','n_clicks'),
    )
    def update_r(n_clicks,usuario,password,wait_time):
        tiempo_espera_maxima =int(wait_time) 
        try:
            if n_clicks:
                descarga_lista_last(wait = tiempo_espera_maxima,usuario=usuario,password=password)
                return notification(text=f'La descarga finalizó',title='Bien')    
        except:
           return notification(text=f'Se cargaron mal',title='Error')





def dash_compromiso():
    app = DjangoDash('compromiso-general',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
        
    ])