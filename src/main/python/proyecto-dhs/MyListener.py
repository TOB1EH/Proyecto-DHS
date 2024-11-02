from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser
from TablaSimbolos import TablaSimbolos
from Contexto import Contexto
from Variable import Variable

class MyListener (compiladoresListener):
    """
    Clase que implementa el listener para el analizador sintáctico. 
    """

    tabla_simbolos = TablaSimbolos()
    pila_variables = []

    def enterPrograma(self, ctx:compiladoresParser.ProgramaContext):
        """
        Método que se ejecuta al entrar en el contexto de la regla "programa".
        """

        print("\n+" + "="*10, "Comienza la Compilacion", "="*10 + "+\n")
        contexto_global = Contexto()                          # Crea el contexto global
        self.tabla_simbolos.agregarContexto(contexto_global); # Agrega el contexto global (primer contexto) a la tabla de simbolos

    def exitPrograma(self, ctx:compiladoresParser.ProgramaContext):
        """
        Método que se ejecuta al salir del contexto de la regla "programa".
        """
        
        print("\n+" + "="*10, "Fin de la Compilacion", "="*10 + "+\n")
        self.tabla_simbolos.borrarContexto() # Borra el contexto global (Ultimo contexto restante)

    def enterBloque(self, ctx:compiladoresParser.BloqueContext):
        """
        Método que se ejecuta al entrar en el contexto de la regla "bloque".
        """

        nuevo_contexto = Contexto()                         # Crea un nuevo Contexto
        self.tabla_simbolos.agregarContexto(nuevo_contexto) # Agrega un nuevo Contexto a la tabla de simbolos

    def exitBloque(self, ctx:compiladoresParser.BloqueContext):
        """
        Método que se ejecuta al salir del contexto de la regla "bloque".
        """

        # Obtenemos todos los contextos de la tabla de simbnolos
        contextos = self.tabla_simbolos.obtenerContextos() 

        # Recorremos el contexto actual en busca de ID no inicializados y/o usados
        for variable in contextos[-1].obtenerIdentificadores().values(): 
            if variable.getInicializado() is False: # Si no esta incializado
                print("Advertencia: La variable '" + variable.obtenerNombre() + "' no fue inicialzada")
            if variable.getUsado() is False: # Si no esta usado:
                print("Advertencia: La variable '" + variable.obtenerNombre() + "' no fue usada")

        # print(self.tabla_simbolos.mostrarContextoActual())  # Muestra el contenido del contexto actual
        self.tabla_simbolos.borrarContexto()                  # Borra el contexto actual
    
    def exitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        """
        Maneja la salida de un contexto de declaración de variables.

        Verifica si la variable ya está declarada en el ámbito local. Si no lo está,
        crea la variable y la agrega a la tabla de símbolos. También maneja la 
        declaración de múltiples variables en una sola instrucción.
        """
        
        # Verifica si la variable ya está declarada en el ámbito local
        if self.tabla_simbolos.buscarLocal(ctx.getChild(1).getText()) is None:
            tipo_dato = str(ctx.getChild(0).getText().upper())          # Obtiene el tipo de dato y lo convierte a mayúsculas
            nombre = str(ctx.getChild(1).getText())                     # Obtiene el nombre de la variable
            variable = Variable(nombre, tipo_dato)                      # Crea un objeto Variable con el nombre y tipo de dato
            self.tabla_simbolos.agregarIdentificador(variable)          # Agrega la variable a la tabla de símbolos en el contexto actual
            
            # Para validar si realmente se estan agregando los ID's a la tabla de contextos en su contexto correspondiente
            print("Nueva variable:", "'" + self.tabla_simbolos.buscarLocal(nombre).obtenerNombre() + "'", "agregada.\n")

            # Maneja la declaración de múltiples variables (si es necesario)
            if self.pila_variables:    
                while self.pila_variables:
                    nueva_variable = self.pila_variables.pop()
                    if self.tabla_simbolos.buscarLocal(nueva_variable) is None:
                        variable = Variable(nueva_variable, tipo_dato)              # Crea una nueva variable para cada nombre en la pila
                        self.tabla_simbolos.agregarIdentificador(variable)          # Agrega cada variable a la tabla de símbolos
                
                        # Para validar si realmente se estan agregando los ID's a la tabla de contextos en su contexto correspondiente
                        print("Nueva variable:", "'" + self.tabla_simbolos.buscarLocal(variable.obtenerNombre()).obtenerNombre() + "'", "agregada.\n")
                    else:
                        # Imprime un mensaje de error si la variable ya fue declarada
                        print("Error: La variable '" + ctx.getChild(1).getText() + "' ya fue declarada en este bloque")
                        return
        else:
            # Imprime un mensaje de error si la variable ya fue declarada
            print("Error: La variable '" + ctx.getChild(1).getText() + "' ya fue declarada en este bloque")
            return

        self.pila_variables.clear() # Para vaciar la pila de nombres de variables después de procesar la declaración.

    def exitLista_variables(self, ctx: compiladoresParser.Lista_variablesContext):
        """
        Maneja la salida de un contexto de lista de variables.
        """

        if ctx.getChildCount():
                self.pila_variables.append(ctx.getChild(1).getText())

    def exitAsignacion(self, ctx:compiladoresParser.AsignacionContext):
        """
        Maneja la salida de un contexto de asignación.
        """

        if self.tabla_simbolos.buscarGlobal(ctx.getChild(0).getText()) is None:
            # Notifica el uso de un ID sin declarar
            print("Error: El identificador '" + ctx.getChild(0).getText() + "' no esta definido")
            return
        
    """ ------------------------------------------------------------------------------------ """

    def exitFactor(self, ctx:compiladoresParser.FactorContext):
        """
        Maneja la salida de un contexto de factor.
        """
        
        if ctx.ID():   # Si el factor es un ID
            identificador = self.tabla_simbolos.buscarGlobal(ctx.getChild(0).getText())   # Busca el ID en la tabla de símbolos
            if  identificador is None: 
                # Notifica el uso de un ID sin declarar
                print("Error: El identificador '" + ctx.getChild(0).getText() + "' no esta definido")
                return
            else:   # Si el ID fue declarado actualiza su estado a usado en caso que no lo este
                self.tabla_simbolos.actualizarUsado(identificador.obtenerNombre())
