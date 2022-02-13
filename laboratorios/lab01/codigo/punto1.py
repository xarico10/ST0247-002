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

    def addArc(self,vertex,destination,weight,arcName = ""):
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
            nodos.append([int(nodo.group(1)),float(nodo.group(2)),float(nodo.group(3)),nodo.group(4)])

    G = GraphAL(numeroNodos,nodos)

    for linea in archivo.readlines():
        arco = re.match("(\d+) (\d+) (\d+\.\d+) ([\w]+)",linea)
        if arco:
            idOrigen = int(arco.group(1))
            indexOrigen = G.getIdIndex(idOrigen)
            G.addArc(indexOrigen,int(arco.group(2)),float(arco.group(3)),arco.group(4))
    print("Array de nodos: " + str(nodos))
    print("Array de listas de los arcos: " + str(G.arregloDeListas))
         
leerGrafo("puentesColgantes.txt")


