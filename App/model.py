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
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Graphs import dfs
from DISClib.ADT import queue as q
from DISClib.Utils import error as error
from math import sin,cos,sqrt,asin,pi
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
                    'codeAirport':None,
                    'components': None,
                    'airports': None,
                    'airportsMap': None,
                    'airportsAD': None,
                    'paths': None,
                    'camino':None,
                    'mst': None
                    }

        analyzer['cities'] = mp.newMap(100,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareCatalog)
        analyzer['cities2'] = mp.newMap(100,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareCatalog)
        analyzer['codeAirport'] = mp.newMap(100,
                                 maptype='PROBING',
                                 loadfactor=0.5,
                                 comparefunction=compareCatalog)
        analyzer['airportsMap'] = mp.newMap(100,
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
        analyzer['airportsAD'] = lt.newList('ARRAY_LIST')
        analyzer['cities_lt'] = lt.newList('ARRAY_LIST')
        analyzer['mst'] = gr.newGraph(datastructure='ADJ_LIST',
                                            directed=True,
                                            size=5000,
                                            comparefunction=compareStopIds)

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
    lt.addLast(analyzer['cities_lt'], city)


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

def addAirportMap(analyzer, IATA, airport):
    airports = analyzer['airportsMap']
    existcity = mp.contains(airports, IATA)
    if existcity:
        entry = mp.get(airports, IATA)
        a = me.getValue(entry)
    else:
        a = newMap()
        mp.put(airports, IATA, a)
    lt.addLast(a['Airport'], airport)

def addCodeAirport(analyzer, codigo, ciudad):
    """
    Mapa de codigo-ciudad con su aeropuerto más cercano
    """

    cities = analyzer['codeAirport']
    existcity = mp.contains(cities, codigo)
    if existcity:
        entry = mp.get(cities, codigo)
        c = me.getValue(entry)
    else:
        c = newAirport(analyzer, ciudad)
        mp.put(cities, codigo, c)

    #lt.addLast(c['Airport'], ciudad)
     

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

def newMap():
    airport = {"Airport": None}
    airport['Airport'] = lt.newList('ARRAY_LIST', compareCatalog)
    return airport


def newAirport(analyzer, ciudad):
    city = {'Airport': None}
    city['Airport'] = lt.newList('ARRAY_LIST', compareCatalog)
    menor = 1000000000
    menorA = None
    for a in lt.iterator(analyzer['airports']):
        d = distancia(a, ciudad)
        if menor > d:
            menor = d
            menorA = a
            
    lt.addLast(city['Airport'], menorA)
    
    return city 

def distancia(a, ciudad):
    lat1 = float(ciudad['lat'])
    long1 = float(ciudad['lng'])
    lat2 = float(a['Latitude'])
    long2 = float(a['Longitude'])
    r = 6371000 #radio terrestre medio, en metros

    c = pi/180 #constante para transformar grados en radianes
    
    #Fórmula de haversine
    d = 2*r*asin(sqrt(sin(c*(lat2-lat1)/2)**2 + cos(c*lat1)*cos(c*lat2)*sin(c*(long2-long1)/2)**2))
    return d     



# Funciones de consulta

#___________________________________________________
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
def getsamples_d(analyzer):
    list_sample = lt.newList(datastructure='ARRAY_LIST')
    first = lt.getElement(analyzer['airports'],1)
    last = lt.getElement(analyzer['airports'],lt.size(analyzer['airports']))
    lt.addLast(list_sample,first)
    lt.addLast(list_sample, last)
    return list_sample
def getsamples_nd(analyzer):
    list_sample = lt.newList(datastructure='ARRAY_LIST')
    first = lt.getElement(analyzer['airports'],1)
    last = lt.getElement(analyzer['airports'],lt.size(analyzer['airports']))
    lt.addLast(list_sample, first)
    lt.addLast(list_sample, last)
    return list_sample

def getsamples_city(analyzer):
    pamplona= analyzer['cities_lt']
    list_sample = lt.newList(datastructure='ARRAY_LIST')
    first = lt.getElement(pamplona,1)
    last = lt.getElement(pamplona,lt.size(pamplona))
    lt.addLast(list_sample, first)
    lt.addLast(list_sample, last)
    return list_sample
#___________________________________________________
#Req 1
def getRoutesbyAirport(analyzer):
    rock = analyzer['connections_d']
    list_airports = lt.newList(datastructure='ARRAY_LIST')
    airports = gr.vertices(rock)
    interconectados = 0
    for airport in lt.iterator(airports):
        indegree = gr.indegree(rock, airport)
        outdegree = gr.outdegree(rock, airport)
        suma = indegree+outdegree
        info = om.get(analyzer['map_airports'],airport)['value']
        dic = {'IATA': airport, 'num_connections': suma, 'info': info}
        if indegree > 0 and outdegree > 0:
            interconectados += 1
        lt.addLast(list_airports, dic)
        
    ms.sort(list_airports,compareReq1)
    return list_airports, interconectados
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

def AeropuertoID(analyzer, id):
    ciudad_aeropuerto = mp.get(analyzer['codeAirport'], id)
    lt_aeropuerto = me.getValue(ciudad_aeropuerto)
    
    return lt_aeropuerto['Airport']

def AeropuertoIATA(analyzer, iata):
    ciudad_aeropuerto = mp.get(analyzer['airportsMap'], iata)
    lt_aeropuerto = me.getValue(ciudad_aeropuerto)
    
    return lt_aeropuerto['Airport']

def aName(aeropuerto):
    for a in lt.iterator(aeropuerto):
        a_name = a['IATA']
        return a_name

def DistanceA(a1, a2):
    for a1 in lt.iterator(a1):
        for a2 in lt.iterator(a2):
            lat1 = float(a1['Latitude'])
            long1 = float(a1['Longitude'])
            lat2 = float(a2['Latitude'])
            long2 = float(a2['Longitude'])
            r = 6371000 #radio terrestre medio, en metros

            c = pi/180 #constante para transformar grados en radianes
            
            #Fórmula de haversine
            d = 2*r*asin(sqrt(sin(c*(lat2-lat1)/2)**2 + cos(c*lat1)*cos(c*lat2)*sin(c*(long2-long1)/2)**2))
            return d 

def camino(analyzer, a1, a2):
    analyzer['camino'] = djk.Dijkstra(analyzer['connections_d'], a1)

    if djk.hasPathTo(analyzer['camino'], a2):
        path = djk.pathTo(analyzer['camino'], a2)
        total = djk.distTo(analyzer['camino'], a2)

        return path, total

def AeropuertoIATA(analyzer, iata):
    ciudad_aeropuerto = mp.get(analyzer['airportsMap'], iata)
    lt_aeropuerto = me.getValue(ciudad_aeropuerto)
    
    return lt_aeropuerto['Airport']
#___________________________________________________
#Req 4
def Lifemiles(analyzer,c_origen, millas):
    distance_km = 1.6*millas
    mst = prim.PrimMST(analyzer['connections_nd'])

    peso = prim.weightMST(analyzer['connections_nd'], mst)
    mst = (prim.edgesMST(analyzer['connections_nd'], mst))['mst']

    for i in lt.iterator(mst):
        addPointConneMst(analyzer, i['vertexA'], i['vertexB'], i['weight'])
    

    mstAnalyzer = analyzer['mst']
    vert = gr.vertices(mstAnalyzer)
    num = lt.size(vert)
    primero = c_origen
    mayor = 0
    camino = None
    dijta = dfs.DepthFirstSearch(analyzer['mst'], primero)

    for v in lt.iterator(vert):
        if dfs.hasPathTo(dijta, v) == True:
            ruta = dfs.pathTo(dijta, v)
            x = lt.size(ruta)
            if x > mayor:
                mayor = x
                camino = ruta
    print(camino)
    distancia = 0
    previo = ""
    for item in lt.iterator(camino):
        if previo != "":
            print(previo,item)
            info = gr.getEdge(analyzer["connections_nd"], previo, item)
            a_sum = info['weight']
            previo = item
            distancia += float(a_sum)
        else:
            previo = item


    residuo = float(distancia) - float(distance_km)

    return num, peso, camino, distancia, residuo

def addVerMst(catalog, pointid):
    try:
        if not gr.containsVertex(catalog['mst'], pointid):
            gr.insertVertex(catalog['mst'], pointid)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:addVerMst')

def addConneMst(catalog, origen, destino, distancia):
    edge = gr.getEdge(catalog['mst'], origen, destino)
    if edge is None:
        gr.addEdge(catalog['mst'], origen, destino, distancia)
    return catalog

def addPointConneMst(catalog, ver1, ver2, distancia):
    try:
        origen = ver1
        destino = ver2
        addVerMst(catalog, origen)
        addVerMst(catalog, destino)
        addConneMst(catalog, origen, destino, distancia)
        addConneMst(catalog, destino, origen, distancia)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:addPointConneMst')



"""
def MST(analyzer):
    mst = prim.PrimMST(analyzer['connections_d'])

    peso = prim.weightMST(analyzer['connections_d'], mst)
    mst = (prim.edgesMST(analyzer['connections_d'], mst))['mst']

    for i in lt.iterator(mst):
        addPointConneMst(analyzer, i['vertexA'], i['vertexB'], i['weight'])
    

    mstAnalyzer = analyzer['mst']
    vert = gr.vertices(mstAnalyzer)
    num = lt.size(vert)
    primero = c_origen
    mayor = millas
    camino = None
    dijta = djk.Dijkstra(analyzer['mst'], primero)
    listaFuncional = lt.newList('ARRAY_LIST')

    for v in lt.iterator(vert):
        if djk.hasPathTo(dijta, v) == True:
            ruta = djk.pathTo(dijta, v)
            x = lt.size(ruta)
            if x > mayor:
                mayor = x
                camino = ruta

    num_m = int(mayor) - int(millas)

    return num, peso, camino, num_m

def addVerMst(catalog, pointid):
    try:
        if not gr.containsVertex(catalog['mst'], pointid):
            gr.insertVertex(catalog['mst'], pointid)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:addVerMst')

def addConneMst(catalog, origen, destino, distancia):
    edge = gr.getEdge(catalog['mst'], origen, destino)
    if edge is None:
        gr.addEdge(catalog['mst'], origen, destino, distancia)
    return catalog

def addPointConneMst(catalog, ver1, ver2, distancia):
    try:
        origen = ver1
        destino = ver2
        addVerMst(catalog, origen)
        addVerMst(catalog, destino)
        addConneMst(catalog, origen, destino, distancia)
        addConneMst(catalog, destino, origen, distancia)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:addPointConneMst')


    --------------------------------------------------------------------------------

    mst = prim.PrimMST(analyzer['connections_d'])

    peso = prim.weightMST(analyzer['connections_d'], mst)
    mst = (prim.edgesMST(analyzer['connections_d'], mst))['mst'] 

    defs = dfs.DepthFirstSearch(analyzer['connections_d'], c_origen)

    for n in peso:
       if djk.hasPathTo(defs, n):
        path = djk.pathTo(defs, n)
        total = djk.distTo(defs, n)

        return path, total

"""

#___________________________________________________
#Req 5

def removeA(analyzer, cIATA):
    lt_adjacents = gr.adjacents(analyzer['connections_d'], cIATA)
    size = lt.size(lt_adjacents)
    return lt_adjacents, size 

def aeropuertosAd(analyzer, ar):
    lt.addLast(analyzer['airportsAD'], ar)
    return analyzer



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
