"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
assert cf

defaul_time = 1000
sys.setrecursionlimit(defaul_time*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Cargar información del catálogo")
    print("2- Encontrar puntos de interacción aérea (Req. 1)")
    print("3- Encontrar clústeres de tráfico aéreo (Req. 2)")
    print("4- Encontrar la ruta más corta entre ciudades (Req. 3)")
    print("5- Utilizar las millas del viajero (Req. 4)")
    print("6- Cuantificar el efecto de un aeropuerto cerrado (Req. 5)")
    print("0- Salir")
    print("*******************************************")

catalog = None

# ___________________________________________________
#  Variables
# ___________________________________________________


airpots_file = 'airports-utf8-small.csv'
country_file = 'worldcities-utf8.csv'
routes_file = 'routes-utf8-small.csv'
initialStation = None
analyzer = None
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        analyzer = controller.init()
        print("Cargando información de los aeropuertos ....")
        controller.loadData(analyzer, airpots_file, country_file, routes_file)
        
        vertices_d = controller.totalStops(analyzer, 'connections_d')
        arcos_d = controller.totalConnections(analyzer, 'connections_d')

        vertices_nd = controller.totalStops(analyzer, 'connections_nd')
        arcos_nd = controller.totalConnections(analyzer, 'connections_nd')

        cities = controller.totalCities(analyzer)
        #airportLt = analyzer['airports']

        print('El total de vértices (aeropuertos) del grafo dirigido son:' + str(vertices_d))
        print('El total de arcos (rutas aereas) del grafo dirigido son:' + str(arcos_d))

        print("------------------------------------------------------------------------------------------------")
        print('El primer aeropuerto cargado del grafo dirigido:')

        print("------------------------------------------------------------------------------------------------")
        print('El último aeropuerto cargado del grafo dirigido:')

        print("----------------------------------------------------------------------------------")

        print('El total de vértices (aeropuertos) del grafo no dirigido son:' + str(vertices_nd))
        print('El total de arcos (rutas aereas) del grafo no dirigido son:' + str(arcos_nd))

        print("------------------------------------------------------------------------------------------------")
        print('El primer aeropuerto cargado del grafo no dirigido:')
        

        print("------------------------------------------------------------------------------------------------")
        print('El último aeropuerto cargado del grafo no dirigido:')
        

        print("----------------------------------------------------------------------------------")
        print('El total de ciudades es: ' + str(cities))

        #Name,City,Country,IATA,Latitude,Longitude

        print("------------------------------------------------------------------------------------------------")
        print('La primera y última ciudad cargada:')
     


    elif int(inputs[0]) == 2:
        #Req 1
        topx = int(input("Ingrese el número de aeropuertos quiere ver: "))
        data = controller.getRoutesbyAirpoirt(analyzer)
        if topx > lt.size(data[0]):
            topx= lt.size(data[0])
        data2 = lt.subList(data[0],1,topx)
        print("---------------------------------------------------------------------")
        print("Aeropuertos interconectados: " + str(data[1]))
        print()
        print('TOP '+ str(topx) +' AEROPUERTOS Y SU NUMERO DE CONEXIONES: ')
        i=1
        for a in lt.iterator(data2):
            print(str(i)+'.\t'+ str(a['info']['Name'])+' ('+ str(a['IATA'])+ '): '+ str(a['num_connections']))
            i +=1

    elif int(inputs[0]) == 3:
        #Req2 
        IATA1 = input('Ingrese el código IATA del aeropuerto 1: ')
        IATA2 = input('Ingrese el código IATA del aeropuerto 2: ')
        if gr.containsVertex(analyzer['connections_d'], IATA1) and gr.containsVertex(analyzer['connections_d'], IATA2) == True:
            tupla = controller.getConnectionsByIATA(analyzer, IATA1, IATA2)
            print('El número de componentes conectados es (número de clústeres presentes): ' + str(tupla[0]))
            print('----------------------------------------------------------------------------------------------')
            if tupla[1] == True:
                print('Los dos aeropuertos dados SI están en el mismo cluster')
            else:
                print('Los dos aeropuertos dados NO están en el mismo cluster')

    elif int(inputs[0]) == 4:
        #Req 3
        c_origen = input('Ingrese la ciudad de origen: ')
        c_destino = input('Ingrese la ciudad de destino: ')

        l_co = controller.getCities(analyzer, c_origen)
        l_cd = controller.getCities(analyzer, c_destino)
        
        if lt.size(l_co) > 1:
            print('OH NO! Hay más de 2 ciudades con ese mismo nombre ')
            for c in lt.iterator(l_co):
                print(c)
            c_o= input('Escoja la ciudad de origen que busca e ingrese su id: ')
        if lt.size(l_cd) > 1:
            print('OH NO! Hay más de 2 ciudades con ese mismo nombre ')
            for c in lt.iterator(l_cd):
                print(c)
            c_d = input('Escoja la ciudad de destino que busca e ingrese su id: ')
        
        if lt.size(l_co) == 1:
            c_o = controller.CiudadesID(analyzer, c_origen)
            
        if lt.size(l_cd) == 1:
            c_d = controller.CiudadesID(analyzer, c_destino)

        print('La ciudad de origen ' + str(c_origen) + ' con id ' + str(c_o))
        print('La ciudad de destino ' + str(c_destino) + ' con id ' + str(c_d))
        print('----------------------------------------------------------------------------')

        print('El aeropuerto de origen es: ')
        a_origen = controller.AeropuertoID(analyzer, c_o)
        print(a_origen)
        a_destino = controller.AeropuertoID(analyzer, c_d)
        print('El aeropuerto de destino es: ')
        print(a_destino)
        a1_IATA = controller.aName(a_origen)
        a2_IATA = controller.aName(a_destino)
        camino = controller.camino(analyzer, a1_IATA, a2_IATA)
        print('----------------------------------------------------------------------------')
        print('La distancia total: ' + str(camino[1]))
        print('Ruta del viaje')
        
        print(camino[0])
        



    elif int(inputs[0]) == 5:
        #Req 4
        c_origen = input('Ingrese la ciudad de origen: ')
        millas = float(input('Ingrese la cantidad de millas disponibles del viajero: '))

        l_co = controller.getCities(analyzer, c_origen)
        
        if lt.size(l_co) > 1:
            print('OH NO! Hay más de 2 ciudades con ese mismo nombre ')
            for c in lt.iterator(l_co):
                print(c)
            c_o= input('Escoja la ciudad de origen que busca e ingrese su id: ')
        
        if lt.size(l_co) == 1:
            c_o = controller.CiudadesID(analyzer, c_origen)

        print('La ciudad de origen ' + str(c_origen) + ' con id ' + str(c_o))
        print('----------------------------------------------------------------------------')

        print('El aeropuerto de origen es: ')
        a_origen = controller.AeropuertoID(analyzer, c_o)
        print(a_origen['elements'][0])
        a_IATA = controller.aName(a_origen)

        Data = controller.Lifemiles(analyzer,a_IATA, millas)

        print('--------------------------------------------------------------------')
        print('El número de nodos conectados al árbol de espansión mínima: ' + str(Data[0]))
        print('El costo total (distancia [Km]) al árbol de expanxión mínima: ' + str(round(Data[1], 2)))
        print('La rama más larga:')
        print(Data[2])
        print('La distancia total recomendada por la rama más larga en millas es de: ' + str(round(Data[3]/1.6,2)))
        if Data[4] > 0:
            print('Te faltan: ' + str(round(Data[4]/1.6,2)) + ' millas para este recorrido')
        else:
            print('Te sobraron: '+ str(round(Data[4]/1.6,2)*(-1)) + ' millas')




    elif int(inputs[0]) == 6:
        #Req 5
        c_IATA = input('Ingrese el código IATA del aeropuerto fuera de funcionamiento: ')
        res = controller.removeA(analyzer, c_IATA)
        print('------------------------------------------------------------------------------------')
        print('Número total de aeropuertos afectados: ' + str(res[1]))
        lista = res[0]
        for a in lt.iterator(lista):
            codigo = a
            ar = controller.AeropuertoIATA(analyzer, codigo)
            lt_ar = controller.aeropuertosAd(analyzer, ar['elements'][0])
        
        lt_aAD = analyzer['airportsAD']

        if lt.size(lt_aAD) >= 6: 
            print('Los 3 primeros aeropuertos: ')
            print(lt_aAD['elements'][0:3])

        elif lt.size(lt_aAD) <= 5: 
            print('Los 2 primeros aeropuertos: ')
            print(lt_aAD['elements'][0:2])

        print('Los últimos aeropuertos: ')
        if lt.size(lt_aAD) >= 6: 
            print('Los 3 últimos aeropuertos: ')
            print(lt_aAD['elements'][-3:])

        elif lt.size(lt_aAD) <= 5: 
            print('Los 2 últimos aeropuertos: ')
            print(lt_aAD['elements'][-2:])
        
        
            
        


    else:
        sys.exit(0)
sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()