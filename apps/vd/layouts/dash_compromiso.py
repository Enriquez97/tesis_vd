from django_plotly_dash import DjangoDash
from apps.vd.constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS
from dash import dcc,html,dash_table, Output, Input, State
import dash_mantine_components as dmc
import base64
import io
import pandas as pd
from apps.vd.data.transformacion import clean_padron
from apps.vd.utils.components import *
from apps.vd.utils.frames import Container,Div, Row ,Column, Store,Content,Modal
from apps.vd.utils.cards import cardGraph
from apps.vd.utils.scraping import descarga_lista_last
import dash_ag_grid as dag
from apps.vd.constans import COLUMNAS_COMPROMISO_1,EESS_TRUJILLO
from apps.vd.data.transformacion import clean_compromiso1_data,clean_columns_c1
import datetime
from apps.vd.data.ingesta import cargarDataCargaVD
from apps.vd.data.lectura import *
import plotly.express as px
from ..utils.functions import completar_segun_periodo,table_periodos
from ..utils.figures import *
    
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

def dashboard_indicadores_vd():
    historico_vd_df = bq_cvd_detalle_df()
    historico_vd_df = historico_vd_df[historico_vd_df['Rango_de_Edad']=='3 - 5 meses']
    historico_cargados_df = bq_historico_carga_vd() 
    historico_cargados_df['Anio_Periodo'] = historico_cargados_df['Anio_Periodo'].astype('string')
    historico_cargados_df['Periodo_VD'] = historico_cargados_df['Anio_Periodo']+'-'+historico_cargados_df['Mes_Periodo']
    historico_cargados_df = historico_cargados_df[historico_cargados_df['Rango_de_Edad']=='3 - 5 meses']
    #historico_vd_dff = completar_segun_periodo(dataframe = cvd_reporte_df, dataframe_historico = historico_vd_df, tipo = 'vd')
    print(historico_vd_df.columns)
    #print(historico_vd_dff.columns)
    periodos = historico_vd_df['Periodo_VD'].unique()
    
    
    app = DjangoDash('dashboard-seguimiento-indicadores',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
        Row([
            Column([
                Column([title(content='Resultados de Visitas Domiciliarias Realizadas (3 a 5 meses)',order=1)])
            ],size=11),
            Column([
                btnDownload()
            ],size=1)
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
                html.Div(children=[dag.AgGrid(
                        id="table-dag-resultados",
                        #rowData=df.to_dict("records"),
                        #columnDefs=[{"field": i,} for i in df.columns],#"cellStyle": {'font-size': 18}
                        defaultColDef = {
                            "resizable": True,
                            "initialWidth": 150,
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
                
            ])
        ]),
        Row([
            Column([
                #Div(id='table-consecutivo',)
                loadingOverlay(cardGraph(id_graph = 'bar-asignados', id_maximize = 'maximize-bar-asignados',height=350))
            ],size=4),
            Column([
                loadingOverlay(cardGraph(id_graph = 'bar-vd-presencial', id_maximize = 'maximize-bar-vd-presencial',height=350))
            ],size=4),
            Column([
                loadingOverlay(cardGraph(id_graph = 'bar-vd-movil', id_maximize = 'maximize-bar-vd-movil',height=350))
            ],size=4)
            
        ]),
        Row([
            Column([
                #Div(id='table-consecutivo',)
                loadingOverlay(cardGraph(id_graph = 'bar-noencontrados', id_maximize = 'maximize-bar-noencontrados',height=350))
            ],size=4),
            Column([
                loadingOverlay(cardGraph(id_graph = 'bar-vd-efectivas', id_maximize = 'maximize-bar-vd-efectivas',height=350))
            ],size=4),
            Column([
                loadingOverlay(cardGraph(id_graph = 'bar-vd-geo', id_maximize = 'maximize-bar-vd-geo',height=350))
            ],size=4)
            
        ]),
        Store(id='data-table'),
        dcc.Download(id="descargar")
        
    ])
    
    @app.callback(
                Output('table-dag-resultados', 'rowData'),
                Output('table-dag-resultados', 'columnDefs'),
                Output('bar-asignados', 'figure'),
                Output('bar-vd-presencial','figure'),
                Output('bar-vd-movil','figure'),
                Output('bar-noencontrados','figure'),
                Output('bar-vd-efectivas','figure'),
                Output('bar-vd-geo','figure'),
                Output('data-table','data'),
                Input('multiselect-periodo', 'value'),
                )
    def update_data_resultados(periodos):
        if periodos == None or periodos == []:
            cargados_all_df = historico_cargados_df[historico_cargados_df['Periodo_VD'] == periodos]
            vd_all_df = historico_vd_df[historico_vd_df['Periodo_VD'] == periodos]
        elif periodos != None:
            cargados_all_df = historico_cargados_df[historico_cargados_df['Periodo_VD'].isin(periodos)]
            vd_all_df = historico_vd_df[historico_vd_df['Periodo_VD'].isin(periodos)]
        
        resultados_df =table_periodos(dataframe_all_data = cargados_all_df, dataframe_detalle_vd = vd_all_df)
        resultados_dff = resultados_df[resultados_df['Periodo']!='TOTAL']
        resultados_dff['mes'] = resultados_dff['Periodo'].str[5:]
        resultados_dff['mes_num'] = resultados_dff.apply(lambda x: mes_num(x['mes']),axis=1)
        
        #asignados
        asignados_df = resultados_dff.groupby(['Periodo','mes_num'])[['Total de Niños Asignados']].sum().sort_values('mes_num').reset_index()
        vd_presencial_df = resultados_dff.groupby(['Periodo','mes_num'])[['Total VD Presencial Válidas']].sum().sort_values('mes_num').reset_index()
        vd_movil_df = resultados_dff.groupby(['Periodo','mes_num'])[['Total VD Presencial por MOVIL']].sum().sort_values('mes_num').reset_index()
        noencontrados_df = resultados_dff.groupby(['Periodo','mes_num'])[['No Encontrados']].sum().sort_values('mes_num').reset_index()
        porcentaje_vd_efectivas_df = resultados_dff.groupby(['Periodo','mes_num'])[['% VD Efectivas']].sum().sort_values('mes_num').reset_index()
        porcentaje_vd_geo_df = resultados_dff.groupby(['Periodo','mes_num'])[['% VD Georreferencia']].sum().sort_values('mes_num').reset_index()
        #resultados_df.to_excel('resultados_c1.xlsx')
        return [
                resultados_df.to_dict("records"),
                [{"field": i,"cellStyle": {'font-size': 18}} for i in resultados_df.columns],
                figure_bar_px(df = asignados_df ,x='Periodo', y = 'Total de Niños Asignados', color = None, titulo = 'Niños Asignados por Periodo',showticklabels_x=True,bottom=20,top=60,height=350, color_list =['#007bff']),
                figure_bar_px(df = vd_presencial_df ,x='Periodo', y = 'Total VD Presencial Válidas', color = None, titulo = 'VD Presenciales Válidas por Periodo',showticklabels_x=True,bottom=20,top=60,height=350, color_list =['#007bff']),
                figure_bar_px(df = vd_movil_df ,x='Periodo', y = 'Total VD Presencial por MOVIL', color = None, titulo = 'VD Presenciales Movil - Periodo',showticklabels_x=True,bottom=20,top=60,height=350, color_list =['#007bff']),
                figure_bar_px(df = noencontrados_df ,x='Periodo', y = 'No Encontrados', color = None, titulo = 'Niños No Encontrados por Periodo',showticklabels_x=True,bottom=20,top=60,height=350, color_list =['#007bff']),
                figure_bar_px(df = porcentaje_vd_efectivas_df ,x='Periodo', y = '% VD Efectivas', color = None, titulo = '% VD Efectivas por Periodo',showticklabels_x=True,bottom=20,top=60,height=350, color_list =['#007bff']),
                figure_bar_px(df = porcentaje_vd_geo_df ,x='Periodo', y = '% VD Georreferencia', color = None, titulo = '% VD Georreferencia por Periodo',showticklabels_x=True,bottom=20,top=60,height=350, color_list =['#007bff']),
                resultados_df.to_dict('series')
        ]
    
    @app.callback(
            
            Output("descargar", "data"),
            Input("data-table","data"),
            Input("btn-download", "n_clicks"),
            prevent_initial_call=True,
            
            )
    def update_download(data,n_clicks_download):
        options=pd.DataFrame(data)
        #options['FECHA'] = options['FECHA'].apply(lambda a: pd.to_datetime(a).date())
        if n_clicks_download:
            return dcc.send_data_frame( options.to_excel, "resultados_c1.xlsx", sheet_name="Sheet_name_1",index =False)
        
            
        
        
    
    
    
    
    @app.callback(
                Output('map-vd', 'figure'),
                Output('table-consecutivo','children'),
                
                Input('multiselect-periodo', 'value'),
                )
    def update_data_resultados(periodos):
        if periodos == None or periodos == []:
            cargados_all_df = historico_cargados_df[historico_cargados_df['Periodo_VD'] == periodos]
            vd_all_df = historico_vd_df[historico_vd_df['Periodo_VD'] == periodos]
        elif periodos != None:
            cargados_all_df = historico_cargados_df[historico_cargados_df['Periodo_VD'].isin(periodos)]
            
            vd_all_df = historico_vd_df[historico_vd_df['Periodo_VD'].isin(periodos)]
        #Total de Niños Asignados
        #Total de VD Completas
        print(vd_all_df.columns)
        vd_all_df['Latitud_Intervencion']=vd_all_df['Latitud_Intervencion'].fillna(0)
        vd_all_df['Longitud_Intervencion']=vd_all_df['Longitud_Intervencion'].fillna(0)
        geo_df = vd_all_df[vd_all_df['Latitud_Intervencion']!= 0]
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

        
        numVD_df = cargados_all_df.groupby(['Numero_Doc_Nino'])[['Numero_de_Visitas_Completas']].sum().reset_index()
        numVD_validas_df = vd_all_df.groupby(['Numero_Doc_Nino','Periodo_VD'])[['VD_Valida']].sum().reset_index()
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