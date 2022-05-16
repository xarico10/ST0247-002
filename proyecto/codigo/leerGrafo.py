import pandas as pd
import numpy as np
import pickle
import math

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
		for tupla in self.arregloDeListasDist[origen]:
			if tupla[1] == destino:
				tupla[0] = nuevaDistancia
				
	def editarAcoso(self,origen,destino,nuevoAcoso):
		for tupla in self.arregloDeListasAcoso	[origen]:
			if tupla[1] == destino:
				tupla[0] = nuevoAcoso
				
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
		
			arcos.append((indexOrigenArco,indexDestinoArco,
				float(fila['length']),float(fila['harassmentRisk']),
				fila['name']))
		
			arcos.append((indexDestinoArco,indexOrigenArco,
				float(fila['length']),float(fila['harassmentRisk']),
				fila['name']))
		
		
		
	G = GraphAL(nNodos,coordenadasNodos,arcos)
	#print(arcos)
	return G

