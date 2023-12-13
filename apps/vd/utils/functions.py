import pandas as pd
import numpy as np
import os
import datetime
from apps.vd.constans import COLUMNAS_COMPROMISO_1,EESS_TRUJILLO

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
    if mes_num == 12:
        lista_end = Mes[6:]
    else:
        lista_end = Mes[6:-(12-mes_num)]
    return lista_end


def completar_segun_periodo(dataframe = None, dataframe_historico = None, tipo = 'carga'):
    lista_drop = ['Fecha_Carga','Periodo_VD'] if tipo =='carga'else ['Fecha_Carga'] 
    filtro_campo = 'Mes_Periodo' if tipo =='carga'else 'Mes_VD'
    mes_num = int(str(datetime.datetime.now())[5:7])
    print(mes_num)
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

def table_periodos(dataframe_all_data = None, dataframe_detalle_vd = None):
        periodo_list = dataframe_detalle_vd['Periodo_VD'].unique()
        periodos = []
        total_niños_cargados = []
        total_niños_asignados = []
        total_vd_completas = []
        total_vd_presencial = []
        total_vd_presencial_validas = []
        total_vd_presencial_novalidas = []
        total_vd_presencial_validas_web = []
        total_vd_presencial_validas_movil = []
        total_no_encontrados = []
        total_rechazados = []
        porcentaje_vd_efectivas = []
        porcentaje_vd_movil = []
        for periodo in periodo_list:
            
            
            all_vd_df = dataframe_all_data[dataframe_all_data['Periodo_VD'] == periodo]
            detalle_vd_df = dataframe_detalle_vd[dataframe_detalle_vd['Periodo_VD'] == periodo]
            
            niños_cargados_total = all_vd_df['Numero_Doc_Nino'].count()
            niños_asignados_total = all_vd_df[all_vd_df['Establecimito_Salud_Meta'].isin(EESS_TRUJILLO)]['Establecimito_Salud_Meta'].count()
            vd_completa_total = all_vd_df['Numero_de_Visitas_Completas'].sum()
            
            periodos.append(periodo)
            total_niños_cargados.append(niños_cargados_total)
            total_niños_asignados.append(niños_asignados_total)
            total_vd_completas.append(vd_completa_total)
            
            detalle_vd_df= detalle_vd_df[detalle_vd_df['Tipo_VD']=='Visita presencial']
            vd_presencial_total = detalle_vd_df['Numero_Doc_Nino'].count()
            vd_presencial_valida_total = detalle_vd_df['VD_Valida'].sum()
            vd_presencial_novalida_total = vd_presencial_total-vd_presencial_valida_total
            vd_presencial_valida_web = detalle_vd_df[(detalle_vd_df['Dispositivo_Intervencion']=='WEB')&(detalle_vd_df['Estado_Intervencion_VD']=='Registrado')]['Dispositivo_Intervencion'].count()
            vd_presencial_valida_movil = detalle_vd_df[(detalle_vd_df['Dispositivo_Intervencion']=='MOVIL')&(detalle_vd_df['Estado_Intervencion_VD']=='Registrado')]['Dispositivo_Intervencion'].count()
            no_encontrados_total = detalle_vd_df[(detalle_vd_df['Etapa_VD']=='No Encontrado')]['Etapa_VD'].count()
            rechazados_total = detalle_vd_df[(detalle_vd_df['Etapa_VD']=='Rechazado')]['Etapa_VD'].count()
            vd_efectivas_porcentaje = round(((niños_cargados_total-vd_presencial_novalida_total-no_encontrados_total-rechazados_total)/niños_cargados_total)*100,1)
            vd_movil_porcentaje = round((vd_presencial_valida_movil/vd_presencial_valida_total)*100,1)
            
            total_vd_presencial.append(vd_presencial_total)
            total_vd_presencial_validas.append(vd_presencial_valida_total)
            total_vd_presencial_novalidas.append(vd_presencial_novalida_total)
            total_vd_presencial_validas_web.append(vd_presencial_valida_web)
            total_vd_presencial_validas_movil.append(vd_presencial_valida_movil)
            total_no_encontrados.append(no_encontrados_total)
            total_rechazados.append(rechazados_total)

            porcentaje_vd_efectivas.append(vd_efectivas_porcentaje)
            porcentaje_vd_movil.append(vd_movil_porcentaje)
            dict_table = {
                'Periodo' : periodos,
                '3-5 Meses' :total_niños_cargados,
                'Total de Niños Asignados' : total_niños_asignados,
                'Total de VD Completas' : total_vd_completas,
                'Total VD Presencial' : total_vd_presencial,
                'Total VD Presencial Válidas' : total_vd_presencial_validas,
                'Total VD Presencial No Válidas' : total_vd_presencial_novalidas,
                'Total VD Presencial por WEB' : total_vd_presencial_validas_web,
                'Total VD Presencial por MOVIL' : total_vd_presencial_validas_movil,
                'No Encontrados' : total_no_encontrados,
                'Rechazados' : total_rechazados,
                '%_VD_Efectivas':porcentaje_vd_efectivas,
                '%_VD_Georreferencia':porcentaje_vd_movil
            }
            dff = pd.DataFrame(dict_table)
        value_total_efectivas_vd = dff['%_VD_Efectivas'].sum()
        value_promedio_efectivas_vd = round(dff['%_VD_Efectivas'].mean(),1)
            
        value_total_geo_vd = dff['%_VD_Georreferencia'].sum()
            
        
        dff.loc['TOTAL',:]= dff.sum(numeric_only=True, axis=0)  
        dff=dff.fillna('TOTAL')
        dff['%_VD_Efectivas']=dff['%_VD_Efectivas'].replace({value_total_efectivas_vd: value_promedio_efectivas_vd})
            
        #
        
        
        
        value_geo_vd = round((dff['Total VD Presencial por MOVIL'].unique()[-1]/dff['Total VD Presencial'].unique()[-1])*100,1)    
        dff['%_VD_Georreferencia']=dff['%_VD_Georreferencia'].replace({value_total_geo_vd: value_geo_vd})
        return dff

def mes_num(x):
    if x == 'Ene':
        return 1
    elif x == 'Feb':
        return 2
    elif x == 'Mar':
        return 3
    elif x == 'Abr':
        return 4
    elif x == 'May':
        return 5
    elif x == 'Jun':
        return 6
    elif x == 'Jul':
        return 7
    elif x == 'Ago':
        return 8
    elif x == 'Set':
        return 9
    elif x == 'Oct':
        return 10
    elif x == 'Nov':
        return 11
    elif x == 'Dic':
        return 12