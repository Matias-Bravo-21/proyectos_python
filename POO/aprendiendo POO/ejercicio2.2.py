class Animal:
    def __init__(self):
        pass

    def comer(self):
        print(f"estoy comiendo")

class mamifero(Animal):
    def __init__(self):
        pass

    def amamantar(self):
        print(f"estoy amamantando")

class Ave(Animal):
    def __init__(self):
        pass

    def volar(self):
        print(f"estoy volando")

class murcielago(mamifero,Ave):
    def __init__(self):
        pass

murcielago1=murcielago()

murcielago1.comer()
murcielago1.amamantar()
murcielago1.volar()