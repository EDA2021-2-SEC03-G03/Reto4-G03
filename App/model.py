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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config
from DISClib.ADT.graph import degree, getEdge, gr
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.Utils import error as error
assert config

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    try:
        analyzer = {
                    'connections_d': None,
                    'connections_nd': None,
                    'cities': None,
                    'cities2': None,
                    'components': None,
                    'airports': None,
                    'paths': None
                    }

        analyzer['cities'] = mp.newMap(100,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareCatalog)
        analyzer['cities2'] = mp.newMap(100,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareCatalog)

        analyzer['connections_d'] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=True,
                                            size=300,
                                            comparefunction=compareStopIds)
        analyzer['connections_nd'] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=False,
                                            size=5000,
                                            comparefunction=compareStopIds)
        analyzer['map_airports'] = om.newMap(omaptype = 'RBT',
                                      comparefunction = compare)
        analyzer['airports'] = lt.newList('ARRAY_LIST')
        analyzer['paths'] = lt.newList('ARRAY_LIST')

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo
def addCity(analyzer, cityID, city):
    cities = analyzer['cities']
    existcity = mp.contains(cities, cityID)
    if existcity:
        entry = mp.get(cities, cityID)
        c = me.getValue(entry)
    else:
        c = newCity()
        mp.put(cities, cityID, c)
    lt.addLast(c['City'], city)

    """
    def addCity(analyzer, city):
    entry = om.get(analyzer['cities'], city['id'])
    if entry is None:
        newEntry = newdata()
        om.put(analyzer['cities'], city['id'], newEntry)
    else:
        newEntry = me.getValue(entry)
    lt.addLast(newEntry, city)
    return analyzer
    """

def addCities(analyzer, cityName, city):
    cities = analyzer['cities2']
    existcity = mp.contains(cities, cityName)
    if existcity:
        entry = mp.get(cities, cityName)
        c = me.getValue(entry)
    else:
        c = newCity()
        mp.put(cities, cityName, c)
    lt.addLast(c['City'], city)

def addAirportLt(analyzer, airport):
    lt.addLast(analyzer['airports'], airport)
    return analyzer

def addAirport(analyzer, airport):
    """
    Adiciona un aeropuerto como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections_d'], airport['IATA']):
            gr.insertVertex(analyzer['connections_d'],airport['IATA'])
            gr.insertVertex(analyzer['connections_nd'],airport['IATA'])
            karen = lt.newList(datastructure='ARRAY_LIST')
            lt.addLast(karen,airport)
            om.put(analyzer['map_airports'],airport['IATA'],airport)
    except Exception as exp:
        error.reraise(exp, 'model:addstop')

def addRoute(analyzer, route):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections_d'], route['Departure'], route['Destination'])
    if edge is None:
        gr.addEdge(analyzer['connections_d'], route['Departure'], route['Destination'],route['distance_km'])
        lt.addLast(analyzer['paths'],route)
    return analyzer

def addRouteND(analyzer):
    """
    Adiciona un arco entre dos estaciones
    """
    route = lt.newList('ARRAY_LIST')
    r1=None
    r2=None
    for a in lt.iterator(analyzer['paths']):
        r1 = gr.getEdge(analyzer['connections_d'], a['Departure'], a['Destination'])
        r2 = gr.getEdge(analyzer['connections_d'], a['Destination'], a['Departure'])
        if r1 is not None and r2 is not None:
            lt.addLast(route, a)

    for r in lt.iterator(route):
        edge = gr.getEdge(analyzer['connections_nd'], r['Departure'], r['Destination'])
        if edge is None:
            gr.addEdge(analyzer['connections_nd'], r['Departure'], r['Destination'],r['distance_km'])

    return analyzer

# Funciones para creacion de datos
def newdata():
    entry = lt.newList('SINGLE_LINKED', compareID)
    return entry

def newCity():
    city = {"City": None}
    city['City'] = lt.newList('ARRAY_LIST', compareCatalog)
    return city

# Funciones de consulta

#Carga de Datos:

def totalStops(analyzer, grafo):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer[grafo])


def totalConnections(analyzer, grafo):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer[grafo])

def totalCities(analyzer): 
    return mp.size(analyzer['cities'])

def totalCities2(analyzer): 
    return lt.size(analyzer['cities2'])
#___________________________________________________
#Req 1
def getRoutesbyAirport(analyzer):
    rock = analyzer['connections_d']
    list_airports = lt.newList(datastructure='ARRAY_LIST')
    airports = gr.vertices(rock)
    for airport in lt.iterator(airports):
        indegree = gr.indegree(rock, airport)
        outdegree = gr.outdegree(rock, airport)
        suma = indegree+outdegree
        info = om.get(analyzer['map_airports'],airport)['value']
        dic = {'IATA': airport, 'num_connections': suma, 'info': info}
        if suma >= 2:
            pass
            #checker = gr.edges(analyzer["connections_nd"])
        lt.addLast(list_airports, dic)
        
    ms.sort(list_airports,compareReq1)
    return list_airports
#___________________________________________________
#Req 2
def getConnectionsByIATA(analyzer, IATA1, IATA2):
    grafo_d = analyzer['connections_d']
    analyzer['components'] = scc.KosarajuSCC(grafo_d)
    res1 = scc.connectedComponents(analyzer['components']) #Verificar si dos aeropuertos están en el mismo clúster
    res2 = scc.stronglyConnected(analyzer['components'], IATA1, IATA2) #Número total de cúlsteres presentes en el grafo dirigido
    return res1, res2 

#___________________________________________________
#Req 3

def getCities(analyzer, ciudad):
    city_value = mp.get(analyzer['cities2'], ciudad)
    list_cities= me.getValue(city_value)

    return list_cities['City']
 
def CiudadesID(analyzer, ciudad):
     lt_ciudades = getCities(analyzer, ciudad)
     for c in lt.iterator(lt_ciudades):
        codigo = c['id']
        return codigo 

# Funciones utilizadas para comparar elementos dentro de una lista
def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def compare(eve1, eve2):
  
    if (eve1 == eve2):
        return 0
    elif (eve1 > eve2):
        return 1
    else:
        return -1

def compareID(a1, a2):
    if int(a1['id']) < int(a2['id']):
        return -1
    elif int(a1['id']) == int(a2['id']):
        return 0
    else:
        return 1

def compareCatalog(category, entry):
    categoryentry = me.getKey(entry)
    if (category == categoryentry):
        return 0
    elif (category > categoryentry):
        return 1
    else:
        return -1 

def compareReq1(a1,a2):
    return a1['num_connections'] > a2['num_connections']

# Funciones de ordenamiento
