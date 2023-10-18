import pandas as pd
from apps.vd.data.credenciales import bq_cred
query_sql_dt = """SELECT * FROM `ew-tesis.dataset_tesis.cvd_detalle` WHERE Rango_de_Edad ='3 - 5 meses'"""
query_all_cargados_vd = """SELECT * FROM `ew-tesis.dataset_tesis.historial_vd_cargados` WHERE Rango_de_Edad ='3 - 5 meses'"""
#query_sql = """SELECT * FROM ew-tesis.bd_tesis.padronnominal"""

vd_all_cargados_df = pd.read_gbq( query = query_all_cargados_vd,project_id = 'ew-tesis',credentials = bq_cred,dialect = 'standard')
vd_all_cargados_df['Anio_Periodo'] = vd_all_cargados_df['Anio_Periodo'].astype('string')
vd_all_cargados_df['Periodo_VD'] = vd_all_cargados_df['Anio_Periodo']+'-'+vd_all_cargados_df['Mes_Periodo']



vd_detalle_df_bq = pd.read_gbq( query = query_sql_dt,project_id = 'ew-tesis',credentials = bq_cred,dialect = 'standard')





def bq_pnominal_df():
    query_data_pnominal = "SELECT * FROM `ew-tesis.dataset_tesis.pnominal`"
    pnominal_bq_df = pd.read_gbq(   query = query_data_pnominal ,
                                    project_id = 'ew-tesis',
                                    credentials = bq_cred,
                                    dialect = 'standard')
    pnominal_bq_df['Fecha_Carga']=pnominal_bq_df['Fecha_Carga'].astype('string')
    pnominal_bq_df['Fecha_Carga'] = pnominal_bq_df['Fecha_Carga'].str[:19]
    pnominal_bq_df['Fecha_creacion_registro'] = pd.to_datetime(pnominal_bq_df['Fecha_creacion_registro'], format="%d/%m/%Y")
    return pnominal_bq_df

def bq_cvd_df():
    query_data_cvd = "SELECT * FROM `ew-tesis.dataset_tesis.cvd` WHERE Rango_de_Edad ='3 - 5 meses'"
    cvd_bq_df = pd.read_gbq(   query = query_data_cvd ,
                                    project_id = 'ew-tesis',
                                    credentials = bq_cred,
                                    dialect = 'standard')
    cvd_bq_df['Fecha_Carga']=cvd_bq_df['Fecha_Carga'].astype('string')
    cvd_bq_df['Fecha_Carga'] = cvd_bq_df['Fecha_Carga'].str[:19]
    cvd_bq_df['Anio_Periodo'] = cvd_bq_df['Anio_Periodo'].astype('string')
    cvd_bq_df['Periodo_VD'] = cvd_bq_df['Anio_Periodo']+'-'+cvd_bq_df['Mes_Periodo']
    return cvd_bq_df

def bq_cvd_detalle_df():
    query_data_cvd_detalle = "SELECT * FROM `ew-tesis.dataset_tesis.cvd_detalle` WHERE Rango_de_Edad ='3 - 5 meses'"
    cvd_detalle_bq_df = pd.read_gbq(   query = query_data_cvd_detalle ,
                                    project_id = 'ew-tesis',
                                    credentials = bq_cred,
                                    dialect = 'standard')
   
    return cvd_detalle_bq_df

def bq_reporte_vd_df():
    query_data_reporte_vd = "SELECT * FROM `ew-tesis.dataset_tesis.reporte_vd`"
    reporte_bd_bq_df = pd.read_gbq(   query = query_data_reporte_vd ,
                                    project_id = 'ew-tesis',
                                    credentials = bq_cred,
                                    dialect = 'standard')
   
    return reporte_bd_bq_df

def bq_cvd_reporte_df():
    query_data_cvd = "SELECT * FROM `ew-tesis.dataset_tesis.cvd_detalle_reporte` WHERE Rango_de_Edad ='3 - 5 meses'"
    cvd_reporte_bq_df = pd.read_gbq(   query = query_data_cvd ,
                                    project_id = 'ew-tesis',
                                    credentials = bq_cred,
                                    dialect = 'standard')

    return cvd_reporte_bq_df

