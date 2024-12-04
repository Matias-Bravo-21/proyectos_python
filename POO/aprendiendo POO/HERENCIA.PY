"""
la herencia nos permite de un molde ampliar a otras clases manteniendo atributos
"""
class persona:
    def __init__(self, nombre,edad,nacionalidad):
        self.nombre = nombre
        self.edad= edad
        self.nacionalidad = nacionalidad
class empleado(persona):
    def __init__(self,nombre,edad,nacionalidad,trabajo,salario):
        super().__init__(nombre,edad,nacionalidad)
        self.trabajo = trabajo
        self.salario = salario

roberto = empleado("roberto",23,"chileno", "programador", 23000)

print()

#herencia multiple

class Artista():
    def __init__(self, habilidad):
        self.habilidad = habilidad
    def mostrar_habilidad(self):
        return (f"mi habilidad es: {self.habilidad}")

class trabajador(persona,Artista):
    def __init__(self, nombre,edad,nacionalidad, habilidad, salario, puesto):
        persona.__init__(self,nombre,edad,nacionalidad)
        Artista.__init__(self,habilidad)
        self.salario = salario
        self.puesto = puesto


trabajadorcantante = trabajador("claudio",23,"chileno","cantar",23000,"cantante de coro")

trabajadorcantante.mostrar_habilidad()