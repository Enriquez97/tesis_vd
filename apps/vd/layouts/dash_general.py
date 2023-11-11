from django_plotly_dash import DjangoDash
from apps.vd.constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS
from dash import dcc,html,dash_table, Output, Input, State
import plotly.express as px
import dash_mantine_components as dmc
import pandas as pd
from apps.vd.data.transformacion import *
from apps.vd.utils.components import *
from apps.vd.utils.cards import cardSection,cardGraph
from apps.vd.utils.frames import Container,Div, Row ,Column, Store,Content,Download
from apps.vd.data.lectura import *
from apps.vd.data.ingesta import cargarDataVdReporte
from apps.vd.utils.table import table_dag
from apps.vd.utils.figures import bar_go_figure,pie_figure
import datetime
import re

def modal_child(estado = 'positivo'):
        if estado == 'positivo':
            out =[
                dmc.Text("Guardado"),
                dmc.Space(h=20),
                dmc.Group(
                    [
                    html.A(dmc.Button("Continuar"),href="/analisis-report-vd",id='link'),

                    ],
                    position="right",
                ),
            ]
        else:
            out =[
                dmc.Text("Error"),
                dmc.Space(h=20),
                
            ]
        return out
def concated_dataframes(dataframe_padron = pd.DataFrame(), dataframe_c1 = pd.DataFrame()):
    c1_df =dataframe_c1[dataframe_c1['Rango de Edad']=='3 - 5 meses']
    general_df =c1_df.merge(dataframe_padron,how = 'left',left_on=["Número Doc Niño"], right_on=["Documento Padron"])#
    return general_df

def nueva_col_dni(dni_meta, dni_padron):
    if len(dni_meta)!= 0:
        resultado = dni_meta
    elif (len(dni_meta)== 0 or dni_meta=='XXXXXXX') and len(dni_padron)!=0:
        resultado = dni_padron
    return resultado    
    

def dash_concatenar_data():
    """"""
    pnominal_fcarga_bq_df = bq_fcarga_pnominal_df()
    cvd_fcarga_bq_df = bq_fcarga_cvd_df()
    cvd_fcarga_detalle_bq_df =bq_f_carga_cvd_detalle_df()
    #pnominal_bq_df= bq_pnominal_df()
    #cvd_bq_df = bq_cvd_df()
    #cvd_detalle_bq_df = bq_cvd_detalle_df()
    """"""
    """"""
    pnominal_fecha_carga = pnominal_fcarga_bq_df['Fecha_Carga'].unique()
    cvd_fecha_carga = cvd_fcarga_bq_df['Fecha_Carga'].unique()
    periodo_cvd_detalle = cvd_fcarga_detalle_bq_df['Periodo_VD'].unique()
    """"""
    
    app = DjangoDash('concatenar-data',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    
    
    
    app.layout = dmc.Container([
        Row([Column([title(content='Generar Lista para las Visitas Domiciliarias',order=1)],size=12)]),
        Row([
            Column([
                select(id='select-fecha-carga-padron', data=sorted(pnominal_fecha_carga),texto='Datos Cargados Padrón Nominal',value= pnominal_fecha_carga[-1],clearable=False)
            ],size=6),
            Column([
                dmc.TextInput(id='text-lastdate-padron',label="Ultimo Nacido",disabled=True,size='md')
            ],size=6),
        ]),
        Row([
            Column([
                select(id='select-fecha-carga-c1', data=sorted(cvd_fecha_carga), texto='Datos Cargados de VD', value = cvd_fecha_carga[-1],clearable=False)
            ],size=6),
            Column([
                dmc.TextInput(id='text-periodo-vd',label="Periodo",disabled=True,size='md')
            ],size=6),
        ]),
        Row([
            Column([
                select(id='select-historial-vd', data=periodo_cvd_detalle, texto='Historial de VD',value = periodo_cvd_detalle[0],clearable=False)
            ],size=6),
            Column([
                dmc.TextInput(id='text-vd-detalle',label="Número de VD Realizadas",disabled=True,size='md')
            ],size=6),
            
        ]),
        
        Row([Column(Div(id='table-concat'))]),
        
        Row([
            
            Column([
                dmc.Center(button(text = 'Descargar', id = 'btn-download',fullwidth = True,margin={'margin-top':30}))
                
            ],size=6),
            
            
            Column([
                dmc.Center(button(text = 'Guardar', id = 'btn-save',fullwidth = True,margin={'margin-top':30})),
                dmc.Modal(
                        title="Mensaje",
                        id="modal-simple",
                        zIndex=10000,
                    
                    ),
            ],size=6),
        ]),
        
        Store(id='data-values'),
        #Download(),
        dcc.Download(id="descargar")
    ],fluid=False)
    
    @app.callback(
                
                Output('text-lastdate-padron','value'),
                Output('text-periodo-vd','value'),
                Output('text-vd-detalle','value'),
                Output('data-values','data'),
                Output('table-concat','children'),
                #Output('output-data-concat','children'),
                Input('select-fecha-carga-padron',"value"),
                Input('select-fecha-carga-c1',"value"),     
                Input('select-historial-vd',"value"),
                #Input('btn-concatenar','n_clicks'),    
    )
    def update_text_input(filter_pnominal, filter_cvd,filter_vd_detalle):#,btn_concatenar
        #carga padron nominal
        pnominal_bq_df= bq_pnominal_df(query = f"SELECT * FROM `ew-tesis.dataset_tesis.pnominal` WHERE Fecha_Carga ='{filter_pnominal}'")
        #carga de niños cargados en el aplicativo de VD
        cvd_bq_df = bq_cvd_df()
        # carga visitas domiciliarias realizadas
        cvd_detalle_bq_df = bq_cvd_detalle_df()
        
        pnominal_df = pnominal_bq_df[pnominal_bq_df['Fecha_Carga']==filter_pnominal]
        fecha_last_pnominal = str(max(pnominal_df['Fecha_creacion_registro'].unique()))[:10]
        cvd_df = cvd_bq_df[cvd_bq_df['Fecha_Carga']==filter_cvd]
        periodo = str(cvd_df['Periodo_VD'].unique()[0])
        cvd_detalle_df =cvd_detalle_bq_df[cvd_detalle_bq_df['Periodo_VD']==filter_vd_detalle]
        num_vd = cvd_detalle_df['Periodo_VD'].count()
        pnominal_dff = clean_padron(dff = pnominal_df)   
        pnominal_dfff = columns_merge_pnominal(pnominal_dff) 
        cvd_dff = clean_compromiso1_data(cvd_df)
        merge_df = cvd_dff.merge(pnominal_dfff,how = 'left',left_on=["Numero_Doc_Nino"], right_on=["Documento_Padron"])
        merge_dff = clean_data_concat(merge_df)
        estado_vd_anterior_df = etapa_VD_detalle(dataframe = cvd_detalle_df)
        report_dff = merge_dff.merge(estado_vd_anterior_df,how = 'left',left_on=["Numero_Doc_Nino"], right_on=["Numero_Doc_Nino"])
        report_dff['Etapa_VD'] = report_dff['Etapa_VD'].fillna('Niño Nuevo')
        try:
            report_final = eliminar_repetidos(report_dff)
        except:
            report_final = pd.DataFrame()
        return fecha_last_pnominal, periodo, num_vd,report_final.to_dict('series'),table_dag(df =report_final )
    
    @app.callback(               
                Output('descargar','data'),
                Input('btn-download','n_clicks'),
                State('data-values','data'),
                State('select-fecha-carga-c1',"value"), 
                prevent_initial_call=True,  
    )
    def update_download(n_clicks_download,data,periodo):
        
        if n_clicks_download:
            name_file = f"report_vd_{periodo}.xlsx"
            df = pd.DataFrame(data)
            df['Direccion_Nino_C'] = df.apply(lambda x:re.sub(r"[^a-zA-Z0-9]", " ", x['Direccion_Nino_C']),axis=1)
            print(df)
            #ddf = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 1, 5, 6], "c": ["x", "x", "y", "y"]})
            return dcc.send_data_frame(df.to_excel, name_file, sheet_name="Sheet_name_1",index =False)

    
    @app.callback(
                
                Output("modal-simple", "opened"),
                Output("modal-simple", "children"),
                
                Input('btn-save','n_clicks'),
                State('data-values','data'),
                State('text-periodo-vd','value'),    
                
                State("modal-simple", "opened"), 
                prevent_initial_call=True,        
    )
    def update_modal(n_clicks_download,data,periodo,opened):
        fecha_carga = str(datetime.datetime.now())[:19]
        
        name_new_column = f"{periodo}-{fecha_carga}"
        df = pd.DataFrame(data)
        df['Carga'] = name_new_column
        try:
            if n_clicks_download:
                cargarDataVdReporte(df = df)
                return True, modal_child()
        except:
                return True, modal_child(estado='negativo')


def dashboard_reporteVD_():
    """"""
    report_vd_bq_df = bq_reporte_vd_df()
    """"""
    """"""
    carga_list = report_vd_bq_df['Carga'].unique()
    
    """"""
    
    app = DjangoDash('analisis_inicio_vd',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
        Row([
            Column([title(id = 'titulo',content='Análisis de las VD',order=1)],size=9),
            Column([
                
                select(id='select-reporte-carga', data = carga_list,texto='', value= carga_list[-1], clearable=False)
            
            ],size=3),
        
        ]),
        
        Row([
        Column([
             Row([
                 Column([cardSection(text='Total Niños',radius='xs',id_value='card-total-menores')],size=12),
             ]),
             Row([
                 Column([cardSection(text='Actores Sociales',radius='xs',id_value='card-total-as')],size=12)
             ]),
             Row([
                 Column([cardSection(text='No Pertenecen Padrón',radius='xs',id_value='card-total-npn')],size=12),
             ]),
             Row([
                 Column([cardSection(text='Sin Asignar',radius='xs',id_value='card-total-sinasig')],size=12),
             ]),
             Row([
                 Column([cardSection(text='Sin DNI',radius='xs',id_value='card-total-sindni')],size=12),
             ]),
             Row([
                Column([cardSection(text='No Encontrados (Mes Anterior)',radius='xs',id_value='card-total-noencon')],size=12), 
             ]),
        
        ],size=2),
        Column([
            Row([
                Column([
            
                segmented(id='segmented-tipo-eess',value = 'num_niños',
                            data =[
                                {'label':'Cantidad de Niños','value':'num_niños'},
                                {'label':'Cantidad de Visitas','value':'num_vd'},
                            ]
                    ),
                loadingOverlay(cardGraph(id_graph = 'bar-eess', id_maximize = 'maximize-bar-eess',height=450))
            
                 ])
            ]),
            Row([
            Column([
                segmented(id='segmented-eess-pn',value = 'EESS_Ultima_Atencion_General_C',
                            data =[
                                {'label':'EESS Compromiso 1','value':'EESS_Ultima_Atencion_General_C'},
                                {'label':'EESS Nacimiento','value':'EESS_nacimiento_padron'},
                                {'label':'EESS Atención','value':'EESS_atencion_padron'},
                                {'label':'EESS Adscripcion','value':'EESS_adscripcion_padron'},
                            ]
                    ),
                loadingOverlay(cardGraph(id_graph = 'bar-eess-pn', id_maximize = 'maximize-bar-eess-pn',height=350))
            ])
            
            ]),
            
        ],size=4),
        Column([ 
                Row([
                 Column([loadingOverlay(cardGraph(id_graph = 'pie-tipodoc-madre', id_maximize = 'maximize-pie-tipodoc-madre',height=240))],size=6),
                 Column([loadingOverlay(cardGraph(id_graph = 'pie-tipodoc-niño', id_maximize = 'maximize-pie-tipodoc-niño',height=240))],size=6)
                ]),
                Row([
                 Column([loadingOverlay(cardGraph(id_graph = 'pie-entidad-actualiza', id_maximize = 'maximize-pie-entidad-actualiza',height=240))],size=6),
                 Column([loadingOverlay(cardGraph(id_graph = 'pie-etapa-vd', id_maximize = 'maximize-pie-etapa-vd',height=240))],size=6)
                ]),
                Row([
                 Column([Div(id='table-vd')],size=12),
                 
                ]),
                
        ],size=6),

        
        ]),
        
    ])
    @app.callback(               
                Output('bar-eess','figure'),
                
                Input('select-reporte-carga','value'),
                Input('segmented-tipo-eess','value'),
                
    )
    def update_bar_eess(filtro_carga,segmented):
        x_title_bar = 'Número de Niños' if segmented == 'num_niños' else 'Número de Visitas'
        x_title_bar = 'N° DE NIÑOS' if segmented == 'num_niños' else 'N° DE VISITAS'
        dff= report_vd_bq_df[report_vd_bq_df['Carga']==filtro_carga]
        if segmented == 'num_niños':
            
            eess_df = dff.groupby(['Establecimito_Salud_Meta'])[['Numero_de_Visitas_Completas']].count().sort_values('Numero_de_Visitas_Completas').reset_index()
            eess_df['Porcentaje'] = round((eess_df['Numero_de_Visitas_Completas']/eess_df['Numero_de_Visitas_Completas'].sum())*100)
            
        elif segmented == 'num_vd':
            eess_df = dff.groupby(['Establecimito_Salud_Meta'])[['Numero_de_Visitas_Completas']].sum().sort_values('Numero_de_Visitas_Completas').reset_index()
            eess_df['Porcentaje'] = round((eess_df['Numero_de_Visitas_Completas']/eess_df['Numero_de_Visitas_Completas'].sum())*100)
        figure_bar_eess = bar_go_figure(df = eess_df,
                                            x = 'Numero_de_Visitas_Completas',
                                            y = 'Establecimito_Salud_Meta',
                                            orientation='h', 
                                            text='Numero_de_Visitas_Completas',
                                            title="Número de Niños por EESS",
                                            clickmode= True,
                                            xaxis_title= x_title_bar,
                                            customdata=['Porcentaje'],
                                            list_colors='#0d6efd',
                                            height=450
                            )
        return figure_bar_eess
    
    @app.callback(               
                Output('titulo','children'),
                Input('select-reporte-carga','value'),
                Input('bar-eess','selectedData'),
                
    )
    def update_titulo(filtro_carga,bar_eess):
        dff= report_vd_bq_df[report_vd_bq_df['Carga']==filtro_carga]
        periodo = dff['Carga'].unique()[0][:8]
        if bar_eess == None:
            badge_=''
            
        else :
            eess = bar_eess['points'][0]['y']
            badge_=dmc.Badge(eess,variant='dot',color='blue', size='lg',radius="lg")
        return ['Análisis de las VD ']+[badge_,dmc.Badge(periodo,variant='dot',color='blue', size='lg',radius="lg")]
    
    
     
    @app.callback(               
                Output('card-total-menores','children'),
                Output('card-total-as','children'),
                Output('card-total-npn','children'),
                Output('card-total-sinasig','children'),
                Output('card-total-sindni','children'),
                Output('card-total-noencon','children'),
                Output('pie-entidad-actualiza','figure'),
                Output('pie-tipodoc-madre','figure'),
                Output('pie-tipodoc-niño','figure'),
                Output('pie-etapa-vd','figure'),
                Output('table-vd','children'),
                #pie-etapa-vd
               
                Input('select-reporte-carga','value'),
                Input('bar-eess','selectedData'),
                
    )
    def update_cards(filtro_carga,bar_eess):
        if bar_eess == None:
            dff= report_vd_bq_df[report_vd_bq_df['Carga']==filtro_carga]
        else:
            eess = bar_eess['points'][0]['y']
            dff= report_vd_bq_df[(report_vd_bq_df['Carga']==filtro_carga)&(report_vd_bq_df['Establecimito_Salud_Meta']==eess)]
        df = clean_data_report(dff)
        total_menores = df['Numero_Doc_Nino'].count()
        total_as = len(df[df['Actor_Social']!='No Especificado']['Actor_Social'].unique())
        total_npn = df[df['Estado_Padron_Nominal']=='No Pertenece al Padron Nominal']['Tipo_Documento_Padron'].count()
        total_sin_asig = df[df['Establecimito_Salud_Meta']=='No Especificado']['Establecimito_Salud_Meta'].count()
        total_sin_dni = df[(df['Tipo_Documento_Padron']!='DNI')&(df['Estado_Padron_Nominal']!='No Pertenece al Padron Nominal')]['Tipo_Documento_Padron'].count()    
        total_no_en = df[df['Etapa_VD']=='No Encontrado']['Etapa_VD'].count()
        
        entidad_df = df.groupby(['Entidad_Actualiza'])[['Numero_Doc_Nino']].count().reset_index()
        
        figure_pie_entidad = pie_figure(df=entidad_df,
                                label_col='Entidad_Actualiza', 
                                value_col='Numero_Doc_Nino',
                                height=240, 
                                showlegend=True,
                                title= 'Entidad que Actualizó Registros',
                                textposition = 'inside',
                                list_or_color=px.colors.qualitative.T10
                                )
        
        tipodoc_madre_df = df.groupby(['Tipo_doc_madre_padron'])[['Numero_Doc_Nino']].count().reset_index()
        figure_pie_tipodocm = pie_figure(df=tipodoc_madre_df,
                                label_col='Tipo_doc_madre_padron', 
                                value_col='Numero_Doc_Nino',
                                height=240, 
                                showlegend=True,
                                title= 'Tipo de Documento Madre',
                                textposition = 'inside',
                                list_or_color=px.colors.qualitative.Set3
                                )
        
        tipodoc_menor_df = df.groupby(['Tipo_Documento_Padron'])[['Numero_Doc_Nino']].count().reset_index()
        figure_pie_tipodocmenor = pie_figure(df=tipodoc_menor_df,
                                label_col='Tipo_Documento_Padron', 
                                value_col='Numero_Doc_Nino',
                                height=240, 
                                showlegend=True,
                                title= 'Tipo de Documento Niño',
                                textposition = 'inside',
                                list_or_color=px.colors.qualitative.Set3
                                )
        
        etapa_df = df.groupby(['Etapa_VD'])[['Numero_Doc_Nino']].count().reset_index()
        figure_pie_etapa = pie_figure(df=etapa_df,
                                label_col='Etapa_VD', 
                                value_col='Numero_Doc_Nino',
                                height=240, 
                                showlegend=True,
                                title= 'Estado de los Niños Cargados',
                                textposition = 'inside',
                                list_or_color=px.colors.qualitative.T10
                                )
        table_df = df[df['Estado_encontrado']=='SI']
        table_dff = table_df[['Establecimito_Salud_Meta','Actor_Social','Nombres_del_Nino_Padron','Numero_Doc_Nino','Direccion_padron','Referencia_direccion_padron','Estado_encontrado']]
        return total_menores,total_as,total_npn,total_sin_asig,total_sin_dni,total_no_en,figure_pie_entidad,figure_pie_tipodocm,figure_pie_tipodocmenor,figure_pie_etapa,table_dag(df = table_dff )
    
    @app.callback(               
                
                Output('bar-eess-pn','figure'),
                #pie-etapa-vd
                Input('select-reporte-carga','value'),
                Input('bar-eess','selectedData'),
                Input('segmented-eess-pn','value')
                
    )
    def update_bars(filtro_carga,bar_eess,segmented_eess):
        if bar_eess == None:
            dff= report_vd_bq_df[report_vd_bq_df['Carga']==filtro_carga]
        else:
            eess = bar_eess['points'][0]['y']
            dff= report_vd_bq_df[(report_vd_bq_df['Carga']==filtro_carga)&(report_vd_bq_df['Establecimito_Salud_Meta']==eess)]
            
        df = clean_data_report(dff)
        eess_df = df.groupby([segmented_eess])[['Numero_Doc_Nino']].count().sort_values('Numero_Doc_Nino').reset_index()
        eess_dff = eess_df[eess_df['Numero_Doc_Nino']>2]
        return bar_go_figure(   
                                df = eess_dff,
                                x = segmented_eess,
                                y = 'Numero_Doc_Nino',
                                orientation='v', 
                                text='Numero_Doc_Nino',
                                title=segmented_eess,
                                clickmode= True,
                                xaxis_title= '',
                                #customdata=['Porcentaje'],
                                list_colors='#0d6efd',
                                height=350,
                                showticklabel_x = False,
                                space_ticked=40
                            )
        
        