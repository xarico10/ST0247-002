def busquedaBinaria(arreglo:list,valor:int):
    limIzq = 0
    limDer = len(arreglo) - 1
    while limIzq <= limDer:
        mitad = (limDer + limIzq) // 2
        if arreglo[mitad] > valor:
            limDer = mitad - 1
        elif arreglo[mitad] < valor:
            limIzq = mitad + 1
        else:
            return mitad
    return -1

def mergeSort(arreglo: list): 
    if len(arreglo) <= 1:
        return arreglo
    mitad = len(arreglo) // 2
    izq = mergeSort(arreglo[:mitad])
    der = mergeSort(arreglo[mitad:])
    return pegarMitades(izq,der)

def pegarMitades(izq,der):
    resultado = []
    indiceIzq = 0
    indiceDer = 0
    while indiceIzq < len(izq) and indiceDer < len(der):
        if izq[indiceIzq] < der[indiceDer]:
            resultado.append(izq[indiceIzq])
            indiceIzq += 1
        else:
            resultado.append(der[indiceDer])
            indiceDer += 1
    #Se pega lo que sobró de izq o der
    resultado += izq[indiceIzq:]
    resultado += der[indiceDer:]
    return resultado
    
print(mergeSort([4,0,3,1,2]))



    

