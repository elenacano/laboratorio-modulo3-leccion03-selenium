from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import datetime


dias_mes = {
    "Jan": 31,
    "Feb": 29,
    "Mar": 31,
    "Apr": 30,
    "May": 31,
    "Jun": 30,
    "Jul": 31,
    "Aug": 31,
    "Sep": 30,
    "Oct": 31,
    "Nov": 30,
    "Dec": 31
}

meses = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}

def getText(linea):
    dato = linea.text
    return dato.strip()


def df_datos_mes(sopa):
    table = sopa.findAll("table", {"class":"days ng-star-inserted"})
    columnas = table[0].findAll("td")

    mes_hoy = datetime.datetime.now().month
    mes_actual = columnas[8].text.strip()
    if meses[mes_hoy]==mes_actual:
        dias = datetime.datetime.now().day
    else:
        dias = dias_mes[mes_actual]
        
    encabezados=columnas[:7]
    encabezados_limpio = list(map(getText,encabezados))

    listas = []
    df = pd.DataFrame()

    # dias
    max1=8+1+dias
    mes=columnas[8:max1]
    listas.append(mes)

    #temperatura
    max2=max1+1+((dias+1)*3)
    temperaturas=columnas[max1+1:max2]
    listas.append(temperaturas)

    #rocío
    max3=max2+1+((dias+1)*3)
    rocio=columnas[max2+1:max3]
    listas.append(rocio)

    #humedad
    max4=max3+1+((dias+1)*3)
    humedad=columnas[max3+1:max4]
    listas.append(humedad)

    #viento
    max5=max4+1+((dias+1)*3)
    viento=columnas[max4+1:max5]
    listas.append(viento)

    #presion
    max6=max5+1+((dias+1)*3)
    presion=columnas[max5+1:max6]
    listas.append(presion)

    #precipitacion
    max7=max6+1+dias+1
    precipitacion = columnas[max6+1:max7]
    listas.append(precipitacion)

    i=0
    for lista in listas:
        lista_limpia = list(map(getText,lista))
        if i!=0 and i!=6:
            df_aux=pd.DataFrame(np.reshape(lista_limpia,(dias+1,3)))
        else:
            df_aux=pd.DataFrame(lista_limpia)
        df = pd.concat([df, df_aux], axis=1)
        i+=1

    #Metemos el mes, renombramos las columnas, rehacemos el indice y que quitamos la columna indice
    df.insert(0,"mes", mes_actual)
    df.columns = ["mes","dia", "max_temp", "avg_temp", "min_temp", "max_rocio", "avg_rocio", "min_rocio", 
                "max_humedad", "avg_humedad", "min_humedad", "max_viento", "avg_viento", 
                "min_viento", "max_presion", "avg_presion", "min_presion", "lluvia"]
    df = df.drop(index=0)
    df.reset_index(inplace=True)
    df.drop("index", axis=1, inplace=True)
    
    return df
