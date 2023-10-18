import pandas as pd
import numpy as np
import os

def nueva_col_dni(dni_meta, dni_padron):
    if len(dni_meta)!= 0:
        return dni_meta
    elif (len(dni_meta)== 0 or dni_meta=='XXXXXXX') and len(dni_padron)!=0:
        return  dni_padron
    
def documento_unique(cnv , cui, dni, cod, tipo):
        if dni !=0:
            resultado = dni
            doc = 'DNI'
        elif dni == 0 and cui != 0:
            resultado = cui
            doc = 'CUI'
        elif cui == 0 and dni == 0 and cnv !=0:
            resultado = cnv
            doc = 'CNV'
        elif cui == 0 and dni == 0 and cnv ==0:
            resultado = cod
            doc = 'CODIGO PADRON'
        #else:
        #    resultado = 11111
        #    doc = 'SIN DOC'
        
        return resultado if tipo == 'DOC' else doc
    
def concatenar_datos(ap,am,nombres):
        if len(ap) != 0 and len(nombres) != 0 and  len(am) != 0:
            resultado = ap+' '+am+' '+nombres
            
        elif len(ap) == 0 and len(nombres) == 0 and len(am) != 0:
            resultado = am
        elif len(ap) != 0 and len(nombres) != 0 and len(am) == 0:
            resultado = ap+' '+nombres
            
        elif len(ap) != 0 and len(nombres) == 0 and len(am) == 0:
            resultado = ap
        
        elif len(ap) == 0 and len(nombres) != 0 and len(am) == 0:
            resultado = nombres
        
        elif len(ap) == 0 and len(nombres) == 0 and  len(am) == 0:
            resultado = 'SIN DATOS'
        return resultado


def semana_text(year, week):
        if len(str(week)) == 1:
            semana = '0'+ str(week)
        else:
            semana = str(week)
        return str(year)+'-'+'Sem'+''+str(semana)
                                          
def trimestre_text(year,trimestre):
        return str(year)+' '+'Trim '+str(trimestre)  
    
    
def dataframe_filtro(values=[],columns_df=[]):
   """
   values son los inputs 
   columns_df son las columnas a comparar para el filtro
   """
   query = ""
   for value, col in zip(values,columns_df):
        if value != None:
            if type(value) == int:
                text=f"`{col}` == {value}"
            elif type(value) == str:
                text=f"`{col}` == '{value}'"
            elif type(value) == list:
                text=f"`{col}` in {value}"
            query += text + " and "
            
   return query[:-5]

def validar_all_none(variables=()):
    contador = 0
    for i in variables:
        if i == None:
            contador = contador +1
    return True if len(variables) == contador else False

def create_stack_np(dataframe = pd.DataFrame(), lista = []):
    return np.stack(tuple(dataframe[elemento] for elemento in lista),axis = -1)

def create_hover_custom(lista = []):
    string_hover = ''
    for i,element in zip(range(len(lista)),lista):
         if element == 'w' or element == 'w' or element == 'w':
               string_hover = string_hover+'<br>'+element+': <b>%{customdata['+str(i)+']:,.2f}</b>'
         else:
               string_hover = string_hover+'<br>'+element+': <b>%{customdata['+str(i)+']}</b>'   
    return string_hover

def calcular_total_vd(dataframe = None):
            acumulador = 0
            for periodo in dataframe['Periodo de Visita'].unique():
                vd_detalle_periodo=dataframe[dataframe['Periodo de Visita']==periodo]
                acumulador+=vd_detalle_periodo.groupby(['Número de Documento','Numeró de Visitas Completas']).count().reset_index()['Numeró de Visitas Completas'].sum()
            return acumulador