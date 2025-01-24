from .compiladoresListener import compiladoresListener
from .compiladoresParser import compiladoresParser
from .Componentes.TablaSimbolos import TablaSimbolos
from .Componentes.Variable import Variable
from .Componentes.Funcion import Funcion
from .Componentes.ID import TipoDato

class MyListener (compiladoresListener):
    """
    Clase que implementa el listener para el analizador sintáctico. 
    """

    tabla_simbolos = TablaSimbolos()   # Instancia de la tabla de símbolos
    dict_variables = {}                # Diccionario para almacenar variables temporales
    errores = []                       # Lista para almacenar errores encontrados
    advertencias = []                  # Lista para almacenar advertencias encontradas
    funcion_actual: Funcion = None     # Para rastrear la funcion actual
    pila_argumentos = []               # Lista para almacenar los argumentos que espera una funcion
    argumentos_a_funcion = []          # Esta lista tendra que guardar los argumentos que se pasan a la funcion en la invocaion

    def reporteErrores(self, ctx, tipo_error:str, mensaje:str):
        """
        Genera un reporte de errores para el compilador

        Este método se encarga de registrar los errores encontrados durante
        el proceso de compilación. Se extrae la línea del contexto donde
        ocurrió el error y se agrega un mensaje de error a la lista de errores.

        Parámetros:
            - ctx: El contexto del error, que contiene información sobre la ubicación del error.
            - tipo_error: Una cadena que indica el tipo de error ("Sintáctico", "Semántico").
            - mensaje: Un mensaje descriptivo que explica el error.
        """
        
        linea = ctx.start.line # Obtiene el número de línea donde ocurrió el error desde el contexto
        self.errores.append(f"Error {tipo_error} en la linea {linea}: {mensaje}") # Agrega un mensaje de error a la lista de errores, incluyendo el tipo y la línea

    def reporteAdvertencias(self, ctx, mensaje:str):
        """
        Genera un reporte de advertencias para el compilador
        """

        linea = ctx.start.line # Obtiene el número de línea donde se controno la advertencia desde el contexto
        self.advertencias.append(f"Advertencia en la linea {linea}: {mensaje}") # Agrega un mensaje de advertencia a la lista de advertencias, incluyendo la línea

    def obtenerNombreContexto(self, ctx):
        """
        Obtiene el nombre del contexto actual.
        Este método determina el nombre del contexto basado en el tipo de estructura
        """
        
        padre = ctx.parentCtx
        # Verifica si padre es una instancia de la clase especifica proporcionada
        if isinstance(padre, compiladoresParser.FuncionContext): # Si el padre es una función
            return f"{padre.getChild(1).getText()}"
        elif isinstance(padre, compiladoresParser.InstruccionContext): # Si el padre es una instrucción
            if isinstance(padre.parentCtx, compiladoresParser.IwhileContext): # Si el padre es 'while'
                return "While"
            elif isinstance(padre.parentCtx, compiladoresParser.IforContext): # Si el padre es 'for'
                return "For"
            elif isinstance(padre.parentCtx, compiladoresParser.IifContext): # Si el padre es 'if'
                return "If"
            elif isinstance(padre.parentCtx, compiladoresParser.IelseContext): # Si el padre es 'else'
                return "Else"
        else: 
            return None

    def buscarAdvertenciasContexto(self, ctx):
        """
        Busca advertencias en el contexto actual.
        Este método busca advertencias en el contexto actual y las agrega a la lista de advertencias
        """

        # Obtenemos todos los contextos de la tabla de simbnolos
        contextos = self.tabla_simbolos.obtenerContextos()
        
        # Recorremos el contexto actual en busca de ID no inicializados y/o usados
        for variable in contextos[-1].obtenerIdentificadores().values(): 
            if variable.getInicializado() is False: # Si no esta incializado
                self.advertencias.append(f"Advertencia: Identificador '{variable.obtenerNombre()}' no inicialzado en bloque {contextos[-1].nombre}")
                # self.reporteAdvertencias(ctx, f"Identificador '{variable.obtenerNombre()}' no inicialzada")
            if variable.getUsado() is False: # Si no esta usado:
                self.advertencias.append(f"Advertencia: Identificador '{variable.obtenerNombre()}' no usado en bloque {contextos[-1].nombre}")
                # self.reporteAdvertencias(ctx, f"Identificador '{variable.obtenerNombre()}' no usada")
    def asignarTiposDeDatos (self, tipo_dato):
        """
        Funcion para asignar tipos de datos a las variables declaradas. 
        """

        if tipo_dato == "char":
            tipo_dato = TipoDato.char
        elif tipo_dato == "int":
            tipo_dato = TipoDato.int
        elif tipo_dato == "float":
            tipo_dato = TipoDato.float
        elif tipo_dato == "double":
            tipo_dato = TipoDato.double
    
        return tipo_dato

    def compararTiposDeDatos (self, ctx, tipo1 : TipoDato, tipo2 : TipoDato):
        """
        Funcion para comparar tipos de datos de dos variables. Y mostrar posibles perdidas de informacion si se asigna una variable
        de mayor orden de jerarquia a una de menor orden.
        """
        
        if tipo1 < tipo2:
            self.reporteAdvertencias(ctx, f"Sintactico: conversión de '{tipo2.getTipoDato()}' a '{tipo1.getTipoDato()}', posible pérdida de datos.")

        return

    def enterPrograma(self, ctx:compiladoresParser.ProgramaContext):
        """
        Método que se ejecuta al entrar en el contexto de la regla "programa".
        Inicializa el contexto global y comienza el proceso de compilación.
        """

        print("\n+" + "="*10, "Comienza la Compilacion", "="*10 + "+\n")
        self.tabla_simbolos.agregarContexto("Global"); # Agrega el contexto global (primer contexto) a la tabla de simbolos
        print(f"=== Entrando al Contexto Global ===")

    def exitPrograma(self, ctx:compiladoresParser.ProgramaContext):
        """
        Método que se ejecuta al salir del contexto de la regla "programa".
        Finaliza el proceso de compilación y muestra los reportes de errores y advertencias.
        """

        nombre_contexto = self.tabla_simbolos.obtenerContextos()
        
        try: 
            print(f"\n=== Saliendo Contexto: {nombre_contexto[-1].nombre} ===") # Notifica que salimos de dicho contexto
        except IndexError:
            print(f"\n=== Saliendo Contexto: Global ===") # Si no hay contexto

        print("\n+" + "="*10, "Fin de la Compilacion", "="*10 + "+\n")
        self.tabla_simbolos.borrarContexto() # Borra el contexto global (Ultimo contexto restante)

        # Muestra el reporte de Errores
        if self.errores:
            print("\nSe encontraron los siguientes errores:")
            for error in self.errores:
                print(error)
        else:
            print("Compilación exitosa. No se encontraron errores.")

        # Muestra el reporte de Advertencias
        if self.advertencias:
            print("\nAdvertencias a tener en cuenta:")
            for advertencia in self.advertencias:
                print(advertencia)
        else:
            print("No aparecieron advertencias.")


    def exitInstruccion(self, ctx:compiladoresParser.InstruccionContext):
        """
        Método que se ejecuta al salir del contexto de la regla "instruccion".
        Verifica si la instrucción termina con un punto y coma.
        """

        # Verifica si el contexto corresponde a uno de estos tipos de instrucción válidos
        if (ctx.declaracion() or ctx.asignacion() or ctx.retornar() or ctx.prototipo_funcion() or ctx.llamada_funcion()):
            if ctx.getChild(1).getText() != ';': # Si no termina con ';' muestra un error
                self.reporteErrores(ctx, "Sintactico", "se esperaba ';'")

    def enterBloque(self, ctx:compiladoresParser.BloqueContext):
        """
        Método que se ejecuta al entrar en el contexto de la regla "bloque".
        Crea un nuevo contexto para las variables locales.
        """

        nombre_contexto = self.obtenerNombreContexto(ctx)
        if nombre_contexto:
            self.tabla_simbolos.agregarContexto(nombre_contexto) # Agrega un nuevo Contexto a la tabla de simbolos
            print(f"\n=== Entrando al Contexto: {nombre_contexto} ===")
        
        # Verifica si padre es una funcion
        if nombre_contexto not in {"While", "For", "If", "Else", None}:
            for arg in self.pila_argumentos:
                self.tabla_simbolos.agregarIdentificador(arg)
                print(f"Se agrego el ID '{arg.obtenerNombre()}' a la funcion '{nombre_contexto}'")
        
    def exitBloque(self, ctx:compiladoresParser.BloqueContext):
        """
        Método que se ejecuta al salir del contexto de la regla "bloque".
        Verifica las variables no inicializadas y no usadas en el bloque.
        """

        # Reporte de errores
        if ctx.getChild(2).getText() != '}':
            linea = ctx.LLC().getSymbol().line
            self.errores.append(f"Error Sintactico en la linea {linea}: se esperaba una instrucción")
            return

        nombre_contexto = self.obtenerNombreContexto(ctx)

        self.buscarAdvertenciasContexto(ctx) 

        print(f"\n=== Saliendo del Contexto: {nombre_contexto} ===")
        
        self.tabla_simbolos.borrarContexto() # Borra el contexto actual
    
    def exitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        """
        Maneja la salida de un contexto de declaración de variables.

        Verifica si la variable ya está declarada en el ámbito local. Si no lo está,
        crea la variable y la agrega a la tabla de símbolos. También maneja la 
        declaración de múltiples variables en una sola instrucción.
        """

        # Verifica si la variable ya está declarada en el ámbito local
        if self.tabla_simbolos.buscarLocal(ctx.getChild(1).getText()) is None:
            tipo_dato = ctx.getChild(0).getText()                       # Obtiene el tipo de dato de la variable como un string

            # Asigna el tipo de dato a la variable
            tipo_dato = self.asignarTiposDeDatos(tipo_dato)

            nombre = str(ctx.getChild(1).getText())                     # Obtiene el nombre de la variable
            variable = Variable(nombre, tipo_dato)                      # Crea un objeto Variable con el nombre y tipo de dato

            self.tabla_simbolos.agregarIdentificador(variable)          # Agrega la variable a la tabla de símbolos en el contexto actual

            # tipo_dato = variable.obtenerTipoDato()
            
            print(f"Nueva variable: '{nombre}' de tipo '{tipo_dato}' agregada.\n") # Revisar para que no agregue el simbolo o solo reporte un error

            if str(ctx.getChild(2).getText()) != '': # Si el 3er hijo en la declaracion es distinto de vacio, existe una definicion
                if self.tipo_dato_obtenido: # Evaluar si los tipos de datos son compatibles en la asignacion
                    
                    

                    self.compararTiposDeDatos(ctx, tipo_dato, self.tipo_dato_obtenido)

                    # if tipo_dato != self.tipo_dato_obtenido:
                    #     self.reporteAdvertencias(ctx, "Sintactico: tipo de dato no compatible")
                    #     return
                    variable.setInicializado() # Marca la variable como inicializada si se proporciona un valor
                    self.tipo_dato_obtenido = None
                else:
                    # Si no fuece un ID 
                    variable.setInicializado() # Marca la variable como inicializada si se proporciona un valor

            # Maneja la declaración de múltiples variables (si es necesario)
            if self.dict_variables:    
                while self.dict_variables:
                    nueva_variable, isInicializado = self.dict_variables.popitem()
                    
                    # Verifica si la variable ya ha sido declarada en el ámbito local
                    if self.tabla_simbolos.buscarLocal(nueva_variable) is None:
                        variable = Variable(nueva_variable, tipo_dato)              # Crea una nueva variable para cada nombre en la pila
                        self.tabla_simbolos.agregarIdentificador(variable)          # Agrega cada variable a la tabla de símbolos
                
                        # Para validar si realmente se estan agregando los ID's a la tabla de contextos en su contexto correspondiente
                        print(f"Nueva variable: '{self.tabla_simbolos.buscarLocal(variable.obtenerNombre()).obtenerNombre()}'" + 
                              f" de tipo '{tipo_dato}' agregada.\n")

                        if isInicializado: # Marca la variable como inicializada si es True
                            variable.setInicializado()
                    else:
                        # Error si la variable ya fue declarada
                        self.reporteErrores(ctx, "Semantico", f"El identificador '{ctx.getChild(1).getText()}' ya esta definido en este bloque")
        else:
            # Imprime un mensaje de error si la variable ya fue declarada
            self.reporteErrores(ctx, "Semantico", f"El identificador '{ctx.getChild(1).getText()}' ya esta definido en este bloque")

        self.dict_variables.clear() # Para vaciar la pila de nombres de variables después de procesar la declaración.

    def exitLista_variables(self, ctx: compiladoresParser.Lista_variablesContext):
        """
        Maneja la salida de un contexto de lista de variables.
        """

        if ctx.getChildCount():
            # self.pila_variables.append(ctx.getChild(1).getText())
            if str(ctx.getChild(2).getText()) != '': # Si el tercer hijo en la lista de variables es distinto de vacio, existe definicion
                self.dict_variables.update({ctx.getChild(1).getText(): True})
                # El dict almacena el nombre de la var como nombre y si esta inicializada con valor (True o False)
            else:
                self.dict_variables.update({ctx.getChild(1).getText(): False})



    def exitAsignacion(self, ctx:compiladoresParser.AsignacionContext):
        """
        Maneja la salida de un contexto de asignación.
        """

        nombre_variable = ctx.getChild(0).getText()
        identificador = self.tabla_simbolos.buscarGlobal(nombre_variable)

        if identificador is None: # Si el identificador no existe en la tabla de simbolos
            # Notifica el uso de un ID sin declarar
            self.reporteErrores(ctx, "Semantico", f"El identificador '{ctx.getChild(0).getText()}' no esta definido")
            return
        else: # Evaluar si los tipos de datos son compatibles en la asignacion
            tipo_dato = identificador.obtenerTipoDato()
            if self.tipo_dato_obtenido:

                self.compararTiposDeDatos(ctx, tipo_dato, self.tipo_dato_obtenido)

                # if tipo_dato != self.tipo_dato_obtenido:
                #     self.reporteAdvertencias(ctx, "Sintactico: tipo de dato no compatible")
                #     return
                identificador.setInicializado() # Marca la variable como inicializada si se proporciona un valor
                self.tipo_dato_obtenido = None

        # Verifica si el valor asignado es correcto
        if ctx.getChild(2) == ctx.opal():
            identificador.setInicializado() # Se inicializa la variable
    
    """ ----------------------------------------------------------- """

    tipo_dato_obtenido = None 

    def exitFactor(self, ctx:compiladoresParser.FactorContext):
        """
        Maneja la salida de un contexto de factor.
        """
        
        if ctx.ID():   # Si el factor es un ID
            identificador = self.tabla_simbolos.buscarGlobal(ctx.getChild(0).getText())   # Busca el ID en la tabla de símbolos
            if  identificador is None: 
                # Notifica el uso de un ID sin declarar
                self.reporteErrores(ctx, "Semantico", f"El identificador '{ctx.getChild(0).getText()}' no esta definido")
                return
            else:   # Si el ID fue declarado actualiza su estado a usado en caso que no lo este
                self.tipo_dato_obtenido = identificador.obtenerTipoDato()
                self.tabla_simbolos.actualizarUsado(identificador.obtenerNombre())
        else: 
            self.tipo_dato_obtenido = None

        # Manejo de parentesis en operaciones logicas:
        if ctx.PA():
            if ctx.getChild(2).getText() != ')':
                self.reporteErrores(ctx, "Semantico", "Falta de cierre de parentesis")
                return

        if ctx.PC():
            if ctx.getChild(0).getText() != '(':
                self.reporteErrores(ctx, "Semantico", "Falta de abertura de parentesis")
                return

    def exitIwhile(self, ctx:compiladoresParser.IwhileContext):
        """
        Maneja la salida de un contexto de while.
        """

        if ctx.getChild(1).getText() != '(':
            self.reporteErrores(ctx, "Sintactico", "Falta parentesis de apertura")
            return

        if ctx.getChild(3).getText() != ')':
            self.reporteErrores(ctx, "Sintactico", "Falta parentesis de cierre")
            return        
        
        # Verifica si es una estructura de una sola linea donde se hace una declaracion:
        if isinstance(ctx.getChild(4).getChild(0), compiladoresParser.DeclaracionContext):
            self.reporteErrores(ctx, "Sintactico", "Una instrucción dependiente no puede ser una declaración")
            return

    def exitIfor(self, ctx:compiladoresParser.IforContext):
        """
        Maneja la salida de un contexto de for.
        """

        if ctx.getChild(1).getText() != '(':
            self.reporteErrores(ctx, "Sintactico", "Falta parentesis de apertura")
            return

        if ctx.getChild(7).getText() != ')':
            self.reporteErrores(ctx, "Sintactico", "Falta parentesis de cierre")
            return
        
        # Verifica si es una estructura de una sola linea donde se hace una declaracion:
        if isinstance(ctx.getChild(8).getChild(0), compiladoresParser.DeclaracionContext):
            self.reporteErrores(ctx, "Sintactico", "Una instrucción dependiente no puede ser una declaración")
            return

    def exitIif(self, ctx:compiladoresParser.IifContext):
        """
        Maneja la salida de un contexto de if.
        """

        if ctx.getChild(1).getText() != '(':
            self.reporteErrores(ctx, "Sintactico", "Falta parentesis de apertura")
            return

        if ctx.getChild(3).getText() != ')':
            self.reporteErrores(ctx, "Sintactico", "Falta parentesis de cierre")
            return

        # Verifica si es una estructura de una sola linea donde se hace una declaracion:
        if isinstance(ctx.getChild(4).getChild(0), compiladoresParser.DeclaracionContext):
            self.reporteErrores(ctx, "Sintactico", "Una instrucción dependiente no puede ser una declaración")
            return

    def exitIelse(self, ctx:compiladoresParser.IelseContext):
        """
        Maneja la salida de un contexto de else.
        """

        # Verifica si es una estructura de una sola linea donde se hace una declaracion:
        if isinstance(ctx.getChild(2).getChild(0), compiladoresParser.DeclaracionContext):
            self.reporteErrores(ctx, "Sintactico", "Una instrucción dependiente no puede ser una declaración")
            return
        
    # def exitRetornar(self, ctx:compiladoresParser.RetornarContext):
        

    #     return

    def exitPrototipo_funcion(self, ctx:compiladoresParser.Prototipo_funcionContext):
        """
        Maneja la salida de un contexto de prototipo de función.
        Es decir, mameja la declaracion de funciones.
        """

        tipo_retorno = ctx.getChild(0).getText().upper()
        nombre = ctx.getChild(1).getText()

        # Verificar si la función ya existe
        if self.tabla_simbolos.buscarGlobal(nombre):
            self.reporteErrores(ctx, "Semantico", f"Función '{nombre}' ya fue declarada")
            # Vacia la pila de argumentos
            if self.pila_argumentos:
                self.pila_argumentos.clear()
            return
        
        # Crear nueva función
        funcion = Funcion(nombre, tipo_retorno)
        self.funcion_actual = funcion # Guardamos la funcion actual.

        # Procesamos los argumentos de la funcion, si existen
        if ctx.getChild(3).getChildCount() != 0:
        # if str(ctx.getChild(3).getText()) != '': # Si la funcion tiene argumentos
            for arg in self.pila_argumentos:
                self.funcion_actual.aregarArgumento(arg)

    
        # Si la funcion no existe Agregar función a la tabla de símbolos
        self.tabla_simbolos.agregarIdentificador(funcion)
        print(f"Nueva funcion: '{self.tabla_simbolos.buscarLocal(nombre).obtenerNombre()}' agregada.\n")

        # Vacia la pila de argumentos
        if self.pila_argumentos:
            self.pila_argumentos.clear()
    
    def exitFuncion(self, ctx:compiladoresParser.FuncionContext):
        """
        Maneja la salida de un contexto de función.
        """

        nombre = ctx.getChild(1).getText()
        funcion = self.tabla_simbolos.buscarGlobal(nombre)

        # Verificar si la función no existe
        if funcion is None: # Si la funcion no existe ==> no tiene prototipo
            # Crear nueva función
            tipo_retorno = ctx.getChild(0).getText().upper()
            funcion = Funcion(nombre, tipo_retorno)
            self.funcion_actual = funcion # Guardamos la funcion actual.
            
            # Procesamos los argumentos de la funcion, si existen
            if str(ctx.getChild(3).getText()) != '': # Si la funcion tiene argumentos
                for arg in self.pila_argumentos:
                    self.funcion_actual.aregarArgumento(arg)
    
            # Si la funcion no existe Agregar función a la tabla de símbolos
            self.tabla_simbolos.agregarIdentificador(funcion)
            funcion.setInicializado() # Se inicializa porque su definicion esta escrita correctamente
            print(f"Nueva funcion: '{funcion.obtenerNombre()}' agregada.\n")
            
            if nombre == 'main':
                funcion.setUsado() # En mi caso marco la funcion principal main como usada
            
            # Vacia la pila de argumentos
            if self.pila_argumentos:
                self.pila_argumentos.clear()
        else:
            # Si la función ya existe, verificar si los argumentos coinciden
            if funcion.obtenerTipoDato() != ctx.getChild(0).getText().upper():
                self.reporteErrores(ctx, "Semantico", f"Tipo de retorno de la funcion no coincide con la declaracion")
                # Vacia la pila de argumentos
                if self.pila_argumentos:
                    self.pila_argumentos.clear()
                return
            
            try:
                # Verificar si los argumentos coinciden
                for ii, arg in enumerate(self.pila_argumentos):
                    # if funcion.args[ii].obtenerNombre() != arg.obtenerNombre() or funcion.args[ii].obtenerTipoDato() != arg.obtenerTipoDato():
                    # Solo se compara la cantidad de argumentos y los tipos de datos entre si, no se compara si el nombre coincide, ya que para
                    # la funcion solo es relevante que coincida la cantidad de argumentos y el tipo de cada uno con su prototipo
                    if funcion.args[ii].obtenerTipoDato() != arg.obtenerTipoDato():
                        self.reporteErrores(ctx, "Semantico", f"Argumento no coincide con su prototipo")
                        # Vacia la pila de argumentos
                        if self.pila_argumentos:
                            self.pila_argumentos.clear()
                        return
            except IndexError: # Si la cantidad de argumentos no coincide
                self.reporteErrores(ctx, "Semantico", f"Número incorrecto de argumentos para función '{funcion.obtenerNombre()}'. "
                f"Esperados: {len(funcion.args)}, Recibidos: {len(self.pila_argumentos)}")
            
            # Si todo salio bien, y el prototipo tiene su definicion de funcion estonces la inicializo
            funcion.setInicializado() # Se inicializa porque su definicion esta escrita correctamente

            # Vacia la pila de argumentos
            if self.pila_argumentos:
                self.pila_argumentos.clear()
    
    def exitArgumentos(self, ctx:compiladoresParser.ArgumentosContext):
        """
        Maneja la salida de un contexto de argumentos.
        """
        
        if ctx.getChildCount(): 
            nombre = ctx.getChild(1).getText()
            tipo_dato = ctx.getChild(0).getText()
            nueva_var = Variable(nombre, tipo_dato)
            nueva_var.setInicializado()  # Los parámetros se consideran inicializados
            nueva_var.setUsado()
            self.pila_argumentos.append(nueva_var) 
    
    def exitLista_argumentos(self, ctx:compiladoresParser.Lista_argumentosContext):
        """
        Se ejecuta al final de la lista de argumentos de una función.
        """

        if ctx.getChildCount():
            nombre = ctx.getChild(2).getText()
            tipo_dato = ctx.getChild(1).getText()
            nueva_var = Variable(nombre, tipo_dato)
            nueva_var.setInicializado()  # Los parámetros se consideran inicializados
            nueva_var.setUsado()
            self.pila_argumentos.append(nueva_var)

    def exitLlamada_funcion_valor(self, ctx:compiladoresParser.Llamada_funcion_valorContext):
        """
        Maneja las llamadas a funcion que retornan un valor.
        """

        # Obtengo el nombre de la variable donde se asigna el valor retorno de la funcion
        nombre_id = ctx.getChild(0).getText()

        # Primero busca si la variable a sido declarada localmente
        id = self.tabla_simbolos.buscarLocal(nombre_id)

        if id is None:
            # Si no esta declarada localmente, busca en la tabla de simbolos global
            id = self.tabla_simbolos.buscarGlobal(nombre_id)
            if id is None:
                # Si no esta declarada en ninguna de las tablas, se considera una variable no declarada
                self.reporteErrores(ctx, "Semantico", f"Varaible '{nombre_id}' no ha sido declarada")
                return
        
        # Si la variable si esta en la tabla de simbolos, se actualiza su estado a Usado (porque se le asigna el valor retorno de la funcion)
        id.setUsado()


    def exitLlamada_funcion(self, ctx:compiladoresParser.Llamada_funcionContext):
        """
        Maneja las llamadas a funciones.
        """

        if ctx.getChild(1).getText() != '(':
            self.reporteErrores(ctx, "Sintactico", "Falta parentesis de apertura")
            self.argumentos_a_funcion.clear()
            return

        if ctx.getChild(3).getText() != ')':
            self.reporteErrores(ctx, "Sintactico", "Falta parentesis de cierre")
            self.argumentos_a_funcion.clear()
            return
        
        nombre_funcion = ctx.getChild(0).getText()
        funcion = self.tabla_simbolos.buscarGlobal(nombre_funcion)

        if funcion: # Si la funcion existe en la tabla de simbolos comprueba que se reciban la misma cantidad de parametros esperados
            if len(funcion.args) != len(self.argumentos_a_funcion):
                self.reporteErrores(ctx, "Semantico", f"Número incorrecto de argumentos para función '{funcion.obtenerNombre()}'. "
                f"Esperados: {len(funcion.args)}, Recibidos: {len(self.pila_argumentos)}")
                self.argumentos_a_funcion.clear()
                return
            funcion.setUsado() # Si la funcion existe, se marca como usada por la invocacion
            print(f"Se invoco la Funcion: {funcion.obtenerNombre()} correctamente")
        else:  # Si la funcion no existe reporta el error
            self.reporteErrores(ctx, "Semantico", f"Funcion '{nombre_funcion}' no fue declarada")
            self.argumentos_a_funcion.clear()
            return        

    def exitArgumentos_a_funcion(self, ctx:compiladoresParser.Argumentos_a_funcionContext):
        """
        Se ejecuta al final de la lista de argumentos de una llamada a función.
        """

        if ctx.getChildCount():
            self.argumentos_a_funcion.append(ctx.getChild(0).getText())

    def exitLista_argumentos_a_funcion(self, ctx:compiladoresParser.Lista_argumentos_a_funcionContext):
        """
        Se ejecuta al final de la lista de argumentos de una llamada a función.
        """
    
        if ctx.getChildCount():
            self.argumentos_a_funcion.append(ctx.getChild(1).getText())


