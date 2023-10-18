from django_plotly_dash import DjangoDash
import pandas as pd
from ..constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS,COLUMNAS_COMPROMISO_1,EESS_TRUJILLO
from ..utils.frames import *
from ..utils.components import *
from ..utils.functions import calcular_total_vd
from dash import *
import dash_mantine_components as dmc
from ..data.transformacion import change_columns_vdetalle
from ..utils.table import table_dag
from apps.vd.data.lectura import bq_cvd_reporte_df
from apps.vd.utils.cards import cardGraph
from ..utils.figures import *
from ..utils.global_callback import callback_opened_modal

def dash_indicador_resultados(dff = bq_cvd_reporte_df()):
    vd_detalle_df = change_columns_vdetalle(df = dff)
    
    carga_list = vd_detalle_df['Fecha_Carga'].unique()
    app = DjangoDash('vd_detalle_resultados',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/assets/css/dashstyle.css" })
    app.layout = Container([
        Modal(id="modal-gauge-vd", size= "75%"),
        Modal(id="modal-bar-vd-novalido", size= "95%"),
        Modal(id="modal-linea-vd", size= "95%"),
        Modal(id="modal-bar-registro-vd", size= "95%"),
        Modal(id="modal-bar-dispositivo-vd", size= "95%"),
        Row([
            Column([title(order=1,content='Resultados de las Visitas Domiciliarias Realizadas')],size=12), 
        ]),    
        Row([
            
            Column([
                multiSelect(id='select-eess',texto='Establecimiento de Salud',data=vd_detalle_df['Establecimiento de Salud'].unique(),place='Seleccione EESS')
            ],size=6),
            Column([
                select(id='select-dispositivo',texto='Dispositivo de Intervención',data=vd_detalle_df['Dispositivo Intervención'].unique())
            ],size=3),
            Column([
                select(id='select-reporte-carga', data = dff['Fecha_Carga'].unique(),texto='Fecha de Carga de Fuente de Datos', value= dff['Fecha_Carga'].unique()[-1], clearable=False)
            ],size=3)
            
        ]), 
        Row([
            Column([
                loadingOverlay(cardGraph(id_graph = 'linea-vd', id_maximize = 'maximize-linea-vd',height=300))
            ],size=6),
            Column([
                loadingOverlay(cardGraph(id_graph = 'gauge-vd', id_maximize = 'maximize-gauge-vd',height=300))
            ],size=3),
            Column([
                loadingOverlay(cardGraph(id_graph = 'bar-vd-novalido', id_maximize = 'maximize-bar-vd-novalido',height=300))
            ],size=3),
            
            
        ]), 
        Row([
            Column([
                loadingOverlay(cardGraph(id_graph = 'bar-registro-vd', id_maximize = 'maximize-bar-registro-vd',height=400))
            ],size=6),
            Column([
                loadingOverlay(cardGraph(id_graph = 'bar-dispositivo-vd', id_maximize = 'maximize-bar-dispositivo-vd',height=400))
            ],size=6),
            
        ]), 
        Div(id='notifications-update-data'),
        Store(id='data-values'),
    ])
    @app.callback(               
                #Output('select-eess','data'),
                #Output('select-dispositivo','data'),
                Output('data-values','data'),
                Output("notifications-update-data","children"),
                Input('select-reporte-carga','value'),
                Input('select-eess','value'), 
                Input('select-dispositivo','value'),         
    )
    def update_filters(carga,eess,dispositivo):#
        vd_df = vd_detalle_df[vd_detalle_df['Fecha_Carga']==carga]
        if (eess == None or len(eess) == 0) and dispositivo == None:
            filt_df = vd_df.copy()
        elif eess != None and dispositivo == None:
            filt_df = vd_df[vd_df['Establecimiento de Salud'].isin(eess)]
        elif (eess == None or len(eess) == 0) and dispositivo != None:
            filt_df = vd_df[vd_df['Dispositivo Intervención']==dispositivo]
        elif eess != None and dispositivo != None:
            filt_df = vd_df[(vd_df['Establecimiento de Salud'].isin(eess))&(vd_df['Dispositivo Intervención']==dispositivo)]
        return [
            #[{'label': i, 'value': i} for i in filt_df['Establecimiento de Salud'].unique()],
            #[{'label': i, 'value': i} for i in vd_df['Dispositivo Intervención'].unique()],
            filt_df.to_dict('series'),
            notification(text=f'Se cargaron {len(filt_df)} filas',title='Update')
        ]
    
    @app.callback(               
                Output('gauge-vd','figure'),
                Output('bar-vd-novalido','figure'),
                Output('linea-vd','figure'),
                Output('bar-registro-vd','figure'),
                Output('bar-dispositivo-vd','figure'),
                Input('data-values','data'),        
    )
    def update_graficos(data):
        data_df = pd.DataFrame(data)
        #gauge
        total_vd_realizar = calcular_total_vd(data_df)
        total_vd_validas = data_df['Visita Válida'].sum()
        #bar no val
        vd_detalle_novalidos_df = data_df[data_df['Estado de Visita']!='Registrado']
        no_val_df = vd_detalle_novalidos_df.groupby(['Establecimiento de Salud','Estado de Visita'])[['Visita Válida']].count().reset_index()#['Visita Válida'].sum()
        no_val_df = no_val_df.rename(columns = {'Visita Válida':'Número de Visitas'})
        #linea vd
        fecha_intervencion_df = data_df.groupby(['Periodo de Visita','Fecha de Intervención'])[['Visita Válida']].count().reset_index()#'Establecimiento de Salud',
        fecha_intervencion_df = fecha_intervencion_df.rename(columns = {'Visita Válida':'Número de Visitas'})
        #bar registro
        eess_etapa_df = data_df.groupby(['Establecimiento de Salud','Tipo de Registro'])[['Visita Válida']].count().sort_values('Visita Válida').reset_index()#['VD_Valida'].sum()
        
        eess_etapa_df = eess_etapa_df.rename(columns = {'Visita Válida':'Número de Visitas'})
        #bar disposi
        dispositivo_eess_df = data_df.groupby(['Dispositivo Intervención','Establecimiento de Salud'])[['Visita Válida']].count().sort_values('Visita Válida').reset_index()
        dispositivo_eess_df = dispositivo_eess_df.rename(columns = {'Visita Válida':'Número de Visitas'})
        return [
            gauge_figure(value = total_vd_validas, maximo_value = total_vd_realizar, titulo = 'Número de Visitas Validas Realizadas'),
            figure_bar_px(df = no_val_df ,x='Número de Visitas', y = 'Establecimiento de Salud', color = None, titulo = 'Visitas NO VALIDAS',showticklabels_x=False,bottom=20,top=40,height=300),
            figure_line_px(df = fecha_intervencion_df ,x='Fecha de Intervención', y = 'Número de Visitas', color = None,text='Número de Visitas', titulo = 'Serie de Tiempo de las Visitas Domiciliarias Realizadas',height=300),
            figure_bar_px(df = eess_etapa_df ,x='Número de Visitas', y = 'Establecimiento de Salud', color = 'Tipo de Registro', titulo = 'Estado de Visitas Domiciliarias por Establecimiento de Salud',bottom=30,top=90),
            figure_bar_px(df = dispositivo_eess_df ,x='Número de Visitas', y = 'Establecimiento de Salud', color = 'Dispositivo Intervención', titulo = 'Dispositivo de Intervención de Visita Domiciliaria',bottom=30)
        ]
        create_graph_comercial_segmented(app=app)
    
    callback_opened_modal(app, modal_id="modal-gauge-vd",children_out_id="gauge-vd", id_button="maximize-gauge-vd")
    callback_opened_modal(app, modal_id="modal-bar-vd-novalido",children_out_id="bar-vd-novalido", id_button="maximize-bar-vd-novalido")
    callback_opened_modal(app, modal_id="modal-linea-vd",children_out_id="linea-vd", id_button="maximize-linea-vd")
    callback_opened_modal(app, modal_id="modal-bar-registro-vd",children_out_id="bar-registro-vd", id_button="maximize-bar-registro-vd")
    callback_opened_modal(app, modal_id="modal-bar-dispositivo-vd",children_out_id="bar-dispositivo-vd", id_button="maximize-bar-dispositivo-vd")    
        