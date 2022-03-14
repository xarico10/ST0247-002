import re
from collections import deque
import numpy as np
#Clase Grafo Lista de Adyacencia
class GraphAL:
    def __init__(self, size:int):
        self.size = size
        self.arregloDeListas = [0]*size
        for i in range(0,size):
            self.arregloDeListas[i] = deque()

    def addVertexInfo(self,id,x,y,name):
        self.vertexInfo[id] = [x,y,name]

    def addArc(self,vertex,destination,weight):
         fila = self.arregloDeListas[vertex]
         fila.append((destination,weight))

    def getSuccessors(self, vertice):
        return [tupla[0] for tupla in self.arregloDeListas[vertice]]

    def getWeight(self, source, destination):
        for tupla in self.arregloDeListas[source]:
            if tupla[0] == destination:
                return tupla[1]
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

def leerGrafo(nombreArchivo):
    archivo = open(nombreArchivo)
    primeraLinea = archivo.readline()
    primeraLinea = re.match("(\d+) (\d+)",primeraLinea)
    G = GraphAL(int(primeraLinea.group(1)))
    nArcos = int(primeraLinea.group(2))
    nArcosLeidos = 1
    while nArcosLeidos <= nArcos:
        arco = archivo.readline()
        arco = re.match("(\d+) (\d+) (\d+)",arco)
        G.addArc(int(arco.group(1)) - 1,int(arco.group(2)) - 1,int(arco.group(3)))
        nArcosLeidos = nArcosLeidos + 1
    archivo.close()
    #print(G.arregloDeListas)
    return G

def BFSSP(G,origen,destino):
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
    ruta = [nodo + 1 for nodo in ruta]
    print(ruta)
    #return ruta,distanciaMinima

def ejemploArchivoPrueba():
    G = leerGrafo('archivoPrueba.txt')
    BFSSP(G,0,G.size - 1)

ejemploArchivoPrueba()