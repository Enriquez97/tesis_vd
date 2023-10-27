import pandas as pd
import numpy as np
import os
import datetime

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
        

def periodos_list():
    mes_num = int(str(datetime.datetime.now())[5:7])
    Mes=['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Set','Oct','Nov','Dic']
    lista_end = Mes[6:-(12-mes_num)]
    return lista_end


def completar_segun_periodo(dataframe = None, dataframe_historico = None, tipo = 'carga'):
    lista_drop = ['Fecha_Carga','Periodo_VD'] if tipo =='carga'else ['Fecha_Carga'] 
    filtro_campo = 'Mes_Periodo' if tipo =='carga'else 'Mes_VD'
    mes_num = int(str(datetime.datetime.now())[5:7])
    Mes=['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Set','Oct','Nov','Dic']
    mes_dict = dict(zip(range(1,13),Mes))
    try:
        mes_text_now = mes_dict[mes_num]
        vd_dff_mes_now = dataframe[(dataframe[filtro_campo]==mes_text_now)]
        vd_dff_mes_last = vd_dff_mes_now[vd_dff_mes_now['Fecha_Carga']==(vd_dff_mes_now['Fecha_Carga'].max())]
        vd_dff_mes_last = vd_dff_mes_last.drop(lista_drop, axis=1)
        return dataframe_historico._append(vd_dff_mes_last,ignore_index=True)
    except:
        return dataframe_historico

def data_vd(dataframe = None, dataframe_carga = None):
    def estado_visita(x,y,z):
        if x <= y and x >= z:
            return 'Visita Oportuna'
        elif x == y and x != z:
            return 'Visita Incompleta'
        elif x>y and x!=z:
            return 'Visita Inválida'
    dataframe['Fecha_Intervencion'] = dataframe['Fecha_Intervencion'].apply(lambda a: pd.to_datetime(a).date())
    list_doc_num = list(dataframe['Numero_Doc_Nino'].unique())
    data_vd_df = pd.DataFrame()
    list_doc =[]
    list_primera_fecha = []
    list_segunda_fecha = []
    list_tercera_fecha = []
    list_num_visitas = []
    list_num_vd_valida = []
    for doc in list_doc_num:

        list_doc.append(doc)
        tr_dff = dataframe[dataframe['Numero_Doc_Nino']==doc]
        list_num_vd_valida.append(tr_dff['VD_Valida'].sum())
        list_fecha_inter =sorted(list(tr_dff['Fecha_Intervencion'].unique()))
        len_fecha_inter = len(list(tr_dff['Fecha_Intervencion'].unique()))
        if len_fecha_inter == 1:
            list_primera_fecha.append(list_fecha_inter[0])
            list_segunda_fecha.append('-')
            list_tercera_fecha.append('-')
            list_num_visitas.append(len_fecha_inter)
        elif len_fecha_inter == 2:
            list_primera_fecha.append(list_fecha_inter[0])
            list_segunda_fecha.append(list_fecha_inter[1])
            list_tercera_fecha.append('-')
            list_num_visitas.append(len_fecha_inter)
        elif len_fecha_inter == 3:
            list_primera_fecha.append(list_fecha_inter[0])
            list_segunda_fecha.append(list_fecha_inter[1])
            list_tercera_fecha.append(list_fecha_inter[2])
            list_num_visitas.append(len_fecha_inter)
    data_vd_df['Numero_Doc_Nino'] = list_doc
    data_vd_df['Numero_visitas'] = list_num_visitas
    data_vd_df['Numero_visitas_validas'] = list_num_vd_valida
    data_vd_df['Primera Visita'] = list_primera_fecha
    data_vd_df['Segunda Visita'] = list_segunda_fecha
    data_vd_df['Tercera Visita'] = list_tercera_fecha
    dfff =  data_vd_df.merge(dataframe_carga,how ='inner', on = 'Numero_Doc_Nino')
    dfff['Estado_Visita'] = dfff.apply(lambda x: estado_visita(x['Numero_visitas'], x['Numero_visitas_validas'],x['Numero_de_Visitas_Completas']),axis=1)
    #.apply(lambda x: semana_text(x['Año'], x['Semana_']),axis=1)
    return dfff