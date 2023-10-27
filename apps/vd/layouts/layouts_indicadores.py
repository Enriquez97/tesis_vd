from django_plotly_dash import DjangoDash
import pandas as pd
from ..constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS,COLUMNAS_COMPROMISO_1,EESS_TRUJILLO
from ..utils.frames import *
from ..utils.components import *
from ..utils.functions import calcular_total_vd,periodos_list,completar_segun_periodo
from dash import *
import dash_mantine_components as dmc
from ..data.transformacion import change_columns_vdetalle
from ..utils.table import table_dag
from apps.vd.data.lectura import bq_historico_carga_vd,bq_cvd_df,bq_pnominal_df,bq_cvd_reporte_df,bq_cvd_detalle_df
from apps.vd.utils.cards import cardGraph,cardSection
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




def dash_indicador_vd_oportunas():
    #historico
    historico_vd_df=bq_historico_carga_vd()
    vd_carga_dff = bq_cvd_df()
    #
    cvd_detalle_df = bq_cvd_detalle_df()
    cvd_reporte_df = bq_cvd_reporte_df() 
    
    periodos = periodos_list()
    app = DjangoDash('vd_oportunas',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/assets/css/dashstyle.css" })
    app.layout = Container([
        Row([
            Column([
                title(content = 'Seguimiento de Visitas Domiciliarias Oportunas',id = 'ti',order=1) 
            ],size=12),
            
        ]),
        Row([
            
            Column([
                multiSelect(id='select-eess',texto='Establecimiento de Salud',data=cvd_detalle_df['Establecimito_Salud_Meta'].unique(),place='Seleccione EESS')
            ],size=6),
            Column([
                select(id='select-as',texto='Actor Social')
            ],size=4),
            Column([
                select(id='select-periodo',texto='Periodo',data=periodos,value = periodos[-1],clearable=False )
            ],size=2)
            
        ]),
        Row([
            Column([cardSection(text='Total Niños Cargados',radius='xs',id_value='card-total-menores')],size=2),
            Column([cardSection(text='Total Visitas Completas',radius='xs',id_value='card-total-vdc')],size=2),
            Column([cardSection(text='Total Visitas Realizadas Válidas',radius='xs',id_value='card-total-vdrv')],size=2),
            Column([cardSection(text='Porcentaje de Visitas Realizadas',radius='xs',id_value='card-porcentaje-vd')],size=2),
            Column([cardSection(text='Promedio de Visitas por EESS',radius='xs',id_value='card-promedio-eess')],size=2),
            Column([cardSection(text='Promedio de Visitas por AS',radius='xs',id_value='card-promedio-as')],size=2),
            
        ]),
        Row([
            Column([
                Div(id='table-vd',style={'height':340})
            ],size=6),
            Column([
                loadingOverlay(cardGraph(id_graph = 'pie-eess-vd', id_maximize = 'maximize-pie-eess-vd',height=350))
            ],size=3),
            Column([
                 loadingOverlay(cardGraph(id_graph = 'pie-etapa-vd', id_maximize = 'maximize-pie-etapa-vd',height=350))
            ],size=3),
            
            
        ]), 
        Row([
            Column([
                loadingOverlay(cardGraph(id_graph = 'bar-estado-visitas', id_maximize = 'maximize-bar-estado-visitas',height=350))
            ],size=6),
            Column([
                loadingOverlay(cardGraph(id_graph = 'line-vd-st', id_maximize = 'maximize-line-vd-st',height=350))
            ],size=6),
            
            
            
        ]), 
        Div(id='notifications-update-data'),
        Store(id='data-vd-completas'),
        Store(id='data-values'),
    ])
    @app.callback(               
                #Output('select-eess','data'),
                #Output('select-dispositivo','data'),
                Output('select-as','data'),
                Output('data-vd-completas','data'),
                Output('data-values','data'),
                Output("notifications-update-data","children"),
                Input('select-periodo','value'),
                Input('select-eess','value'), 
                Input('select-as','value'),         
    )
    def update_filters(periodo,eess,actor_social):#
        historico_carga_dff = completar_segun_periodo(dataframe = vd_carga_dff, dataframe_historico = historico_vd_df)
        historico_vd_dff = completar_segun_periodo(dataframe = cvd_reporte_df, dataframe_historico = cvd_detalle_df, tipo = 'vd')
        historicof_carga_dff = historico_carga_dff[historico_carga_dff['Mes_Periodo']==periodo]
        historicof_vd_dff = historico_vd_dff[historico_vd_dff['Mes_VD']==periodo]
        
        
        vd_det_as_df=historicof_vd_dff.groupby(['Numero_Doc_Nino','Actor_Social'])[['Rango_de_Edad']].count().reset_index()
        table_num_vd_completas = historicof_carga_dff.groupby(['Numero_Doc_Nino','Establecimito_Salud_Meta'])[['Numero_de_Visitas_Completas']].sum().reset_index()
        table_num_vd_completas = table_num_vd_completas.merge(vd_det_as_df,how ='left', on = 'Numero_Doc_Nino').fillna('No Especificado')
        #vd_df = vd_detalle_df[vd_detalle_df['Fecha_Carga']==carga]
        if (eess == None or len(eess) == 0) and actor_social == None:
            filt_df = historicof_vd_dff.copy()
            filt_table = table_num_vd_completas.copy()
        elif eess != None and actor_social == None:
            filt_df = historicof_vd_dff[historicof_vd_dff['Establecimito_Salud_Meta'].isin(eess)]
            filt_table = table_num_vd_completas[table_num_vd_completas['Establecimito_Salud_Meta'].isin(eess)]
        elif (eess == None or len(eess) == 0) and actor_social != None:
            filt_df = historicof_vd_dff[historicof_vd_dff['Actor_Social']==actor_social]
            filt_table = table_num_vd_completas[table_num_vd_completas['Actor_Social']==actor_social]
        elif eess != None and actor_social != None:
            filt_df = historicof_vd_dff[(historicof_vd_dff['Establecimito_Salud_Meta'].isin(eess))&(historicof_vd_dff['Actor_Social']==actor_social)]
            filt_table = table_num_vd_completas[(table_num_vd_completas['Establecimito_Salud_Meta'].isin(eess))&(table_num_vd_completas['Actor_Social']==actor_social)]
        return [
            [{'label': i, 'value': i} for i in filt_df['Actor_Social'].unique()],
            filt_table.to_dict('series'),
            #[{'label': i, 'value': i} for i in vd_df['Dispositivo Intervención'].unique()],
            filt_df.to_dict('series'),
            notification(text=f'Se cargaron {len(filt_df)} filas',title='Update')
        ]
    
    @app.callback(               
                #Output('select-eess','data'),
                #Output('select-dispositivo','data'),
                Output('card-total-menores','children'),
                Output('card-total-vdc','children'),
                Output('card-total-vdrv','children'),
                Output('card-porcentaje-vd','children'),
                Output('card-promedio-eess','children'),
                Output('card-promedio-as','children'),
                Output('table-vd','children'),
                Output('bar-estado-visitas','figure'),
                Output('pie-eess-vd','figure'),
                Output('pie-etapa-vd','figure'),
                Output('line-vd-st','figure'),
               
                Input('data-vd-completas','data'),
                Input('data-values','data'),       
    )
    def update_data(data_table,data):
        table_num_vd_completas = pd.DataFrame(data_table)
        df = pd.DataFrame(data)
        print(table_num_vd_completas)
        total_ninos_cargados = table_num_vd_completas['Numero_Doc_Nino'].count()
        total_ninos_vd = table_num_vd_completas['Numero_de_Visitas_Completas'].sum()
        total_vd_realizadas = df['VD_Valida'].sum()
        porcentaje = f"{round((total_vd_realizadas/total_ninos_vd)*100)}%"#
        promedio_eess = round(total_vd_realizadas/len(df['Establecimito_Salud_Meta'].unique()))
        promedio_as =round(total_vd_realizadas/ len(df['Actor_Social'].unique()))
        dff_Data_=data_vd(dataframe = df, dataframe_carga = table_num_vd_completas)
        eess_estado_vd_dff=dff_Data_.groupby(['Estado_Visita','Establecimito_Salud_Meta'])[['Numero_visitas_validas']].sum().sort_values('Numero_visitas_validas').reset_index()
        estado_vd_dff=dff_Data_.groupby(['Estado_Visita'])[['Numero_visitas_validas']].sum().reset_index()
        
        etapa_dff = df.groupby(['Etapa_VD'])[['Actor_Social']].count().reset_index()
        etapa_dff = etapa_dff.rename(columns = {'Actor_Social':'Número de Visitas Realizadas'})
        
        st_fecha_inter_df = df.groupby(['Estado_VD','Fecha_Intervencion'])[['Actor_Social']].count().reset_index()
        st_fecha_inter_df =st_fecha_inter_df.rename(columns = {'Actor_Social':'Número de Visitas Realizadas'})
        return [
            total_ninos_cargados,
            total_ninos_vd,
            total_vd_realizadas,
            porcentaje,
            promedio_eess,
            promedio_as,
            table_dag(df=dff_Data_),
            figure_bar_px(df = eess_estado_vd_dff ,x='Numero_visitas_validas', y = 'Establecimito_Salud_Meta', color = 'Estado_Visita', titulo = 'Estado de las Visitas',showticklabels_x=True,bottom=20,top=85,height=350),
            pie_figure(df=estado_vd_dff,
                                label_col='Estado_Visita', 
                                value_col='Numero_visitas_validas',
                                height=350, 
                                showlegend=True,
                                title= 'Estado de las Visitas',
                                textposition = 'inside',
                                list_or_color=px.colors.qualitative.T10
                                ),
            pie_figure(df=etapa_dff,
                                label_col='Etapa_VD', 
                                value_col='Número de Visitas Realizadas',
                                height=350, 
                                showlegend=False,
                                title= 'Tipo de Visita',
                                textposition = 'inside',
                                list_or_color=px.colors.qualitative.T10,
                                
                                ),
            figure_line_px(df = st_fecha_inter_df ,x='Fecha_Intervencion', y = 'Número de Visitas Realizadas', color = 'Estado_VD',text='Número de Visitas Realizadas', titulo = 'Serie de Tiempo de las Visitas Domiciliarias Realizadas',height=350,top=85)
        ]

def dash_indicador_vd_consecutivas():
    #historico
    historico_vd_df=bq_historico_carga_vd()
    vd_carga_dff = bq_cvd_df()
    #
    cvd_detalle_df = bq_cvd_detalle_df()
    cvd_reporte_df = bq_cvd_reporte_df() 
    
    periodos = periodos_list()
    app = DjangoDash('vd_consecutivas',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/assets/css/dashstyle.css" })
    app.layout = Container([
        Row([
            Column([
                title(content = 'Seguimiento de Visitas Domiciliarias Consecutivas',id = 'ti',order=1) 
            ],size=12),
            
        ]),
        Row([
            
            Column([
                multiSelect(id='select-eess',texto='Establecimiento de Salud',data=cvd_detalle_df['Establecimito_Salud_Meta'].unique(),place='Seleccione EESS')
            ],size=6),
            Column([
                select(id='select-as',texto='Actor Social')
            ],size=4),
            Column([
                select(id='select-periodo',texto='Periodo',data=periodos,clearable=True )
            ],size=2)
            
        ]),
        Row([
            Column([cardSection(text='Total de Niños Evaluados',radius='xs',id_value='card-total-evaluados')],size=2),
            Column([cardSection(text='Total Niños Cargados',radius='xs',id_value='card-total-menores')],size=2),
            Column([cardSection(text='Total Visitas Completas',radius='xs',id_value='card-total-vdc')],size=2),
            Column([cardSection(text='Total Visitas Realizadas Válidas',radius='xs',id_value='card-total-vdrv')],size=2),
            Column([cardSection(text='Porcentaje de Visitas Realizadas',radius='xs',id_value='card-porcentaje-vd')],size=2),
            Column([cardSection(text='Promedio de Visitas por EESS',radius='xs',id_value='card-promedio-eess')],size=2),
            
            
        ]),
        Row([
            
            Column([
                loadingOverlay(cardGraph(id_graph = 'pie-consecutivo', id_maximize = 'maximize-pie-consecutivo',height=350))
            ],size=3),
            Column([
                 #loadingOverlay(cardGraph(id_graph = 'pie-etapa-vd', id_maximize = 'maximize-pie-etapa-vd',height=350))
                 loadingOverlay(cardGraph(id_graph = 'pie-eess_vd', id_maximize = 'maximize-pie-eess_vd',height=350))
            ],size=3),
            Column([
                Div(id='table-vd')
                
            ],size=6),
            
            
        ]),
        Row([
            Column([
                loadingOverlay(cardGraph(id_graph = 'bar-total-vd', id_maximize = 'maximize-bar-total-vd',height=350))
            ],size=6),
            Column([
                #loadingOverlay(cardGraph(id_graph = 'pie-consecutivo', id_maximize = 'maximize-pie-consecutivo',height=350))
            ],size=3),
            Column([
                 
                 #loadingOverlay(cardGraph(id_graph = 'pie-etapa-vd', id_maximize = 'maximize-pie-etapa-vd',height=350))
            ],size=3),
            
            
            
        ]),
        Div(id='notifications-update-data'),
        Store(id='data-vd-completas'),
        Store(id='data-values'),
    ])
    @app.callback(               
                #Output('select-eess','data'),
                #Output('select-dispositivo','data'),
                Output('select-as','data'),
                Output('data-vd-completas','data'),
                Output('data-values','data'),
                Output("notifications-update-data","children"),
                Input('select-periodo','value'),
                Input('select-eess','value'), 
                Input('select-as','value'),         
    )
    def update_filters(periodo,eess,actor_social):#
        historico_carga_dff = completar_segun_periodo(dataframe = vd_carga_dff, dataframe_historico = historico_vd_df)
        historico_vd_dff = completar_segun_periodo(dataframe = cvd_reporte_df, dataframe_historico = cvd_detalle_df, tipo = 'vd')
        if periodo == None:
            historicof_carga_dff = historico_carga_dff.copy()
            historicof_vd_dff = historico_vd_dff.copy()
        else:
            historicof_carga_dff = historico_carga_dff[historico_carga_dff['Mes_Periodo']==periodo]
            historicof_vd_dff = historico_vd_dff[historico_vd_dff['Mes_VD']==periodo]
        
        
        vd_det_as_df=historicof_vd_dff.groupby(['Numero_Doc_Nino','Actor_Social'])[['Rango_de_Edad']].count().reset_index()
        table_num_vd_completas = historicof_carga_dff.groupby(['Numero_Doc_Nino','Establecimito_Salud_Meta'])[['Numero_de_Visitas_Completas']].sum().reset_index()
        table_num_vd_completas = table_num_vd_completas.merge(vd_det_as_df,how ='left', on = 'Numero_Doc_Nino').fillna('No Especificado')
        #vd_df = vd_detalle_df[vd_detalle_df['Fecha_Carga']==carga]
        if (eess == None or len(eess) == 0) and actor_social == None:
            filt_df = historicof_vd_dff.copy()
            filt_table = table_num_vd_completas.copy()
        elif eess != None and actor_social == None:
            filt_df = historicof_vd_dff[historicof_vd_dff['Establecimito_Salud_Meta'].isin(eess)]
            filt_table = table_num_vd_completas[table_num_vd_completas['Establecimito_Salud_Meta'].isin(eess)]
        elif (eess == None or len(eess) == 0) and actor_social != None:
            filt_df = historicof_vd_dff[historicof_vd_dff['Actor_Social']==actor_social]
            filt_table = table_num_vd_completas[table_num_vd_completas['Actor_Social']==actor_social]
        elif eess != None and actor_social != None:
            filt_df = historicof_vd_dff[(historicof_vd_dff['Establecimito_Salud_Meta'].isin(eess))&(historicof_vd_dff['Actor_Social']==actor_social)]
            filt_table = table_num_vd_completas[(table_num_vd_completas['Establecimito_Salud_Meta'].isin(eess))&(table_num_vd_completas['Actor_Social']==actor_social)]
        return [
            [{'label': i, 'value': i} for i in filt_df['Actor_Social'].unique()],
            filt_table.to_dict('series'),
            #[{'label': i, 'value': i} for i in vd_df['Dispositivo Intervención'].unique()],
            filt_df.to_dict('series'),
            notification(text=f'Se cargaron {len(filt_df)} filas',title='Update')
        ]
    @app.callback(               
                
                #
                Output('card-total-evaluados','children'),
                Output('card-total-menores','children'),
                Output('card-total-vdc','children'),
                Output('card-total-vdrv','children'),
                Output('card-porcentaje-vd','children'),
                Output('card-promedio-eess','children'),
                
                Output('table-vd','children'),
                Output('pie-consecutivo','figure'),
                Output('pie-eess_vd','figure'),
                #pie-eess_vd
                Output('bar-total-vd','figure'),
                #Output('pie-eess-vd','figure'),
                #Output('pie-etapa-vd','figure'),
                #Output('line-vd-st','figure'),
               
                Input('data-vd-completas','data'),
                Input('data-values','data'),       
    )
    def update_data(data_table,data):
        table_num_vd_completas = pd.DataFrame(data_table)
        df = pd.DataFrame(data)
        print(table_num_vd_completas)
        total_niños_evaluados = len(table_num_vd_completas['Numero_Doc_Nino'].unique())
        total_ninos_cargados = table_num_vd_completas['Numero_Doc_Nino'].count()
        total_ninos_vd = table_num_vd_completas['Numero_de_Visitas_Completas'].sum()
        total_vd_realizadas = df['VD_Valida'].sum()
        porcentaje = f"{round((total_vd_realizadas/total_ninos_vd)*100)}%"#
        promedio_eess = round(total_vd_realizadas/len(df['Establecimito_Salud_Meta'].unique()))
        
        numVD_df = table_num_vd_completas.groupby(['Numero_Doc_Nino'])[['Numero_de_Visitas_Completas']].sum().reset_index()
        numVD_validas_df = df.groupby(['Numero_Doc_Nino','Periodo_VD'])[['VD_Valida']].sum().reset_index()
        pivot_vd_dff = numVD_validas_df.pivot_table(index=('Numero_Doc_Nino'),values=('VD_Valida'),columns='Periodo_VD').reset_index().fillna(0)
        dff_pivot = pivot_vd_dff.merge(numVD_df,how ='inner',on = ['Numero_Doc_Nino'])
        dff_pivot['Total_VD_REALIZADAS'] = (pivot_vd_dff[list(dff_pivot.columns[1:-1])].sum(axis=1))
        
        
        def comparador_n_vd(x,y):
            if x == y:
                return 'Es VD Consecutiva'
            else:
                return 'No es VD Consecutiva'
        dff_pivot['ESTADO_CONSECUTIVO'] = dff_pivot.apply(lambda x: comparador_n_vd(x['Numero_de_Visitas_Completas'], x['Total_VD_REALIZADAS']),axis=1)
        print(dff_pivot)
        pie_dff_consecutivo = dff_pivot.groupby(['ESTADO_CONSECUTIVO'])[['Total_VD_REALIZADAS']].count().reset_index()
        #dff_Data_=data_vd(dataframe = df, dataframe_carga = table_num_vd_completas)
        #eess_estado_vd_dff=dff_Data_.groupby(['Estado_Visita','Establecimito_Salud_Meta'])[['Numero_visitas_validas']].sum().sort_values('Numero_visitas_validas').reset_index()
        #estado_vd_dff=dff_Data_.groupby(['Estado_Visita'])[['Numero_visitas_validas']].sum().reset_index()
        
        
        #etapa_dff = df.groupby(['Etapa_VD'])[['Actor_Social']].count().reset_index()
        #etapa_dff = etapa_dff.rename(columns = {'Actor_Social':'Número de Visitas Realizadas'})
        
        #st_fecha_inter_df = df.groupby(['Estado_VD','Fecha_Intervencion'])[['Actor_Social']].count().reset_index()
        #st_fecha_inter_df =st_fecha_inter_df.rename(columns = {'Actor_Social':'Número de Visitas Realizadas'})
        print(df.columns)
        vd_df_eess_mes = df.groupby(['Establecimito_Salud_Meta','Mes_VD'])[['Numero_VD']].count().reset_index()
        #'Establecimito_Salud_Meta'])[['Numero_de_Visitas_Completas']]
        eess_dff_visits=table_num_vd_completas.groupby(['Establecimito_Salud_Meta'])[['Numero_de_Visitas_Completas']].count().reset_index()
        return [
            total_niños_evaluados,
            total_ninos_cargados,
            total_ninos_vd,
            total_vd_realizadas,
            porcentaje,
            promedio_eess,
            table_dag(df=dff_pivot),
            pie_figure(df=pie_dff_consecutivo,
                                label_col='ESTADO_CONSECUTIVO', 
                                value_col='Total_VD_REALIZADAS',
                                height=350, 
                                showlegend=True,
                                title= 'Estado de las Visitas Consecutivas',
                                textposition = 'inside',
                                list_or_color=px.colors.qualitative.T10
                                ),
            pie_figure(df=eess_dff_visits,
                                label_col='Establecimito_Salud_Meta', 
                                value_col='Numero_de_Visitas_Completas',
                                height=350, 
                                showlegend=False,
                                title= 'Carga de Niños por EESS',
                                textposition = 'inside',
                                list_or_color=px.colors.qualitative.T10
                                ),
            figure_bar_px(df = vd_df_eess_mes ,x='Numero_VD', y = 'Establecimito_Salud_Meta', color = 'Mes_VD', titulo = 'Número de Visitas por Periodo',showticklabels_x=True,bottom=20,top=85,height=350),
        ]

def dash_indicador_vd_georreferenciadas():
    #historico
    historico_vd_df=bq_historico_carga_vd()
    vd_carga_dff = bq_cvd_df()
    #
    cvd_detalle_df = bq_cvd_detalle_df()
    cvd_reporte_df = bq_cvd_reporte_df() 
    
    periodos = periodos_list()
    app = DjangoDash('vd_geo',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/assets/css/dashstyle.css" })
    app.layout = Container([
        Row([
            Column([
                title(content = 'Seguimiento de Visitas Domiciliarias Georreferenciadas',id = 'ti',order=1) 
            ],size=12),
            
        ]),
        Row([
            
            Column([
                multiSelect(id='select-eess',texto='Establecimiento de Salud',data=cvd_detalle_df['Establecimito_Salud_Meta'].unique(),place='Seleccione EESS')
            ],size=6),
            Column([
                select(id='select-as',texto='Actor Social')
            ],size=4),
            Column([
                select(id='select-periodo',texto='Periodo',data=periodos,clearable=True )
            ],size=2)
            
        ]),
        Row([
            #Column([cardSection(text='Total de Niños Evaluados',radius='xs',id_value='card-total-evaluados')],size=2),
            Column([cardSection(text='Total Niños Cargados',radius='xs',id_value='card-total-cargados')],size=3),
            Column([cardSection(text='Total Visitas Completas',radius='xs',id_value='card-total-vd')],size=3),
            Column([cardSection(text='Total Visitas Georreferenciadas',radius='xs',id_value='card-total-geo')],size=3),
            Column([cardSection(text='% Visitas Georreferenciadas',radius='xs',id_value='card-porcentaje-geo')],size=3),
            #Column([cardSection(text='Total Visitas Realizadas Válidas',radius='xs',id_value='card-total-vdrv')],size=2),
        ]),
        Row([
            Column([
                loadingOverlay(cardGraph(id_graph = 'map-vd', id_maximize = 'maximize-map-vd',height=350))
            ],size=6),
            Column([
                loadingOverlay(cardGraph(id_graph = 'bar-vd-dispositivo', id_maximize = 'maximize-bar-vd-dispositivo',height=350))
            ],size=3),
            Column([
                 loadingOverlay(cardGraph(id_graph = 'pie-etapa-vd', id_maximize = 'maximize-pie-etapa-vd',height=350))
            ],size=3),
        ]),
    ])
    @app.callback(               
                #Output('select-eess','data'),
                #Output('select-dispositivo','data'),
                Output('select-as','data'),
                Output('data-vd-completas','data'),
                Output('data-values','data'),
                Output("notifications-update-data","children"),
                Input('select-periodo','value'),
                Input('select-eess','value'), 
                Input('select-as','value'),         
    )
    def update_filters(periodo,eess,actor_social):#
        historico_carga_dff = completar_segun_periodo(dataframe = vd_carga_dff, dataframe_historico = historico_vd_df)
        historico_vd_dff = completar_segun_periodo(dataframe = cvd_reporte_df, dataframe_historico = cvd_detalle_df, tipo = 'vd')
        if periodo == None:
            historicof_carga_dff = historico_carga_dff.copy()
            historicof_vd_dff = historico_vd_dff.copy()
        else:
            historicof_carga_dff = historico_carga_dff[historico_carga_dff['Mes_Periodo']==periodo]
            historicof_vd_dff = historico_vd_dff[historico_vd_dff['Mes_VD']==periodo]
        
        
        vd_det_as_df=historicof_vd_dff.groupby(['Numero_Doc_Nino','Actor_Social'])[['Rango_de_Edad']].count().reset_index()
        table_num_vd_completas = historicof_carga_dff.groupby(['Numero_Doc_Nino','Establecimito_Salud_Meta'])[['Numero_de_Visitas_Completas']].sum().reset_index()
        table_num_vd_completas = table_num_vd_completas.merge(vd_det_as_df,how ='left', on = 'Numero_Doc_Nino').fillna('No Especificado')
        #vd_df = vd_detalle_df[vd_detalle_df['Fecha_Carga']==carga]
        if (eess == None or len(eess) == 0) and actor_social == None:
            filt_df = historicof_vd_dff.copy()
            filt_table = table_num_vd_completas.copy()
        elif eess != None and actor_social == None:
            filt_df = historicof_vd_dff[historicof_vd_dff['Establecimito_Salud_Meta'].isin(eess)]
            filt_table = table_num_vd_completas[table_num_vd_completas['Establecimito_Salud_Meta'].isin(eess)]
        elif (eess == None or len(eess) == 0) and actor_social != None:
            filt_df = historicof_vd_dff[historicof_vd_dff['Actor_Social']==actor_social]
            filt_table = table_num_vd_completas[table_num_vd_completas['Actor_Social']==actor_social]
        elif eess != None and actor_social != None:
            filt_df = historicof_vd_dff[(historicof_vd_dff['Establecimito_Salud_Meta'].isin(eess))&(historicof_vd_dff['Actor_Social']==actor_social)]
            filt_table = table_num_vd_completas[(table_num_vd_completas['Establecimito_Salud_Meta'].isin(eess))&(table_num_vd_completas['Actor_Social']==actor_social)]
        return [
            [{'label': i, 'value': i} for i in filt_df['Actor_Social'].unique()],
            filt_table.to_dict('series'),
            #[{'label': i, 'value': i} for i in vd_df['Dispositivo Intervención'].unique()],
            filt_df.to_dict('series'),
            notification(text=f'Se cargaron {len(filt_df)} filas',title='Update')
        ]
    @app.callback(               
                
                #
                Output('card-total-cargados','children'),
                Output('card-total-vd','children'),
                Output('card-total-geo','children'),
                Output('card-porcentaje-geo','children'),
                
                
                #Output('map-vd','figure'),
                #$Output('pie-consecutivo','figure'),
                #Output('pie-eess_vd','figure'),
                
                
               
                Input('data-vd-completas','data'),
                Input('data-values','data'),       
    )
    def update_data(data_table,data):
        table_num_vd_completas = pd.DataFrame(data_table)
        df = pd.DataFrame(data)
        print(table_num_vd_completas)
        
        total_ninos_cargados = table_num_vd_completas['Numero_Doc_Nino'].count()
        total_ninos_vd = table_num_vd_completas['Numero_de_Visitas_Completas'].sum()
        
        total_vd_realizadas = df['VD_Valida'].sum()
        total_geo = df[(df['Dispositivo_Intervencion']=='MOVIL')&(df['Estado_Intervencion_VD']=='Registrado')]['Dispositivo_Intervencion'].count()
        porcentaje = f"{round((total_geo/total_vd_realizadas)*100)}%"#
        #promedio_eess = round(total_vd_realizadas/len(df['Establecimito_Salud_Meta'].unique()))
        df['Latitud_Intervencion']=df['Latitud_Intervencion'].fillna(0)
        df['Longitud_Intervencion']=df['Longitud_Intervencion'].fillna(0)
        geo_df = df[df['Latitud_Intervencion']!= 0]
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
        
        return[
            total_ninos_cargados,
            total_ninos_vd,
            total_geo,
            porcentaje,
            #fig
        ]