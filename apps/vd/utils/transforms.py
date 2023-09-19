import pandas as pd
import numpy as np
import os

from apps.vd.utils.functions import *
from apps.vd.constans import COLUMNAS_PADRON

def clean_padron(df):
    dff = df.drop(COLUMNAS_PADRON, axis=1)
    dff = dff.rename(columns = {'CÓDIGO DEL PADRON NOMINAL(COD. PAD)': 'COD_PADRON',
       'NÚMERO DE CERTIFICADO\nDE NACIDO VIVO (CNV)': 'CNV',
       'CÓDIGO UNICO DE IDENTIDAD (CUI)': 'CUI',
       'NÚMERO DE DOCUMENTO NACIONAL DE IDENTIFICACIÓN (DNI)': 'DNI',
       'APELLIDO PATERNO\nDEL NIÑO': 'AP_MENOR',
       'APELLIDO MATERNO\nDEL NIÑO': 'AM_MENOR',
       'NOMBRES DEL NIÑO': 'NOMBRES_MENOR',
       'CÓDIGO DE SEXO\nDEL NIÑO\n(1=MASCULINO\n2=FEMENINO)': 'Sexo',
       'FECHA DE NACIMIENTO\nDEL NIÑO(DD/MM/AAAA)': 'Fecha de Nacimiento', 
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
       'ENTIDAD': 'Entidad Actualiza', 
       'TIPO REGISTRO':'Tipo_registro'
    })
    dff[['CNV', 'CUI', 'DNI']]=dff[['CNV', 'CUI', 'DNI']].fillna(0)#.astype('int')
    dff[['CNV', 'CUI', 'DNI']]=dff[['CNV', 'CUI', 'DNI']].astype('int')
    # dataframe['Semana'] = dataframe.apply(lambda x: semana_text(x['Año'], x['Semana_']),axis=1)
    dff['Documento Padron']= dff.apply(lambda x: documento_unique(x['CNV'], x['CUI'],x['DNI'],'DOC'),axis=1)
    dff['Tipo Documento Padron'] = dff.apply(lambda x: documento_unique(x['CNV'], x['CUI'],x['DNI'],'TIPO'),axis=1)
    
    dff[['AP_MENOR', 'AM_MENOR', 'NOMBRES_MENOR']]=dff[['AP_MENOR', 'AM_MENOR', 'NOMBRES_MENOR']].fillna('')
    dff['Nombres del Niño Padron'] = dff.apply(lambda x: concatenar_datos(x['AP_MENOR'], x['AM_MENOR'],x['NOMBRES_MENOR']),axis=1)
    dff[['AP_MADRE_MENOR', 'AM_MADRE_MENOR', 'NOMBRES_MADRE_MENOR']]=dff[['AP_MADRE_MENOR', 'AM_MADRE_MENOR', 'NOMBRES_MADRE_MENOR']].fillna('')
    dff['Nombres Madre del Niño Padron'] = dff.apply(lambda x: concatenar_datos(x['AP_MADRE_MENOR'], x['AM_MADRE_MENOR'],x['NOMBRES_MADRE_MENOR']),axis=1)
    
    dff[['AP_JEFEFAMILIA_MENOR','AM_JEFEFAMILIA_MENOR', 'NOMBES_JEFEFAMILIA_MENOR']]=dff[['AP_JEFEFAMILIA_MENOR','AM_JEFEFAMILIA_MENOR', 'NOMBES_JEFEFAMILIA_MENOR']].fillna('')
    dff['Nombres JefeFamilia del Niño Padron'] = dff.apply(lambda x: concatenar_datos(x['AP_JEFEFAMILIA_MENOR'], x['AM_JEFEFAMILIA_MENOR'],x['NOMBES_JEFEFAMILIA_MENOR']),axis=1)
    
    return dff
 
def clean_compromiso1_data(df):
    drop_columnas = ['External ID','Centro de salud Ultima Atención','Lote','Total de llamadas válidas realizadas',
                     'Dato para saber como fue creado','Referencia Direccion','De seguro menor','Nombre de la madre',
                     'Paciente con anemía.1','Total de Intervenciones No encontrado y Rechazado'
    ]
    dff = df.drop(drop_columnas, axis=1)
    dff = dff.rename(columns = {
        'Establecimiento Salud del Actor Social Sectorizado/Establecimiento de Salud': 'Establecimito Salud Meta',
        'Actor Social/Nombre': 'Actor Social',
        'Número de Documento': 'Número Doc Niño',
        'Name': 'Nombres del Niño',
        'Dirección': 'Dirección Niño C',
        'Dirección 2': 'Dirección 2 Niño C',
        'Celular de la madre': 'Celular madre C', 
        'Celular de la madre 2': 'Celular madre 2 C',
        'Fecha Nac.' : 'Fecha Nacimiento C',
        'Rango de edad' : 'Rango de Edad', 
        'Centro de salud Ultima Atención.1' : 'EESS Ultima Atencion C',
        'Centro de Salud Fecha de Atención': 'EESS Fecha Ultima Atencion C',
        'Centro de salud última atención en general': 'EESS Ultima Atencion GeneralC',
        'Centro de salud fecha de atención en general': 'EESS Fecha Ultima Atencion General C', 
        'Pinta ok':'Pinta',
        'Número de Visitas completas': 'Número de Visitas Completas',
        'Mes': 'Mes Periodo', 
        'Año': 'Año Periodo',
        'Dni de la madre': 'Dni de la Madre C',
        'Manzana/Zona/Zona': 'Zona',
        'Manzana/Manzana':'Manzana',
        'Manzana/Sector':'Sector',
        'Total de visitas validas Realizadas': 'Visitas Válidas Realizadas',
        'Es no encontrado':'ES NO ENCONTRADO',
        'Fecha Máxima de Intervención':'Fecha Máxima de Intervención C',
        'Fecha Mínima de Inicio de Intervención': 'Fecha Mínima de Inicio de Intervención C',
        'Intervenciones': 'Intervenciones C',
        'ESSALUD': 'ESSALUD C', 
        'Es elegido en la muestra o monitoreo': 'Es parte de la Muestra C',
        'Inactivado Permanentemente': 'Inactivado Permanentemente C', 
        'Paciente con anemía':'Niño con Anemía', 
        'RENIPRESS última atención en general': 'RENIPRESS Ultima Atención', 
        'Resultado': 'Resultado Muestra',
        'Seguro Fuerzas Armadas o PNP':'Seguro SANIDAD', 
        'Seguro Privado':'Seguro Privado', 
        'Seguro SIS':'Seguro  SIS',
        'estado': 'Estado C',
        }
    )
    dff[['Establecimito Salud Meta','Actor Social','Zona','Manzana','Sector']]=dff[['Establecimito Salud Meta','Actor Social','Zona','Manzana','Sector']].replace(False,'No Especificado')
    dff['Celular madre 2 C'] = dff['Celular madre 2 C'].replace(False,'')
    dff['Celular madre 2 C'] = dff['Celular madre 2 C'].astype('string')
    dff['Celular madre 2 C'] = dff['Celular madre 2 C'].fillna('')
    dff['Celular madre 2 C'] = dff['Celular madre 2 C'].replace('.','')
    dff['Intervenciones C'] = dff['Intervenciones C'].replace(False,'No Pertenecio')
    dff['Resultado Muestra'] = dff['Resultado Muestra'].replace(False,'No Especifica')
    return dff