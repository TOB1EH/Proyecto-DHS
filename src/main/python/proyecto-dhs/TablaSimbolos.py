# from typing import List
from Contexto import Contexto
from ID import ID

class TablaSimbolos:
    # atributo privado para almacenar la referencia instancia unica de la clase
    _instance = None 
    
    # Sobreescritura del metodo 'new' que se usa cuando se intenta crear una    
    # nueva instancia de la clase
    # Recibe la clase misma como argumento convencionalmente llamado 'cls'
    # Este método se llama antes que __init__ y es responsable de crear y 
    # devolver la nueva instancia.'
    def __new__(cls):
        # Verifica si ya existe una instancia de la clase
        if cls._instance is None: 
            # Si no existe instancia, crea una nueva y la asigna al atributo '_instance'
            cls._instance = super(TablaSimbolos, cls).__new__(cls) # llama al método '__new__' de la superclase 'object'
            cls._instance.contextos = [] # Revisar
        # Devuelve la instancia de la clase
        return cls._instance


    def addContexto(self, nuevo_contexto: Contexto):
        self.contextos.append(nuevo_contexto)

    def delContexto(self):
        if self.contextos:
            self.contextos.pop()

    def addIdentificador(self, identificador: ID):
        if self.contextos:
            self.contextos[-1].addID(identificador)

    def buscar_local(self, nombre: str) -> ID:
        if self.contextos:
            return self.contextos[-1].buscarID(nombre)
        return None # Si la lista de contextos esta vacia

    def buscar_global(self, nombre: str) -> ID:
        if self.contextos:    
            for contexto in reversed(self.contextos):
                resultado = contexto.buscarID(nombre)
                if resultado:
                    return resultado
        return None # Si la lista de contextos esta vacia

    # toString
    def __str__(self):
        return f"TablaSimbolos(contextos={self.contextos})"