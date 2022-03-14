import string
import numpy as np
import re
from itertools import permutations
from itertools import chain
from collections import deque

#Clase Grafo Lista de Adyacencia
class GraphAL:
    def __init__(self, size, info = []):
        self.arregloDeListas = [0]*size
        for i in range(0,size):
            self.arregloDeListas[i] = deque()
        self.vertexInfo = info
        self.edges = []

    def addVertexInfo(self,id,x,y,name):
        self.vertexInfo[id] = [x,y,name]

    def addArc(self,vertex,destination,weight,arcName = ""):
         fila = self.arregloDeListas[vertex]
         fila.append((destination,weight,arcName))

    def getSuccessors(self, vertice):
        return [tupla[0] for tupla in self.arregloDeListas[vertice]]

    def getWeight(self, source, destination):
        for tupla in self.arregloDeListas[source]:
            if tupla[0] == destination:
                return tupla[1]
    
    def getIndex(self,id:string):
        for index,nodo in enumerate(self.vertexInfo):
                if str(nodo[0]) == id:
                    return index

#Leer el grafo desde el archivo
def leerGrafo(nombreArchivo):
    archivo = open(nombreArchivo)
    leyendoNodos = True
    numeroNodos = 0
    nodos = []

    while leyendoNodos:
        linea = archivo.readline()
        if re.search('Arco',linea):
            leyendoNodos = False
        elif re.search('\d',linea):
            numeroNodos = numeroNodos + 1
            nodo = re.match("(\d+) (\d+\.\d+) (\d+\.\d+) (\w+)",linea)
            nodos.append([nodo.group(1),float(nodo.group(2)),float(nodo.group(3)),nodo.group(4)])

    G = GraphAL(numeroNodos,nodos)

    for linea in archivo.readlines():
        arco = re.match("(\d+) (\d+) (\d+\.\d+) ([\w]+)",linea)
        if arco:
            idOrigen = arco.group(1)
            indexOrigen = G.getIndex(idOrigen)
            idDestino = arco.group(2)
            indexDestino = G.getIndex(idDestino)
            G.addArc(indexOrigen,indexDestino,float(arco.group(3)),arco.group(4))
    archivo.close()
    #print("Array de nodos: " + str(nodos))
    #print("Array de listas de los arcos: " + str(G.arregloDeListas))
    return G

class Nodo:
    def __init__(self,valor,profundidad,distancia = 0):
        self.valor = valor
        self.profundidad = profundidad
        self.distancia = distancia
        self.padre = None

class Arbol:
    def __init__(self,valorRaiz):
        diccionarioDeArreglos = {}
        raiz = Nodo(valorRaiz,0)
        raiz.padre = raiz
        diccionarioDeArreglos[0] = [raiz]
        self.diccionarioDeArreglos = diccionarioDeArreglos

    def agregarNodo(self,nodo:Nodo):
        try:
            self.diccionarioDeArreglos[nodo.profundidad].append(nodo)
        except:
            self.diccionarioDeArreglos[nodo.profundidad] = [nodo]

    def esAntecesor(self,posiblePadre:Nodo,posibleHijo:Nodo):     
        for profundidad in range(posibleHijo.profundidad):
            nodosPadres = [nodo.padre for nodo in self.diccionarioDeArreglos[profundidad]]
            valorPadres = [nodoPadre.valor for nodoPadre in nodosPadres]
            if posiblePadre.valor in valorPadres:
                return True        
        return False


def BFSSP(G,idOrigen,idDestino):
    origen = G.getIndex(idOrigen)
    destino = G.getIndex(idDestino)
    arbol = Arbol(origen)
    profundidad = 0
    distanciaMinima = np.Inf
    ruta = [-1]
    while profundidad in arbol.diccionarioDeArreglos.keys():
        for nodoInicial in arbol.diccionarioDeArreglos[profundidad]:
            vecinos = G.getSuccessors(nodoInicial.valor)
            for valorVecino in vecinos:
                distanciaHastaVecino = nodoInicial.distancia + G.getWeight(nodoInicial.valor,valorVecino)
                nodoVecino = Nodo(valorVecino,profundidad + 1,distanciaHastaVecino)
                nodoVecino.padre = nodoInicial
                if not arbol.esAntecesor(nodoVecino,nodoInicial):
                    arbol.agregarNodo(nodoVecino)
                    if nodoVecino.valor == destino and nodoVecino.distancia < distanciaMinima:
                        distanciaMinima = nodoVecino.distancia
                        ruta = [0]*(profundidad + 2)
                        posicionNodoRuta = profundidad + 1
                        nodoRuta = nodoVecino
                        while posicionNodoRuta >= 0:
                            ruta[posicionNodoRuta] = nodoRuta.valor
                            nodoRuta = nodoRuta.padre
                            posicionNodoRuta = posicionNodoRuta - 1
        profundidad = profundidad + 1
    return (ruta,distanciaMinima)
    
                          
def ejemploPuentesColgantes():
    G = leerGrafo('puentesColgantes.txt')
    print(BFSSP(G,'10000','2'))

ejemploPuentesColgantes()