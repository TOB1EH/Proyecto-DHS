from ID import ID, TipoDato

class Funcion(ID):
    def __init__(self, nombre: str, tipo_dato: TipoDato):
        super().__init__(nombre, tipo_dato)
        # self.args = list()
        self.args: list[ID] = []
    