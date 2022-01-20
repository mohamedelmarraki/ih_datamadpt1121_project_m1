import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import requests


def BiciMad(): #m_acquisition
    df_BiciMad = pd.read_json("../data/bicimad_stations.json")
    return df_BiciMad



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
