from Variable import Variable
from ID import ID

class Contexto:
    def __init__(self):
        # self._tabla = dict()
        self._tabla: dict[str, ID] = {}

    def addID (self, variable: Variable):
        self._tabla[variable.nombre] = variable

    def buscarID (self, nombre: str) -> Variable:
        return self.tabla.get(nombre)

    # toString
    def __str__(self):
        return f"Contexto(tabla={self.tabla})"