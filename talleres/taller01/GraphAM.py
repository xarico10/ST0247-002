# Implementación de grafos con matrices de adyacencia
class GraphAm:
    #Constructor de la clase
    #Size:  numero de vertices del grafo
    def __init__(self, size):
        self.matriz = np.zeros((size,size))

    def getWeight(self, source, destination):
        return self.matriz[source][destination]


    def addArc(self, source, destination, weight):
        self.matriz[source][destination]=weight

    def getSuccessors(self, vertex):
        succesors=[]
        for j in range(size):
            if self.matriz[vertex][j]!= np.inf:
                succesors.append(matriz[vertex][j])
        return succesors 

