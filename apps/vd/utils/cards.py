from dash import dcc,html
import dash_mantine_components as dmc
import plotly.graph_objs as go
from apps.vd.utils.components import actionIcon
from apps.vd.utils.figures import create_graph_empty
from dash_iconify import DashIconify

figure_vacia = create_graph_empty()

def cardGraph(
    id_maximize='id-maximize',
    id_graph='id-graph',
    with_id=True,
    fig=None,
    icon_maximize=True,
    height = 400
):
    if icon_maximize == True:
        #padding
        if with_id == True:
            return html.Div([
                dmc.Card(
                                    children=[
                                        actionIcon(id=id_maximize),
                                        #actionIcon(ids=id_download,icono='download'),
                                        dcc.Graph(id=id_graph,figure = figure_vacia)
                                        
                                    ],
                                    withBorder=True,
                                    shadow="sm",
                                    radius="md",
                                    style={'padding': "0px", 'height':height}
                                
                                )
            ])
        elif with_id == False:
            return html.Div([
                dmc.Card(
                                    children=[
                                        actionIcon(id=id_maximize),
                                        #actionIcon(ids=id_download,icono='download'),
                                        dcc.Graph(figure=fig)
                                        
                                    ],
                                    withBorder=True,
                                    shadow="sm",
                                    radius="md",
                                    style={'padding': "0px", 'height':height}
                                )
            ])
    else:
            if with_id == True:
                return html.Div([
                    dmc.Card(
                                        children=[
                                            #actionIcon(ids=id_maximize,style=button_style),
                                            #actionIcon(ids=id_download,icono='download'),
                                            dcc.Graph(id=id_graph,figure = figure_vacia)
                                            
                                        ],
                                        withBorder=True,
                                        shadow="sm",
                                        radius="md",
                                        style={'padding': "0px", 'height':height}
                                    )
                ])
            elif with_id == False:
                return html.Div([
                    dmc.Card(
                                        children=[
                                            #actionIcon(ids=id_maximize,style=button_style),
                                            #actionIcon(ids=id_download,icono='download'),
                                            dcc.Graph(figure = fig)
                                            
                                        ],
                                        withBorder=True,
                                        shadow="sm",
                                        radius="md",
                                        style={'padding': "0px", 'height':height}
                                    )
                ])
                
def cardSection(id_value = '',shadow='xl', radius='md', border =  True, text = '', num = 0, color_text ='white',color_section_title = '#0d6efd',contenido ='numero', content = [], padding_section=5,color_section_content = 'white', icon =''):
    if contenido == 'numero':
            section =  dmc.Text(children=[dmc.Center(children=num,id=id_value)], weight=500, style={"fontSize": 30})
                            
    elif contenido == 'tabla':
            section = content
                        
                    
    return dmc.Card(
            children=[
                dmc.CardSection(
                    children=[
                            
                            dmc.Text(children =[dmc.Center(children=[DashIconify(icon=icon, width=25,className="me-1"),text])] , weight=500, color=color_text),
                    ],
                    withBorder=True,
                    inheritPadding=True,
                    p = 3,
                    style={'backgroundColor':color_section_title},
                    
                    #py="xs",
                    #bg = "blue"
                ),
                dmc.CardSection(children = section,p=padding_section,style={'backgroundColor':color_section_content}),
            ],
            withBorder = border,
            shadow = shadow,
            radius = radius,

        )