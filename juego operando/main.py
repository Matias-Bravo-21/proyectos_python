#juego de fusion
class guerrero():
    def __init__(self,nombre):
        self.nombre = nombre
    
    def atacar(self):
        pass

    def defenderse(self):
        pass

    def fusionarse(self):
        pass

class sayayin(guerrero):
    def __init__(self, nombre,edad,defensa,poder,ki):
        super().__init__(nombre)
        self.edad = edad
        self.poder = poder
        self.ki = ki
        self.defensa = defensa
    def atacar(self):
        return self.poder
    
    def defenderse(self):
        return self.defensa
    
    def __add__(self,otroguerrero):
        return self.poder + otroguerrero.poder

class namekusei(guerrero):
    def __init__(self, nombre,edad, defensa,poder,ki):
        super().__init__(nombre)
        self.edad = edad
        self.poder = poder
        self.ki = ki
        self.defensa = defensa

    def atacar(self):
        return self.poder
    
    def defenderse(self):
        return self.defensa
    
    def __add__(self,otroguerrero):
        return self.poder + otroguerrero.poder
    
goku = sayayin("son goku",37,48,104,84)

picolo = namekusei("piccolo", 21,46,36,39)

fusion = goku + picolo

print(fusion)