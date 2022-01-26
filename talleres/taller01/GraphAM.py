import numpy as np
class GraphAm:

    def __init__(self, size):
        self.matriz = np.zeros((size,size))        

    def getWeight(self, source, destination):
        return self.matriz[source][destination]

    def addArc(self, source, destination, weight):
        self.matriz[source][destination] = weight

    def getSuccessors(self, vertex):
        return np.nonzero(self.matriz[vertex])