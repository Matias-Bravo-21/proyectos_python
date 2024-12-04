import random

lista = []

def crear_numeros(repeticiones):
    for i in range(repeticiones):
        num = random.randint(0,100)
        lista.append(num)
crear_numeros(10)
#solucion facil
#lista.sort()
def ordenamiento_burbuja(lista):
    length = len(lista) - 1
    for i in range(0,length):
        for j in range(0 ,length):
            if lista[j] > lista[j+1]:
                aux = lista[j]
                lista[j] = lista[j+1]
                lista[j+1] = aux

#imprimimos la litsa desordenada
print(lista)
#llamamos a la funcion
ordenamiento_burbuja(lista)
#imprimimos la lista ordenada
print(lista)

