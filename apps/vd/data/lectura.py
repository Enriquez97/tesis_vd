import pandas as pd
from apps.vd.data.credenciales import bq_cred


#PADRON NOMINAL
def bq_pnominal_df(query = "SELECT * FROM `ew-tesis.dataset_tesis.pnominal`"):
    query_data_pnominal = query
    pnominal_bq_df = pd.read_gbq(   query = query_data_pnominal ,
                                    project_id = 'ew-tesis',
                                    credentials = bq_cred,
                                    dialect = 'standard')
    return pnominal_bq_df

# DATA UNICA DEL ULTIMO MES DE CARGA VD
def bq_cvd_df(query = "SELECT * FROM `ew-tesis.dataset_tesis.cvd` WHERE Rango_de_Edad !='Otros menores a 12 meses'"):
    query_data_cvd = query#
    cvd_bq_df = pd.read_gbq(   query = query_data_cvd ,
                                    project_id = 'ew-tesis',
                                    credentials = bq_cred,
                                    dialect = 'standard')
    cvd_bq_df['Fecha_Carga']=cvd_bq_df['Fecha_Carga'].astype('string')
    cvd_bq_df['Fecha_Carga'] = cvd_bq_df['Fecha_Carga'].str[:19]
    cvd_bq_df['Anio_Periodo'] = cvd_bq_df['Anio_Periodo'].astype('string')
    cvd_bq_df['Periodo_VD'] = cvd_bq_df['Anio_Periodo']+'-'+cvd_bq_df['Mes_Periodo']
    return cvd_bq_df

#historico de visitas domiciarias completadas durante el mes
def bq_cvd_detalle_df(query = "SELECT * FROM `ew-tesis.dataset_tesis.cvd_detalle` WHERE Rango_de_Edad !='Otros menores a 12 meses'"):
    query_data_cvd_detalle = query
    cvd_detalle_bq_df = pd.read_gbq(   query = query_data_cvd_detalle ,
                                    project_id = 'ew-tesis',
                                    credentials = bq_cred,
                                    dialect = 'standard')
   
    return cvd_detalle_bq_df


#DATA DE LISTA REALIZADA PARA LA BUSQUEDA CON CONCATENACION DE DATOS DEL PN
def bq_reporte_vd_df():#!='Otros menores a 12 meses'
    query_data_reporte_vd = "SELECT * FROM `ew-tesis.dataset_tesis.reporte_vd`"
    reporte_bd_bq_df = pd.read_gbq(   query = query_data_reporte_vd ,
                                    project_id = 'ew-tesis',
                                    credentials = bq_cred,
                                    dialect = 'standard')
   
    return reporte_bd_bq_df

def bq_cvd_reporte_df():
    query_data_cvd = "SELECT * FROM `ew-tesis.dataset_tesis.cvd_detalle_reporte` WHERE Rango_de_Edad !='Otros menores a 12 meses'"
    cvd_reporte_bq_df = pd.read_gbq(   query = query_data_cvd ,
                                    project_id = 'ew-tesis',
                                    credentials = bq_cred,
                                    dialect = 'standard')

    return cvd_reporte_bq_df


def bq_historico_carga_vd():
    query = "SELECT * FROM `ew-tesis.dataset_tesis.historial_vd_cargados`"
    cvd_historico = pd.read_gbq(   query = query ,
                                    project_id = 'ew-tesis',
                                    credentials = bq_cred,
                                    dialect = 'standard')

    return cvd_historico



### FILTROS

#PADRON
def bq_fcarga_pnominal_df():
    #query_data_pnominal = "SELECT * FROM `ew-tesis.dataset_tesis.pnominal`"
    query_data_pnominal = "SELECT DISTINCT Fecha_Carga FROM `ew-tesis.dataset_tesis.pnominal`"
    #SELECT DISTINCT Nombre FROM empleados;
    pnominal_bq_df = pd.read_gbq(   query = query_data_pnominal ,
                                    project_id = 'ew-tesis',
                                    credentials = bq_cred,
                                    dialect = 'standard')
    #pnominal_bq_df['Fecha_Carga']=pnominal_bq_df['Fecha_Carga'].astype('string')
    #pnominal_bq_df['Fecha_Carga'] = pnominal_bq_df['Fecha_Carga'].str[:19]
    #pnominal_bq_df['Fecha_creacion_registro'] = pd.to_datetime(pnominal_bq_df['Fecha_creacion_registro'], format="%d/%m/%Y")
    return pnominal_bq_df

#cvd

def bq_fcarga_cvd_df():
    #query_data_cvd = "SELECT * FROM `ew-tesis.dataset_tesis.cvd` WHERE Rango_de_Edad ='3 - 5 meses'"
    query_data_cvd ="SELECT DISTINCT Fecha_Carga FROM `ew-tesis.dataset_tesis.cvd` "
    cvd_bq_df = pd.read_gbq(   query = query_data_cvd ,
                                    project_id = 'ew-tesis',
                                    credentials = bq_cred,
                                    dialect = 'standard')
    cvd_bq_df['Fecha_Carga']=cvd_bq_df['Fecha_Carga'].astype('string')
    cvd_bq_df['Fecha_Carga'] = cvd_bq_df['Fecha_Carga'].str[:19]
    return cvd_bq_df

#historico vd 

def bq_f_carga_cvd_detalle_df():
    query_data_cvd_detalle = "SELECT DISTINCT Periodo_VD FROM `ew-tesis.dataset_tesis.cvd_detalle` "
    cvd_detalle_bq_df = pd.read_gbq(   query = query_data_cvd_detalle ,
                                    project_id = 'ew-tesis',
                                    credentials = bq_cred,
                                    dialect = 'standard')
   
    return cvd_detalle_bq_df

#solo periodos
def bq_periodos_historico_carga(query = "SELECT DISTINCT Mes_Periodo FROM `ew-tesis.dataset_tesis.historial_vd_cargados`"):
    #query = "SELECT * FROM `ew-tesis.dataset_tesis.historial_vd_cargados` WHERE Rango_de_Edad ='3 - 5 meses'"
    cvd_historico = pd.read_gbq(   query = query ,
                                    project_id = 'ew-tesis',
                                    credentials = bq_cred,
                                    dialect = 'standard')

    return cvd_historico

def bq_periodos_historico_vd(query = "SELECT DISTINCT Mes_VD FROM `ew-tesis.dataset_tesis.cvd_detalle`"):
    #query = "SELECT * FROM `ew-tesis.dataset_tesis.historial_vd_cargados` WHERE Rango_de_Edad ='3 - 5 meses'"
    cvd_historico = pd.read_gbq(   query = query ,
                                    project_id = 'ew-tesis',
                                    credentials = bq_cred,
                                    dialect = 'standard')

    return cvd_historico


def bq_call_select(column = '', table = '' ):
    #query = "SELECT * FROM `ew-tesis.dataset_tesis.historial_vd_cargados` WHERE Rango_de_Edad ='3 - 5 meses'"
    df = pd.read_gbq(   query = f"SELECT DISTINCT {column} FROM `ew-tesis.dataset_tesis.{table}`" ,
                                    project_id = 'ew-tesis',
                                    credentials = bq_cred,
                                    dialect = 'standard')

    return df