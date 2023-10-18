import pandas as pd
import numpy as np
import os

from apps.vd.utils.functions import *
from apps.vd.constans import DROP_COLUMNAS_PADRON, DROP_COLUMNAS_C1,DROP_VD_DETALLADO

def clean_columns_padron(dataframe = pd.DataFrame()):
    dff = dataframe.drop(DROP_COLUMNAS_PADRON, axis=1)
    dff = dff.rename(columns = {'CÓDIGO DEL PADRON NOMINAL(COD. PAD)': 'COD_PADRON',
       'NÚMERO DE CERTIFICADO\nDE NACIDO VIVO (CNV)': 'CNV',
       'CÓDIGO UNICO DE IDENTIDAD (CUI)': 'CUI',
       'NÚMERO DE DOCUMENTO NACIONAL DE IDENTIFICACIÓN (DNI)': 'DNI',
       'APELLIDO PATERNO\nDEL NIÑO': 'AP_MENOR',
       'APELLIDO MATERNO\nDEL NIÑO': 'AM_MENOR',
       'NOMBRES DEL NIÑO': 'NOMBRES_MENOR',
       'ESTADO DE TRAMITE DE DNI':'Estado_tramite_DNI',
       'FECHA DE TRAMITE DE DNI':'Fecha_tramite_DNI',
       'CÓDIGO DE SEXO\nDEL NIÑO\n(1=MASCULINO\n2=FEMENINO)': 'Sexo',
       'FECHA DE NACIMIENTO\nDEL NIÑO(DD/MM/AAAA)': 'Fecha_Nacimiento', 
       'EJE VIAL': 'Eje_vial', 
       'DESCRIPCIÓN': 'Direccion_padron',
       'REFERENCIA DE DIRECCIÓN': 'Referencia_direccion_padron', 
       'NOMBRE DE \nCENTRO POBLADO': 'Nombre_cp',
       'ÁREA DEL CENTRO POBLADO': 'Tipo_cp', 
       'MENOR VISITADO': 'Estado_visita', 
       '¿MENOR ENCONTRADO?': 'Estado_encontrado',
       'FECHA DE VISITA': 'Fecha_visita', 
       'FUENTE DE DATOS': 'Fuente_datos', 
       'FECHA DE FUENTE DE DATOS': 'Fecha_fuente_datos',
       'NOMBRE DEL EESS NACIMIENTO': 'EESS_nacimiento_padron', 
        'NOMBRE DEL EESS': 'EESS_atencion_padron',
       'FRECUENCIA DE ATENCION': 'Frecuenta_atencion_padron', 
       'NOMBRE DEL EESS ADSCRIPCIÓN': 'EESS_adscripcion_padron',
       'TIPO DE DOCUMENTO DE LA MADRE': 'Tipo_doc_madre_padron',
       'NUMERO DE DOCUMENTO  DE LA MADRE(DEL MENOR\nDE EDAD)':'Doc_num_madre_padron',
       'APELLIDO PATERNO DE LA MADRE (DEL MENOR DE EDAD)': 'AP_MADRE_MENOR',
       'APELLIDO MATERNO DE LA MADRE (DEL MENOR DE EDAD)': 'AM_MADRE_MENOR',
       'NOMBRES DE LA \nMADRE(DEL MENOR DE \nEDAD)': 'NOMBRES_MADRE_MENOR',
       'NUMERO DE CELULAR DE LA MADRE': 'Num_cel_madre_padron',
       'DIRECCION DE CORREO ELECTRONICO DE LA MADRE': 'Correo_madre_padron',
       'GRADO DE\nINSTRUCCIÓN DE LA\nMADRE(DEL MENOR DE EDAD)':'Grado_instruccion_madre_padron',
       'LENGUA \nHABITUAL DE LA\nMADRE(DEL MENOR DE EDAD)':'Lengua_madre_padron',
       'TIPO DE DOCUMENTO DEL JEFE DE FAMILIA': 'Tipo_doc_jefefamilia_padron',
       'NUMERO DE DOCUMENTO DEL JEFE DE\nFAMILIA(DEL MENOR DE EDAD)':'Doc_num_jefefamilia_padron',
       'APELLIDO \nPATERNO DEL JEFE\nDE FAMILIA (DEL MENOR DE EDAD)': 'AP_JEFEFAMILIA_MENOR',
       'APELLIDO \nMATERNO DEL JEFE\nDE FAMILIA (DEL MENOR DE EDAD)': 'AM_JEFEFAMILIA_MENOR',
       'NOMBRES DEL JEFE\nDE FAMILIA (DEL MENOR DE EDAD)':'NOMBES_JEFEFAMILIA_MENOR',
       'ESTADO REGISTRO\n0=INACTIVO\n1= ACTIVO\n2=ACTIVO OBSERVADO': 'Estado_registro',
       'FECHA \nCREACIÓN DE \nREGISTRO': 'Fecha_creacion_registro', 
       'USUARIO \nQUE CREA':'Usuario_creacion_registro',
       'FECHA DE \nMODIFICACIÓN \nDEL REGISTRO': 'Fecha_modificacion_registro', 
       'USUARIO QUE \nMODIFICA':'Usuario_modifica_registro',
       'ENTIDAD': 'Entidad_Actualiza', 
       'TIPO REGISTRO':'Tipo_registro',
       'TIPO DE SEGURO\nDEL BENEFICIARIO\n0=NINGUNO\n1=SIS\n2=ESSALUD\n3=SANIDAD\n4=PRIVADO\n': 'Tipo_Seguro',
       'PROGRAMAS SOCIALES DEL NIÑO(A)\n0=NINGUNO\n1=PIN\n2=PVL\n4=JUNTOS\n5=QALIWARMA \n7=CUNA+ SCD\n8=CUNA+ SAF': 'Programas_Sociales',
    })
    dff['Doc_num_jefefamilia_padron']=dff['Doc_num_jefefamilia_padron'].astype('string')
    #dff[['CNV', 'CUI', 'DNI']] = dff[['CNV', 'CUI', 'DNI']].astype(float)
    #dff[['COD']] = dff[['COD']].astype(float)
    #dff['Tipo de documento Jefe de Familia']=dff['Tipo de documento Jefe de Familia'].astype('string')
    #dff=dff.fillna('')
    return dff

def clean_columns_c1(dataframe = pd.DataFrame()):
    dff = dataframe.drop(DROP_COLUMNAS_C1, axis=1)
    dff = dff.rename(columns = {
        'Establecimiento Salud del Actor Social Sectorizado/Establecimiento de Salud': 'Establecimito_Salud_Meta',
        'Actor Social/Nombre': 'Actor_Social',
        'Número de Documento': 'Numero_Doc_Nino',
        'Name': 'Nombres_del_Nino',
        'Dirección': 'Direccion_Nino_C',
        'Dirección 2': 'Direccion_2_Nino_C',
        'Celular de la madre': 'Celular_madre_C', 
        'Celular de la madre 2': 'Celular_madre_2_C',
        'Fecha Nac.' : 'Fecha_Nacimiento_C',
        'Rango de edad' : 'Rango_de_Edad', 
        'Centro de salud Ultima Atención.1' : 'EESS_Ultima_Atencion_C',
        'Centro de Salud Fecha de Atención': 'EESS_Fecha_Ultima_Atencion_C',
        'Centro de salud última atención en general': 'EESS_Ultima_Atencion_General_C',
        'Centro de salud fecha de atención en general': 'EESS_Fecha_Ultima_Atencion_General_C', 
        'Pinta ok':'Pinta',
        'Número de Visitas completas': 'Numero_de_Visitas_Completas',
        'Mes': 'Mes_Periodo', 
        'Año': 'Anio_Periodo',
        'Dni de la madre': 'Dni_de_la_Madre_C',
        'Manzana/Zona/Zona': 'Zona',
        'Manzana/Manzana':'Manzana',
        'Manzana/Sector':'Sector',
        'Total de visitas validas Realizadas': 'Visitas_Validas_Realizadas',
        'Es no encontrado':'ES_NO_ENCONTRADO',
        'Fecha Máxima de Intervención':'Fecha_Maxima_de_Intervencion_C',
        'Fecha Mínima de Inicio de Intervención': 'Fecha_Minima_de_Inicio_de_Intervencion_C',
        'Intervenciones': 'Intervenciones_C',
        'ESSALUD': 'ESSALUD_C', 
        'Es elegido en la muestra o monitoreo': 'Es_parte_de_la_Muestra_C',
        'Inactivado Permanentemente': 'Inactivado_Permanentemente_C', 
        'Paciente con anemía':'Nino_con_Anemia', 
        'RENIPRESS última atención en general': 'RENIPRESS_Ultima_Atencion', 
        'Resultado': 'Resultado_Muestra',
        'Seguro Fuerzas Armadas o PNP':'Seguro_SANIDAD', 
        'Seguro Privado':'Seguro_Privado', 
        'Seguro SIS':'Seguro_SIS',
        'estado': 'Estado_C',
        }
    )
    dff[['Establecimito_Salud_Meta','Actor_Social','Zona','Manzana','Sector']]=dff[['Establecimito_Salud_Meta','Actor_Social','Zona','Manzana','Sector']].replace(False,'No Especificado')
    dff['Resultado_Muestra'] = dff['Resultado_Muestra'].replace(False,'')
    #dff=dff.fillna('vacio')
    return dff


def clean_padron(dff = pd.DataFrame()):
    
    dff[['CNV', 'CUI', 'DNI']]=dff[['CNV', 'CUI', 'DNI']].fillna(0)#.astype('int')
    dff[['CNV', 'CUI', 'DNI']]=dff[['CNV', 'CUI', 'DNI']].astype('int')
    # dataframe['Semana'] = dataframe.apply(lambda x: semana_text(x['Año'], x['Semana_']),axis=1)
    dff['Documento_Padron']= dff.apply(lambda x: documento_unique(x['CNV'], x['CUI'],x['DNI'],x['COD_PADRON'],'DOC'),axis=1)
    dff['Tipo_Documento_Padron'] = dff.apply(lambda x: documento_unique(x['CNV'], x['CUI'],x['DNI'],x['COD_PADRON'],'TIPO'),axis=1)
    
    dff[['AP_MENOR', 'AM_MENOR', 'NOMBRES_MENOR']]=dff[['AP_MENOR', 'AM_MENOR', 'NOMBRES_MENOR']].fillna('')
    dff['Nombres_del_Nino_Padron'] = dff.apply(lambda x: concatenar_datos(x['AP_MENOR'], x['AM_MENOR'],x['NOMBRES_MENOR']),axis=1)
    dff[['AP_MADRE_MENOR', 'AM_MADRE_MENOR', 'NOMBRES_MADRE_MENOR']]=dff[['AP_MADRE_MENOR', 'AM_MADRE_MENOR', 'NOMBRES_MADRE_MENOR']].fillna('')
    dff['Nombres_Madre_del_Nino_Padron'] = dff.apply(lambda x: concatenar_datos(x['AP_MADRE_MENOR'], x['AM_MADRE_MENOR'],x['NOMBRES_MADRE_MENOR']),axis=1)
    
    dff[['AP_JEFEFAMILIA_MENOR','AM_JEFEFAMILIA_MENOR', 'NOMBES_JEFEFAMILIA_MENOR']]=dff[['AP_JEFEFAMILIA_MENOR','AM_JEFEFAMILIA_MENOR', 'NOMBES_JEFEFAMILIA_MENOR']].fillna('')
    dff['Nombres_JefeFamilia_del_Nino_Padron'] = dff.apply(lambda x: concatenar_datos(x['AP_JEFEFAMILIA_MENOR'], x['AM_JEFEFAMILIA_MENOR'],x['NOMBES_JEFEFAMILIA_MENOR']),axis=1)
    
    dff['Doc_num_jefefamilia_padron']=dff['Doc_num_jefefamilia_padron'].astype('string')
    
    dff['Doc_num_madre_padron'] = dff['Doc_num_madre_padron'].astype('string')
    dff['Doc_num_madre_padron'] = dff['Doc_num_madre_padron'].fillna('')
    dff['Doc_num_madre_padron'] = dff['Doc_num_madre_padron'].replace([np.nan],[''])
    return dff

def columns_merge_pnominal(dataframe = pd.DataFrame()):
    columns_utils_pnominal =['Tipo_Documento_Padron', 'Documento_Padron','Nombres_del_Nino_Padron','Fecha_Nacimiento','Direccion_padron',
    'Referencia_direccion_padron','Estado_encontrado', 'Fuente_datos','EESS_nacimiento_padron', 'EESS_atencion_padron',
    'Frecuenta_atencion_padron','EESS_adscripcion_padron','Tipo_doc_madre_padron','Doc_num_madre_padron',
    'Nombres_Madre_del_Nino_Padron','Num_cel_madre_padron','Tipo_doc_jefefamilia_padron','Doc_num_jefefamilia_padron',
    'Nombres_JefeFamilia_del_Nino_Padron','Entidad_Actualiza'
    ]
    return dataframe[columns_utils_pnominal]
 
def clean_compromiso1_data(dff = pd.DataFrame()):
    dff['Anio_Periodo'] = dff['Anio_Periodo'].astype('string')
    dff['Periodo_VD'] = dff['Anio_Periodo']+'-'+dff['Mes_Periodo']
    dff[['Establecimito_Salud_Meta','Actor_Social','Zona','Manzana','Sector']]=dff[['Establecimito_Salud_Meta','Actor_Social','Zona','Manzana','Sector']].replace(False,'No Especificado')
    dff['Dni_de_la_Madre_C'] = dff['Dni_de_la_Madre_C'].fillna('')
    return dff



def etapa_VD_detalle(dataframe = pd.DataFrame()):
    etapavd_df = dataframe.groupby(['Periodo_VD','Numero_Doc_Nino','Etapa_VD'])[['Actor_Social']].count().reset_index()
    etapa_df_last = etapavd_df[['Numero_Doc_Nino','Etapa_VD']]
    return etapa_df_last
###concat
def clean_data_concat(dataframe = pd.DataFrame()):
    dataframe['Doc_num_madre_padron']=dataframe['Doc_num_madre_padron'].replace(pd.NA, '')
    dataframe['DNI_madre'] = dataframe.apply(lambda x: nueva_col_dni(x['Dni_de_la_Madre_C'], x['Doc_num_madre_padron']),axis=1)
    columns = ['Establecimito_Salud_Meta','Actor_Social','Tipo_Documento_Padron','Numero_Doc_Nino','Documento_Padron', 
    'Nombres_del_Nino_Padron','Nombres_del_Nino','Fecha_Nacimiento_C','Fecha_Nacimiento','Rango_de_Edad',
    'Pinta','Numero_de_Visitas_Completas', 'Mes_Periodo', 'Anio_Periodo','Fecha_Minima_de_Inicio_de_Intervencion_C',
    'Fecha_Maxima_de_Intervencion_C','Direccion_Nino_C','Direccion_padron','Referencia_direccion_padron',
    'Direccion_2_Nino_C','Estado_encontrado','Fuente_datos','EESS_Ultima_Atencion_C','EESS_Fecha_Ultima_Atencion_C', 
    'EESS_Ultima_Atencion_General_C','EESS_Fecha_Ultima_Atencion_General_C','EESS_nacimiento_padron','EESS_atencion_padron',
    'Frecuenta_atencion_padron', 'EESS_adscripcion_padron','Celular_madre_C', 'Celular_madre_2_C','Num_cel_madre_padron',
    'Dni_de_la_Madre_C','Tipo_doc_madre_padron','Doc_num_madre_padron','Nombres_Madre_del_Nino_Padron',
    'Tipo_doc_jefefamilia_padron', 'Doc_num_jefefamilia_padron','Nombres_JefeFamilia_del_Nino_Padron','Entidad_Actualiza', 
    'Seguro_SANIDAD', 'Seguro_Privado', 'Seguro_SIS'
    ]
    
    return dataframe[columns]

def eliminar_repetidos(df = pd.DataFrame() ):
    data_repetidos = df.groupby(['Numero_Doc_Nino'])[['Fecha_Nacimiento_C']].count().reset_index()
    lista_repetidos = list(data_repetidos[data_repetidos['Fecha_Nacimiento_C']>=2]['Numero_Doc_Nino'])
    df_sin_repetidos =df[(df['Numero_Doc_Nino'].isin(lista_repetidos))&(df['Tipo_Documento_Padron'].isin(['DNI']))]
    df_principal = df[~(df['Numero_Doc_Nino'].isin(lista_repetidos))]
    return df_principal._append(df_sin_repetidos,ignore_index=True)



def clean_data_report(df):
    def pertenece_padron(x):
        return 'No Pertenece al Padron Nominal' if x == 'NR Padron' else 'Pertenece al Padron Nominal'
    value_empty = 'NR Padron'
    df['Documento_Padron'] = df['Documento_Padron'].fillna('0')
    df['Documento_Padron'] = df['Documento_Padron'].astype(int)
    df['Documento_Padron'] = df['Documento_Padron'].astype(object)
    df['Tipo_Documento_Padron'] = df['Tipo_Documento_Padron'].fillna(value_empty)
    df['EESS_Ultima_Atencion_C'] = df['EESS_Ultima_Atencion_C'].fillna('Vacio')
    df['EESS_Ultima_Atencion_General_C'] = df['EESS_Ultima_Atencion_General_C'].fillna('Vacio')
    df['EESS_nacimiento_padron'] = df['EESS_nacimiento_padron'].fillna('Vacio')
    df['EESS_atencion_padron'] = df['EESS_atencion_padron'].fillna('Vacio')
    
    df['Frecuenta_atencion_padron'] = df['Frecuenta_atencion_padron'].fillna('Vacio')
    df['EESS_adscripcion_padron'] = df['EESS_adscripcion_padron'].fillna('Vacio')
    
    df['Entidad_Actualiza'] = df['Entidad_Actualiza'].fillna('Vacio')
    df['Estado_Padron_Nominal'] = df.apply(lambda x: pertenece_padron(x['Tipo_Documento_Padron']),axis=1)
    #Tipo_doc_madre_padron
    df['Tipo_doc_madre_padron'] = df['Tipo_doc_madre_padron'].fillna('Vacio')
    return df


def clean_VD_detalle(dataframe = pd.DataFrame()):
    def change_rango_edad(x):
        if x == 1:
            return '3 - 5 meses'
        elif x == 2:
            return '6 - 12 meses'
        
    dff = dataframe.drop(DROP_VD_DETALLADO, axis=1)
    dff = dff.rename(columns = {
        'Establecimiento Salud':'Establecimito_Salud_Meta', 
        'Actor Social':'Actor_Social',
        'Número de documento del niño':'Numero_Doc_Nino',   
        'Paciente':'Nombres_del_Nino', 
        'Dirección':'Dirección_Nino_C', 
        'Rango edad':'Rango_de_Edad', 
        'Estado':'Estado_VD', 
        'Etapa':'Etapa_VD',
        'Dispositivo Intervención':'Dispositivo_Intervencion', 
        'Tipo de registro VD':'Tipo_VD', 
        'Fecha Intervención':'Fecha_Intervencion',
        'Latitud Intervención':'Latitud_Intervencion', 
        'Longitud Intervención':'Longitud_Intervencion',
        'Mes':'Mes_VD', 
        'Año':'Anio_VD',
        'Estado Intervención':'Estado_Intervencion_VD',
        'Número de visitas válidas por mes':'Numero_VD', 
        'Periodo':'Periodo_VD',
        'Total de visitas realizadas válidas' :'VD_Valida'
    })
    dff[['Numero_VD','VD_Valida']] = dff[['Numero_VD','VD_Valida']].astype(int)
    #.apply(lambda x: documento_unique(x['CNV'], x['CUI'],x['DNI'],'DOC'),axis=1)
    dff['Rango_de_Edad'] = dff.apply(lambda x: change_rango_edad(x['Rango_de_Edad']),axis=1)
    return dff


############# CHANGE NAME COLUMNS

def change_columns_vdetalle(df = None):
    df = df.rename(columns = {
                            'Establecimito_Salud_Meta': 'Establecimiento de Salud', 
                            'Actor_Social':'Actor Social',
                            'Numero_Doc_Nino': 'Número de Documento',   
                            'Nombres_del_Nino': 'Nombres del menor', 
                            'Dirección_Nino_C': 'Dirección', 
                            'Rango_de_Edad': 'Rango de Edad', 
                            'Estado_VD':'Estado de Visita', 
                            'Etapa_VD':'Tipo de Registro',
                            'Dispositivo_Intervencion': 'Dispositivo Intervención', 
                            'Tipo_VD': 'Tipo de Visita', 
                            'Fecha_Intervencion':'Fecha de Intervención',
                            'Latitud_Intervencion':'Latitud', 
                            'Longitud_Intervencion':'Longitud',
                            'Mes_VD':'Mes de Visita', 
                            'Anio_VD':'Año de Visita',
                            'Estado_Intervencion_VD':'Estado de Intervención',
                            'Numero_VD':'Numeró de Visitas Completas', 
                            'Periodo_VD':'Periodo de Visita',
                            'VD_Valida':'Visita Válida'
                        })
    return df