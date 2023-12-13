
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from apps.vd.utils.functions import *

def create_graph_empty(text=''):
    layout = dict(
        autosize=True,
        annotations=[dict(text=text, showarrow=False)],
        #paper_bgcolor="#1c2022",
        #plot_bgcolor="#1c2022",
        #font_color="#A3AAB7",
        font=dict(color="FFFF", size=20),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
    )
    return {"data": [], "layout": layout}

def line_figure(
        df = pd.DataFrame(), x = '', y = '', color = None, height = 360,x_title = '',
        y_title = '', title_legend = '', order = {}, title ='',
        template = 'plotly_white', discrete_color = {}, custom_data=[],
        hover_template = '', size_text = 17, legend_orizontal = True, markers = False,legend_font_size = 12,
        tickfont_x = 11, tickfont_y = 11
    ):
        figure = px.line(
            df, x = x, y = y, color = color , template = template,
            color_discrete_map = discrete_color, 
             hover_name = color,
            custom_data = custom_data,
            markers = markers,
            category_orders=order,
            #color_discrete_sequence  = '#0d6efd'
        )
        figure.update_layout(
            title = f"<b>{title}</b>",
            title_font_family="sans-serif", 
            title_font_size = 18,
            title_font_color = "rgba(0, 0, 0, 0.7)",
            margin = dict( l = 20, r = 40, b = 20, t = 40, pad = 0, autoexpand = True),
            height = height,
            xaxis_title = '<b>'+x_title+'</b>',
            yaxis_title = '<b>'+y_title+'</b>',
            legend_title_text = title_legend,
            legend=dict(font=dict(size=legend_font_size,color="black"))
        )
        figure.update_traces(hovertemplate =hover_template)#,cliponaxis=False
        figure.update_xaxes(tickfont=dict(size=tickfont_x),color='rgba(0, 0, 0, 0.8)',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True) 
        figure.update_yaxes(tickfont=dict(size=tickfont_y),color='rgba(0, 0, 0, 0.8)',showticklabels = True,title_font_family="sans-serif",title_font_size = 13,automargin=True)
        figure.update_layout(hovermode="x unified",hoverlabel=dict(font_size=size_text,font_family="sans-serif",bgcolor='rgba(255,255,255,0.75)'))
        if legend_orizontal == True:
            figure.update_layout(legend=dict(orientation="h",yanchor="bottom",xanchor="right",y=1.02,x=1))
        return figure


def pie_figure(df = pd.DataFrame(),label_col = '', 
             value_col = '',list_or_color = None, dict_color = None,
             title = '', textinfo = 'percent+label+value' , textposition = 'inside',
             height = 400, showlegend = True, color_list = [], textfont_size = 12
             
    ):
        
        figure = go.Figure()
        figure.add_trace(
            go.Pie(labels=df [label_col],values=df[value_col],
                
                marker_colors = list_or_color,
                #hovertemplate='<br><b>'+label_col+': %{labels}</b><br><b>'+value_col+': %{value:,.2f}</b>'
                hoverlabel=dict(font_size=15,bgcolor="white"),
                hovertemplate = "<b>%{label}</b> <br>Porcentaje:<b> %{percent} </b></br>Total: <b>%{value}</b>",
                name='',
                )
        )    

        figure.update_layout(
            title={'text': f"<b>{title}</b>",'y':0.97,'x':0.5,'xanchor': 'center','yanchor': 'top'},
            title_font_family="sans-serif", 
            title_font_size = 18,
            title_font_color = "rgba(0, 0, 0, 0.7)",
        
        )
        figure.update_traces(textposition = textposition, textinfo = textinfo)
        figure.update_traces(hoverinfo='label+percent+value', textfont_size = textfont_size,marker=dict(line=dict(color='#000000', width=1)))
        figure.update_layout(height = height,margin = dict(t=40, b=30, l=10, r=10),showlegend = showlegend)
        
        return figure
    
def bar_go_figure(df = pd.DataFrame(), x = '', y = '', text = '', orientation = 'v', height = 400 ,
        title = '', space_ticked = 130, xaxis_title = '',yaxis_title = '', showticklabel_x = True, 
        showticklabel_y = True , color_dataframe= '#145f82',list_or_color = None, customdata = [],
        template = 'plotly_white', size_tickfont = 11, title_font_size = 20, clickmode = False,
        list_colors = []
    ):  
        #print(df)
        figure = go.Figure()
        if len(customdata)>0:
            custom = create_stack_np(dataframe = df, lista = customdata)
            hover_aditional_datacustom = create_hover_custom(lista = customdata)
        else:
            custom = []
            hover_aditional_datacustom = ""
            
        if orientation == 'h':
            value_left = space_ticked
            value_bottom = 40
            hover = '<br>'+y+': <b>%{y}</b><br>'+x+': <b>%{x}</b>'+hover_aditional_datacustom
        elif orientation == 'v': 
            value_left = 60
            value_bottom = space_ticked
            hover = '<br>'+x+': <b>%{x}</b><br>'+y+': <b>%{y}</b>'+hover_aditional_datacustom
            
        if  type(list_or_color) == list:
                value_colors =  list_or_color  
                
        elif type(list_or_color) == dict:

                try :
                    value_colors = [list_or_color[i] for i in df[x]]
                except:
                    value_colors = [list_or_color[i] for i in df[y]]
        else :
            value_colors = color_dataframe
        figure.add_trace(
            go.Bar(y = df[y],
                   x = df[x],   
                   text = df[text],
                   
                   orientation = orientation,
                   textposition = 'outside',
                   #texttemplate =' %{text:.2s}',
                   #marker_color = [DICT_CULTIVOS_COLOR[i]for i in df[color_dataframe]] if color_dataframe == 'CULTIVO' else value_colors,    
                   marker_color = list_colors,
                   opacity=0.9,
                   name = '',
                   customdata = custom,
                   hovertemplate=hover,
                   #hoverinfo='none',
                   hoverlabel=dict(font_size=13,bgcolor='rgba(255,255,255,0.75)',font_family="sans-serif",font_color = 'black'),
                   cliponaxis=False,
            )
        )
        
        figure.update_layout(
                template = template,
                title={'text': f"<b>{title}</b>",'y':0.97,'x':0.5,'xanchor': 'center','yanchor': 'top'},
                #title_font_color="#145f82",
                xaxis_title='<b>'+xaxis_title+'</b>',
                yaxis_title='<b>'+yaxis_title+'</b>',
                legend_title="",
                #font=dict(size=15,color="black"),
                title_font_family="sans-serif", 
                title_font_size = title_font_size,
                title_font_color = "rgba(0, 0, 0, 0.7)",
                height = height, 
                
        )
        if clickmode == True:
            figure.update_layout(clickmode='event+select')
        size_list = len(df[x].unique()) if orientation == 'v' else len(df[y].unique())
        figure.update_xaxes(tickfont=dict(size=size_tickfont),color='black',showticklabels = showticklabel_x,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
        figure.update_yaxes(tickfont=dict(size=size_tickfont),color='black',showticklabels = showticklabel_y,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
        figure.update_layout(margin=dict(l = value_left, r = 40, b= value_bottom, t = 40, pad = 1))
        
        if  size_list== 1:
            figure.update_layout(bargap=0.7)
        elif size_list== 2:
            figure.update_layout(bargap=0.4)
        elif size_list== 3:
            figure.update_layout(bargap=0.3)

        return figure

def figure_bar_px(titulo = '',x_titulo = '',y_titulo = '',l_titulo = '', df = None , x = '', y = '', color = '', barmode = 'stack' , template = 'none', height = 400, showticklabels_x = True,showticklabels_y = True,bottom=100,top=60, color_list = px.colors.qualitative.Safe):
  fig = px.bar(df, x = x, y = y,color = color, barmode = barmode, template = template,height = height,text_auto=True, color_discrete_sequence= color_list)
  fig.update_traces(textfont_size=16,textfont_family = "sans-serif",textfont_color ='black', textangle=0, textposition="outside", cliponaxis=False)
  fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))
  fig.update_layout(
              title = f"<b>{titulo}</b>",
              title_font_family="sans-serif", 
              title_font_size = 18,
              title_font_color = "rgba(0, 0, 0, 0.7)",
              margin = dict( l = 20, r = 40, b = bottom, t = top, pad = 1, autoexpand = True),

              xaxis_title = '<b>'+x_titulo+'</b>',
              yaxis_title = '<b>'+y_titulo+'</b>',
              legend_title_text = l_titulo,
              legend=dict(font=dict(size=14,color="black"))
          )
  fig.update_xaxes(tickfont=dict(size=12),color='black',showticklabels = showticklabels_x,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
  fig.update_yaxes(tickfont=dict(size=12),color='black',showticklabels = showticklabels_y,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
  fig.update_traces(hovertemplate ='<br>'+x+': <b>%{x}</b><br>'+y+': <b>%{y}</b>',hoverlabel=dict(font_size=14,bgcolor="white"))
  #fig.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
  #,type='category'
  return fig#.show()

def figure_line_px(titulo = '',x_titulo = '',y_titulo = '',l_titulo = '', df = None , x = '', y = '', color = '' , template = 'none', height = 400, showticklabels_x = True,showticklabels_y = True,text ='',facet_row = None,bottom=20,top=40):
  fig = px.line(df, x = x, y = y,color = color, template = template,height = height, color_discrete_sequence=px.colors.qualitative.Safe,facet_row = facet_row)
  fig.update_traces(text = text,textfont_size=16,textfont_family = "sans-serif",textfont_color ='black', textposition="bottom right", cliponaxis=False)
  fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))
  fig.update_layout(
              title = f"<b>{titulo}</b>",
              title_font_family="sans-serif", 
              title_font_size = 18,
              title_font_color = "rgba(0, 0, 0, 0.7)",
              margin = dict( l = 20, r = 40, b = bottom, t = top, pad = 0, autoexpand = True),

              xaxis_title = '<b>'+x_titulo+'</b>',
              yaxis_title = '<b>'+y_titulo+'</b>',
              legend_title_text = l_titulo,
              legend=dict(font=dict(size=14,color="black"))
          )
  fig.update_xaxes(tickfont=dict(size=14),color='black',showticklabels = showticklabels_x,title_font_family="sans-serif",title_font_size = 13,automargin=True)#,showgrid=True, gridwidth=1, gridcolor='black',
  fig.update_yaxes(tickfont=dict(size=14),color='black',showticklabels = showticklabels_y,title_font_family="sans-serif",title_font_size = 13,automargin=True)  
  fig.update_traces(hovertemplate ='<br>'+x+': <b>%{x}</b><br>'+y+': <b>%{y}</b>',hoverlabel=dict(font_size=15,bgcolor="white"))
  #fig.update_layout(paper_bgcolor='#f7f7f7',plot_bgcolor='#f7f7f7')
  #,type='category'
  return fig

def gauge_figure( value = 0, maximo_value = 100, titulo = '',height = 300):
  fig = go.Figure(go.Indicator(
      mode = "gauge+number",#+delta
      value = value,
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': titulo, 'font': {'size': 20}},
      #delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
      gauge = {
          'axis': {'range': [None, maximo_value], 'tickwidth': 1, 'tickcolor': "darkblue"},
          'bar': {'color': "blue"},
          'bgcolor': "white",
          'borderwidth': 2,
          'bordercolor': "gray",
          #'steps': [
          #    {'range': [0, 250], 'color': 'cyan'},
          #    {'range': [250, 400], 'color': 'royalblue'}],
          #'threshold': {
          #    'line': {'color': "red", 'width': 4},
          #    'thickness': 0.9,
          #    'value': sumador}
        }))

  fig.update_layout(paper_bgcolor = "white", font = {'color': "black", 'family': "sans-serif",'size': 20},height = height)
  return fig


def indicador_figure(value = 100, delta_reference = 320, title = ''
             
    ):
    fig = go.Figure(go.Indicator(
                        mode = "number+delta",
                        value = value,
                        number = {'suffix': "%"}, 
                        delta = {'position': "bottom", 'reference': delta_reference},
                        title = {"text": f"<b>{title}</b>",'font': {'size': 23}},
                        
                    ))

    fig.update_layout(paper_bgcolor = "lightgray")
    
    return fig

def indicador_vd_figure(value = 100, delta_reference = 320, title = '', height = 300, percent = 10
             
    ):
    fig = go.Figure(go.Indicator(
                        mode = "number+delta",
                        value = value,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        number = {'valueformat':'.0f'},
                       # number = {'suffix': "%"}, 
                        delta = {'relative':False, 'reference': delta_reference, "valueformat": ".0f"},
                        title = {"text": f"<b>{title}</b>",'font': {'size': 23}},
                        
                    ))

    #fig.update_layout(paper_bgcolor = "lightgray")
    fig.update_layout(height = height)
    fig.add_annotation(x=0.5, y=-0.2, text=f"{percent}%", font=dict(color="black",size = 25), showarrow=False)
    #fig.add_annotation(x=0.5, y=0.4, text="30%", font=dict(color="green"), showarrow=False)
    
    return fig