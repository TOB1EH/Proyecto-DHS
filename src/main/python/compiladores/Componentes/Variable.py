from .ID import ID, TipoDato

class Variable(ID):
    def __init__(self, nombre: str, tipo_dato: TipoDato):
        super().__init__(nombre, tipo_dato)