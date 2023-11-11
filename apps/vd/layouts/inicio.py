from django_plotly_dash import DjangoDash
from ...vd.constans import EXTERNAL_SCRIPTS, EXTERNAL_STYLESHEETS
from ..utils.frames import *
import dash_mantine_components as dmc
from dash import *
from PIL import Image

image_ingesta = "https://aitor-medrano.github.io/bigdata2122/imagenes/etl/01ingesta.png"
image_organizar = "https://www.paovidal.com/wp-content/uploads/2017/12/sitio-web-1080x630.jpg"
image_seguimiento = "data:image/png;base64,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"
image_download = "https://media.wired.com/photos/5ad12bb9e35f1739afde9541/master/w_2560%2Cc_limit/facebook_data_omit-TA.jpg"
image_vd = "https://img.freepik.com/vector-premium/doctor-visitas-domiciliarias-servicios-medicos-dibujos-animados_82574-6189.jpg"
image_svdo = 'https://allinkawsay.ins.gob.pe/wp-content/uploads/2020/09/visita-domiciliaria.jpg'
image_svdc = 'https://img.freepik.com/vector-gratis/ilustracion-concepto-mensajero_114360-1156.jpg?size=338&ext=jpg&ga=GA1.1.386372595.1697760000&semt=ais'
image_svdg = 'https://esarco.es/wp-content/uploads/2020/05/certificado-coordenadas-georreferenciadas.png'
imagen_rvd = 'https://previews.123rf.com/images/lembergvector/lembergvector2112/lembergvector211200033/178732022-proceso-de-medici%C3%B3n-de-indicadores-clave-de-desempe%C3%B1o-de-la-empresa-resultados-estrat%C3%A9gicos-y.jpg'

def card_index( img = '', title_card = '', description = '', url = ''):
    
    return Div([dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Image(
                    src = img,#Image.open(f"apps/graph/build/containers/assets/{img}"),
                    height=300,
                )
            ),
            dmc.Group(
                [
                    dmc.Text(title_card, weight=500,size="lg"),
                    dmc.Badge("habilitado", color="green", variant="light"),
                ],
                position="apart",
                mt="md",
                mb="xs",
            ),
            dmc.Text(
                description ,
                size="sm",
                color="dimmed",
            ),
        html.A(
            dmc.Button(
                "Ingresar",
                variant="light",
                color="blue",
                fullWidth=True,
                mt="md",
                radius="md",
            ),
            href=url
        )
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        
    )])
def dash_home():
    app = DjangoDash('home', external_stylesheets=EXTERNAL_STYLESHEETS,external_scripts=EXTERNAL_SCRIPTS)
    app.layout = Container([
    Row([
        Column([
            card_index(
                    img = image_ingesta,
                    title_card= "Ingesta de Datos",
                    url = '/ingesta-any'
            )
        ], size=3),
        Column([
            card_index(
                img = image_organizar,
                title_card= "Organización de VD", 
                url = '/unir-data'
            )
        ], size=3),
        Column([
            card_index(
                img = image_vd,
                title_card= "Dashboard de Visitas Domiciliarias",
                url = '/vd_detalle_resultados'
            )
        ], size=3),
        Column([
            card_index(
                img = image_seguimiento,
                title_card= "Análisis VD con Padrón", 
                url= '/analisis-report-vd'
            )
        ], size=3),
    ]),
    Row([
        Column([
            card_index(
                img = image_svdo,
                title_card= "Seguimiento Visitas Oportunas",
                url = '/vd-oportunas'
            )
        ], size=3),
        Column([
            card_index(
                img = image_svdc,
                title_card= "Seguimiento Visitas Consecutivas", 
                url = '/vd-consecutivas'
            )
        ], size=3),
        Column([
            card_index(
                img = image_svdg,
                title_card= "Seguimiento Visitas Georreferenciadas", 
                url = '/vd-georreferenciadas'
            )
        ], size=3),
        Column([
            card_index(
                img = imagen_rvd,
                title_card= "Resultados Visitas Resultados", 
                url= '/dashboard-seguimiento'
            )
        ], size=3),
    ]),
    
    ])
    return app