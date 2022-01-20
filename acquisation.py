import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import requests
import argparse
import sys

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



def BiciMad():
    df4 = pd.read_json("data/bicimad_stations.json")
    lat = [float(i["geometry_coordinates"].split(",")[0].replace("[", "")) for index, i in df4.iterrows()]
    lon = [float(row["geometry_coordinates"].split(",")[1].replace("]", "")) for index, row in df4.iterrows()]
    df4["LATITUD"] = lon
    df4["LONGITUD"] = lat
    newdf = df4.drop(["activate","no_available","total_bases","dock_bikes","free_bases","reservations_count","geometry_type","geometry_coordinates","light","number","id"], axis='columns')
    newdf['Distance'] = newdf.apply(lambda x: to_mercator(x['LATITUD'], x['LONGITUD']), axis =1)
    return newdf



def DataSets():
    aparcamientos_residentes = requests.get("https://datos.madrid.es/egob/catalogo/202584-0-aparcamientos-residentes.json")
    aparcamientos_residentes1 = aparcamientos_residentes.json()
    df = pd.json_normalize(aparcamientos_residentes1['@graph'])

    aparcamientos_publicos = requests.get("https://datos.madrid.es/egob/catalogo/202625-0-aparcamientos-publicos.json")
    aparcamientos_publicos1 = aparcamientos_publicos.json()
    df1 = pd.json_normalize(aparcamientos_publicos1['@graph'])
    
    df_concatenado = pd.concat ([df1, df] ,ignore_index=True)
    df_clean = df_concatenado.drop(["@id","@type","id","relation","address.district.@id","address.area.@id","address.locality","address.postal-code","organization.accesibility","organization.schedule","organization.organization-desc", "organization.services"], axis='columns')
    df_clean.rename(columns={"title":"Place of interest","organization.organization-name":"Type of place","address.street-address":"Place address","location.latitude":"Latitud", "location.longitude":"Longitud"},inplace=True)
    df_clean['Distance'] = df_clean.apply(lambda x: to_mercator(x['Latitud'], x['Longitud']), axis =1)
    df_clean[["Place of interest", "Type of place", "Place address","Latitud","Longitud"]]
    return df_clean




def combine():
    df_combinado = DataSets().merge(BiciMad(), how="cross")
    df_combinado['Distancia'] = df_combinado.apply(lambda x: distance_meters(x['Distance_x'], x['Distance_y']), axis =1)
    df_final = df_combinado.drop(["Latitud","Longitud","Distance_x","LATITUD","LONGITUD","Distance_y"], axis='columns')
    return df_final


newdf = BiciMad()
df_clean = DataSets()
df_final = combine()


def all_min():
    pro_main = combine().sort_values(by = "Distancia", ascending = True).groupby('Place of interest')["Type of place",'Place address', 'name','address'].nth(0)
    return pro_main




def search_min():
    Lugar_de_interes = str(input("introduce el lugar de interes: "))
    Pro = combine()[combine()["Type of place"]==Lugar_de_interes]
    busqueda = Pro.sort_values(by="Distancia",ascending=True).head(1)
    return busqueda




args = parser.parse_args(sys.argv[1:])
if args.tipo == "MasCercana":
    ubicacion_mas_cercana = search_min()
    # print(ubicacion_mas_cercana)
    ubicacion_mas_cercana.to_csv("data/ubicacion_mas_cercana.csv", sep= ";")
    print("archivo estacion mas cercana guardado en la carpeta de DATA")
elif args.tipo == "TodasEstaciones":
    distancias_ubicacion = all_min()
    # print(distancias_ubicacion)
    distancias_ubicacion.to_csv("data/todas_las_ubicaciones.csv", sep= ";")
    print("archivo de todas las estaciones guardado en la carpeta de DATA")
else:
    print("opcion erronea, solo podemos meter: MasCercana o TodasEstaciones")


