import numpy as np
import itertools
class GraphAm:
    #Constructor de la clase
    #Size:  numero de vertices del grafo
    def __init__(self, size = 0):
        self.size = size
        self.matriz  = np.zeros((size,size))
#       self.vectores = []*size
        
    def getWeight(self, source, destination):
        return self.matriz[source][destination]

    def addArc(self, source, destination, weight):
        self.matriz[source][destination] = weight

    def getSuccessors(self, vertex):
        return np.nonzero(self.matriz[vertex])

#   def agregarInfoVectores(self,vectores):
#       self.vectores = vectores
        
def powerset(iterable):
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) \
        for r in range(len(s)+1))

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
                    diferencia = set(conjunto).difference(set(
                        [elementoConjunto]))
                    diferencia = tuple(diferencia)
                    caminoActual = G.getWeight(elementoConjunto,nodo) + \
                    g[elementoConjunto,diferencia]
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

def punto2(nombreArchivo):
    archivo = open(nombreArchivo)
    numeroEscenarios = int(archivo.readline())
    #escenarios[i] = (G,[dimX_i,dimY_i],[origenX_i,origenY_i],numeroDesechos_i,[[dimX_desecho_k_i,dimY_desecho_k_i])
    
    for escenario in range(numeroEscenarios):
        dimensiones = archivo.readline()
        dimensiones = dimensiones.split(' ')
        dimensiones = [int(dimension) for dimension in dimensiones]
        
        origen = archivo.readline()
        origen = origen.split(' ')
        origen = [int(coordenada) for coordenada in origen]
        
        numeroDesechos = int(archivo.readline())
        numeroNodos = numeroDesechos + 1
        coordenadasDesechos = []
        coordenadasDesechos.append(origen)
        
        
        for desecho in range(numeroDesechos):
            coordenadas = archivo.readline()
            coordenadas = coordenadas.split(' ')
            coordenadas = [int(coordenada) for coordenada in coordenadas]
            coordenadasDesechos.append(coordenadas)
        
        G = GraphAm(numeroNodos)
        
        for nodo1 in range(numeroNodos - 1):
            for nodo2 in range(nodo1 + 1,numeroNodos):
                #Métrica del taxista
                distanciaTaxista = abs(coordenadasDesechos[nodo1][0] - 
                    coordenadasDesechos[nodo2][0]) + \
                    abs(coordenadasDesechos[nodo1][1] - \
                        coordenadasDesechos[nodo2][1])
                
                G.addArc(nodo1, nodo2, distanciaTaxista)
                G.addArc(nodo2, nodo1, distanciaTaxista)
        
        ruta,distMin = HeldKarp(G,0)
        print('The shortest path has length ' + str(distMin))
        
            
        
    archivo.close()

def main():
    punto2('entrada.txt')

main()