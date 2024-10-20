from enum import Enum
from abc import ABC

class TipoDato(Enum):
    INT     = 1
    FLOAT   = 2
    CHAR    = 3

class ID(ABC):
    def __init__(self, nombre: str, tipo_dato):
        self.nombre = nombre
        self.tipo_dato = tipo_dato
        self.inicializado = False
        self.usado = False

    def setInicializado (self):
        self.inicializado = True

    def setUsado (self):
        self.usado = True