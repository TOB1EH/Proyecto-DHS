from enum import Enum
from abc import ABC

class TipoDato(Enum):
    char    = 1
    int     = 2
    float   = 3
    double  = 4

    def getTipoDato (self):
        return self.name
    
    # Implementamos los métodos de comparación basados en self.value
    def __lt__(self, other):
        if isinstance(other, TipoDato):
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, TipoDato):
            return self.value <= other.value
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, TipoDato):
            return self.value > other.value
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, TipoDato):
            return self.value >= other.value
        return NotImplemented

class ID(ABC):

    miContexto = None

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
    
    def obtenerTipoDato(self):
        """
        Obtiene el tipo de dato del ID.
        """

        return self._tipo_dato