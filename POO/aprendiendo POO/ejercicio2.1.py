class persona:
    def __init__(self,nombre,edad):
        self.nombre =nombre
        self.edad =edad
    def mostrarnombre(self):
        print(f"mi nombre es: {self.nombre}")
    def mostraredad(self):
        print(f"mi edad es: {self.edad}")
    
class estudiante(persona):
    def __init__(self, nombre,edad,grado):
        super().__init__(nombre,edad)
        self.grado = grado

    def mostrarGrado(self):
        print(f"mi grado es: {self.grado}")

alumno = estudiante("matias",23,"1er año informatica")

alumno.mostrarnombre()
alumno.mostraredad()
alumno.mostrarGrado()