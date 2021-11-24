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
assert cf


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
    print("2- Encontrar puntos de interaxión aérea (Req. 1)")
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


airpots_file = 'airports_full.csv'
country_file = 'worldcities.csv'
routes_file = 'routes_full.csv'
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
        #print(cont["connections_d"])
        #print(analyzer['cities'])
        vertices_d = controller.totalStops(analyzer, 'connections_d')
        arcos_d = controller.totalConnections(analyzer, 'connections_d')

        vertices_nd = controller.totalStops(analyzer, 'connections_nd')
        arcos_nd = controller.totalConnections(analyzer, 'connections_nd')

        cities = controller.totalCities2(analyzer)

        print('El total de vértices (aeropuertos) del grafo dirigido son:' + str(vertices_d))
        print('El total de arcos (rutas aereas) del grafo dirigido son:' + str(arcos_d))

        print("------------------------------------------------------------------------------------------------")

        print('El total de vértices (aeropuertos) del grafo no dirigido son:' + str(vertices_nd))
        print('El total de arcos (rutas aereas) del grafo no dirigido son:' + str(arcos_nd))

        print("------------------------------------------------------------------------------------------------")
        print('El total de ciudades es: ' + str(cities))

        print("------------------------------------------------------------------------------------------------")
        print('La primera ciudad cargada:')
        print(analyzer['cities2']['elements'][0])

        print("------------------------------------------------------------------------------------------------")
        print('La última ciudad cargada:')
        print(analyzer['cities2']['elements'][-1:])


    elif int(inputs[0]) == 2:
        pass

    elif int(inputs[0]) == 3:
        pass

    elif int(inputs[0]) == 4:
        pass

    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:
        pass


    else:
        sys.exit(0)
sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()