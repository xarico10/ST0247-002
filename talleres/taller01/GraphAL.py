#Implementación de grafo con lista de adyacencia
class GraphAL:
    def __init__(self,size):
        self.arreglo=[0]*size
        for i in range(size):
            arreglo[i]=deque()
            
    def addArc(self,vertex,edge,weigth):
        fila=self.arreglo[vertex]
        parejaDestinoPeso=(edge,weigth)
        fila.append(parejaDestinoPeso)
        
    def getSuccessors(self, vertice):
        fila=self.matriz[vertice]
        succesors=[]
        for deque in fila:
            succesors.append(deque)
        return succesors
    
    def getWeight(self, source, destination):
        fila=self.matriz[source]
        for deque in fila:
            if fila[deque][0]==destination:
                return fila[deque][1]
