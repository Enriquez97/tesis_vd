from django_plotly_dash import DjangoDash
from apps.vd.constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS
from dash import dcc,html,dash_table, Output, Input, State
import dash_mantine_components as dmc
import base64

import io
import pandas as pd
from google.cloud import bigquery
from apps.vd.data.transformacion import clean_padron
from apps.vd.utils.components import *
from apps.vd.utils.frames import Container,Div, Row ,Column, Store
#from apps.vd.utils.data import padron_df_dash, padron_anio_list
from apps.vd.utils.functions import dataframe_filtro, validar_all_none
from apps.vd.utils.cards import cardGraph
from apps.vd.utils.figures import line_figure,pie_figure, bar_go_figure
import dash_ag_grid as dag
from datetime import datetime, date, timedelta
from ...vd.data.lectura import *
from apps.vd.data.transformacion import clean_columns_padron, clean_columns_c1,transform_padron
from ..constans import LISTA_COLORES_BAR
#from apps.vd.data.lectura import padron_dataframe_bq#padron_dataframe_bq
#print(padron_dataframe_bq)
def dash_carga_padron():
    app = DjangoDash('carga-padron',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
        Row([
            Column([title(content='Importar Datos de Padrón Nominal',order=1)])
        ]),
        Row([
            Column([
                upload(upload_id='upload-data-padron-1',stack_id='content-padron-1'),
                dmc.Center(Div(id='output-data-upload-1'))
                
            ],size=6),
            Column([
                upload(upload_id='upload-data-padron-2',stack_id='content-padron-2'),
                dmc.Center(Div(id='output-data-upload-2'))
                
            ],size=6),
        ]),
        
        Row([
            Column([
                #dcc.Graph(id='graph-1')
                Div(id='graph-1')
            ],size=6),
            Column([
                #dcc.Graph(id='graph-2')
                Div(id='graph-2')
            ],size=6),
        ]),
        Row([
            Column([
                dmc.Center(button(text = 'Guardar', id = 'btn-guardar-data'))
                
            ],size=12),
            
        ]),
        Row([
            Column([
                Div(id='alert')
            ],size=12),
            
        ]),
        Store(id='data-value'),
        
    ])
    
    @app.callback(
                Output('output-data-upload-1', 'children'),
                Output('output-data-upload-2', 'children'),
                Output('graph-1', 'children'),
                Output('graph-2', 'children'),
                Output('data-value','data'),
                Input('upload-data-padron-1', 'contents'),
                Input('upload-data-padron-2', 'contents'),
                #Input('btn-guardar-data','n_clicks')
                
                )
    def update_output(upload_1, upload_2):
        #df.to_dict('series'),
        if upload_1 == None and upload_2 == None:
            print('sin datos')
            return [dmc.Text(f"Sin carga"),dmc.Text(f"Sin carga"),dmc.Text(f"Sin tabla"),dmc.Text(f"Sin tabla"),None]
        elif upload_1 != None and upload_2 == None:
            content_string_1 = upload_1.split(',')[1]
            first_decoded = base64.b64decode(content_string_1)
            primer_df = pd.read_excel(io.BytesIO(first_decoded),skiprows=4)
            #df_1=clean_padron(primer_df)
            df_1 = primer_df.copy()
            df_1 = clean_columns_padron(df_1)
            print('datos lado 1')
            return [dmc.Text(f"{df_1.shape[0]}", weight=700),
                    dmc.Text(f""),
                    dag.AgGrid(
                        id="get-started-example-basic-df",
                        rowData=df_1.to_dict("records"),
                        columnDefs=[{"field": i} for i in df_1.columns],
                    ),
                    dmc.Text(f"Sin tabla"),
                    df_1.to_dict('series')
                    
            ]
        elif upload_1 == None and upload_2 != None:
            content_string_2 = upload_2.split(',')[1]
            second_decoded = base64.b64decode(content_string_2)
            segundo_df = pd.read_excel(io.BytesIO(second_decoded),skiprows=4)
            #df_2=clean_padron(segundo_df)
            df_2 = segundo_df.copy()
            df_2 = clean_columns_padron(df_2)
            print('datos lado 2')
            return [dmc.Text(f""),
                    dmc.Text(f"{df_2.shape[0]}"),
                    dmc.Text(f"Sin tabla"),
                    dag.AgGrid(
                        id="get-started-example-basic-df",
                        rowData=df_2.to_dict("records"),
                        columnDefs=[{"field": i} for i in df_2.columns],
                    ),
                    df_2.to_dict('series')
                    
                ]
        elif upload_1 != None and upload_2 != None:
            
            content_string_1 = upload_1.split(',')[1]
            content_string_2 = upload_2.split(',')[1]
            
            first_decoded = base64.b64decode(content_string_1)
            second_decoded = base64.b64decode(content_string_2)
            primer_df = pd.read_excel(io.BytesIO(first_decoded),skiprows=4)
            #df_1=clean_padron(primer_df)
            df_1 = primer_df.copy()
            df_1 = clean_columns_padron(df_1)
            segundo_df = pd.read_excel(io.BytesIO(second_decoded),skiprows=4)
            #df_2=clean_padron(segundo_df)
            df_2 = segundo_df.copy()
            df_2 = clean_columns_padron(df_2)
            #padron_df._append(padron,ignore_index=True)
            dff = df_1._append(df_2,ignore_index= True)
            
            return [dmc.Text(f"{df_1.shape[0]}"),
                    dmc.Text(f"{df_2.shape[0]}"),
                    dag.AgGrid(
                        id="get-started-example-basic-df",
                        rowData=df_1.to_dict("records"),
                        columnDefs=[{"field": i} for i in df_1.columns],
                    ),
                    dag.AgGrid(
                        id="get-started-example-basic-df",
                        rowData=df_2.to_dict("records"),
                        columnDefs=[{"field": i} for i in df_2.columns],
                    ),
                    dff.to_dict('series')
            ]
            
    @app.callback(
                Output('alert', 'children'),
                Input('data-value','data'),
                Input('btn-guardar-data','n_clicks'),
                
                )
    def update_save( data,n_clicks_guardar):
            try:
                df = pd.DataFrame(data)
                
                if n_clicks_guardar:
                    #cargarDataPadron
                    df['Fecha_Carga'] = datetime.datetime.now()
                    print(df)
                    schema_df = [{'name': i , 'type': 'STRING'} for i in df.columns]
                    cargarDataPadron(df,None)
                    return Div(content=[dmc.Alert("Se almaceno correctamente nuevamente",title="Correcto :",color="blue",duration=5000)])
                    """
                    print('aqui estoy cuy')
                    if os.path.exists('p_data.parquet'):
                        data_parquet_df = pd.read_parquet('p_data.parquet', engine='pyarrow')
                        df['Fecha de Carga'] = str(datetime.datetime.now())
                        dff = data_parquet_df._append(df,ignore_index=True)
                        #print(dff.info())
                        dff.to_parquet('p_data.parquet')
                        return Div(content=[dmc.Alert("Se almaceno correctamente nuevamente",title="Correcto :",color="blue",duration=5000)])
                    else:
                        
                        df['Fecha de Carga'] = str(datetime.datetime.now())
                        #print(df.info())
                        df.to_parquet('p_data.parquet')
                        return Div(content=[dmc.Alert("Se almaceno correctamente",title="Correcto :",color="blue",duration=5000)])
                    """
            except:
                return Div(content=[dmc.Alert("No existen datos para almacenar",title="Error :",color="red",duration=5000)])
            
            
"""
if n_click_guardar:
            if upload_1 == None and upload_2 == None:
            #
                alerta = dmc.Alert("No olvide ingresar la data",title="Error :",color="red",duration=5000)
            elif upload_1 != None and upload_2 == None:
                if os.path.exists('p_data.parquet'):
                    data_parquet_df = pd.read_parquet('p_data.parquet', engine='pyarrow')
                    data_parquet_df._append(meta_df,ignore_index=True) 
"""
from ..data.lectura import bq_pnominal_df
#padron_df = bq_pnominal_df()
#padron_df = transform_padron(dff = padron_df)
#print(padron_df.columns)



def dash_padron_nominal():
    print('DASHBOARD - PADRON NOMINAL')
    print('Consulta de BG')
    select_carga = bq_fcarga_pnominal_df()
    print('termina consulta')
    print('Crear Objeto DjangoDash')
    select_ = sorted(select_carga['Fecha_Carga'].unique())
    app = DjangoDash('padron-general',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
        Row([Column([title(content='Padrón Nominal',order=1)],size=12)]),
        Row([
            Column([datepicker_(text = 'Rango Inicio', tipo = 'inicio')],size=2), 
            Column([datepicker_(text = 'Rango Fin', tipo = 'fin')],size=2), 
            Column([select(id='select-eess',texto='EESS de Atención',searchable=True)],size=3),
            Column([select(id='select-entidadUpdate',texto='Entidad Actualiza Registro',searchable=True)],size=2),
            Column([select(id='select-reporte-carga', data = select_,texto='Fecha de Carga de Fuente de Datos', value= select_[-1], clearable=False)],size=2),
            Column([btnDownload()],size=1)
        ]),
        Row([
            Column([
                segmented(id='segmented-st',value = 'Mes',
                          data =[
                              {'label':'Fecha','value':'Fecha de Nacimiento'},
                              {'label':'Mes','value':'Mes'},
                              {'label':'Trimestre','value':'Trimestre'},
                              {'label':'Año','value':'Año'},
                        ]
                ),
                loadingOverlay(cardGraph(id_graph = 'line-st',height=350))
            ],size=6),
            Column([
                segmented(id='segmented-pie',value = 'Entidad Actualiza',
                        data =[
                              {'label':'Entidad Actualiza','value':'Entidad Actualiza'},
                              {'label':'Frecuencia de Atención','value':'Frecuencia de Atención'},
                              {'label':'Estado Encontrado','value':'Estado Encontrado'},
                              {'label':'Tipo de Documento','value':'Tipo de Documento'},
                              {'label':'Tipo Documento Madre','value':'Tipo de Documento - Madre'},
                        ]
                ),
                loadingOverlay(cardGraph(id_graph = 'pie',height=350))
            ],size=6),
        ]),
        Row([
            Column([
                segmented(id='segmented-eess',value = 'Establecimiento de Salud de Atención',
                          data =[
                              {'label':'EESS de Nacimiento','value':'Establecimiento de Salud de Nacimiento'},
                              {'label':'EESS de Atención','value':'Establecimiento de Salud de Atención'},
                              {'label':'EESS de Adscripción','value':'Establecimiento de Salud de Adscripción'},
                        ]
                ),
                loadingOverlay(cardGraph(id_graph = 'bar-eess',height=400))
            ],size=4),
            Column([
                loadingOverlay(cardGraph(id_graph = 'pie-estado-registro',height=435))
            
            ],size=2),
            Column([
                loadingOverlay(cardGraph(id_graph = 'pie-ejevial',height=435))
            
            ],size=3),
            Column([
                loadingOverlay(cardGraph(id_graph = 'pie-ref',height=435))
            
            ],size=3),    
        ]),
        Div(id='notifications-update-data'),
        Store(id='data-values'),
        dcc.Download(id="descargar")
    ])
    print('Se ejecutan los callbacks')
    
    @app.callback(
        Output('select-eess','data'),
        Output('select-entidadUpdate','data'),
        Output("data-values","data"),
        Output("notifications-update-data","children"),
        Input('select-reporte-carga','value'),
        Input('datepicker-inicio','value'),
        Input('datepicker-fin','value'),
        Input('select-eess','value'),
        Input('select-entidadUpdate','value'),
    )
    def update_filtro_data(*args):
        print('Callback de filtrado de data')
        pnominal_df = bq_pnominal_df(query = f"SELECT * FROM `ew-tesis.dataset_tesis.pnominal`WHERE Fecha_Carga = '{args[0]}'")
        df = transform_padron(dff=pnominal_df)
        dff = df[(df['Fecha de Nacimiento']>=args[1])&(df['Fecha de Nacimiento']<=args[2])]
        if validar_all_none(variables = (args[3:])) == True:
            dfff=dff.copy()
        else:
            dfff=dff.query(dataframe_filtro(values=list(args[3:]),columns_df=['Establecimiento de Salud de Atención','Entidad Actualiza']))        
        return [
            [{'label': i, 'value': i} for i in dfff['Establecimiento de Salud de Atención'].unique()],
            [{'label': i, 'value': i} for i in dfff['Entidad Actualiza'].unique()],
            dfff.to_dict('series'),
            notification(text=f'Se cargaron {len(dfff)} filas',title='Update')
        ]
    
    @app.callback(
        Output('line-st','figure'),
        Input("data-values","data"),
        Input("segmented-st","value"),            
    )
    def update_graph_linea(data,segmented):
       print('Callback de Segmented-Linechart')
       df = pd.DataFrame(data) 
       if segmented == 'Mes':
            st_df=df.groupby([segmented,'Mes Num'])[['Tipo de Documento']].count().sort_values('Mes Num').reset_index()
       else:
            st_df=df.groupby([segmented])[['Tipo de Documento']].count().reset_index()
       return line_figure(df = st_df, 
                          x = [segmented], 
                          y = 'Tipo de Documento',
                          height = 350, 
                          x_title = 'Fecha',
                          y_title = 'Número de Niños Nacidos',
                          title=' N° de Niños Nacidos'          
        )
    
    @app.callback(
        Output('pie','figure'),
        Input("data-values","data"),
        Input("segmented-pie","value"),             
    )
    def update_graph_pie(data,segmented):
       print('Callback de Segmented-Piechart')
       df = pd.DataFrame(data) 
       df[segmented]=df[segmented].fillna('Sin Registro')
       dff=df.groupby([segmented])[['Fecha de Nacimiento']].count().reset_index()
       return pie_figure(df = dff, 
                         label_col= segmented, 
                         value_col = 'Fecha de Nacimiento',
                         title = segmented,
                         height=350,
                         textposition = 'inside',
                         textfont_size=13,
                         list_or_color=['#71dbd2','#eeffdb','#ade4b5','#d0eaa3','#fff18c']
        )
       
    
    @app.callback(
        Output('bar-eess','figure'),
        Input("data-values","data"),
        Input("segmented-eess","value"),         
    )
    def update_graph_bar(data,segmented):
        print('Callback de Segmented-Barchart')
        df = pd.DataFrame(data) 
        df[segmented]=df[segmented].fillna('Sin Registro')
        dff=df.groupby([segmented])[['Tipo de Documento']].count().sort_values('Tipo de Documento').reset_index()
        dff = dff[dff['Tipo de Documento']>3]
        dff = dff.rename(columns = {'Tipo de Documento':'N° de Niños'})
        return bar_go_figure(df = dff, 
                             x = 'N° de Niños',
                             y = segmented,
                             orientation='h',
                             height = 400, 
                             title = segmented,
                             text='N° de Niños',
                             xaxis_title='N° de Niños',
                             yaxis_title='Establecimiento de Salud',
                             list_colors=LISTA_COLORES_BAR        
        )
    
    @app.callback(
                    Output('pie-estado-registro','figure'),
                    Output('pie-ejevial','figure'),
                    Output('pie-ref','figure'),
                    Input("data-values","data"),             
    )
    def update_graph_pie_2(data):
        print('Callback de Piecharts')
        df = pd.DataFrame(data)
        estado_reg_df=df.groupby(['Estado de Registro'])[['Tipo de Documento']].count().reset_index() 
        estado_eje_df=df.groupby(['Estado Eje Vial'])[['Tipo de Documento']].count().reset_index() 
        estado_ref_df=df.groupby(['Estado Referencias'])[['Tipo de Documento']].count().reset_index()
         
        return[
            pie_figure(df = estado_reg_df, 
                         label_col= 'Estado de Registro', 
                         value_col = 'Tipo de Documento',
                         title = 'Estado de Registro',
                         height=435,
                         list_or_color = ['#8eb2c5','#f98f6f'],
                         textfont_size=15,
                         showlegend=False
                        ),
            pie_figure(df = estado_eje_df, 
                         label_col= 'Estado Eje Vial', 
                         value_col = 'Tipo de Documento',
                         title = 'Estado Eje Vial',
                         height=435,
                         list_or_color = ['#079ea6','#19274e'],
                         textfont_size=15
                        ),
            pie_figure(df = estado_ref_df, 
                         label_col= 'Estado Referencias', 
                         value_col = 'Tipo de Documento',
                         title = 'Estado Referencias',
                         height=435,
                         list_or_color = ['#a85163','#b4dec1'],
                         textfont_size=15
                         ),
        ]
    
    @app.callback(
            
            Output("descargar", "data"),
            Input("data-values","data"),
            Input("btn-download", "n_clicks"),
            prevent_initial_call=True,
            
            )
    def update_download(data,n_clicks_download):
        print('Callback Descargar data')
        options=pd.DataFrame(data)
        if n_clicks_download:
            return dcc.send_data_frame( options.to_excel, "padron.xlsx", sheet_name="Sheet_name_1",index =False)
        
