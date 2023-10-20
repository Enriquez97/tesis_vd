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
from apps.vd.utils.frames import Container,Div, Row ,Column, Store,Content,Modal
#from apps.vd.utils.data import padron_df_dash, padron_anio_list
from apps.vd.utils.functions import dataframe_filtro, validar_all_none
from apps.vd.utils.cards import cardGraph
from apps.vd.utils.figures import line_figure,pie_figure, bar_go_figure
from apps.vd.utils.scraping import descarga_lista_last
import dash_ag_grid as dag
from apps.vd.constans import COLUMNAS_COMPROMISO_1,EESS_TRUJILLO
from apps.vd.data.transformacion import clean_compromiso1_data,clean_columns_c1
import os
import datetime
from apps.vd.data.ingesta import cargarDataCargaVD
from apps.vd.data.lectura import *
import plotly.express as px
    
def dash_carga_compromiso():
    app = DjangoDash('carga-compromiso',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
        
        Row([Column([title(content='Importar datos del Compromiso 1',order=1)],size=12)]),
        
        
        Row([Column(upload(upload_id='upload-compromiso-1',stack_id='content-compromiso-1'))]),
        Row([Column(Div(id='output-data-upload-1'))]),
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
        Store(id='data-value')
    ])
    @app.callback(
                Output('output-data-upload-1', 'children'),
                Output('data-value','data'),
                Input('upload-compromiso-1', 'contents'),
                )
    def cargar_data_compromiso(upload):
        if upload == None :
            return dmc.Text(f"Sin carga"),None
        else:
            content_string_1 = upload.split(',')[1]
            first_decoded = base64.b64decode(content_string_1)
            df = pd.read_excel(io.BytesIO(first_decoded),names = COLUMNAS_COMPROMISO_1)
            dff = clean_columns_c1(df)
            return [
                dag.AgGrid(id="get-started-example-basic-df",rowData=dff.to_dict("records"),columnDefs=[{"field": i} for i in dff.columns]),
                dff.to_dict('series')  
            ]
    
    @app.callback(
                Output('alert', 'children'),
                Input('data-value','data'),
                Input('btn-guardar-data','n_clicks'),
                
                )
    def update_save( data,n_clicks_guardar):
        
        try:
            
            
            if n_clicks_guardar:
                
                df = pd.DataFrame(data)
                df['Fecha_Carga'] = datetime.datetime.now()
                cargarDataCargaVD(df)
                return Div(content=[dmc.Alert("Se almaceno correctamente",title="Correcto :",color="blue",duration=5000)])
                """
                
                if os.path.exists('c1_data.parquet'):
                    print('existe el archivo cuy v:')
                    data_parquet_df = pd.read_parquet('c1_data.parquet', engine='pyarrow')
                    df['Fecha de Carga'] = str(datetime.datetime.now())
                    dff = data_parquet_df._append(df,ignore_index=True)
                    
                    dff.to_parquet('c1_data.parquet')
                    return Div(content=[dmc.Alert("Se almaceno correctamente nuevamente",title="Correcto :",color="blue",duration=5000)])
                else:
                    print('no existe nada owo')
                    df['Fecha de Carga'] = str(datetime.datetime.now())
                    print(df)
                    df.to_parquet('c1_data.parquet')
                    return Div(content=[dmc.Alert("Se almaceno correctamente",title="Correcto :",color="blue",duration=5000)])
                """
        except:
             print('no ed')
             return Div(content=[dmc.Alert("No existen datos para almacenar",title="Error :",color="red",duration=5000)])
        
    

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
    
    
def dash_carga_vd_realizadas():
    app = DjangoDash('carga-compromiso',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
        Row([Column([title(content='Importar el Detalle de Visitas Domiciliarias',order=1)],size=12)]),
        
        
        Row([Column(upload(upload_id='upload-compromiso-1',stack_id='content-compromiso-1'))]),
        Row([Column(Div(id='output-data-upload-1'))]),
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
        Store(id='data-value')
    ])
    @app.callback(
                Output('output-data-upload-1', 'children'),
                Output('data-value','data'),
                Input('upload-compromiso-1', 'contents'),
                )
    def cargar_data_compromiso(upload):
        if upload == None :
            return dmc.Text(f"Sin carga"),None
        else:
            content_string_1 = upload.split(',')[1]
            first_decoded = base64.b64decode(content_string_1)
            df = pd.read_excel(io.BytesIO(first_decoded),names = COLUMNAS_COMPROMISO_1)
            dff = clean_columns_c1(df)
            return [
                dag.AgGrid(id="get-started-example-basic-df",rowData=dff.to_dict("records"),columnDefs=[{"field": i} for i in dff.columns]),
                dff.to_dict('series')  
            ]
    
    @app.callback(
                Output('alert', 'children'),
                Input('data-value','data'),
                Input('btn-guardar-data','n_clicks'),
                
                )
    def update_save( data,n_clicks_guardar):
        
        try:
            
            
            if n_clicks_guardar:
                
                df = pd.DataFrame(data)
                df['Fecha_Carga'] = datetime.datetime.now()
                cargarDataCargaVD(df)
                return Div(content=[dmc.Alert("Se almaceno correctamente",title="Correcto :",color="blue",duration=5000)])
                """
                
                if os.path.exists('c1_data.parquet'):
                    print('existe el archivo cuy v:')
                    data_parquet_df = pd.read_parquet('c1_data.parquet', engine='pyarrow')
                    df['Fecha de Carga'] = str(datetime.datetime.now())
                    dff = data_parquet_df._append(df,ignore_index=True)
                    
                    dff.to_parquet('c1_data.parquet')
                    return Div(content=[dmc.Alert("Se almaceno correctamente nuevamente",title="Correcto :",color="blue",duration=5000)])
                else:
                    print('no existe nada owo')
                    df['Fecha de Carga'] = str(datetime.datetime.now())
                    print(df)
                    df.to_parquet('c1_data.parquet')
                    return Div(content=[dmc.Alert("Se almaceno correctamente",title="Correcto :",color="blue",duration=5000)])
                """
        except:
             print('no ed')
             return Div(content=[dmc.Alert("No existen datos para almacenar",title="Error :",color="red",duration=5000)])

def table_dag(df = pd.DataFrame):
    return html.Div(children=[dag.AgGrid(
                        id="table-dag-resultados",
                        rowData=df.to_dict("records"),
                        columnDefs=[{"field": i,} for i in df.columns],#"cellStyle": {'font-size': 18}
                        defaultColDef = {
                            "resizable": True,
                            "initialWidth": 130,
                            "wrapHeaderText": True,
                            "autoHeaderHeight": True,
                        },
                        rowClassRules={"bg-primary fw-bold": "['TOTAL'].includes(params.data.Periodo)"},
                        className="ag-theme-alpine headers1",
                        dashGridOptions = {"domLayout": "autoHeight"},
                        #getRowId="params.data.State",
                        columnSize="sizeToFit",
                        style={"height": None}
                    )])

def  dashboard_indicadores_vd():
    vd_detalle_df_bq = bq_cvd_detalle_df()
    periodos = vd_detalle_df_bq['Periodo_VD'].unique()
    
    def table_periodos(dataframe_all_data = vd_all_cargados_df, dataframe_detalle_vd = vd_detalle_df_bq):
        periodo_list = dataframe_detalle_vd['Periodo_VD'].unique()
        periodos = []
        total_niños_cargados = []
        total_niños_asignados = []
        total_vd_completas = []
        total_vd_presencial = []
        total_vd_presencial_validas = []
        total_vd_presencial_novalidas = []
        total_vd_presencial_validas_web = []
        total_vd_presencial_validas_movil = []
        total_no_encontrados = []
        total_rechazados = []
        porcentaje_vd_efectivas = []
        porcentaje_vd_movil = []
        for periodo in periodo_list:
            
            
            all_vd_df = dataframe_all_data[dataframe_all_data['Periodo_VD'] == periodo]
            detalle_vd_df = dataframe_detalle_vd[dataframe_detalle_vd['Periodo_VD'] == periodo]
            
            niños_cargados_total = all_vd_df['Numero_Doc_Nino'].count()
            niños_asignados_total = all_vd_df[all_vd_df['Establecimito_Salud_Meta'].isin(EESS_TRUJILLO)]['Establecimito_Salud_Meta'].count()
            vd_completa_total = all_vd_df['Numero_de_Visitas_Completas'].sum()
            
            periodos.append(periodo)
            total_niños_cargados.append(niños_cargados_total)
            total_niños_asignados.append(niños_asignados_total)
            total_vd_completas.append(vd_completa_total)
            
            detalle_vd_df= detalle_vd_df[detalle_vd_df['Tipo_VD']=='Visita presencial']
            vd_presencial_total = detalle_vd_df['Numero_Doc_Nino'].count()
            vd_presencial_valida_total = detalle_vd_df['VD_Valida'].sum()
            vd_presencial_novalida_total = vd_presencial_total-vd_presencial_valida_total
            vd_presencial_valida_web = detalle_vd_df[(detalle_vd_df['Dispositivo_Intervencion']=='WEB')&(detalle_vd_df['Estado_Intervencion_VD']=='Registrado')]['Dispositivo_Intervencion'].count()
            vd_presencial_valida_movil = detalle_vd_df[(detalle_vd_df['Dispositivo_Intervencion']=='MOVIL')&(detalle_vd_df['Estado_Intervencion_VD']=='Registrado')]['Dispositivo_Intervencion'].count()
            no_encontrados_total = detalle_vd_df[(detalle_vd_df['Etapa_VD']=='No Encontrado')]['Etapa_VD'].count()
            rechazados_total = detalle_vd_df[(detalle_vd_df['Etapa_VD']=='Rechazado')]['Etapa_VD'].count()
            vd_efectivas_porcentaje = round(((niños_cargados_total-vd_presencial_novalida_total-no_encontrados_total-rechazados_total)/niños_cargados_total)*100,1)
            vd_movil_porcentaje = round((vd_presencial_valida_movil/vd_presencial_valida_total)*100,1)
            
            total_vd_presencial.append(vd_presencial_total)
            total_vd_presencial_validas.append(vd_presencial_valida_total)
            total_vd_presencial_novalidas.append(vd_presencial_novalida_total)
            total_vd_presencial_validas_web.append(vd_presencial_valida_web)
            total_vd_presencial_validas_movil.append(vd_presencial_valida_movil)
            total_no_encontrados.append(no_encontrados_total)
            total_rechazados.append(rechazados_total)

            porcentaje_vd_efectivas.append(vd_efectivas_porcentaje)
            porcentaje_vd_movil.append(vd_movil_porcentaje)
            dict_table = {
                'Periodo' : periodos,
                '3-5 Meses' :total_niños_cargados,
                'Total de Niños Asignados' : total_niños_asignados,
                'Total de VD Completas' : total_vd_completas,
                'Total VD Presencial' : total_vd_presencial,
                'Total VD Presencial Válidas' : total_vd_presencial_validas,
                'Total VD Presencial No Válidas' : total_vd_presencial_novalidas,
                'Total VD Presencial por WEB' : total_vd_presencial_validas_web,
                'Total VD Presencial por MOVIL' : total_vd_presencial_validas_movil,
                'No Encontrados' : total_no_encontrados,
                'Rechazados' : total_rechazados,
                '% VD Efectivas':porcentaje_vd_efectivas,
                '% VD Georreferencia':porcentaje_vd_movil
            }
            dff = pd.DataFrame(dict_table)
        value_total_efectivas_vd = dff['% VD Efectivas'].sum()
        value_promedio_efectivas_vd = round(dff['% VD Efectivas'].mean(),1)
            
        value_total_geo_vd = dff['% VD Georreferencia'].sum()
            
        
        dff.loc['TOTAL',:]= dff.sum(numeric_only=True, axis=0)  
        dff=dff.fillna('TOTAL')
        dff['% VD Efectivas']=dff['% VD Efectivas'].replace({value_total_efectivas_vd: value_promedio_efectivas_vd})
            
        #
        
        
        
        value_geo_vd = round((dff['Total VD Presencial por MOVIL'].unique()[-1]/dff['Total VD Presencial'].unique()[-1])*100,1)    
        dff['% VD Georreferencia']=dff['% VD Georreferencia'].replace({value_total_geo_vd: value_geo_vd})
        return dff
    app = DjangoDash('dashboard-seguimiento-indicadores',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
        Row([
            Column([
                Column([title(content='Seguimiento de Visitas Domiciliarias Realizadas',order=1)])
            ])
        ]),
        Row([
            Column([
                multiSelect(id='multiselect-periodo',data=periodos,value = periodos,size='sm')
                #Div(id='table-resultados')
            ],size = 6)
        ]),
        Row([
            Column([
                #table_dag(df =  table_periodos())
                Div(id='table-resultados')
            ])
        ]),
        Row([
            Column([
                Div(id='table-consecutivo',)
                #loadingOverlay(cardGraph(id_graph = 'bar-eess', id_maximize = 'maximize-bar-eess',height=400))
            ],size=8),
            #Column([
            #    loadingOverlay(cardGraph(id_graph = 'bar-finanzas-ubruta', id_maximize = 'maximize-bar-finanzas-ubruta',height=400))
            #],size=4),
            Column([
                loadingOverlay(cardGraph(id_graph = 'map-vd', id_maximize = 'maximize-map-vd',height=400))
            ],size=4)
        ])
        
    ])
    
    @app.callback(
                Output('table-resultados', 'children'),
                
                Input('multiselect-periodo', 'value'),
                )
    def update_data_resultados(periodos):
        if periodos == None or periodos == []:
            all_vd_df = vd_all_cargados_df[vd_all_cargados_df['Periodo_VD'] == periodos]
            detalle_vd_df = vd_detalle_df_bq[vd_detalle_df_bq['Periodo_VD'] == periodos]
        elif periodos != None:
            all_vd_df = vd_all_cargados_df[vd_all_cargados_df['Periodo_VD'].isin(periodos)]
            detalle_vd_df = vd_detalle_df_bq[vd_detalle_df_bq['Periodo_VD'].isin(periodos)]
        
        resultados_df =table_periodos(dataframe_all_data = all_vd_df, dataframe_detalle_vd = detalle_vd_df)
        #resultados_df.to_excel('resultados_c1.xlsx')
        return table_dag(df =  resultados_df)
    
    @app.callback(
                Output('map-vd', 'figure'),
                Output('table-consecutivo','children'),
                
                Input('multiselect-periodo', 'value'),
                )
    def update_data_resultados(periodos):
        if periodos == None or periodos == []:
            all_vd_df = vd_all_cargados_df[vd_all_cargados_df['Periodo_VD'] == periodos]
            detalle_vd_df = vd_detalle_df_bq[vd_detalle_df_bq['Periodo_VD'] == periodos]
        elif periodos != None:
            all_vd_df = vd_all_cargados_df[vd_all_cargados_df['Periodo_VD'].isin(periodos)]
            
            detalle_vd_df = vd_detalle_df_bq[vd_detalle_df_bq['Periodo_VD'].isin(periodos)]
        #Total de Niños Asignados
        #Total de VD Completas
        print(all_vd_df.columns)
        detalle_vd_df['Latitud_Intervencion']=detalle_vd_df['Latitud_Intervencion'].fillna(0)
        detalle_vd_df['Longitud_Intervencion']=detalle_vd_df['Longitud_Intervencion'].fillna(0)
        geo_df = detalle_vd_df[detalle_vd_df['Latitud_Intervencion']!= 0]
        fig = px.scatter_mapbox(
                    geo_df,
                    lat="Latitud_Intervencion",
                    lon="Longitud_Intervencion",
                    hover_name="Establecimito_Salud_Meta",
                    hover_data=["Actor_Social", "Nombres_del_Nino"],
                    #color_discrete_map =dict_eess,
                    zoom=12,
                    height=400,
                )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        
        numVD_df = all_vd_df.groupby(['Numero_Doc_Nino'])[['Numero_de_Visitas_Completas']].sum().reset_index()
        numVD_validas_df = detalle_vd_df.groupby(['Numero_Doc_Nino','Periodo_VD'])[['VD_Valida']].sum().reset_index()
        pivot_vd_dff = numVD_validas_df.pivot_table(index=('Numero_Doc_Nino'),values=('VD_Valida'),columns='Periodo_VD').reset_index().fillna(0)
        dff_pivot = pivot_vd_dff.merge(numVD_df,how ='inner',on = ['Numero_Doc_Nino'])
        dff_pivot['Total_VD_REALIZADAS'] = (pivot_vd_dff[list(dff_pivot.columns[1:-1])].sum(axis=1))
        def comparador_n_vd(x,y):
            if x == y:
                return 'Es VD Consecutiva'
            else:
                return 'No es VD Consecutiva'
        dff_pivot['ESTADO_CONSECUTIVO'] = dff_pivot.apply(lambda x: comparador_n_vd(x['Numero_de_Visitas_Completas'], x['Total_VD_REALIZADAS']),axis=1)
        test_dfff = dff_pivot[dff_pivot['ESTADO_CONSECUTIVO'] == 'No es VD Consecutiva']
        table_ddd= html.Div(children=[dag.AgGrid(
                        id="table-dag-resultados",
                        rowData=test_dfff.to_dict("records"),
                        columnDefs=[{"field": i,} for i in test_dfff.columns],#"cellStyle": {'font-size': 18}
                        defaultColDef = {
                            "resizable": True,
                            "initialWidth": 130,
                            "wrapHeaderText": True,
                            "autoHeaderHeight": True,
                        },
                        #rowClassRules={"bg-primary fw-bold": "['TOTAL'].includes(params.data.Periodo)"},
                        className="ag-theme-alpine headers1",
                        #dashGridOptions = {"domLayout": "autoHeight"},
                        #getRowId="params.data.State",
                        columnSize="sizeToFit",
                        style={"height": 400}
                    )])
        return fig, table_ddd