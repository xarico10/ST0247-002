import numpy as np
from itertools import permutations
from itertools import chain

def leerEntrada(nombreArchivo):
  archivo = open(nombreArchivo)
  numeroReinas = int(archivo.readline())
  entradas = []
  while numeroReinas != 0:
    #Diccionario de casillas prohibidas
    casillasProhibidas = {}
    #Leer todas las filas del tablero
    for indexFila in range(numeroReinas):
      fila = archivo.readline()
      if '*' in fila: #Hay por lo menos un asterísco en la fila actual
        casillasProhibidasFila = []
                #Se almacena la posición de todos los asteríscos de la fila en casillasProhibidasFila
        for index,caracter in zip(range(len(fila)),fila):
          if caracter == '*':
            casillasProhibidasFila.append(index)
        casillasProhibidas[indexFila] = casillasProhibidasFila
    entradas.append([numeroReinas,casillasProhibidas])
    numeroReinas = int(archivo.readline())
  archivo.close() 
  return entradas

def permutacionEsValida(nReinas,permutacion,casillasProhibidasTablero):
  for i in range(nReinas):
    if i in casillasProhibidasTablero.keys():
      if casillasProhibidasTablero[i] == [permutacion[i]]:
        return False
    for j in range(i + 1,nReinas):
      if abs(permutacion[i] - permutacion[j]) == abs(i - j):
        return False
  return True

def nReinasCasillasProhibidas(arrayEntrada):
  for entrada,entradaIndex in zip(arrayEntrada,range(len(arrayEntrada))):
    nSoluciones = 0
    nReinas = entrada[0]
    casillasProhibidasTablero = entrada[1]
    permutaciones = permutations(range(nReinas))
    for permutacion in permutaciones:
      permutacionValida = permutacionEsValida(nReinas,permutacion,casillasProhibidasTablero)
      if permutacionValida:
        nSoluciones = nSoluciones + 1
    print('Case ' + str(entradaIndex + 1) + ': ' + str(nSoluciones))
      


def ejecucionEjemplo():
  arrayEntrada = leerEntrada('archivoPrueba.txt')
  nReinasCasillasProhibidas(arrayEntrada)
    
ejecucionEjemplo()