from django_plotly_dash import DjangoDash
import pandas as pd
import base64
import io

from ..constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS,COLUMNAS_COMPROMISO_1,EESS_TRUJILLO
from ..utils.frames import *
from ..utils.components import *
from dash import *
import dash_mantine_components as dmc
from ..data.transformacion import clean_columns_padron,clean_columns_c1,clean_VD_detalle
from ..utils.table import table_dag
from ..data.ingesta import cargarDataPadron,cargarDataCargaVD,cargarDataVDetalle

def modal_child(estado = 'positivo',href = "/"):
        if estado == 'positivo':
            out =[
                dmc.Text("Guardado"),
                dmc.Space(h=20),
                dmc.Group(
                    [
                    html.A(dmc.Button("Continuar"),href=href,id='link'),

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
    
indicaciones_pnominal = dmc.List(
                        icon=dmc.ThemeIcon(
                            DashIconify(icon="radix-icons:check-circled", width=16),
                            radius="xl",
                            color="teal",
                            size=24,
                        ),
                        size="sm",
                        spacing="sm",
                        children=[
                            dmc.ListItem("Coordinar con el Responsable del Padrón Nominal"),
                            dmc.ListItem("Solicitar los reportes de todos los Niños del Padrón Nominal"),
                            dmc.ListItem("El primer reporte es de todos los niños sin observaciones"),
                            dmc.ListItem("El segundo reporte es de todos los niños observados"),
                            dmc.ListItem("Esos reportes se ingresan por separado en cada upload"),
                            
                        ],
                    )


PNOMINAL_TAB = Row([
                                        Column([
                                        html.Div([
                                                dmc.Card(
                                                    children=[
                                                        dmc.CardSection(
                                                            dmc.Group(
                                                                children=[
                                                                    dmc.Text("Ingestar Datos del Padrón Nominal", weight=500, align = 'center'),
                                                                    
                                                                ],
                                                                position="apart",
                                                            ),
                                                            withBorder=True,
                                                            inheritPadding=True,
                                                            py="xs",
                                                        ),
                                                        dmc.CardSection(
                                                            dmc.Grid(
                                                                children=[
                                                                    dmc.Col(upload(upload_id='upload-data-padron-1',stack_id='content-padron-1',text_btn = 'Seleccione Archivo (1) del Padrón Nominal'), span=6),
                                                                    dmc.Col(dmc.TextInput(id='text-lastdate-padron',label="",disabled=True,size='md'), span=6),
                                                                    dmc.Col(upload(upload_id='upload-data-padron-2',stack_id='content-padron-2', text_btn = 'Seleccione Archivo (2) del Padrón Nominal'), span=6),
                                                                    dmc.Col(dmc.TextInput(id='text-lastdate-padron-1',label="",disabled=True,size='md'), span=6),
                                                                    #
                                                                    dmc.Col(span="auto"),
                                                                    dmc.Col(button(text = 'Guardar', id = 'btn-guardar-data-pnominal',fullwidth=True), span=6),
                                                                    dmc.Col(span="auto"),
                                                                    dmc.Modal(
                                                                            title="Alerta",
                                                                            id="modal-alerta-pn",
                                                                            zIndex=10000,
                                                                        
                                                                    ),
                                                                
                                                                ],
                                                                gutter="xl",
                                                            ),
                                                            withBorder=True,
                                                            inheritPadding=True,
                                                            py="xs",
                                                        ),
                                                        
                                                        
                                                    
                                                    ],
                                                    withBorder=True,
                                                    shadow="sm",
                                                    radius="md",
                                                    #style={'padding': "0px", 'height':300}
                                                            
                                                )
                                            ]),
                                        #indicaciones_pnominal,  
                                        ]) 
                                    ]), 


C1_TAB = Row([
                                        Column([
                                        
                                        html.Div([
                                                dmc.Card(
                                                    children=[
                                                        dmc.CardSection(
                                                            dmc.Group(
                                                                children=[
                                                                    dmc.Text("Ingestar Carga de Niños", weight=500, align = 'center'),
                                                                    
                                                                ],
                                                                position="apart",
                                                            ),
                                                            withBorder=True,
                                                            inheritPadding=True,
                                                            py="xs",
                                                        ),
                                                        dmc.CardSection(
                                                            dmc.Grid(
                                                                children=[
                                                                    dmc.Col(upload(upload_id='upload-carga',stack_id='content-carga',text_btn= 'Seleccione Archivo de Carga de Niños'), span=6),
                                                                    dmc.Col(dmc.TextInput(id='text-data-upload-carga',label="",disabled=True,size='md'), span=6),
                                                                    
                                                                    #
                                                                    dmc.Col(span="auto"),
                                                                    dmc.Col(button(text = 'Guardar', id = 'btn-guardar-data-carga',fullwidth=True), span=6),
                                                                    dmc.Col(span="auto"),
                                                                    dmc.Modal(
                                                                            title="Alerta",
                                                                            id="modal-alerta-c1",
                                                                            zIndex=10000,
                                                                        
                                                                    ),
                                                                
                                                                ],
                                                                gutter="xl",
                                                            ),
                                                            withBorder=True,
                                                            inheritPadding=True,
                                                            py="xs",
                                                        ),
                                                        
                                                        
                                                    
                                                    ],
                                                    withBorder=True,
                                                    shadow="sm",
                                                    radius="md",
                                                    #style={'padding': "0px", 'height':300}
                                                            
                                                )
                                            ])  
                                        ]) 
                                    ]), 


VD_TAB = Row([
                                        Column([
                                        
                                        html.Div([
                                                dmc.Card(
                                                    children=[
                                                        dmc.CardSection(
                                                            dmc.Group(
                                                                children=[
                                                                    dmc.Text("Ingestar Visitas Domiciliarias Realizadas", weight=500, align = 'center'),
                                                                    
                                                                ],
                                                                position="apart",
                                                            ),
                                                            withBorder=True,
                                                            inheritPadding=True,
                                                            py="xs",
                                                        ),
                                                        dmc.CardSection(
                                                            dmc.Grid(
                                                                children=[
                                                                    dmc.Col(upload(upload_id='upload-vd',stack_id='content-vd',text_btn= 'Seleccione Archivo de Visitas Domiciliarias'), span=6),
                                                                    dmc.Col(dmc.TextInput(id='text-data-vd',label="",disabled=True,size='md'), span=6),
                                                                    
                                                                    #
                                                                    dmc.Col(span="auto"),
                                                                    dmc.Col(button(text = 'Guardar', id = 'btn-guardar-data-vd',fullwidth=True), span=6),
                                                                    dmc.Col(span="auto"),
                                                                    dmc.Modal(
                                                                            title="Alerta",
                                                                            id="modal-alerta-vdetalle",
                                                                            zIndex=10000,
                                                                        
                                                                    ),
                                                                
                                                                ],
                                                                gutter="xl",
                                                            ),
                                                            withBorder=True,
                                                            inheritPadding=True,
                                                            py="xs",
                                                        ),
                                                        
                                                        
                                                    
                                                    ],
                                                    withBorder=True,
                                                    shadow="sm",
                                                    radius="md",
                                                    #style={'padding': "0px", 'height':300}
                                                            
                                                )
                                            ])  
                                        ]) 
                                    ]), 





def Tabs (rol = 'Administrador'):
    if rol == 'Administrador':
        return dmc.Tabs(
                    value='pnominal',
                    #style = {'background-color':'blue'},
                    children=[
                        
                        dmc.TabsList(
                            position="right",
                            grow=True,
                            children=[
                                dmc.Tab("Padrón Nominal", value="pnominal"),
                                dmc.Tab("Carga de Niños", value="c1"),
                                dmc.Tab("Visitas Domiciliarias", value="vd"),
                                
                            ],
                        ),
                        dmc.TabsPanel(value="pnominal",children=PNOMINAL_TAB),
                        dmc.TabsPanel(value="c1",children=C1_TAB),
                        dmc.TabsPanel(value="vd",children=VD_TAB),
                        # tabs panel below
                    ],
                )
    else:
        return dmc.Tabs(
                    value='pnominal',
                    #style = {'background-color':'blue'},
                    children=[
                        
                        dmc.TabsList(
                            position="right",
                            grow=True,
                            children=[
                                dmc.Tab("Padrón Nominal", value="pnominal"),
                                dmc.Tab("Compromiso 1", value="c1"),
                                
                                
                            ],
                        ),
                        dmc.TabsPanel(value="pnominal",children=PNOMINAL_TAB),
                        dmc.TabsPanel(value="c1",children=C1_TAB),
                        # tabs panel below
                    ],
                )
    




def dash_ingestas():
    app = DjangoDash('ingesta-any',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/assets/css/dashstyle.css" })
    app.layout = Content([
        Row([
            Column([title(content='Ingesta de Datos',order=1)]) 
        ]), 
        Row([
            Column([
                Tabs()
            ]) 
        ]),
        Store(id='data-value'),
        Store(id='data-c1-value'),
        Store(id='data-vd-value') 
    ])
    @app.callback(
                Output('text-lastdate-padron', 'value'),
                Output('text-lastdate-padron-1', 'value'),
                Output('data-value','data'),
                Input('upload-data-padron-1', 'contents'),
                Input('upload-data-padron-2', 'contents'),
                #Input('btn-guardar-data','n_clicks')
                
                )
    def update_pnominal(upload_1, upload_2):
        #df.to_dict('series'),
        if upload_1 == None and upload_2 == None:
            
            return '', '', None
        elif upload_1 != None and upload_2 == None:
            content_string_1 = upload_1.split(',')[1]
            first_decoded = base64.b64decode(content_string_1)
            primer_df = pd.read_excel(io.BytesIO(first_decoded),skiprows=4)
            df_1 = primer_df.copy()
            df_1 = clean_columns_padron(df_1)
           
            return f"{df_1.shape[0]}",'',df_1.to_dict('series')
        
        elif upload_1 == None and upload_2 != None:
            content_string_2 = upload_2.split(',')[1]
            second_decoded = base64.b64decode(content_string_2)
            segundo_df = pd.read_excel(io.BytesIO(second_decoded),skiprows=4)
            #df_2=clean_padron(segundo_df)
            df_2 = segundo_df.copy()
            df_2 = clean_columns_padron(df_2)
            print('datos lado 2')
            return '',f"{df_2.shape[0]}",df_2.to_dict('series')
        
        elif upload_1 != None and upload_2 != None:
            
            content_string_1 = upload_1.split(',')[1]
            content_string_2 = upload_2.split(',')[1]
            
            first_decoded = base64.b64decode(content_string_1)
            second_decoded = base64.b64decode(content_string_2)
            primer_df = pd.read_excel(io.BytesIO(first_decoded),skiprows=4)
            df_1 = primer_df.copy()
            df_1 = clean_columns_padron(df_1)
            segundo_df = pd.read_excel(io.BytesIO(second_decoded),skiprows=4)
            df_2 = segundo_df.copy()
            df_2 = clean_columns_padron(df_2)
            dff = df_1._append(df_2,ignore_index= True)
            
            return f"{df_1.shape[0]}",f"{df_2.shape[0]}",dff.to_dict('series')
    
    @app.callback(
                Output('modal-alerta-pn', 'opened'),
                Output('modal-alerta-pn', 'children'),
                
                Input('btn-guardar-data-pnominal','n_clicks'),
                State('data-value','data'),
                State('modal-alerta-pn', 'opened'),
                prevent_initial_call=True, 
                )
    def update_save_pn(n_clicks_guardar,data,opened):
                import datetime
                df = pd.DataFrame(data)
                
                if n_clicks_guardar:
                    
                        df['Fecha_Carga'] = datetime.datetime.now()
                        print(df)
                        try:
                            cargarDataPadron(df,None)
                            return True, modal_child()
                        except:
                            return True, modal_child(estado='negativo')
    
    @app.callback(
                Output('text-data-upload-carga', 'value'),
                Output('data-c1-value','data'),
                Input('upload-carga', 'contents'),
                )
    def update_c1(upload):
        if upload == None :
            return '',None
        else:
            content_string_1 = upload.split(',')[1]
            first_decoded = base64.b64decode(content_string_1)
            df = pd.read_excel(io.BytesIO(first_decoded),names = COLUMNAS_COMPROMISO_1)
            dff = clean_columns_c1(df)
            return f"{dff.shape[0]}",dff.to_dict('series')  
    
    @app.callback(
                Output('modal-alerta-c1', 'opened'),
                Output('modal-alerta-c1', 'children'),
                
                Input('btn-guardar-data-carga','n_clicks'),
                State('data-c1-value','data'),
                State('modal-alerta-c1', 'opened'),
                prevent_initial_call=True, 
                )
    def update_save_c1(n_clicks_guardar,data,opened):
                import datetime
                df = pd.DataFrame(data)
                
                if n_clicks_guardar:
                    
                        df['Fecha_Carga'] = datetime.datetime.now()
                        print(df)
                        try:
                            cargarDataCargaVD(df)
                            return True, modal_child()
                        except:
                            return True, modal_child(estado='negativo')
    
    @app.callback(
                Output('text-data-vd', 'value'),
                Output('data-vd-value','data'),
                Input('upload-vd', 'contents'),
                )
    def update_vdetalle(upload):
        if upload == None :
            return '',None
        else:
            content_string_1 = upload.split(',')[1]
            first_decoded = base64.b64decode(content_string_1)
            df = pd.read_excel(io.BytesIO(first_decoded))
            dff = clean_VD_detalle(df)
            return f"{dff.shape[0]}",dff.to_dict('series')
    
    @app.callback(
                Output('modal-alerta-vdetalle', 'opened'),
                Output('modal-alerta-vdetalle', 'children'),
                
                Input('btn-guardar-data-vd','n_clicks'),
                State('data-vd-value','data'),
                State('modal-alerta-vdetalle', 'opened'),
                prevent_initial_call=True, 
                )
    def update_save_c1(n_clicks_guardar,data,opened):
                import datetime
                df = pd.DataFrame(data)
                
                if n_clicks_guardar:
                    
                    df['Fecha_Carga'] = datetime.datetime.now()
                    print(df)
                    try:
                        cargarDataVDetalle(df)
                        return True, modal_child(href='/vd_detalle_resultados')
                    except:
                        return True, modal_child(estado='negativo')  
            