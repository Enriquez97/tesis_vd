
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

COLUMNAS_PADRON = [
    'N°','TIPO DE DOCUMENTO\nDE IDENTIDAD DEL NIÑO\n(DNI=1\nCUI=2\nCNV=3\nCOD. PAD=4)',
    'CÓDIGO DE UBIGEO\nDEL DISTRITO',
    'NOMBRE DEL \nDEPARTAMENTO', 'NOMBRE DE LA\nPROVINCIA',
    'NOMBRE DEL\nDISTRITO', 'CÓDIGO DE CENTRO\nPOBLADO',
    'CÓDIGO DEL EESS NACIMIENTO','CÓDIGO DEL EESS','CÓDIGO DEL EESS ADSCRIPCIÓN',
    'TIPO DE SEGURO\nDEL BENEFICIARIO\n0=NINGUNO\n1=SIS\n2=ESSALUD\n3=SANIDAD\n4=PRIVADO\n',
    'PROGRAMAS SOCIALES DEL NIÑO(A)\n0=NINGUNO\n1=PIN\n2=PVL\n4=JUNTOS\n5=QALIWARMA \n7=CUNA+ SCD\n8=CUNA+ SAF',
    'CODIGO DE\nINSTITUCION \nEDUCATIVA','NOMBRE DE \nINSTITUCION\n EDUCATIVA',
    '\n1=MADRE\n2=PADRE\n3=HERMANO\n4=OTRO FAMILIAR\n5=OTRO','\n1=MADRE\n2=PADRE\n3=HERMANO\n4=OTRO FAMILIAR\n5=OTRO.1',
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