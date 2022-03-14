def seAtacanHastaI(tablero,i):
  for j in range(i + 1):
     for k in range(j + 1,i + 1):
        if abs(tablero[j] - tablero[k]) == abs(j - k) or tablero[j] == tablero[k]:
           return True
  return False

def nreinas(n:int):
  nreinasAuxPrint(n,0,[0]*n)
  
def nreinasAuxPrint(n:int,c:int,t:list):
  if c == n:
    print(t)
    return
  else:
    for f in range(n):
      t[c] = f
      if seAtacanHastaI(t,c):
        pass
      else:
        nreinasAuxPrint(n,c + 1,t)

def nreinasAuxLista(n:int,c:int,t:list,l:list):
  if c == n:
    l.append(t)
    return
  else:
    for f in range(n):
      t[c] = f
      if seAtacanHastaI(t,c):
        pass
      else:
        nreinasAuxLista(n,c + 1,t,l)

def hayCamino(g, o:int, d:int, visitados:list)->bool:
  if o == d:
    return True
  else:
    for vecino in g.getSuccessors(o):
      hayCaminoDelVecinoAd = hayCamino(g,vecino,d)
      if hayCaminoDelVecinoAd:
        return True
    return False #·Si nunca dio verdadero, es falso

def main():
    print(nreinas(4))
main()