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
                