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
from apps.vd.utils.components import title, loadingOverlay, upload,select, multiSelect,notification,segmented
from apps.vd.utils.frames import Container,Div, Row ,Column, Store
from apps.vd.utils.data import padron_df_dash, padron_anio_list
from apps.vd.utils.functions import dataframe_filtro, validar_all_none
from apps.vd.utils.cards import cardGraph
from apps.vd.utils.figures import line_figure,pie_figure, bar_go_figure
import dash_ag_grid as dag
#client = bigquery.Client()

# Perform a query.
#QUERY = (
#    'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` '
#    'WHERE state = "TX" '
#    'LIMIT 100')
#query_job = client.query(QUERY)  # API request
#rows = query_job.result()  # Waits for query to finish

#for row in rows:
#    print(row.name)

    
def dash_carga_padron():
    app = DjangoDash('carga-padron',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
        Row([
            Column([title(content='Importar Datos de Padrón Nominal',order=1)])
        ]),
        Row([
            Column([
                upload(upload_id='upload-data-padron-1',stack_id='content-padron-1'),
                Div(id='output-data-upload-1')
            ],size=6),
            Column([
                upload(upload_id='upload-data-padron-2',stack_id='content-padron-2'),
                Div(id='output-data-upload-2')
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
        
        
    ])
    
    @app.callback(
                Output('output-data-upload-1', 'children'),
                Output('output-data-upload-2', 'children'),
                Output('graph-1', 'children'),
                Output('graph-2', 'children'),
                Input('upload-data-padron-1', 'contents'),
                Input('upload-data-padron-2', 'contents'),
                
                )
    def update_output(upload_1, upload_2):
        if upload_1 == None and upload_2 == None:
            return dmc.Text(f"Sin carga"),dmc.Text(f"Sin carga"),dmc.Text(f"Sin tabla"),dmc.Text(f"Sin tabla"),
        elif upload_1 != None and upload_2 == None:
            content_string_1 = upload_1.split(',')[1]
            first_decoded = base64.b64decode(content_string_1)
            primer_df = pd.read_excel(io.BytesIO(first_decoded),skiprows=4)
            df_1=clean_padron(primer_df)
            
            return [dmc.Text(f"{df_1.shape[0]}", weight=700),
                    dmc.Text(f"Sin carga"),
                    dag.AgGrid(
                        id="get-started-example-basic-df",
                        rowData=df_1.to_dict("records"),
                        columnDefs=[{"field": i} for i in df_1.columns],
                    ),
                    dmc.Text(f"Sin tabla"),
                    
            ]
        elif upload_1 == None and upload_2 != None:
            content_string_2 = upload_2.split(',')[1]
            second_decoded = base64.b64decode(content_string_2)
            segundo_df = pd.read_excel(io.BytesIO(second_decoded),skiprows=4)
            df_2=clean_padron(segundo_df)
            
            return [dmc.Text(f"Sin carga"),
                    dmc.Text(f"{df_2.shape[0]}"),
                    dmc.Text(f"Sin tabla"),
                    dag.AgGrid(
                        id="get-started-example-basic-df",
                        rowData=df_2.to_dict("records"),
                        columnDefs=[{"field": i} for i in df_2.columns],
                    ),
                    
                ]
        elif upload_1 != None and upload_2 != None:
            
            content_string_1 = upload_1.split(',')[1]
            content_string_2 = upload_2.split(',')[1]
            
            first_decoded = base64.b64decode(content_string_1)
            second_decoded = base64.b64decode(content_string_2)
            primer_df = pd.read_excel(io.BytesIO(first_decoded),skiprows=4)
            df_1=clean_padron(primer_df)
            segundo_df = pd.read_excel(io.BytesIO(second_decoded),skiprows=4)
            df_2=clean_padron(segundo_df)
            
            #dag.AgGrid(
            #id="get-started-example-basic-df",
            #rowData=dff.to_dict("records"),
            #columnDefs=[{"field": i} for i in dff.columns],
        #)
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
            ]


def dash_padron_nominal():
    app = DjangoDash('padron-general',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
        Row([
            Column([title(content='Padrón Nominal',order=1)],size=4),
            Column([multiSelect(id='multiselect-year',texto='Años',data = padron_anio_list)],size=3),
            Column([select(id='select-eess',texto='EESS de Atención',searchable=True)],size=3),
            Column([select(id='select-entidadUpdate',texto='Entidad Actualiza Registro',searchable=True)],size=2),
        
        ]),
        Row([
            Column([
                segmented(id='segmented-st',value = 'Mes',
                          data =[
                              {'label':'Fecha','value':'Fecha de Nacimiento'},
                              {'label':'Mes','value':'Mes'},
                              #{'label':'Semana','value':'Semana'},
                              {'label':'Trimestre','value':'Trimestre'},
                              {'label':'Año','value':'Año'},
                        ]
                ),
                loadingOverlay(cardGraph(id_graph = 'line-st',height=300))
            ],size=6),
            Column([
                segmented(id='segmented-pie',value = 'Entidad Actualiza',
                          data =[
                              
                              {'label':'Entidad Actualiza','value':'Entidad Actualiza'},
                              {'label':'Frecuenta de Atención','value':'Frecuenta_atencion_padron'},
                              {'label':'Estado Encontrado','value':'Estado_encontrado'},
                              {'label':'Tipo Documento Niño','value':'Tipo Documento Padron'},
                              {'label':'Tipo Documento Madre','value':'Tipo_doc_madre_padron'},
                              #{'label':'Sexo','value':'Sexo'},
                        ]
                ),
                loadingOverlay(cardGraph(id_graph = 'pie',height=300))
            
            ],size=6),
        ]),
        Row([
            Column([
                segmented(id='segmented-eess',value = 'EESS_nacimiento_padron',
                          data =[
                              {'label':'EESS de Salud','value':'EESS_nacimiento_padron'},
                              {'label':'EESS de Atención','value':'EESS_atencion_padron'},
                              {'label':'EESS de Adscripción','value':'EESS_adscripcion_padron'},
                              
                        ]
                ),
                loadingOverlay(cardGraph(id_graph = 'bar-eess',height=400))
            ],size=6),
            Column([
                
            
            ],size=6),
        
        
        ]),
        Div(id='notifications-update-data'),
        Store(id='data-values'),
    ])
    @app.callback(
                    Output('select-eess','data'),
                    Output('select-entidadUpdate','data'),
                    Output("data-values","data"),
                    Output("notifications-update-data","children"),
                    Input('multiselect-year','value'),
                    Input('select-eess','value'),
                    Input('select-entidadUpdate','value'),
    )
    def update_filtro_data(*args):
        padron_df_dash['Año'] = padron_df_dash['Año'].astype('string')
        if validar_all_none(variables = (args)) == True:
            df=padron_df_dash.copy()
        else:
            df=padron_df_dash.query(dataframe_filtro(values=list(args),columns_df=['Año','EESS_atencion_padron','Entidad Actualiza']))
        
        #anio=[{'label': i, 'value': i} for i in df['Año'].unique()]
        return [
            [{'label': i, 'value': i} for i in df['EESS_atencion_padron'].unique()],
            [{'label': i, 'value': i} for i in df['Entidad Actualiza'].unique()],
            df.to_dict('series'),
            notification(text=f'Se cargaron {len(df)} filas',title='Update')
        ]

    @app.callback(
                    Output('line-st','figure'),
                    Input("data-values","data"),
                    Input("segmented-st","value"),
                    
    )
    def update_graph_linea(data,segmented):
       df = pd.DataFrame(data) 
       print(df)
       if segmented == 'Mes':
            st_df=df.groupby([segmented,'Mes_'])[['Tipo Documento Padron']].count().sort_values('Mes_').reset_index()
       else:
            st_df=df.groupby([segmented])[['Tipo Documento Padron']].count().reset_index()
       print(st_df)
       return line_figure(df = st_df, 
                          x = [segmented], 
                          y = 'Tipo Documento Padron',
                          height = 300, 
                          x_title = 'Fecha',
                          y_title = 'Número de Niños Nacidos',
                          
        )
    
    @app.callback(
                    Output('pie','figure'),
                    Input("data-values","data"),
                    Input("segmented-pie","value"),
                    
    )
    def update_graph_pie(data,segmented):
       df = pd.DataFrame(data) 
       df[segmented]=df[segmented].fillna('Sin Registro')
       
       dff=df.groupby([segmented])[['Fecha de Nacimiento']].count().reset_index()
      
       return pie_figure(df = dff, 
                         label_col= segmented, 
                         value_col = 'Fecha de Nacimiento',
                         title = segmented,
                         height=300)
    
    @app.callback(
                    Output('bar-eess','figure'),
                    Input("data-values","data"),
                    Input("segmented-eess","value"),
                    
    )
    def update_graph_bar(data,segmented):
        df = pd.DataFrame(data) 
        df[segmented]=df[segmented].fillna('Sin Registro')
        dff=df.groupby([segmented])[['Tipo Documento Padron']].count().sort_values('Tipo Documento Padron').reset_index()
        return bar_go_figure(df = dff, 
                             x = 'Tipo Documento Padron',
                             y = segmented,
                             orientation='h',
                             height = 400, 
                             title = segmented,
                             text='Tipo Documento Padron',
                             xaxis_title='N° de Niños',
                             yaxis_title='Establecimiento de Salud'
        )