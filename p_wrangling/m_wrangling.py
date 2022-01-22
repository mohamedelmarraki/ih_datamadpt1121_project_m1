import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import requests


def all_min(df_final):
    pro_main = df_final.sort_values(by = "Distancia", ascending = True).groupby('Place of interest')["Type of place",'Place address', 'name','address'].nth(0)
    return pro_main


def search_min(df_final):
    Lugar_de_interes = str(input("introduce el lugar de interes: "))
    Pro = df_final[df_final["Type of place"]==Lugar_de_interes]
    busqueda = Pro.sort_values(by="Distancia",ascending=True).head(1)
    return busqueda


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