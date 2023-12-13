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
from ..data.ingesta import *
from ..data.lectura import *

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
        elif estado == 'existe':
            out =[
                dmc.Text("El periodo ya esta ingestado o pocos registros validos"),
                
                dmc.Space(h=20),
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
                                #dmc.Tab("Visitas Domiciliarias Finalizadas", value="hvd"),
                                
                            ],
                        ),
                        dmc.TabsPanel(value="pnominal",children=PNOMINAL_TAB),
                        dmc.TabsPanel(value="c1",children=C1_TAB),
                        dmc.TabsPanel(value="vd",children=VD_TAB),
                        #dmc.TabsPanel(value="hvd",children=VD_HISTORICO),
                        # tabs panel below
                    ],
                )#VD_HISTORICO
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
        Store(id='data-vd-value'), 
        Store(id='data-hvd-value'),
    ])
    @app.callback(
                Output('text-lastdate-padron', 'value'),
                Output('text-lastdate-padron-1', 'value'),
                Output('data-value','data'),
                Input('upload-data-padron-1', 'contents'),
                Input('upload-data-padron-2', 'contents'),
                )
    def update_pnominal(upload_1, upload_2):
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
            df_2 = segundo_df.copy()
            df_2 = clean_columns_padron(df_2)
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
                try:
                    ingestaBq(dataframe = df, table = 'pnominal')
                    return True, modal_child(href='/padron')
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
                df['Celular_madre_C'] = df['Celular_madre_C'].astype('string')
                if n_clicks_guardar:
                    try:
                        df['Fecha_Carga'] = datetime.datetime.now()
                        ingestaBq(dataframe = df, table = 'cvd')
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
            try:
                ingestaBq(dataframe = df, table = 'cvd_detalle_reporte')
                return True, modal_child(href='/vd_detalle_resultados')
            except:
                return True, modal_child(estado='negativo')  

CARGA_HISTORICO= Row([
                    Column([
                                        
                        html.Div([
                            dmc.Card(
                                children=[
                                    dmc.CardSection(
                                        dmc.Group(
                                            children=[
                                                dmc.Text("Ingestar Carga de Periodo Terminado", weight=500, align = 'center'),
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
                                                dmc.Col(upload(upload_id='upload-hc',stack_id='content-hc',text_btn= 'Seleccione Archivo de Carga'), span=6),
                                                dmc.Col(dmc.TextInput(id='text-data-hc',label="",disabled=True,size='md'), span=6),
                                                dmc.Col(span="auto"),
                                                dmc.Col(button(text = 'Guardar', id = 'btn-guardar-data-hc',fullwidth=True), span=6),
                                                dmc.Col(span="auto"),
                                                dmc.Modal(
                                                    title="Alerta",
                                                    id="modal-alerta-hc",
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
                            )
                        ])  
                     ]) 
                 ]), 

VD_HISTORICO= Row([
                    Column([
                                        
                        html.Div([
                            dmc.Card(
                                children=[
                                    dmc.CardSection(
                                        dmc.Group(
                                            children=[
                                                dmc.Text("Ingestar Visitas Realizadas de Periodo Terminado", weight=500, align = 'center'),
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
                                                dmc.Col(upload(upload_id='upload-hvd',stack_id='content-hvd',text_btn= 'Seleccione Archivo de Visitas Realizadas'), span=6),
                                                dmc.Col(dmc.TextInput(id='text-data-hvd',label="",disabled=True,size='md'), span=6),
                                                dmc.Col(span="auto"),
                                                dmc.Col(button(text = 'Guardar', id = 'btn-guardar-data-hvd',fullwidth=True), span=6),
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
                            )
                        ])  
                     ]) 
                 ]), 


def Tabs_adm ():
    
        return dmc.Tabs(
                    value='hc',
                    #style = {'background-color':'blue'},
                    children=[
                        
                        dmc.TabsList(
                            position="right",
                            grow=True,
                            children=[
                                dmc.Tab("Termino de Periodo - Carga", value="hc"),
                                dmc.Tab("Termino de Periodo - Visitas Realizadas", value="hvd"),
                                
                            ],
                        ),
                        dmc.TabsPanel(value="hc",children=CARGA_HISTORICO),
                        dmc.TabsPanel(value="hvd",children=VD_HISTORICO),
                        # tabs panel below
                    ],
                )#VD_HISTORICO
        
def dash_ingesta_periodo():
    app = DjangoDash('ingesta',external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.css.append_css({ "external_url" : "/static/assets/css/dashstyle.css" })
    app.layout = Content([
        Row([
            Column([title(content='Ingesta de Datos al Termino de Periodo',order=1)]) 
        ]), 
        Row([
            Column([
                Tabs_adm()
            ]) 
        ]),
        
        Store(id='data-hc-value'), 
        Store(id='data-hvd-value'),
    ])
    @app.callback(
                Output('text-data-hc', 'value'),
                Output('data-hc-value','data'),
                Input('upload-hc', 'contents'),
                )
    def update_historico_carga(upload):
        if upload == None :
            return '',None
        else:
            content_string_1 = upload.split(',')[1]
            first_decoded = base64.b64decode(content_string_1)
            df = pd.read_excel(io.BytesIO(first_decoded),names = COLUMNAS_COMPROMISO_1)
            dff = clean_columns_c1(df)
            mes_periodo = dff['Mes_Periodo'].unique()[0]
            anio_periodo = dff['Anio_Periodo'].unique()[0]
            cantidad_rows = dff.shape[0]
            string_text = f"{mes_periodo}-{anio_periodo} - rows: {cantidad_rows}"
            return string_text,dff.to_dict('series')
    
    @app.callback(
                Output('modal-alerta-hc', 'opened'),
                Output('modal-alerta-hc', 'children'),
                
                Input('btn-guardar-data-hc','n_clicks'),
                State('data-hc-value','data'),
                State('modal-alerta-hc', 'opened'),
                prevent_initial_call=True, 
                )
    def update_save_historico_cargo(n_clicks_guardar,data,opened):
            
                dff = pd.DataFrame(data)
                num_pinta = dff[dff['Pinta']==True]['Pinta'].count()
                print(dff)
                if n_clicks_guardar:
                        #try:
                            mes_periodo = dff['Mes_Periodo'].unique()[0]
                            periodos_h =bq_periodos_historico_carga()
                            print(periodos_h)
                            lista_periodos = list(periodos_h['Mes_Periodo'])
                            print(lista_periodos)
                            var_condi = mes_periodo in lista_periodos
                            if var_condi == False and num_pinta >500:
                                #historial_vd_cargados
                                ingestaBq(dataframe = dff, table = 'historial_vd_cargados')

                                return True, modal_child()
                            #else:
                            #   return True, modal_child(estado = 'existe')
                                
                        #except:
                        #    return True, modal_child(estado='negativo')
    
    @app.callback(
                Output('text-data-hvd', 'value'),
                Output('data-hvd-value','data'),
                Input('upload-hvd', 'contents'),
                )
    def update_historico_vd(upload):
        if upload == None :
            return '',None
        else:
            content_string_1 = upload.split(',')[1]
            first_decoded = base64.b64decode(content_string_1)
            df = pd.read_excel(io.BytesIO(first_decoded))
            dff = clean_VD_detalle(df)
            mes_periodo = dff['Mes_VD'].unique()[0]
            anio_periodo = dff['Anio_VD'].unique()[0]
            cantidad_rows = dff.shape[0]
            string_text = f"{mes_periodo}-{anio_periodo} - rows: {cantidad_rows}"
            return string_text,dff.to_dict('series')
    
    @app.callback(
                Output('modal-alerta-vdetalle', 'opened'),
                Output('modal-alerta-vdetalle', 'children'),
                
                Input('btn-guardar-data-hvd','n_clicks'),
                State('data-hvd-value','data'),
                State('modal-alerta-vdetalle', 'opened'),
                prevent_initial_call=True, 
                )
    def update_save_historico_cargo(n_clicks_guardar,data,opened):
            
                dff = pd.DataFrame(data)
                
                
                num_rows=dff['Mes_VD'].count()
                num_rows = int(num_rows)
                if n_clicks_guardar:
                        #try:
                            mes_periodo = dff['Mes_VD'].unique()[0]
                            
                            periodos_h =bq_periodos_historico_vd()
                            
                            lista_periodos = list(periodos_h['Mes_VD'])
                            var_condi = mes_periodo in lista_periodos
                            if var_condi == False and num_rows>1200:
                                ingestaBq(dataframe = dff, table = 'cvd_detalle')
                                return True, modal_child()
                            #else:
                            #   return True, modal_child(estado = 'existe')
                                
                        #except:
                        #    return True, modal_child(estado='negativo')