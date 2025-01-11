
from .Contexto import Contexto
from .ID import ID

class TablaSimbolos:
    _instancia = None # atributo privado para almacenar la referencia instancia unica de la clase 
    
    # _contextos  = []
    _contextos: list[Contexto] = [] # atributo privado de la lista de contextos de la tabla
    
    def __new__(cls):
        """
        Método especial que se utiliza para crear una nueva instancia de la clase.

        Este método es parte del patrón Singleton, que asegura que solo haya una 
        única instancia de la clase 'TablaSimbolos' durante la ejecución del programa.

        Args:
            cls: La clase que se está instanciando.

        Returns:
            La instancia única de la clase 'TablaSimbolos'.
        """
    
        # Verifica si ya existe una instancia de la clase
        if cls._instancia is None: 
            # Si no existe instancia, crea una nueva y la asigna al atributo '_instancia'
            cls._instancia = super(TablaSimbolos, cls).__new__(cls)  # Llama al método '__new__' de la superclase 'object'

            # (Opcional) Inicializa atributos adicionales para la nueva instancia
            # cls._instancia.contextos = []

        # Devuelve la instancia de la clase, ya sea la existente o la recién creada
        return cls._instancia

    def agregarContexto(self, nombre):
        """
        Agrega un nuevo contexto a la lista de la tabla de simbolos.
        """
        
        nuevo_contexto = Contexto(nombre)
        self._contextos.append(nuevo_contexto)

    def borrarContexto(self):
        """
        Elimina el contexto actual de la lista de contextos de la tabla
        """
        if self._contextos:
            self._contextos.pop()

    def obtenerContextos(self):
        """
        Devuelve la lista de contextos de la tabla de simbolos
        """
        
        return self._contextos

    def agregarIdentificador(self, identificador: ID):
        """ 
        Agrega un identificador de una variable o funcion dentro del ultimo
        Contexto registrado en la tabla de simbolos
        """
        
        if self._contextos:
            self._contextos[-1].agregarID(identificador)

    def buscarLocal(self, nombre: str):
        """
        Busca localmente en un Contexto el nombre de una variable o funcion
        Retorna el valor del ID encontrado o None si no existe
        """
        
        if self._contextos:
            return self._contextos[-1].buscarID(nombre)
        return None # Si la lista de contextos esta vacia

    def buscarGlobal(self, nombre: str) -> ID:
        """ 
        Este método recorre la lista de contextos en orden inverso y utiliza 
        el método `buscarID` de cada contexto para intentar encontrar un 
        identificador que coincida con el nombre proporcionado.

        Args:
            nombre (str): El nombre del identificador que se desea buscar.

        Returns:
            ID: El identificador encontrado si existe en alguno de los contextos; 
            de lo contrario, devuelve None si no se encuentra o si la lista de 
            contextos está vacía.
        """
        
        if self._contextos:    
            for contexto in reversed(self._contextos):
                resultado = contexto.buscarID(nombre)
                if resultado:
                    return resultado
        return None # Si la lista de contextos esta vacia o el ID no existe globalmente
    
    def actualizarUsado (self, nombre:str):
        """
            Busca localmente en un Contexto el nombre de una variable o funcion y 
            si no esta usado actualiza su estado a usado. El identificador debe
            existir en la tabla de simbolo, caso contrario no hace nada.
        """

        identificador = self.buscarGlobal(nombre)
        if identificador.getUsado() is False: # Si el ID no esta usado
            identificador.setUsado() # Setea su valor a usado

    def mostrarContextoActual (self):
        """ 
        Retorna el toString del Contexto actual
        """
        
        if self._contextos:
            return self._contextos[-1].__str__()

    def obtenerNombreContexto(self):
        """
        Retorna el nombre del Contexto actual
        """

        if self._contextos:
            return self._contextos[-1].nombre
        return "Sin Contexto"
    
    def __str__(self):
        """
        Retorna el toString de la tabla de simbolos
        """
        
        return f"TablaSimbolos(contextos={self._contextos})"