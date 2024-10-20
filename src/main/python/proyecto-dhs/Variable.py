from ID import ID, TipoDato

class Variable(ID):
    def __init__(self, nombre: str, tipo_dato: TipoDato):
        super().__init__(nombre, tipo_dato)


    def __str__(self):
        return f"Variable(nombre={self.nombre}, tipo={self.tipo_dato}, inicializado={self.inicializado}, usado={self.usado})"