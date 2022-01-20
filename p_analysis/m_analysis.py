import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import requests



def clean(df): #reporting
    newdf = df.drop(["activate","no_available","total_bases","dock_bikes","free_bases","reservations_count","geometry_type","geometry_coordinates","light","number","id"], axis='columns')
    newdf['Distance'] = newdf.apply(lambda x: to_mercator(x['LATITUD'], x['LONGITUD']), axis =1)
    return newdf

def df_final(df_clean):
    df_clean['Distance'] = df_clean.apply(lambda x: to_mercator(x['Latitud'], x['Longitud']), axis =1)
    df_clean[["Place of interest", "Type of place", "Place address","Latitud","Longitud"]]
    return df_clean




def combine(newdf, df_clean):
    df_combinado = df_clean.merge(newdf, how="cross")
    df_combinado['Distancia'] = df_combinado.apply(lambda x: distance_meters(x['Distance_x'], x['Distance_y']), axis =1)
    df_final = df_combinado.drop(["Latitud","Longitud","Distance_x","LATITUD","LONGITUD","Distance_y"], axis='columns')
    return df_final