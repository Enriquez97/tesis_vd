import pandas as pd
from apps.vd.utils.functions import semana_text,trimestre_text

padron_nominal_df = pd.read_parquet('padron_nominal.parquet', engine='pyarrow')

padron_df_dash = padron_nominal_df[['ESTADO DE TRAMITE DE DNI','Sexo', 'Fecha de Nacimiento', 'Eje_vial',
        'Referencia_direccion_padron', 'Estado_visita','Estado_encontrado', 'Fecha_visita', 'Fuente_datos',
       'Fecha_fuente_datos', 'EESS_nacimiento_padron', 'EESS_atencion_padron',
       'Frecuenta_atencion_padron', 'EESS_adscripcion_padron',
       'Tipo_doc_madre_padron', 'Num_cel_madre_padron','Estado_registro',
       'Fecha_modificacion_registro', 'Usuario_modifica_registro',
       'Entidad Actualiza', 'Año', 'Trimestre_', 'Trimestre',
       'Semana_', 'Semana', 'Mes_', 'Mes', 'Dia', 'Documento Padron',
       'Tipo Documento Padron']]
padron_anio_list = sorted(padron_nominal_df['Año'].astype('string').unique())
padron_eess_atencion_list = sorted(padron_nominal_df['EESS_atencion_padron'].unique())
padron_entidad_actualiza_list = sorted(padron_nominal_df['Entidad Actualiza'].unique())
