
import dash_bootstrap_components as dbc
import plotly.express as px

# MODIFICA EL IDIOMA POR DEFECTO DE UN DATAPICKER dmc
EXTERNAL_SCRIPTS = [
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/dayjs.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/locale/es.min.js",
]

EXTERNAL_STYLESHEETS =  [
                            dbc.themes.BOOTSTRAP,
                            "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css",
                            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css',
                            dbc.icons.BOOTSTRAP
                        ]

DROP_COLUMNAS_PADRON = [
    'N°',
    'TIPO DE DOCUMENTO\nDE IDENTIDAD DEL NIÑO\n(DNI=1\nCUI=2\nCNV=3\nCOD. PAD=4)',
    'CÓDIGO DE UBIGEO\nDEL DISTRITO',
    'NOMBRE DEL \nDEPARTAMENTO', 
    'NOMBRE DE LA\nPROVINCIA',
    'NOMBRE DEL\nDISTRITO', 
    'CÓDIGO DE CENTRO\nPOBLADO',
    'CÓDIGO DEL EESS NACIMIENTO',
    'CÓDIGO DEL EESS',
    'CÓDIGO DEL EESS ADSCRIPCIÓN',
    'CODIGO DE\nINSTITUCION \nEDUCATIVA',
    'NOMBRE DE \nINSTITUCION\n EDUCATIVA',
    '\n1=MADRE\n2=PADRE\n3=HERMANO\n4=OTRO FAMILIAR\n5=OTRO',
    '\n1=MADRE\n2=PADRE\n3=HERMANO\n4=OTRO FAMILIAR\n5=OTRO.1',
]

DROP_COLUMNAS_C1 = [
    'External ID',
    'Centro de salud Ultima Atención',
    'Lote',
    'Total de llamadas válidas realizadas',
    'Dato para saber como fue creado',
    'Referencia Direccion',
    'De seguro menor',
    'Nombre de la madre',
    'Paciente con anemía.1',
    'Total de Intervenciones No encontrado y Rechazado'
]

COLUMNAS_COMPROMISO_1 = ['External ID',
       'Establecimiento Salud del Actor Social Sectorizado/Establecimiento de Salud',
       'Actor Social/Nombre', 'Número de Documento', 'Name', 'Dirección',
       'Dirección 2', 'Celular de la madre', 'Celular de la madre 2',
       'Fecha Nac.', 'Rango de edad', 'Centro de salud Ultima Atención',
       'Centro de salud Ultima Atención.1',
       'Centro de Salud Fecha de Atención',
       'Centro de salud última atención en general',
       'Centro de salud fecha de atención en general', 'Pinta ok',
       'Número de Visitas completas', 'Mes', 'Año', 'Dni de la madre',
       'Manzana/Zona/Zona', 'Manzana/Manzana', 'Manzana/Sector', 'Lote',
       'Total de visitas validas Realizadas',
       'Total de llamadas válidas realizadas', 'Es no encontrado',
       'Fecha Máxima de Intervención',
       'Fecha Mínima de Inicio de Intervención', 'Intervenciones',
       'De seguro menor', 'Dato para saber como fue creado', 'ESSALUD',
       'Es elegido en la muestra o monitoreo', 'Inactivado Permanentemente',
       'Nombre de la madre', 'Paciente con anemía', 'Paciente con anemía.1',
       'RENIPRESS última atención en general', 'Referencia Direccion',
       'Resultado', 'Seguro Fuerzas Armadas o PNP', 'Seguro Privado',
       'Seguro SIS', 'Total de Intervenciones No encontrado y Rechazado',
       'estado'
]

DROP_VD_DETALLADO= [
    'External ID',
    'Nombre a mostrar',
    'Dispositivo',
    'Duración',
    'Meses',
    'Motivo de límite excedido',
    'Nombre de la madre',
    'Dni de la madre'
]

EESS_TRUJILLO=['LIBERTAD', 'CLUB DE LEONES', 'LOS GRANADOS "SAGRADO CORAZON"','LOS JARDINES', 'SAN MARTIN DE PORRES', 'PESQUEDA II', 'EL BOSQUE','ARANJUEZ', 'CENTRO DE SALUD LA UNION', 'PESQUEDA III']

LISTA_COLORES_BAR = px.colors.diverging.Portland+px.colors.diverging.Earth+px.colors.diverging.balance+px.colors.diverging.Tealrose+px.colors.qualitative.Plotly+px.colors.qualitative.Dark24+px.colors.qualitative.Light24+px.colors.qualitative.Alphabet


CONDITIONAL_EFECTIVAS = [
    {
    "condition": "params.data.VD_Efectivas_Porcentaje < 70",
     "style":{"backgroundColor": "#ff0000"}
    },
    {
    "condition": "params.data.VD_Efectivas_Porcentaje >= 70 && params.data.VD_Efectivas_Porcentaje < 80",
     "style":{"backgroundColor": "#ffff00"}
    },
    {
    "condition": "params.data.VD_Efectivas_Porcentaje >= 80",
     "style":{"backgroundColor": "#008000", "color": "white"}
    },
]

CONDITIONAL_GEO= [
    {
    "condition": "params.data.VD_Geo_Porcentaje < 47",
     "style":{"backgroundColor": "#ff0000"}
    },
    {
    "condition": "params.data.VD_Geo_Porcentaje >= 47",
     "style":{"backgroundColor": "#008000", "color": "white"}
    },
]