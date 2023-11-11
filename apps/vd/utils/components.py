import dash_mantine_components as dmc
from dash import html,dcc
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
from datetime import datetime, date, timedelta

def title(order = 2, align = 'center', content = '',id = '-' ):
    return dmc.Title(children = content,order = order,align = align, id = id)

def offcanvas(
        componentes=[], label='', size_width=250, placement = "start"
    ):
        return html.Div(
            dbc.Offcanvas(
                        scrollable=True,
                        id="offcanvas-placement",
                        title=label,
                        is_open=False,
                        backdrop=False,
                        style={"width": size_width},
                        children =componentes,
                        placement = placement
                        )
        )
        
def loadingOverlay(
        component,type="bars",colors="#01414b",size="xl"
    ):
        return html.Div(dmc.LoadingOverlay(component,
                            loaderProps={"variant": type, "color": colors, "size": size},
                            #loader=dmc.Image(
                            #    src="https://i.imgur.com/KIj15up.gif", alt="", caption="", width=70,height=70#
                            #    ),
))
        
def spoiler(text=""):
        return html.Div([
                dmc.Spoiler(
                    #id=ids,
                    showLabel="Mostrar más",
                    hideLabel="Hide",
                    maxHeight=50,
                    children=[
                        dmc.Text(children=text)
                    ],
                )
        ])
        
def notification(id='',text='',title=''):
        return dmc.Notification(
            id=id,
            title=title,
            message=[text],
            disallowClose=False,
            radius="xl",
            icon=[DashIconify(icon="feather:database", width=128)],
            action="show",
        )

def modalMaximize(content=[]):
            return html.Div(
                [
                    dbc.ModalHeader(close_button=True),
                    dbc.ModalBody([content]),
                ],
            )

def text(id = '', text = '',weight = 800, align = "center"):
        return dmc.Text(text, weight=weight,align=align)

def button(text="",variant="filled",color="blue",id='btn',fullwidth = False, margin = {}):
        return html.Div(
                [
                    dmc.Button(text,variant=variant,color=color,id=id, fullWidth= fullwidth,style = margin),
                ]
            )
        
def actionIcon(
        variant="default",
        color="blue",
        id='btn-icon',
        style={'position': 'absolute','top': '4px','right': '4px','z-index': '99'},
        icono='maximize'
    ):
        return html.Div(
                dmc.ActionIcon(
                                DashIconify(icon=f"feather:{icono}"), 
                                color=color, 
                                variant=variant,
                                id=id,
                                n_clicks=0,
                                mb=10,
                                style=style
                            ),
            )
        
def checkbox(
        ids=None,label=""
    ):
        return html.Div(
            [
                dmc.Checkbox(id=ids, label=label, mb=10)
            ]
        )

def checkboxGroup(
        ids,texto,value=[],orientacion="horizontal",size="xs",requerido=False,offset="sm",space="xs",child=[]
    ):
        return html.Div(
                    [
                        dmc.CheckboxGroup(
                            id=ids,
                            label=texto,
                            value=value,
                            size=size,
                            #description="This is anonymous",
                            orientation=orientacion,
                            withAsterisk=requerido,
                            offset=offset,
                            mb=1,
                            spacing=space,
                            children=child,
                        ),
                    ]
        )

def checkboxChild(list):
        return [dmc.Checkbox(label=i, value=i) for i in list]
    
def checkList(ids,texto,options=[],value=[],inline=False):
        return dbc.Checklist(  
                                        id=ids,
                                        options=options,
                                        value=value,
                                        inline=inline,
                                        input_checked_style={
                                            "backgroundColor": "rgb(34, 139, 230)",
                                            "borderColor": "rgb(34, 139, 230)",
                                        },     
                ),

def datepickerRange(
        id='',
        label='',
        size='sm',
        disabled=False,
        
    ):
        return html.Div(
                        [
                            dmc.DateRangePicker(
                                id=id,
                                label=label,
                                locale='es',
                                size=size,
                                disabled=disabled,
                            ), 
                        ]
                    )

def datePicker(
        id="",text='',value=None,minimo=None,maximo=None
    ):
        return html.Div([
            dmc.DatePicker(
                id = id,
                label = text,
                #description="You can also provide a description",
                minDate = minimo,
                maxDate = maximo,
                value = value,
                locale = "es",
                clearable = False
                
            ),
        ])

def inputNumber(id = 'id-number',label = '', value = 10):
        return html.Div(
            dmc.NumberInput(
                id=id,
                label= label,
                value = int(value),
                precision=1,
                min=5,
                step=1,
                max=500,
                #style={"width": 250},
            )
        )
        
def radioGroup(
        id='',texto='',value=[],size="sm",space="xs",orientacion="horizontal",children=[]
    ):
        return  html.Div(
                    [
                        dmc.RadioGroup(
                            id=id,
                            children=children,
                            value=value,
                            label=texto,
                            size=size,
                            spacing=space,
                            mt=1,
                            orientation=orientacion,
                        ),
                        
                    ]
                )

def select(id='',texto='',place="Seleccione",value=None,data=[],clearable=True, searchable = False, size='md'):
        return  html.Div(
            dmc.Select(
                id=id,
                data=data,
                label=texto,
                clearable=clearable,
                placeholder=place,
                style={'font-size': "90%"},
                value=value,
                size=size,
                searchable = searchable

            )
    )

def multiSelect(id='w',texto='',place="",value=None,data=[],size='md'):
        return html.Div(
            dmc.MultiSelect(
                        id=id,
                        label=texto,
                        placeholder=place,
                        searchable=True,
                        nothingFound="Opción no encontrada",
                        value=value,
                        data=data,
                        style={'font-size': "70%"},
                        size=size, 
                    )
        ) 

def segmented(id='',value=None,data=[],full_width=True,color='rgb(34, 184, 207)',size='xs'):
        return html.Div([
                dmc.SegmentedControl(
                                    id=id,
                                    value=value,
                                    data=data,
                                    fullWidth=full_width,
                                    color=color,
                                    size=size
                                ),
        ])   


def upload(upload_id = 'upload-data', stack_id = 'contents', text_btn = ''):
    return dcc.Upload(
            id = upload_id,
            children=loadingOverlay([dmc.Stack(id = stack_id, 
                    children=[
                        #html.I(className='fas fa-upload fa-fw fa-3x upload-icon'),
                        #dmc.Text('Arrastre y suelte archivos aquí para cargarlos.', className='upload-text'),
                        dmc.Button(
                            text_btn,
                            id='upload-button',
                            radius='lg',
                            color='gray'
                        )
                    ], align='center', spacing='xl')
                    ])
            )

def btnDownload(
        variant="default",color="blue"
    ):
        return html.Div(
                dmc.ActionIcon(
                                DashIconify(icon="feather:download"), 
                                color=color, 
                                variant=variant,
                                id="btn-download",
                                n_clicks=0,
                                mb=10,
                            ),
            )