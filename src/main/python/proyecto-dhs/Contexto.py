
from ID import ID

class Contexto:
    def __init__(self):
        # self._tabla = {}
        # self._tabla = dict()
        self._tabla: dict[str, ID] = {} # Un Contexto es una tabla de ID's

    def agregarID (self, identificador: ID):
        """
        Agrega un ID de una variable o funcion a la tabla
        """
        self._tabla[identificador.obtenerNombre()] = identificador

    def buscarID (self, nombre: str):
        """
        Busca un ID con su nombre y lo retorna
        """
        return self._tabla.get(nombre)

    def obtenerIdentificadores (self) -> dict:
        """ 
        Retorna una copia de la tabla de identificadores
        """
        return self._tabla

    def __str__(self):
        """
        Devuelve una representación en cadena de la tabla de ID's
        """
        return f"Contexto(tabla={self._tabla})"