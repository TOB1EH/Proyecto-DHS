from enum import Enum
from abc import ABC

class TipoDato(Enum):
    INT     = 1
    FLOAT   = 2
    CHAR    = 3

class ID(ABC):
    def __init__(self, nombre: str, tipo_dato: TipoDato):
        self._nombre = nombre
        self._tipo_dato = tipo_dato
        self._inicializado = False
        self._usado = False

    def setInicializado (self):
        """
        Indica que el ID ha sido inicializado.
        """
        self._inicializado = True

    def setUsado (self):
        """
        Indica que el ID ha sido usado.
        """
        self._usado = True

    def getInicializado (self):
        """
        Indica si el ID ha sido inicializado.
        """

        return self._inicializado

    def getUsado (self):
        """
        Indica si el ID ha sido usado.
        """

        return self._usado

    def obtenerNombre (self):
        """
        Obtiene el nombre del ID.
        """
        return self._nombre