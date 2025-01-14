﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
from DISClib.ADT.graph import gr
from DISClib.DataStructures import adjlist as alt


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    analyzer = model.newAnalyzer()
    return analyzer
# Funciones para la carga de datos
def loadData(analyzer, airports_file, country_file, routes_file):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    airportsfile = cf.data_dir + airports_file
    countryfile = cf.data_dir + country_file
    routesfile = cf.data_dir + routes_file
    DictAirports = csv.DictReader(open(airportsfile, encoding="utf-8"),
                                delimiter=",")
    DictCountry = csv.DictReader(open(countryfile, encoding="utf-8"),
                                delimiter=",")
    DictRoutes = csv.DictReader(open(routesfile, encoding="utf-8"),
                                delimiter=",")                            
    for airport in DictAirports:
        model.addAirport(analyzer, airport)
        model.addAirportLt(analyzer, airport)
        model.addAirportMap(analyzer, airport['IATA'], airport)
    for route in DictRoutes:
        model.addRoute(analyzer, route)
    
    model.addRouteND(analyzer)
    for city in DictCountry:
        model.addCity(analyzer, city['id'], city)
        model.addCities(analyzer, city['city'], city)
        model.addCodeAirport(analyzer, city['id'], city)
    return analyzer
    
    #print(analyzer['map_airports']['elements'][0:10])
def getsamples_d(analyzer):
    return model.getsamples_d(analyzer)
def getsamples_nd(analyzer):
    return model.getsamples_nd(analyzer)
def getsamples_city(analyzer):
    return model.getsamples_city(analyzer)
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
#_______________________________________________
#Req 1
def getRoutesbyAirpoirt(analyzer):
    return model.getRoutesbyAirport(analyzer)
#---------------------------------------------

#_______________________________________________
#Req 2
def getConnectionsByIATA(analyzer, IATA1, IATA2):
    return model.getConnectionsByIATA(analyzer, IATA1, IATA2)
#---------------------------------------------

#_______________________________________________
#Req 3

def getCities(analyzer, ciudad):
    return model.getCities(analyzer, ciudad)

def CiudadesID(analyzer, ciudad):
    return model.CiudadesID(analyzer, ciudad)

def AeropuertoID(analyzer, id):
    return model.AeropuertoID(analyzer, id)

def aName(aeropuerto):
    return model.aName(aeropuerto)

def DistanceA(a1, a2):
    return model.DistanceA(a1, a2)
#________________________________________________
#Req 4
def Lifemiles(analyzer,c_origen, millas):
    return model.Lifemiles(analyzer,c_origen, millas)

#________________________________________________
#Req 5
def removeA(analyzer, cIATA):
    return model.removeA(analyzer, cIATA)

def AeropuertoIATA(analyzer, iata):
    return model.AeropuertoIATA(analyzer, iata)

def aeropuertosAd(analyzer, ar):
    return model.aeropuertosAd(analyzer, ar)

#------------------------------------------------

def camino(analyzer, a1, a2):
    return model.camino(analyzer, a1, a2)

#---------------------------------------------

#Carga de datos 
def totalStops(analyzer, grafo):
    return model.totalStops(analyzer, grafo)

def totalConnections(analyzer, grafo):
    return model.totalConnections(analyzer, grafo)

def totalCities(analyzer):
    return model.totalCities(analyzer)

def totalCities2(analyzer):
    return model.totalCities2(analyzer)
