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


def usuario(df_clean):
    for i in range(3):
        a = (input("Si desea obtener la BiciMad más cercana a su lugar de intéres introduce el número 1                                                          "+
               "Si desea obtener la BiciMad más cercana a todos sus lugares de intéres introduce el número 2                                              "+"La opcíon intoroducida es la: "))
        if a =="1":
            Lugar_de_interes = str(input("introduce el lugar de interes: "))
            Pro = df_clean[df_clean["Type of place"]==Lugar_de_interes]
            busqueda = Pro.sort_values(by="Distancia",ascending=True).head(1)
            pro_main.to_csv("data/BiciMad_Mas_Cercana.csv", sep= ";")
            print("El archivo de la BiciMad más cercana a su lugar de intéres se encuentra guardado en la carpeta data, en formato CSV")
            return busqueda
            break
        elif a == "2":
            pro_main = df_clean.sort_values(by = "Distancia", ascending = True).groupby('Place of interest')["Type of place",'Place address', 'name','address'].nth(0)
            pro_main.to_csv("data/BiciMads_Mas_Cercana.csv", sep= ";")
            print("El archivo de la BiciMad más cercana a cada uno de sus lugares de intéres se encuentra guardado en la carpeta data, en formato CSV")
            return pro_main
            break

        else:
            print("Lo sentimos la opcíon introducida no existe, vuelva a ejecutar de nuevo el programa")