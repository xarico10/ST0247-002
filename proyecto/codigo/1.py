import pandas as pd
import numpy as np
import time
from collections import deque
import pickle
import math

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

def heapDown(H:list,i:int):
	n = len(H)
	while 2*(i + 1) <= n - 1:
		k = 2*i + 1
		if H[k] > H[k + 1]:
			k = k + 1
		if H[i] > H[k]:
			#Swap(H[i],H[k])
			elementoEnI = H[i]
			H[i] = H[k]
			H[k] = elementoEnI
			i = k
		else:
			return H
		
	if 2*i + 1 == n - 1 and H[i] > H[n - 1]:
		#Swap(H[i],H[n - 1])
		elementoEnI = H[i]
		H[i] = H[n - 1]
		H[n - 1] = elementoEnI
		return H
	
	return H

#Algoritmo de Floyd
def construirHeap(H:list):
	n = len(H)
	for i in range(math.floor(n/2) - 1,-1,-1):
		H = heapDown(H,i)
	return H

def main():
	H = [5,1,2,6,7,9,3]
	print(construirHeap(H))
	
main()