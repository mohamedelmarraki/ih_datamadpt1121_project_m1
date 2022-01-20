
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import argparse
import requests
import numpy as np
import sys
import fuzzywuzzy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from p_acquisition import m_acquisition as mac
from p_wrangling import m_wrangling as mwr
from p_analysis import m_analysis as man 
from p_reporting import m_reporting as mre



parser = argparse.ArgumentParser()
parser.add_argument(
    "--tipo",
    dest = "tipo",
    default = "MasCercana",
    help = "parametro para selecionar el tipo de ejecucion. Posibles valores: MasCercana , TodasEstaciones"
)


def to_mercator(lat, long):
    # transform latitude/longitude data in degrees to pseudo-mercator coordinates in metres
    c = gpd.GeoSeries([Point(lat, long)], crs=4326)
    c = c.to_crs(3857)
    return c

def distance_meters(lat_start, long_start, lat_finish, long_finish):
    # return the distance in metres between to latitude/longitude pair point in degrees (i.e.: 40.392436 / -3.6994487)
    start = to_mercator(lat_start, long_start)
    finish = to_mercator(lat_finish, long_finish)
    return start.distance(finish)

def distance_meters(mercator_start, mercator_finish):
    return mercator_start.distance(mercator_finish)



def BiciMad(): #m_acquisition
    df_BiciMad = pd.read_json("data/bicimad_stations.json")
    return df_BiciMad


df_BiciMad =BiciMad()


def lat_lon(df_BiciMad): #reporting
    lat = [float(column["geometry_coordinates"].split(",")[0].replace("[", "")) for index, column in df_BiciMad.iterrows()]
    lon = [float(column["geometry_coordinates"].split(",")[1].replace("]", "")) for index, column in df_BiciMad.iterrows()]
    df_BiciMad["LATITUD"] = lon
    df_BiciMad["LONGITUD"] = lat
    return df_BiciMad
df_BiciMad = lat_lon(df_BiciMad)

def clean(df_BiciMad): #analysis
    newdf = df_BiciMad.drop(["activate","no_available","total_bases","dock_bikes","free_bases","reservations_count","geometry_type","geometry_coordinates","light","number","id"], axis='columns')
    newdf['Distance'] = newdf.apply(lambda x: to_mercator(x['LATITUD'], x['LONGITUD']), axis =1)
    return newdf

newdf = clean(df_BiciMad)




def aparcamientos_residentes(): #m_acquisition
    aparcamientos_residentes = requests.get("https://datos.madrid.es/egob/catalogo/202584-0-aparcamientos-residentes.json")
    aparcamientos_residentes1 = aparcamientos_residentes.json()
    df1 = pd.json_normalize(aparcamientos_residentes1['@graph'])
    return df1


def aparcamientos_publicos(): #m_acquisition
    aparcamientos_publicos = requests.get("https://datos.madrid.es/egob/catalogo/202625-0-aparcamientos-publicos.json")
    aparcamientos_publicos1 = aparcamientos_publicos.json()
    df2 = pd.json_normalize(aparcamientos_publicos1['@graph'])
    return df2

df1 = aparcamientos_residentes()
df2 = aparcamientos_publicos()


def concatenate(df1, df2): #reporting
    df_concatenado = pd.concat ([df1, df2] ,ignore_index=True)
    df_clean = df_concatenado.drop(["@id","@type","id","relation","address.district.@id","address.area.@id","address.locality","address.postal-code","organization.accesibility","organization.schedule","organization.organization-desc", "organization.services"], axis='columns')
    df_clean.rename(columns={"title":"Place of interest","organization.organization-name":"Type of place","address.street-address":"Place address","location.latitude":"Latitud", "location.longitude":"Longitud"},inplace=True)
    return df_clean


df_clean = concatenate(df1, df2)


def df_final(df_clean):
    df_clean['Distance'] = df_clean.apply(lambda x: to_mercator(x['Latitud'], x['Longitud']), axis =1)
    df_clean[["Place of interest", "Type of place", "Place address","Latitud","Longitud"]]
    return df_clean

df_clean = df_final(df_clean)

datos = [(column["Place of interest"]) for index, column in df_clean.iterrows()]
datos_unicos = list(set(datos))

def combine(newdf, df_clean):
    df_combinado = df_clean.merge(newdf, how="cross")
    df_combinado['Distancia'] = df_combinado.apply(lambda x: distance_meters(x['Distance_x'], x['Distance_y']), axis =1)
    df_final = df_combinado.drop(["Latitud","Longitud","Distance_x","LATITUD","LONGITUD","Distance_y"], axis='columns')
    return df_final

df_final = combine(newdf, df_clean)


def usuario(df_final):
    for i in range(3):
        a = (input("Si desea obtener la BiciMad más cercana a su lugar de intéres introduce el número 1                                                                                                                                                                  "+
               "Si desea obtener la BiciMad más cercana a todos sus lugares de intéres introduce el número 2                                                                                                                                                         "+"La opcíon intoroducida es la: "))
        if a =="1":
            Lugar_de_interes = str(input("introduce el lugar de interes: "))
            def match_names(Lugar_de_interes, datos_unicos, min_score=0):
                max_score = -1
                max_name = ''
                for x in datos_unicos:
                    score = fuzz.ratio(Lugar_de_interes.lower(), x.lower())
                    if (score > min_score) & (score > max_score):
                        max_name = x
                        max_score = score
                        return max_name
            max_name = match_names(Lugar_de_interes, datos_unicos, min_score=90)
            Pro = df_final[df_final["Type of place"]==max_name]
            busqueda = Pro.sort_values(by="Distancia",ascending=True).head(1)
            busqueda.to_csv("data/BiciMad_Mas_Cercana.csv", sep= ";")
            print("El archivo de la BiciMad más cercana a su lugar de intéres se encuentra guardado en la carpeta data, en formato CSV")
            break
        elif a == "2":
            pro_main = df_final.sort_values(by = "Distancia", ascending = True).groupby('Place of interest')["Type of place",'Place address', 'name','address'].nth(0)
            pro_main.to_csv("data/BiciMads_Mas_Cercana.csv", sep= ";")
            print("El archivo de la BiciMad más cercana a cada uno de sus lugares de intéres se encuentra guardado en la carpeta data, en formato CSV")
            break

        else:
            print("Lo sentimos la opcíon introducida no existe, vuelva a ejecutar de nuevo el programa")




args = parser.parse_args(sys.argv[1:])
if args.tipo == "MasCercana":
    ubicacion_mas_cercana = usuario(df_final)