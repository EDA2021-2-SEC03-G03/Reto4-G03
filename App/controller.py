"""
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
        model.addAirportND(analyzer, airport)
    for route in DictRoutes:
        model.addRoute(analyzer, route)
        model.addRouteND(analyzer, route)
    for city in DictCountry:
        model.addCity(analyzer, city)
        model.addCities(analyzer, city)
    
    return analyzer
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

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