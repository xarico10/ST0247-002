import pandas as pd
import numpy as np
import time
from collections import deque
import pickle

class GraphAL:
	def __init__(self,size,infoNodos = [],arrayArcos = []):
		self.size = size
		self.arregloDeListas = [0]*size
		self.infoNodos = infoNodos
		self.infoArcos = arrayArcos
		for i in range(size):
			self.arregloDeListas[i] = deque()
			
		#arrayArcos = [origen,destino,peso,acoso,nombre]
		i = 0
		for arco in arrayArcos:
			self.arregloDeListas[arco[0]].append([arco[1],arco[2],arco[3],
				arco[4]])
			
	def addArc(self, vertex, destination, weight, acoso = 0, nombre = ''):
		fila = self.arregloDeListas[vertex]
		fila.append([destination,weight,acoso,nombre])
	
	def addInfoNodos(self,infoNodos):
		self.infoNodos = infoNodos
	
	def getSuccessors(self, vertice):
		return [tupla[0] for tupla in self.arregloDeListas[vertice]]
	
	def getWeight(self, source, destination):
		for tupla in self.arregloDeListas[source]:
			if tupla[0] == destination:
				return tupla[1]
			
	def obtenerAcoso(self, source, destination):
		for tupla in self.arregloDeListas[source]:
			if tupla[0] == destination:
				if tupla[2] is None:
					return 0
				return tupla[2]
	
	def editarArco(self,origen,destino,nuevoPeso):
		for tupla in self.arregloDeListas[origen]:
			if tupla[0] == destino:
				tupla[1] = nuevoPeso

def leerGrafo():
	
	dataFrame = pd.read_csv('calles_de_medellin_con_acoso.csv',sep = ';')
	dataFrame['harassmentRisk'] = dataFrame['harassmentRisk'].fillna(0)
	dataFrame['name'] = dataFrame['name'].fillna('')

	nNodos = 0
	coordenadasNodos = []
	arcos = []
	n = 0
	for indexFila,fila in dataFrame.iterrows():
			
		origenArco,destinoArco = fila['origin'],fila['destination']
		
		if origenArco in coordenadasNodos:
			indexOrigenArco = coordenadasNodos.index(origenArco)
		else:
			coordenadasNodos.append(origenArco)
			indexOrigenArco = nNodos
			nNodos += 1
			
		if destinoArco in coordenadasNodos:
			indexDestinoArco = coordenadasNodos.index(destinoArco)
		else:
			coordenadasNodos.append(destinoArco)
			indexDestinoArco = nNodos
			nNodos += 1
		
		if [indexOrigenArco,indexDestinoArco,float(fila['length']),
			float(fila['harassmentRisk']),fila['name']] not in arcos:
		
			arcos.append([indexOrigenArco,indexDestinoArco,
				float(fila['length']),float(fila['harassmentRisk']),
				fila['name']])
		
		if not fila['oneway']:
			if [indexDestinoArco,indexOrigenArco,float(fila['length']),
				float(fila['harassmentRisk']),fila['name']] not in arcos:
			
				arcos.append([indexDestinoArco,indexOrigenArco,
					float(fila['length']),float(fila['harassmentRisk']),
					fila['name']])
		
	G = GraphAL(nNodos,coordenadasNodos,arcos)
	#print(arcos)
	return G

#ALGORITMO 1
#Algoritmo de Dijkstra (min dist)
def elMasCercanoNoVisitado(G,v,visitados):
	vecinos = G.getSuccessors(v)
	distMin = np.Inf
	nodoMasCerca = -1
	for vecino in vecinos:
		if G.getWeight(v,vecino) <= distMin and not visitados[vecino]:
			distMin = G.getWeight(v,vecino)
			nodoMasCerca = vecino
	return nodoMasCerca

def actualizarLista(G,v,distancias,predecesores):
	vecinos = G.getSuccessors(v)
	for vecino in vecinos:
		if distancias[v] + G.getWeight(v,vecino) <= distancias[vecino]:
			distancias[vecino] = distancias[v] + G.getWeight(v,vecino)
			predecesores[vecino] = v
	return (distancias,predecesores)

def DijkstraA(G:GraphAL,source:int):
	distancias = [np.Inf]*G.size
	predecesores = [-1]*G.size
	visitados = [False]*G.size
	distancias[source] = 0
	predecesores[source] = source
	nVisitados = 0
	while nVisitados < G.size:
		if nVisitados == 0:
			v = source
		else:
			v = elMasCercanoNoVisitado(G,v,visitados)
		visitados[v] = True
		(distancias,predecesores) = actualizarLista(G,v,distancias,predecesores)
		nVisitados = nVisitados + 1
	return (distancias,predecesores)

def obtenerRuta(G:GraphAL,origen:int,destino:int,distancias:list,
	predecesores:list):
	ruta = [destino]
	acoso = 0
	nodoActual = destino
	while nodoActual != origen and nodoActual != -1:
		
		acoso += G.obtenerAcoso(predecesores[nodoActual],nodoActual)
		nodoActual = predecesores[nodoActual]
		ruta.append(nodoActual)
		
	ruta.reverse()
	return (ruta,distancias[destino],acoso)

def Dijkstra(G:GraphAL,source:int):
	distancias = [np.Inf]*G.size
	predecesores = [-1]*G.size
	


def DijkstraAcosoMinDist(G:GraphAL,origen:int,destino:int,nivelAcoso:float):
	
	(distancias,predecesores) = Dijkstra(G,origen)
	(ruta,distancia,acoso) = obtenerRuta(G,origen,destino,distancias,
		predecesores)
	
	while acoso > nivelAcoso and distancia < np.Inf:
		#Se encuentra el arco de máximo acoso en la ruta
		nodoOrigenMaximoAcosoArco = -1
		nodoDestinoMaximoAcosoArco = -1
		maximoAcosoArco = 0
		for indexNodoRuta in range(len(ruta) - 1):
			nodoOrigenArco = ruta[indexNodoRuta]
			nodoDestinoArco = ruta[indexNodoRuta + 1]
			acosoArco = G.obtenerAcoso(nodoOrigenArco,nodoDestinoArco)* \
			G.getWeight(nodoOrigenArco,nodoDestinoArco)/distancias[destino]
			
			if acosoArco > maximoAcosoArco:
				maximoAcosoArco = acosoArco
				nodoOrigenMaximoAcosoArco = nodoOrigenArco
				nodoDestinoMaximoAcosoArco = nodoDestinoArco
		#Se edita el arco de máximo acoso (su valor se vuelve infinito)
		G.editarArco(nodoOrigenMaximoAcosoArco,nodoDestinoMaximoAcosoArco,
			np.Inf)
		
		#Se vuelve a ejecutar Dijkstra
		(distancias,predecesores) = Dijkstra(G,origen)
		(ruta,distancia,acoso) = obtenerRuta(G,origen,destino,distancias,
			predecesores)
	return (ruta,distancia,acoso)

def ejemplo():
	G = GraphAL(6)
	G.addArc(0,1,2,3)
	G.addArc(0,2,4)
	G.addArc(1,2,1,2)
	G.addArc(1,3,7,4)
	G.addArc(2,4,3,1)
	G.addArc(3,5,1,3)
	G.addArc(4,5,5,8)
	G.addArc(4,3,2,8)
	
	print(DijkstraAcosoMinDist(G,0,5,10))

def crearGrafo():
	G = leerGrafo()
	pickle.dump(G, open("variableStoringFile.dat", "wb"))

def main():
	G = pickle.load(open("variableStoringFile.dat", "rb"))
	start = time.time()
	distancias,predecesores = Dijkstra(G,16)
	sucesores = [G.getSuccessors(vertice) for vertice in [16,17,18,19]]
	print(sucesores)
	for sucesor in sucesores:
		for vertice in sucesor:
			print('Vertice')
			print(vertice)
			print('Distancia')
			print(distancias[vertice])
			print('Predecesor')
			print(predecesores[vertice])
	
#	print(G.getSuccessors(16))
#	print(G.getSuccessors(17))
#	print(G.getSuccessors(18))
#	print(G.getSuccessors(19))
#	print(G.getSuccessors(5387))
#	print(G.getSuccessors(5391))
#	print(G.getSuccessors(144))
#	print(G.getSuccessors(152))
	end = time.time()
	#print(end - start)
	
main()