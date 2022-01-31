#Punto 1
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
  permutacionesAux(cadena,"")

def permutacionesAux(pregunta, respuesta):
    if len(pregunta) == 0:
        print(respuesta)
    else:
        for i in range(0,len(pregunta)):
            permutacionesAux(pregunta[0:i] + pregunta[i + 1:],respuesta + pregunta[i])

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
    subconjuntos("abc")
main()            