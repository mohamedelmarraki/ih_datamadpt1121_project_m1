import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import requests


def lat_lon(df): #analysis
    lat = [float(column["geometry_coordinates"].split(",")[0].replace("[", "")) for index, column in df.iterrows()]
    lon = [float(column["geometry_coordinates"].split(",")[1].replace("]", "")) for index, column in df.iterrows()]
    df["LATITUD"] = lon
    df["LONGITUD"] = lat
    return df






def concatenate(df1, df2): #reporting
    df_concatenado = pd.concat ([df1, df2] ,ignore_index=True)
    df_clean = df_concatenado.drop(["@id","@type","id","relation","address.district.@id","address.area.@id","address.locality","address.postal-code","organization.accesibility","organization.schedule","organization.organization-desc", "organization.services"], axis='columns')
    df_clean.rename(columns={"title":"Place of interest","organization.organization-name":"Type of place","address.street-address":"Place address","location.latitude":"Latitud", "location.longitude":"Longitud"},inplace=True)
    return df_clean