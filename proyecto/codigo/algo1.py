import pandas as pd
import numpy as np
import time
import pickle
import math
import heapq

class GraphAL:
	def __init__(self,size,infoNodos = [],arrayArcos = []):
		self.size = size
		self.arregloDeListasDist = [0]*size
		self.arregloDeListasAcoso = [0]*size
		self.infoNodos = infoNodos
		self.infoArcos = arrayArcos
		for i in range(size):
			self.arregloDeListasDist[i] = []
			self.arregloDeListasAcoso[i] = []
			
		#arrayArcos = [origen,destino,distancia,acoso,nombre]
		#arregloDeListasDist[origen] = (distancia,destino,nombre)
		#arregloDeListasAcoso[origen] = (acoso,destino,nombre)
		for arco in arrayArcos:
			self.arregloDeListasDist[arco[0]].append((arco[2],arco[1],arco[4]))
			self.arregloDeListasAcoso[arco[0]].append((arco[3],arco[1],arco[4]))
	
	def addArc(self,origen,destino,distancia,acoso = 0, nombre = ''):
		self.arregloDeListasDist[origen].append((distancia,destino,nombre))
		self.arregloDeListasAcoso[origen].append((acoso,destino,nombre))
	
	def getSuccessors(self, vertice):
		return [tupla[1] for tupla in self.arregloDeListasDist[vertice]]
	
	def obtenerDistancia(self, source, destination):
		for tupla in self.arregloDeListasDist[source]:
			if tupla[1] == destination:
				return tupla[0]
			
	def obtenerAcoso(self, source, destination):
		for tupla in self.arregloDeListasAcoso[source]:
			if tupla[1] == destination:
				if tupla[0] is None:
					return 0
				return tupla[0]
			
	def editarDistancia(self,origen,destino,nuevaDistancia):
		for index,tupla in zip(range(len(self.arregloDeListasDist[origen])),self.arregloDeListasDist[origen]):
			if tupla[1] == destino:
				self.arregloDeListasDist[origen][index] = (nuevaDistancia,tupla[1],tupla[2])
			
	def editarAcoso(self,origen,destino,nuevoAcoso):
		for index,tupla in zip(range(len(self.arregloDeListasAcoso[origen])),self.arregloDeListasAcoso[origen]):
			if tupla[1] == destino:
				self.arregloDeListasDist[origen][index] = (nuevoAcoso,tupla[1],tupla[2])
				
	def indexEnLista(self,origen,destino):
		for i in range(len(self.arregloDeListasDist[origen])):
			tupla = self.arregloDeListasDist[origen][i]
			if tupla[1] == destino:
				return i
		return

def Algo1(G:GraphAL,origen:int,destino:int,tolAcoso):
	distancias,acosos,predecesores = DijkstraMinDist(G,origen)
	ruta = obtenerRuta(destino, predecesores)
	mejorRuta = ruta
	mejorDist = distancias[destino]
	mejorAcoso = acosos[destino]
	while acosos[destino] > tolAcoso and distancias[destino] != np.Inf:
		mejorRuta = ruta
		mejorDist = distancias[destino]
		mejorAcoso = acosos[destino]
		
		#Encontrar arco máximo acoso
		acosoMax = 0
		nodoOrigenMaxAcoso = -1
		nodoDestinoMaxAcoso = -1
		for indexNodoOrigen in range(len(ruta) - 1):
			nodoOrigen = ruta[indexNodoOrigen]
			nodoDestino = ruta[indexNodoOrigen + 1]
			acosoArco = G.obtenerAcoso(nodoOrigen,nodoDestino)
			if acosoArco > acosoMax:
				nodoOrigenMaxAcoso = nodoOrigen
				nodoDestinoMaxAcoso = nodoDestino
				acosoMax = acosoArco
		#Edita arco por Inf
		G.editarDistancia(nodoOrigenMaxAcoso,nodoDestinoMaxAcoso,np.Inf)
		distancias,acosos,predecesores = DijkstraMinDist(G, origen)
		ruta = obtenerRuta(destino, predecesores)
		
	if distancias[destino] < np.Inf:
		mejorDist = distancias[destino]
		mejorAcoso = acosos[destino]
		mejorRuta = ruta
	else:
		print('Tolerancia no alcanzada: retornando última ruta evaluada')
		
	return mejorDist,mejorAcoso,mejorRuta
		
def DijkstraMinDist(G:GraphAL,origen:int):
	distancias = [np.Inf]*G.size
	pred = [-1]*G.size
	
	distancias[origen] = 0
	colaPrioridad = [(0,origen,'')]
	heapq.heapify(colaPrioridad)
	
	while len(colaPrioridad) != 0:
		tuplaVerticeMasCercano = heapq.heappop(colaPrioridad)
		verticeMasCercano = tuplaVerticeMasCercano[1]
		distanciaMasCercano = tuplaVerticeMasCercano[0]
		
		if distanciaMasCercano > distancias[verticeMasCercano]:
			continue
		
		for tuplaVecino in G.arregloDeListasDist[verticeMasCercano]:
			verticeVecino = tuplaVecino[1]
			distanciaVecino = distanciaMasCercano + tuplaVecino[0]
			tuplaVecinoAcoso = G.arregloDeListasAcoso[verticeMasCercano]
			
			if distanciaVecino < distancias[verticeVecino]:
				distancias[verticeVecino] = distanciaVecino
				pred[verticeVecino] = verticeMasCercano
				tuplaVecino = (distanciaVecino,tuplaVecino[1],tuplaVecino[2])
				heapq.heappush(colaPrioridad,tuplaVecino)
				
	acosos = [0]*G.size
	nodosSinOrigen = set(range(G.size)) - set([origen])
	nodosSinOrigen = list(nodosSinOrigen)
	for nodo in nodosSinOrigen:
		predecesor = pred[nodo]
		nodoActual = nodo
		acoso = 0
		while predecesor != -1:
			acoso += G.obtenerAcoso(predecesor, nodoActual)
			nodoActual = predecesor
			predecesor = pred[predecesor]
			
		acosos[nodo] = acoso
			
	return distancias,acosos,pred

def obtenerRuta(destino,predecesores):
	ruta = [destino]
	nodoActual = destino
	predecesor = predecesores[destino]
	while predecesor != -1:
		ruta.append(predecesor)
		nodoActual = predecesor
		predecesor = predecesores[nodoActual]
		
	ruta.reverse()
	return ruta
	
def main():
	a = [np.Inf]*5
	print(a)
	
def ejemplo():
	G = GraphAL(8)
	G.addArc(0, 1, 4, 5)
	G.addArc(0, 2, 2, 1)
	G.addArc(0, 5, 7, 6)
	
	G.addArc(1, 0, 4, 5)
	G.addArc(1, 3, 2, 14)
	
	G.addArc(2, 0, 2, 1)
	G.addArc(2, 5, 3, 2)
	G.addArc(2, 4, 8, 4)
	
	G.addArc(3, 1, 2, 14)
	G.addArc(3, 5, 5, 4)
	G.addArc(3, 6, 6, 5)
	
	G.addArc(4, 2, 8, 4)
	G.addArc(4, 7, 3, 4)
	
	G.addArc(5, 7, 4, 7)
	G.addArc(5, 0, 7, 6)
	G.addArc(5, 2, 3, 2)
	G.addArc(5, 3, 5, 4)
	
	
	G.addArc(6, 3, 6, 5)
	G.addArc(6, 7, 2, 3)
	
	G.addArc(7, 4, 3, 4)
	G.addArc(7, 6, 2, 3)
	G.addArc(7, 5, 4, 7)
	
	origen = 0
	destino = 3
	distancias,acosos,predecesores = DijkstraMinDist(G,origen)
	print((distancias,acosos,predecesores))
	ruta = obtenerRuta(destino,predecesores)
	print(Algo1(G,origen,destino,11))
	
	

def a():
#	G = leerGrafo()
#	pickle.dump(G, open("variableStoringFile.dat", "wb"))
	G = pickle.load(open("variableStoringFile.dat", "rb"))
	origen = 1321
	destino = 1981
	distancias,acosos,predecesores = DijkstraMinDist(G, origen)
	print(distancias[destino])
	print(acosos[destino])
	
	start = time.time()	
	Algo1(G, origen, destino, 19)
	end = time.time()
	print(end - start)
	
	
a()