import pandas as pd
import pandas_gbq
from apps.vd.data.credenciales import bq_cred


def cargarDataPadron(df = pd.DataFrame(),schema ={}):
    
    
    return pandas_gbq.to_gbq(dataframe = df,
                      destination_table = 'dataset_tesis.pnominal',
                      project_id='ew-tesis',
                      if_exists = 'append',#append
                      credentials = bq_cred,
                      table_schema =  schema             
    )
    

def cargarDataCargaVD(df = pd.DataFrame(),schema ={}):
    
    
    return pandas_gbq.to_gbq(dataframe = df,
                      destination_table = 'dataset_tesis.cvd',
                      project_id='ew-tesis',
                      if_exists = 'append',#append
                      credentials = bq_cred,
                      table_schema =  schema             
    )
    
def cargarDataVdReporte(df = pd.DataFrame(),schema ={}):
    
    
    return pandas_gbq.to_gbq(dataframe = df,
                      destination_table = 'dataset_tesis.reporte_vd',
                      project_id='ew-tesis',
                      if_exists = 'append',#append
                      credentials = bq_cred,
                      table_schema =  schema             
    )
    
    
def cargarDataVDetalle(df = pd.DataFrame(),schema ={}):
    
    
    return pandas_gbq.to_gbq(dataframe = df,
                      destination_table = 'dataset_tesis.cvd_detalle_reporte',
                      project_id='ew-tesis',
                      if_exists = 'append',#append
                      credentials = bq_cred,
                      table_schema =  schema             
    )