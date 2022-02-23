import numpy as np
from collections import deque
class GraphALNoDirigido:
    def __init__(self, size):
        self.size = size
        self.arregloDeListas = [0]*size
        for i in range(0,size):
            self.arregloDeListas[i] = deque()

    def addArc(self, vertex, destination, weight = 1):
         filaOrigen = self.arregloDeListas[vertex]
         filaOrigen.append((destination,weight))
         filaDestino = self.arregloDeListas[destination]
         filaDestino.append((vertex,weight))

    def getSuccessors(self, vertice):
        return [tupla[0] for tupla in self.arregloDeListas[vertice]]

    def getWeight(self, source, destination):
        for tupla in self.arregloDeListas[source]:
            if tupla[0] == destination:
                return tupla[1]

class GraphAmNoDirigido:
    def __init__(self, size):
        self.size = size
        self.matriz = np.zeros((size,size))        

    def getWeight(self, source, destination):
        return self.matriz[source][destination]

    def addArc(self, source, destination, weight = 1):
        self.matriz[source][destination] = weight
        self.matriz[destination][source] = weight

    def getSuccessors(self, vertex):
        return np.nonzero(self.matriz[vertex])

def estaBienPintadoHastaI(G,solucion,i):
    for nodo in range(i + 1):
        colorVertice = solucion[nodo]
        sucesores = np.array(G.getSuccessors(nodo))
        sucesores = sucesores[sucesores <= i]
        for sucesor in sucesores:
            colorSucesor = solucion[sucesor]
            if colorSucesor == colorVertice:
                return False
    return True

def sePuedePintarMColores(G,m):
    solucion = np.zeros(G.size)
    nodo = 0
    posicion = 0
    return pintarMColoresAux(G,m,solucion,posicion)

def pintarMColoresAux(G,m,solucion,posicion):
    if posicion == G.size:
        #print(solucion)
        return True
    for color in range(m):
        solucion[posicion] = color
        if estaBienPintadoHastaI(G,solucion,posicion):
            if pintarMColoresAux(G,m,solucion,posicion + 1):
                return True
    return False

def minimoColores(G):
    sePuedePintar = False
    m = 0
    while not sePuedePintar:
        m = m + 1
        sePuedePintar = sePuedePintarMColores(G,m)
    return m

    



def main():
    G = GraphALNoDirigido(7)
    G.addArc(0,1)
    G.addArc(1,2)
    G.addArc(1,6)
    G.addArc(2,3)
    G.addArc(2,4)
    G.addArc(2,5)
    G.addArc(3,1)
    G.addArc(3,2)
    G.addArc(3,6)
    G.addArc(4,2)
    G.addArc(4,5)
    G.addArc(4,6)
    print(sePuedePintarMColores(G,3))
    print(minimoColores(G))
main()

