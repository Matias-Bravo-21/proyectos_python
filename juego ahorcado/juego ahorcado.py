import random
import palabras_secretas
import time
import turtle
"""
def tablero():
    #crear la ventana
    pestaña = turtle.Screen()
    pestaña.title("bienvenido al ahorcado de matias.py")
    pestaña.setup(width=600,height=600)
    pestaña.bgcolor("white")

    #DIBUJAR EL AHORCAdo
    t = turtle.Turtle()
    t.speed(0)
    t.width(5)

    #funcion para dibujar al ahorcado
    def dibujo():
        t.penup()
        t.goto(-200,-200)
        t.pendown()
        t.forward(200)
        t.right(90)
        t.forward(50)
        t.right(90)
        t.forward(20)
        t.right(90)
        t.forward(10)
        t.right(90)
        
    dibujo()
    pestaña.mainloop()
"""

def obtener_palabra_aleatoria():
    palabras = palabras_secretas.palabras_secretas
    palabra_aleatoria=random.choice(palabras)
    return palabra_aleatoria

def mostrar_tablero(palabra_secreta, letras_adivinadas):
    tablero = ""
    for letra in palabra_secreta:
        if letra in letras_adivinadas:
            tablero +=letra
        else:
            tablero += "_"
    print(tablero)
"""
def tiempo_funcion(tiempo):
    for i in range(tiempo, 0, -1):
        print(f"tiempo restante: {i}")
        #time.sleep(1)
    print(tiempo)
"""
def jugar_ahorcado():
    palabra_secreta1 = obtener_palabra_aleatoria()
    letra_adivinadas = []
    intentos_restantes = 6
    palabra_secreta = (palabra_secreta1).lower()

    while intentos_restantes > 0:
        tiempo =60
        #tiempo_funcion(tiempo)
        mostrar_tablero(palabra_secreta,letra_adivinadas)
        letra = input("introduce una letra: ").lower()

        if letra in letra_adivinadas:
            print("ya has introducido esta letra bro intenta otra")
            continue
        
        if letra in palabra_secreta:
            letra_adivinadas.append(letra)
            intentos_restantes += 1
            tiempo = 60
            print("has ganado 1 intento")
            if set(letra_adivinadas) == set(palabra_secreta):
                print(f"has ganado bro adivinaste {palabra_secreta}")
                break
        else:
            intentos_restantes-=1
            print(f"letra incorrecta te quedan {intentos_restantes}")
    if intentos_restantes == 0:
        print(f"has perdido la palabra era {palabra_secreta}")

jugar_ahorcado()
#tablero()
                          