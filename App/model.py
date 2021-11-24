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
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
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
                    'airports': None,
                    'paths': None
                    }

        analyzer['cities'] = om.newMap(omaptype = 'RBT',
                                      comparefunction = compare)
        analyzer['cities2'] = lt.newList('ARRAY_LIST', cmpfunction=compareID)

        analyzer['connections_d'] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=True,
                                            size=300,
                                            comparefunction=compareStopIds)
        analyzer['connections_nd'] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=False,
                                            size=5000,
                                            comparefunction=compareStopIds)
        analyzer['airports'] = lt.newList('ARRAY_LIST')
        analyzer['paths'] = lt.newList('ARRAY_LIST')

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo
def addCity(analyzer, city):
    entry = om.get(analyzer['cities'], city['id'])
    if entry is None:
        newEntry = newdata()
        om.put(analyzer['cities'], city['id'], newEntry)
    else:
        newEntry = me.getValue(entry)
    lt.addLast(newEntry, city)
    return analyzer

def addCities(analyzer, city):
    lt.addLast(analyzer['cities2'], city)
    return analyzer

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
    return om.size(analyzer['cities'])

def totalCities2(analyzer): 
    return lt.size(analyzer['cities2'])


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

# Funciones de ordenamiento
