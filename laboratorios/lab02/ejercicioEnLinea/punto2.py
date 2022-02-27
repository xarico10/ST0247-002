import numpy as np
from itertools import permutations

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
        print(entradas)  
        numeroReinas = int(archivo.readline())
    archivo.close() 
    print(entradas)    

def seAtacanHastaI(tablero,i):
  for j in range(i + 1):
     for k in range(j + 1,i + 1):
        if abs(tablero[j] - tablero[k]) == abs(j - k) or tablero[j] == tablero[k]:
           return True
  return False

def nReinasCasillasProhibidas(n:int):
	#nreinasAuxPrint(n,0,[0]*n)
    l = []
    nReinasAux(n,0,[0]*n,l)
    return l

def nReinasAux(n:int,c:int,t:list,l:list):
  if c == n:
    l.append(t)
    print(t)
    #print(l)
    return
  else:
    for f in range(n):
      t[c] = f
      if not seAtacanHastaI(t,c):
        nReinasAux(n,c + 1,t,l)
        

#def nReinasCasillasProhibidasBT(arrayEntrada):



# def nReinasCasillasProhibidas(arrayEntrada):
#     for entrada in arrayEntrada:
#         nReinas = entrada[0]
#         casillasProhibidas = entrada[1]
#         permutaciones

    





def main():
    nReinasCasillasProhibidas(4)
    
main()