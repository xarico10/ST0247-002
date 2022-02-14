import readline
import numpy as np
import re
from collections import deque

class GraphAL:
    def __init__(self, size, info = []):
        self.arregloDeListas = [0]*size
        for i in range(0,size):
            self.arregloDeListas[i] = deque()
        self.vertexInfo = info

    def addVertexInfo(self,id,x,y,name):
        self.vertexInfo[id] = [x,y,name]

    def addArc(self,vertex,destination,weight = 0,arcName = ""):
         fila = self.arregloDeListas[vertex]
         fila.append((destination,weight,arcName))

    def getSuccessors(self, vertice):
        return [tupla[0] for tupla in self.arregloDeListas[vertice]]

    def getWeight(self, source, destination):
        for tupla in self.arregloDeListas[source]:
            if tupla[0] == destination:
                return tupla[1]
    
    def getIdIndex(self,id):
        for index,nodo in enumerate(self.vertexInfo):
                if nodo[0] == id:
                    return index

def isBicolorable(nombreArchivo):
    grafos = []
    archivo = open(nombreArchivo)
    linea = archivo.readline()
    while linea != '0':
        numeroNodos = int(linea)
        G = GraphAL(numeroNodos)
        numeroArcos = int(archivo.readline())
        conteoArcos = 0
        while conteoArcos < numeroArcos:
            linea = archivo.readline()
            arco = re.match("(\d) (\d)",linea)
            G.addArc(int(arco.group(1)),int(arco.group(2)))
            conteoArcos = conteoArcos + 1
        grafos.append(G)
        linea = archivo.readline()
    archivo.close()


def DFS(G:GraphAL):
    descubiertos = np.zeros((1,len(G.arregloDeListas)))


def main():
    isBicolorable('entrada.txt')

main()


