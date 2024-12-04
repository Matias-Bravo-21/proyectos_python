from constantes import constantes

class Personaje:
    def __init__(self, Nombre, edad):
        self.nombre = Nombre
        self.edad = edad
        self.corazon = constantes.corazon
        self.cerebro = constantes.cerebro
        self.musculatura = constantes.musculatura
        self.atletismo = constantes.atletismo
        self.vida = constantes.vida
    
    def presentarse(self):
        return f"Hola, soy {self.nombre}, tengo {self.edad} años."

    def mostrar_estadisticas(self):
        return (f"Estadísticas de {self.nombre}:\n"
                f"Corazón: {self.corazon}\n"
                f"Cerebro: {self.cerebro}\n"
                f"Musculatura: {self.musculatura}\n"
                f"Atletismo: {self.atletismo}\n"
                f"Vida: {self.vida}")
    
    #getters
    def get_nombre(self):
        return self.nombre

    def get_edad(self):
        return self.edad

    def get_corazon(self):
        return f"El corazón está al {self.corazon}"

    def get_cerebro(self):
        return f"El cerebro está al {self.cerebro}"

    def get_musculatura(self):
        return f"La musculatura está al {self.musculatura}"

    def get_atletismo(self):
        return f"El atletismo está al {self.atletismo}"

    def get_vida(self):
        return f"La vida está al {self.vida}"
    
    # Setters
    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_edad(self, edad):
        self.edad = edad

    def set_corazon(self, corazon):
        self.corazon = corazon

    def set_cerebro(self, cerebro):
        self.cerebro = cerebro

    def set_musculatura(self, musculatura):
        self.musculatura = musculatura

    def set_atletismo(self, atletismo):
        self.atletismo = atletismo

    def set_vida(self, vida):
        self.vida = vida
