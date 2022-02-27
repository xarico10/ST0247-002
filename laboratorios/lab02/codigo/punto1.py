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
            indexOrigen = G.getIdIndex(idOrigen)
            G.addArc(indexOrigen,arco.group(2),float(arco.group(3)),arco.group(4))
    archivo.close()
    #print("Array de nodos: " + str(nodos))
    #print("Array de listas de los arcos: " + str(G.arregloDeListas))
    return G

#Determinar si una permutación (camino) es un camino Hamiltoniano válido en el grafo y calcular su distancia
def revisarCamino(G:GraphAL,camino):
    if not camino[0] in G.getSuccessors(G.getIdIndex(camino[-1])): #No hay un arco desde el último nodo al primero
        return False,np.Inf
    distancia = 0
    for indexNodoCamino,nodo in enumerate(camino[:-1]):
        indexNodo = G.getIdIndex(nodo)
        sucesoresNodo = G.getSuccessors(indexNodo)
        if not camino[indexNodoCamino + 1] in sucesoresNodo:
            return False,np.Inf
        else:
            distancia = distancia + G.getWeight(indexNodo,camino[indexNodoCamino + 1])
    return True,distancia + G.getWeight(G.getIdIndex(camino[-1]),camino[0])

def hamiltonianoMasCorto(G:GraphAL):
    vertices = [infoVertice[0] for infoVertice in G.vertexInfo]
    permutaciones = permutations(vertices)
    caminoMasCorto = []
    distanciaMinima = np.Inf
    for permutacion in permutaciones:
        esCamino,distancia = revisarCamino(G,permutacion)
        if esCamino and distancia < distanciaMinima:
            caminoMasCorto = list(chain(permutacion))
            caminoMasCorto.append(permutacion[0])
            distanciaMinima = distancia
    return caminoMasCorto,distanciaMinima

def ejemploPuentesColgantes():
    G = leerGrafo('puentesColgantes.txt')
    caminoMasCorto,distanciaMinima = hamiltonianoMasCorto(G)
    print('El recorrido que pasa por todos los vértices exactamente una vez y vuelve al nodo inicial es ' + str(caminoMasCorto))
    print('Con costo = ' + str(distanciaMinima))

ejemploPuentesColgantes()