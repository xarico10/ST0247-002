import numpy as np
import itertools
# Implementación de grafos con matrices de adyacencia
class GraphAm:
    #Constructor de la clase
    #Size:  numero de vertices del grafo
    def __init__(self, size = 0):
        self.size = size
        self.matriz  = np.zeros((size,size))
        
    def getWeight(self, source, destination):
        return self.matriz[source][destination]

    def addArc(self, source, destination, weight):
        self.matriz[source][destination] = weight

    def getSuccessors(self, vertex):
        return np.nonzero(self.matriz[vertex])

def powerset(iterable):
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


def g(x:int,S:set):
    if S == set():
        return 

def HeldKarp(G:GraphAm,origen:int = 0):
    #g(x,S): Indica el costo mínimo que empieza en el nodo fuente, pasa por 
    # todos los nodos del conjunto S y termina en el nodo x
    g = {}
    #p(x,S): Indica el último nodo visitado en S antes de llegar al nodo x
    p = {}
    
    nodosSinOrigen = list(range(G.size))
    nodosSinOrigen.remove(origen)
    nodosSinOrigen = set(nodosSinOrigen)
    powerSetSinOrigen = powerset(nodosSinOrigen)
    for conjunto in powerSetSinOrigen:
        for nodo in nodosSinOrigen.difference(conjunto):
            if conjunto == ():
                g[nodo,()] = G.getWeight(origen,nodo)
                p[nodo,()] = origen
            else:
                caminoMinimo = np.Inf
                p[nodo,conjunto] = -1
                for elementoConjunto in conjunto:
                    diferencia = set(conjunto).difference(set([elementoConjunto]))
                    diferencia = tuple(diferencia)
                    caminoActual = G.getWeight(elementoConjunto,nodo) + g[elementoConjunto,diferencia]
                    if caminoActual < caminoMinimo:
                        caminoMinimo = caminoActual
                        g[nodo,conjunto] = caminoActual
                        p[nodo,conjunto] = elementoConjunto
    
    caminoMinimo = np.Inf
    for nodo in nodosSinOrigen:
        diferencia = set(nodosSinOrigen).difference(set([nodo]))
        diferencia = tuple(diferencia)
        caminoActual = G.getWeight(nodo,origen) + g[nodo,diferencia]
        if caminoActual < caminoMinimo:
            caminoMinimo = caminoActual
            g[origen,tuple(nodosSinOrigen)] = caminoActual
            p[origen,tuple(nodosSinOrigen)] = nodo
    
    nodosSinOrigen = set(nodosSinOrigen)
    ruta = [origen]
    nodoActual = origen
    while nodosSinOrigen != set():
        nodoActual = p[nodoActual,tuple(nodosSinOrigen)]
        ruta.append(nodoActual)
        nodosSinOrigen.remove(nodoActual)
        
    ruta.append(origen)
    
    return (ruta,caminoMinimo)
            
            

def main():
    G = GraphAm(size = 4)
    G.addArc(0, 1, 7)
    G.addArc(0, 2, 15)
    G.addArc(0, 3, 6)
    G.addArc(1, 0, 2)
    G.addArc(1, 2, 7)
    G.addArc(1, 3, 3)
    G.addArc(2, 0, 9)
    G.addArc(2, 1, 6)
    G.addArc(2, 3, 12)
    G.addArc(3, 0, 10)
    G.addArc(3, 1, 4)
    G.addArc(3, 2, 8)
    
    #print(G.matriz)
    print(HeldKarp(G,0))
    
    

main()
