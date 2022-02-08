#Punto 1
from math import factorial


def subconjuntos(cadena):
  subconjuntosAux(cadena, "")
  
def subconjuntosAux(pregunta, respuesta):
  if len(pregunta) == 0:
    print(respuesta)
  else:
    subconjuntosAux(pregunta[1:],respuesta + pregunta[0])
    subconjuntosAux(pregunta[1:],respuesta)

#Punto 2
def permutaciones(cadena):
    lista = []
    permutacionesAux(cadena,"",lista)
    return lista


def permutacionesAux(pregunta,respuesta,lista):
    if len(pregunta) == 0:
        #print(respuesta)
        lista.append(respuesta)
    else:
        for i in range(0,len(pregunta)):
            permutacionesAux(pregunta[0:i] + pregunta[i + 1:],respuesta + pregunta[i],lista)
##Punto 3
def nReinas(n:int):
    pass    
def nReinasAux():
    pass


#Punto 4
def permutacionesRepeticion(cadena):
    permutacionesRepeticionAux(cadena,"")

def permutacionesRepeticionAux(pregunta,respuesta):
    if len(respuesta) == len(pregunta):
        print(respuesta)
    else:
        for i in range(0,len(pregunta)):
            permutacionesRepeticionAux(pregunta,respuesta + pregunta[i])

def main():
    print(permutaciones("abc"))
main()            