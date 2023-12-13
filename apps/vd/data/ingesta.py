import pandas as pd
import pandas_gbq
from apps.vd.data.credenciales import bq_cred

def ingestaBq(dataframe = None, table = ''):
    return pandas_gbq.to_gbq(
        dataframe = dataframe,
        destination_table = f'dataset_tesis.{table}',
        project_id='ew-tesis',
        if_exists = 'append',
        credentials = bq_cred,    
        table_schema ={}         
    )

