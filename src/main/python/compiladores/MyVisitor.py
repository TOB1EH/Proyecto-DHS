from .compiladoresVisitor import compiladoresVisitor
from .compiladoresParser import compiladoresParser

class Temporal():
    def __init__(self):
        self.contador = -1
    
    def getTemporal(self):
        self.contador += 1
        return f't{self.contador}'
    
class Etiqueta():
    def __init__(self):
        self.contador = -1

    def getEtiqueta(self):
        self.contador += 1
        return f'l{self.contador}'

class MyVisitor (compiladoresVisitor):
    def __init__(self): 
        
        self.file                    = None
        self.ruta                    = './output/codigoIntermedio.txt' 
        self.temporales              = []
        self.etiquetas               = []
        self.generadorDeTemporales   = Temporal()
        self.generadorDeEtiquetas    = Etiqueta()

        self.operando1               = None
        self.operando2               = None
        self.operador                = None
        self.isComparador            = False
        self.isSumador               = False
        self.isParentesisOperando2   = False


    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("-" + "=" * 30 + "-")
        print("-- Comienza a generar Codigo Intermedio --")
        self.file = open(self.ruta, "w")

        self.visitInstrucciones(ctx.getChild(0))

        self.file.close()
        print("-- Codigo Intermedio generado Correctamente --")
        print("-" + "=" * 30 + "-")

    # # Visit a parse tree produced by compiladoresParser#instrucciones.
    # def visitInstrucciones(self, ctx:compiladoresParser.InstruccionesContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#instruccion.
    # def visitInstruccion(self, ctx:compiladoresParser.InstruccionContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#bloque.
    # def visitBloque(self, ctx:compiladoresParser.BloqueContext):
    #     return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#declaracion.
    def visitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        
        # Guardo el valor del identificador de la declaracion
        id = ctx.getChild(1).getText()

        # Si existe el hijo 3 (Definicion), entonces hay una asignacion a la variable
        if ctx.getChild(2).getChildCount() != 0:
            self.visitDefinicion(ctx.getChild(2))

            # Si hay un temporal, es el ultimo paso de la asignacion, es decir, hubo operaciones dentro de la asignacion
            if self.temporales:
                self.file.write(f"{id} = {self.temporales.pop()}\n\n")
                # self.temporales.clear()
            
            # De la contrario la variable solo almacena un factor
            else:
                self.file.write(f"{id} = {self.operando1}\n\n")
            
            # Reseteo los los elementos para las operaciones
            self.operando1 = None
            self.operando2 = None
            self.operador  = None
        
        # De lo contrario solo se declaro la varible vacia
        else:
            self.file.write(f'Declaracion de la variable {id}\n')


    # Visit a parse tree produced by compiladoresParser#definicion.
    def visitDefinicion(self, ctx:compiladoresParser.DefinicionContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
        self.visitOpal(ctx.getChild(1))


    # # Visit a parse tree produced by compiladoresParser#lista_variables.
    # def visitLista_variables(self, ctx:compiladoresParser.Lista_variablesContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#tipo_dato.
    # def visitTipo_dato(self, ctx:compiladoresParser.Tipo_datoContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#asignacion.
    def visitAsignacion(self, ctx:compiladoresParser.AsignacionContext):
        # Guardo el valor del identificador de la declaracion
        id = ctx.getChild(0).getText()

        self.visitOpal(ctx.getChild(2))

        # Si hay un temporal, es el ultimo paso de la asignacion, es decir, hubo operaciones dentro de la asignacion
        if self.temporales:
            self.file.write(f"{id} = {self.temporales.pop()}\n\n")
            # self.temporales.clear()
        
        # De la contrario la variable solo almacena un factor
        else:
            self.file.write(f"{id} = {self.operando1}\n\n")
        
        # Reseteo los los elementos para las operaciones
        self.operando1 = None
        self.operando2 = None
        self.operador  = None
        
    # Visit a parse tree produced by compiladoresParser#opal.
    def visitOpal(self, ctx:compiladoresParser.OpalContext):
        self.visitOplogicos(ctx.getChild(0))
        

    # Visit a parse tree produced by compiladoresParser#oplogicos.
    def visitOplogicos(self, ctx:compiladoresParser.OplogicosContext):
        self.visitLogico(ctx.getChild(0))

    # # Visit a parse tree produced by compiladoresParser#lor.
    # def visitLor(self, ctx:compiladoresParser.LorContext):
    #     return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#logico.
    def visitLogico(self, ctx:compiladoresParser.LogicoContext):
        self.visitConjunto(ctx.getChild(0))

        # if self.isComparador:
        #     self.visitConjunto(ctx.getChild(0))
        #     self.isComparador = False



    # # Visit a parse tree produced by compiladoresParser#land.elf.operando1
    # def visitLand(self, ctx:compiladoresParser.LandContext):
    #     return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#conjunto.
    def visitConjunto(self, ctx:compiladoresParser.ConjuntoContext):
        
        
        """ ------------------------------------------ Funcion --------------------------------------------------- """
        def visitarSubConjunto (ctx):
            # Visita C
            self.visitC(ctx.getChild(0))
    
            # Si la bandera esta activa, recorro el arbol para comparar los terminos de igualdad
            if self.isComparador:
                self.visitC(ctx.getChild(0)) # Los terminos del conjunto se ecuentran dentro de C
                # super().visitC(ctx)         
                self.isComparador = False    # Reseteo la bandera
        """ -------------------------------------- Fin de la Funcion --------------------------------------------- """
        



        # # Si el hijo 1 (Igualdad) no es vacio, entonces hay una comparacion de igualdad
        # if ctx.getChild(1).getChildCount() != 0:
        #     # Si la bandera es True, estoy en la segunda pasada encargada de hacer las comparaciones de igualdad a las operaciones
        #     if self.isComparador:

        #         # Si el hijo 0 (C) tiene un hijo 1 (Comparar) vacio, entonces no hay operacion de comparacion
        #         cond1 = ctx.getChild(0).getChild(1).getChildCount() == 0

        #         # Si el hijo 0 (C) tiene un hijo 0 (Exp) tiene un hijo 1 (E) vacio, entonces no hay operacion de suma/resta
        #         cond2 = ctx.getChild(0).getChild(0).getChild(1).getChildCount() == 0

        #         # Si el hijo 0 (C) tiene un hijo 0 (Exp) tiene un hijo 0 (Term) que tiene un hijo 1 (T) vacio, entonces es un termino simple
        #         cond3 = ctx.getChild(0).getChild(0).getChild(0).getChild(1).getChildCount() == 0


        #         # Entonces si se cumplen las condiciones, operando1 es un termino simple
        #         if cond1 and cond2 and cond3:
        #             self.isComparador = False
        #             visitarSubConjunto(ctx)
        #             self.isComparador = True

        #         # De lo contrario
        #         else:
        #             self.operando1 = self.temporales.pop(0)
                
        #         # # Si el hijo 1 (E) tiene un hijo 1 (Term) que tiene un hijo 0 (Factor) distinto de 3, entonces no hay operaciones entre parentesis
        #         # if ctx.getChild(1).getChild(1).getChild(0).getChildCount() != 3:
                
        #         """ Ver como evaluar para que solo se cree ciertas veces """
        #         # Genero un temporal
        #         self.temporales.append(self.generadorDeTemporales.getTemporal())

        #         # Visita el hijo 1 (Igualdad) para obtener la siguiente operacion
        #         self.visitIgualdad(ctx.getChild(1))

        #     # Si la bandera es False, estoy en la primera pasada en busca operaciones de comparacion (<=, >=, <, >)
        #     else:
        #         # Visito al subconjunto en busca de operaciones de comparacion
        #         visitarSubConjunto(ctx)

        #         # Visito Igualdad  en busca de comparaciones de igualdad
        #         self.visitIgualdad(ctx.getChild(1))

        #         # Al activar esta banera se realizara la segunda pasada para hacer comparaciones de igualdad
        #         self.isComparador = True

        # # De lo contrario no hay comparaciones de igualdad, asi que solo visita al subconjunto en busca de operaciones de comparacion
        # else:                
        #     visitarSubConjunto(ctx)

        """ ------------------------------------------------------------------------------------- """

        # Si el hijo 1 (Igualdad) no es vacio, entonces hay una comparacion de igualdad
        if ctx.getChild(1).getChildCount() != 0:

                # Si el hijo 0 (C) tiene un hijo 1 (Comparar) vacio, entonces no hay operacion de comparacion
                cond1 = ctx.getChild(0).getChild(1).getChildCount() == 0

                # Si el hijo 0 (C) tiene un hijo 0 (Exp) tiene un hijo 1 (E) vacio, entonces no hay operacion de suma/resta
                cond2 = ctx.getChild(0).getChild(0).getChild(1).getChildCount() == 0

                # Si el hijo 0 (C) tiene un hijo 0 (Exp) tiene un hijo 0 (Term) que tiene un hijo 1 (T) vacio, entonces es un termino simple
                cond3 = ctx.getChild(0).getChild(0).getChild(0).getChild(1).getChildCount() == 0


                # Entonces si se cumplen las condiciones, operando1 es un termino simple
                if cond1 and cond2 and cond3:
                    visitarSubConjunto(ctx)

                # De lo contrario
                else:
                    visitarSubConjunto(ctx)
                    self.operando1 = self.temporales.pop(0)
                
                
                """ Ver como evaluar para que solo se cree ciertas veces """
                # # Genero un temporal
                self.temporales.append(self.generadorDeTemporales.getTemporal())

                # Visito Igualdad  en busca de comparaciones de igualdad
                self.visitIgualdad(ctx.getChild(1))

        # De lo contrario no hay comparaciones de igualdad, asi que solo visita al subconjunto en busca de operaciones de comparacion
        else:                
            visitarSubConjunto(ctx)


        


    # Visit a parse tree produced by compiladoresParser#igualdad.
    def visitIgualdad(self, ctx:compiladoresParser.IgualdadContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
        """ ------------------------------------------ Funcion --------------------------------------------------- """
        def visitarSubConjunto (ctx):
            # Visita C
            self.visitC(ctx.getChild(1))
    
            # Si la bandera esta activa, recorro el arbol para comparar los terminos de igualdad
            if self.isComparador:
                self.visitC(ctx.getChild(1)) # Los terminos del conjunto se ecuentran dentro de C
                # super().visitC(ctx)         
                self.isComparador = False    # Reseteo la bandera
        """ -------------------------------------- Fin de la Funcion --------------------------------------------- """

        
        # if self.isComparador:
        #     # Guarda el valor actual del operando1
        #     operando1 = self.operando1

        #     # Si el hijo 1 (C) tiene un hijo 1 (Comparar) vacio, entonces no hay operacion de comparacion
        #     cond1 = ctx.getChild(1).getChild(1).getChildCount() == 0
            
        #     # Si el hijo 1 (C) tiene un hijo 0 (Exp) tiene un hijo 1 (E) vacio, entonces no hay operacion de suma/resta
        #     cond2 = ctx.getChild(1).getChild(0).getChild(1).getChildCount() == 0

        #     # Si el hijo 1 (C) tiene un hijo 0 (Exp) tiene un hijo 0 (Term) que tiene un hijo 1 (T) vacio, entonces es un termino simple
        #     cond3 = ctx.getChild(1).getChild(0).getChild(0).getChild(1).getChildCount() == 0


        #     if cond1 and cond2 and cond3:
        #         self.isComparador = False
        #         visitarSubConjunto(ctx)
        #         self.isComparador = True

        #         self.operando2 = self.operando1

        #     # De lo contrario
        #     else:
        #         self.operando2 = self.temporales.pop(0)

        #         if not self.temporales: self.temporales.append(self.generadorDeTemporales.getTemporal())

        #     self.operador = ctx.getChild(0).getText()
           
        #     # Reasigno el valor original del operando1
        #     self.operando1 = operando1

        #     # Escribe en el archivo de salida la suma/resta de los terminos igualados a un temporal generado
        #     self.file.write(f'{self.temporales[-1]} = {self.operando1} {self.operador} {self.operando2}\n')

            
        #     # Si el hijo 2 (igualdad) no es vacio, hay mas operaciones de comparacion de igualdad
        #     if ctx.getChild(2).getChildCount() != 0:
        #         # Genero un temporal para guardar el resultado de la sigueinte operacion
        #         temporal = self.generadorDeTemporales.getTemporal()
                
        #         # Operando1 para la siguiente operacion sera el temporal generado en la operacion actual
        #         self.operando1 = self.temporales.pop()

        #         # Agrego el temporal generado a la lista de temporales
        #         self.temporales.append(temporal)
                
        #         # Visita Igualdad para obtener el resultado de la siguiente operacion de suma/resta
        #         self.visitIgualdad(ctx.getChild(2))


        # # De lo contrario, estoy en la primera pasada en busca de comparaciones entre operaciones
        # else:
        #     # Si el hijo 2 (Igualdad) no es vacio, entonces hay mas comparaciones de igualdad
        #     if ctx.getChild(2).getChildCount() != 0:
                
        #         visitarSubConjunto(ctx)
                
        #         # Visita Igualdad en busca de la siguiente operacion de comparacion de igualdad
        #         self.visitIgualdad(ctx.getChild(2))


        #     # De lo contrario no hay mas comparaciones de igualdad
        #     else:
        #         visitarSubConjunto(ctx)
        

        """ ------------------------------------------------------------------------------------------------------------- """

        # if ctx.getChild(2).getChildCount() != 0:
        # Guarda el valor actual del operando1
        operando1 = self.operando1
        
        # Si el hijo 1 (C) tiene un hijo 1 (Comparar) vacio, entonces no hay operacion de comparacion
        cond1 = ctx.getChild(1).getChild(1).getChildCount() == 0
        
        # Si el hijo 1 (C) tiene un hijo 0 (Exp) tiene un hijo 1 (E) vacio, entonces no hay operacion de suma/resta
        cond2 = ctx.getChild(1).getChild(0).getChild(1).getChildCount() == 0
        
        # Si el hijo 1 (C) tiene un hijo 0 (Exp) tiene un hijo 0 (Term) que tiene un hijo 1 (T) vacio, entonces es un termino simple
        cond3 = ctx.getChild(1).getChild(0).getChild(0).getChild(1).getChildCount() == 0
        
        # Entonces si se cumplen estas condiciones
        if cond1 and cond2 and cond3:
            visitarSubConjunto(ctx)
            self.operando2 = self.operando1
        
        # De lo contrario
        else:
            visitarSubConjunto(ctx)
            
            self.operando2 = self.temporales.pop(0)
            # if not self.temporales: self.temporales.append(self.generadorDeTemporales.getTemporal())
        
        
        self.operador = ctx.getChild(0).getText()
        
        # Reasigno el valor original del operando1
        self.operando1 = operando1
        
        # Escribe en el archivo de salida la suma/resta de los terminos igualados a un temporal generado
        self.file.write(f'{self.temporales[-1]} = {self.operando1} {self.operador} {self.operando2}\n')
        
        # Si el hijo 2 (igualdad) no es vacio, hay mas operaciones de comparacion de igualdad
        if ctx.getChild(2).getChildCount() != 0:
        
            # Genero un temporal para guardar el resultado de la sigueinte operacion
            temporal = self.generadorDeTemporales.getTemporal()
            
            # Operando1 para la siguiente operacion sera el temporal generado en la operacion actual
            self.operando1 = self.temporales.pop()
            
            # Agrego el temporal generado a la lista de temporales
            self.temporales.append(temporal)
            
            # Visita Igualdad para obtener el resultado de la siguiente operacion de suma/resta
            self.visitIgualdad(ctx.getChild(2))

   
        # # De lo contrario no hay mas comparaciones de igualdad
        # else:
        #     visitarSubConjunto(ctx)


    # Visit a parse tree produced by compiladoresParser#c.
    def visitC(self, ctx:compiladoresParser.CContext):
        
        """ ------------------------------------------ Funcion --------------------------------------------------- """
        def visitarExpresion (ctx):
            """ 
                Visita la regla gramatical Exp, y evalua si la bandera para el segundo recorrido esta activa para 
                sumar/restar los terminos obtenidos en la primera pasada
            """

            # Visita Exp
            self.visitExp(ctx.getChild(0))

            # Si la bandera es True recorro el arbol para sumar los terminos
            if self.isSumador:
                self.visitExp(ctx.getChild(0)) # Los terminos se encuentran dentro de Exp (expresion)
                # super().visitExp(ctx) 
                self.isSumador = False # Reseteo la bandera
        """ -------------------------------------- Fin de la Funcion --------------------------------------------- """

        
        # Si el hijo 1 (Comparar) no es vacio, entonces hay una operacion de comparacion
        if ctx.getChild(1).getChildCount() != 0:
            # Si la bandera es True, estoy en la segunda pasada encargada de comparar las operaciones
            if self.isComparador:

                # Si el hijo 0 (Exp) tiene un hijo 1 (E) vacio, entonces no hay operacion de suma/resta
                cond1 = ctx.getChild(0).getChild(1).getChildCount() == 0

                # Si el hijo 0 (Exp) tiene un hijo 0 (Term) tiene un hijo 1 (T) vacio, entonces es un termino simople
                cond2 = ctx.getChild(0).getChild(0).getChild(1).getChildCount() == 0

                # # Si el hijo 0 (Exp) tiene un hijo 1 (E) vacio, entonces no hay operacion de suma/resta
                # if ctx.getChild(0).getChild(1).getChildCount() == 0:
                #     # Si el hijo 0 (Exp) tiene un hijo 0 (Term) tiene un hijo 1 (T) vacio, entonces es un termino simople
                #     if ctx.getChild(0).getChild(0).getChild(1).getChildCount() == 0:
                
                # Entonces si ambas se cumplen:
                if cond1 and cond2:
                    visitarExpresion(ctx)
               
                # De lo contrario
                else:
                    self.operando1 = self.temporales.pop(0)

                    # # Si la pila de temporales esta vacia, debo crear otro para asignar la operacion actual:
                    # if not self.temporales: self.temporales.append(self.generadorDeTemporales.getTemporal())
                
                """ Ver como evaluar para que solo se cree ciertas veces """
                # Genero un temporal para la comparacion
                self.temporales.append(self.generadorDeTemporales.getTemporal()) # Como evaluar si debo crear o no el temporal

                # Visito Comparar en busca de operaciones de comparacion
                self.visitComparar(ctx.getChild(1))

            # Si la bandera es False, estoy en la primera pasada en busca operaciones de suma/resta
            else:
                # # Si el hijo 0 (Exp) tiene un hijo 1 (E) no vacio, hay una operacion de suma/resta
                # if ctx.getChild(0).getChild(1).getChildCount() != 0:
                #     visitarExpresion(ctx)

                visitarExpresion(ctx)

                # Visito Comparar en busca de operaciones de comparacion
                self.visitComparar(ctx.getChild(1))

                # Como primero busco operaciones de suma/resta y existen mas comparaciones, debo evaluar dichas comparaciones entre si
                self.isComparador = True
                # Al activar esta bandera se realizara la segunda pasada para comparar las operaciones obtenidas

        # De lo contrario no hay mas comparaciones
        else:
            visitarExpresion(ctx)


    # Visit a parse tree produced by compiladoresParser#comparar.
    def visitComparar(self, ctx:compiladoresParser.CompararContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount == 0:
            return
        
        """ ------------------------------------------ Funcion --------------------------------------------------- """
        def visitarExpresion (ctx):
            """ 
                Visita la regla gramatical Exp, y evalua si la bandera para el segundo recorrido esta activa para 
                sumar/restar los terminos obtenidos en la primera pasada
            """

            # Visita Exp
            self.visitExp(ctx.getChild(1))

            # Si la bandera es True recorro el arbol para sumar los terminos
            if self.isSumador:
                self.visitExp(ctx.getChild(1)) # Los terminos se encuentran dentro de Exp (expresion)
                # super().visitExp(ctx) # Los terminos se encuentran dentro de Exp (expresion)
                self.isSumador = False # Reseteo la bandera
        """ -------------------------------------- Fin de la Funcion --------------------------------------------- """
        
        # Si la bandera es True, estoy en la segunda pasada encargada de comparar las operaciones
        if self.isComparador:
            # Guardo el valor del operando1
            operando1 = self.operando1

            # Si el hijo 0 (Exp) tiene un hijo 1 (E) vacio, entonces no hay operacion de suma/resta
            cond1 = ctx.getChild(1).getChild(1).getChildCount() == 0

            # Si el hijo 0 (Exp) tiene un hijo 0 (Term) tiene un hijo 1 (T) vacio, entonces es un termino simople
            cond2 = ctx.getChild(1).getChild(0).getChild(1).getChildCount() == 0


            # # Si el hijo 0 (Exp) tiene un hijo 1 (E) vacio, entonces no hay operacion de suma/resta
            # if ctx.getChild(1).getChild(1).getChildCount() == 0:
            #     # Si el hijo 0 (Exp) tiene un hijo 0 (Term) tiene un hijo 1 (T) vacio, entonces es un termino simople
            #     if ctx.getChild(1).getChild(0).getChild(1).getChildCount() == 0:
            
            # Entonces si ambas se cumplen:
            if cond1 and cond2:
                visitarExpresion(ctx)
                        
                # Como Exp es llamada dentro de Comparar, el operando1 obtenido es el operando2
                self.operando2 = self.operando1
            
            # De lo contrario, hay una operacion de suma/resta guardada en un
            else:
                self.operando2 = self.temporales.pop(0)

                # Si la pila de temporales esta vacia, debo crear otro para asignar la operacion actual:
                # if not self.temporales: self.temporales.append(self.generadorDeTemporales.getTemporal())

            
            # Restauro el valor original del operando1
            self.operando1 = operando1

            # Guardo el operador de comparacion
            self.operador = ctx.getChild(0).getText()

            # Escribo en el archivo la operacion de comparacion igualada a un temporal
            self.file.write(f'{self.temporales[-1]} = {self.operando1} {self.operador} {self.operando2}\n')

            # Si el hijo 2 (Comparar) no es vacio, hay una operacion de comparacion
            if ctx.getChild(2).getChildCount() != 0:
                # Genero un nuevo temporal
                temporal = self.generadorDeTemporales.getTemporal()

                # El ultimo temporal de la lista, sera el primer operando para la siguiente operacion
                self.operando1 = self.temporales.pop()

                # Agrego el nuevo temporal a la lista
                self.temporales.append(temporal)

                # Visito el hijo 2 (Comparar)
                self.visitComparar(ctx.getChild(2))
        
        # De lo contrario, estoy en la primera pasada en busca de operaciones de suma/resta
        else:
            # Si el hijo 2 (Comparar) no es vacio, entonces hay una operacion de comparacion
            if ctx.getChild(2).getChildCount() != 0:
                
                # # Si el hijo 1 (Exp) tiene un hijo 1 (E) no vacio, entonces hay mas sumas/restas
                # if ctx.getChild(1).getChild(1).getChildCount() != 0:
                #     visitarExpresion(ctx)

                visitarExpresion(ctx)
                
                # Visito el hijo 2 (Comparar)
                self.visitComparar(ctx.getChild(2))


            # De lo contrario no hay mas operaciones de suma/resta
            else:
                # # Si el hijo 1 (Exp) tiene un hijo 1 (E) no vacio, entonces hay mas sumas/restas
                # if ctx.getChild(1).getChild(1).getChildCount() != 0:
                #     visitarExpresion(ctx)

                visitarExpresion(ctx)


    # Visit a parse tree produced by compiladoresParser#exp.
    def visitExp(self, ctx:compiladoresParser.ExpContext):

        # Si el hijo 1 (E) no es vacio, entonces hay una operacion de suma/resta
        if ctx.getChild(1).getChildCount() != 0:
            # Si la bandera es True, estoy en la segunda pasada encargada de sumar los terminos (temporales y factores)
            if self.isSumador:
                # Si el hijo 0 (Term) tiene un hijo 1 (T) que esta vacio, entonces el termino es un factor y no una operacion de multiplicacion/division
                if ctx.getChild(0).getChild(1).getChildCount() == 0:
                    # Visita Term para obtener operando1 que es un termino simple (factor, es decir, un numero o un id)
                    self.visitTerm(ctx.getChild(0)) 
               
                # De lo contrario el hijo 0 (Term) es un termino compuesto el cual se guardo en la lista de temporales
                else:
                    self.operando1 = self.temporales.pop(0)
                
                # Si el hijo 1 (E) tiene un hijo 1 (Term) que tiene un hijo 0 (Factor) distinto de 3, entonces no hay operaciones entre parentesis
                if ctx.getChild(1).getChild(1).getChild(0).getChildCount() != 3:
                
                # if not self.isParentesisOperando2:
                    # Genero un temporal para la suma
                    self.temporales.append(self.generadorDeTemporales.getTemporal())

                # Visita el hijo 1 (E) para obtener operando2 y el operador de suma/resta
                self.visitE(ctx.getChild(1))

            # Si la bandera es False, estoy en la primera pasada en busca operaciones de multiplicacion/division
            else:
                # Si es un termnino compuesto (x * y) visito Term para generar los temporales correspondientes
                if ctx.getChild(0).getChild(1).getChildCount() != 0:
                    # Visito Primero Term en busca de operaciones de multiplicacion/division
                    self.visitTerm(ctx.getChild(0))

                # Visito E en busca de operaciones de multiplicacion/division
                self.visitE(ctx.getChild(1))

                # Como primero busco operaciones de multiplicacion/division y existen sumas/restas debo sumar los terminos
                self.isSumador = True
                # Al activar esta banera se realizara la segunda pasada para sumar los terminos invocada por la regla gramatical C

        # De lo contrario no hay mas sumas/restas y visita el unico termino de la operacion
        else:                
            self.visitTerm(ctx.getChild(0))

    
    # Visit a parse tree produced by compiladoresParser#e.
    def visitE(self, ctx:compiladoresParser.EContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return

        # Si la bandera esta activa, entonces estoy en la segunda pasada encargada de sumar/restar los terminos
        if self.isSumador:
            # Guarda el valor actual del operando1 que bien puede ser un termino simple o un temporal
            operando1 = self.operando1

            """ ------------------------------------------------------------------------------ """
            def obtenerOperando2 (ctx):
                """ 
                    Funcion para obtener el valor del operando2 de la operacion actual.
                """
                # Si el hijo 1 (Term) tiene un hijo 1 (T) que esta vacio, entonces el term es un termino simple
                if ctx.getChild(1).getChild(1).getChildCount() == 0:
                    # Visita Term para obtener el valor del operando1 (termino simple de un factor)
                    self.visitTerm(ctx.getChild(1))
                    
                    # Dentro del hijo (E) trabaja el lado derecho de la suma/resta, por lo tanto el operando1 es en realidad el operando2 de toda la operacion que invoca a (E)
                    self.operando2 = self.operando1
    
                # De lo contrario el hijo 1 (Term) tiene un hijo 1 (T) que no esta vacio, entonces es un termino compuesto (temporal)
                else:
                    # Como estoy en E, el operando2 es el valor del temporal que se creo en la primera pasada (resultados de las multiplicaciones/divisiones)
                    self.operando2 = self.temporales.pop(0)
                    
                    # Si la pila de temporales esta vacia, debo crear otro para asignar la operacion actual:
                    if not self.temporales: self.temporales.append(self.generadorDeTemporales.getTemporal())
            
            """ ------------------------------------------------------------------------------- """
            
            # Si el hijo 1 (Term) tiene un hijo 0 (Factor) que tiene 1 hijo, entonces es un factor simple (un numero o un id)
            if ctx.getChild(1).getChild(0).getChildCount() == 1:
                obtenerOperando2(ctx)

            # Si el hijo 1 (Term) tiene un hijo 0 (Factor) que tiene 2 hijos, entonces es un factor negado
            elif ctx.getChild(1).getChild(0).getChildCount() == 2:
                return

            # Si el hijo 1 (Term) tiene un hijo 0 (Factor) que tiene 3 hijos, entonces es una operacion entre parentesis
            elif ctx.getChild(1).getChild(0).getChildCount() == 3:
                
                # Si el hijo 1 (Term) tine un hijo 1 (T) que no es 0, entonces es operacion compuesta (x * y)
                if ctx.getChild(1).getChild(1).getChildCount() != 0:
                    # Invoca a la funcion para obtener el operando2 correspondiente
                    obtenerOperando2(ctx)
                else:

                    # Invoca a la funcion para obtener el operando2 correspondiente
                    obtenerOperando2(ctx)

                    # Genera el temporal para trabajar al termino entre parentesis
                    self.temporales.append(self.generadorDeTemporales.getTemporal())

       
            # Guarda el operador de suma/resta de la operacion actual
            self.operador  = ctx.getChild(0).getText()
            
            # Reasigno el valor original del operando1
            self.operando1 = operando1

            # Escribe en el archivo de salida la suma/resta de los terminos igualados a un temporal generado
            self.file.write(f'{self.temporales[-1]} = {self.operando1} {self.operador} {self.operando2}\n')

            
            # Si el hijo 2 (E) no es vacio, hay mas operaciones de suma/resta
            if ctx.getChild(2).getChildCount() != 0:
                # Genero un temporal para guardar el resultado de la sigueinte operacion
                temporal = self.generadorDeTemporales.getTemporal()
                
                # Operando1 para la sigueinte operacion sera el temporal generado en la operacion actual
                self.operando1 = self.temporales.pop()

                # Agrego el temporal generado a la lista de temporales
                self.temporales.append(temporal)
                
                # Visita E para obtener el resultado de la siguiente operacion de suma/resta
                self.visitE(ctx.getChild(2))


        # De lo contrario, estoy en la primera pasada en busca de operaciones de multiplicacion/division
        else:
            # Si el hijo 2 (E) no es vacio, entonces hay una operacion de suma/resta. Esto significa que tengo 2 o mas sumas/restas
            if ctx.getChild(2).getChildCount() != 0:
                
                # Si es un termnino compuesto (x * y), lo visito para generar el temporal de la operacion
                if ctx.getChild(1).getChild(1).getChildCount() != 0:
                    self.visitTerm(ctx.getChild(1))
                
                # Visita E en busca de la siguiente operacion de suma/resta
                self.visitE(ctx.getChild(2))


            # De lo contrario no hay mas operaciones de suma/resta
            else:
                # Si es un termnino compuesto (x * y) lo visito en busca de operaciones de creacion de temporales
                if ctx.getChild(1).getChild(1).getChildCount() != 0:
                    self.visitTerm(ctx.getChild(1))

            
    # Visit a parse tree produced by compiladoresParser#term.
    def visitTerm(self, ctx:compiladoresParser.TermContext): 
        # Guardo el primer operando de la operacion de multiplicacion/division
        self.operando1 = self.visitFactor(ctx.getChild(0))

        # Si el hijo 1 no es vacio, entonces hay una operacion de multiplicacion/division
        if ctx.getChild(1).getChildCount() != 0:
            # Si la bandera no esta activa, genero temporales para las operaciones compuestas (x * y)
            
            # Si el operando2 no es una operacion entre parentesis
            if ctx.getChild(1).getChild(1).getChildCount() != 3:
                self.temporales.append(self.generadorDeTemporales.getTemporal())
            
            # Visita la regla gramatical T
            self.visitT(ctx.getChild(1))


    # Visit a parse tree produced by compiladoresParser#t.
    def visitT(self, ctx:compiladoresParser.TContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
        # Si el hijo 1 (Factor) tiene 1 hijo, entonces es un factor simple (un numero o un id)
        if ctx.getChild(1).getChildCount() == 1:
            # Guardo el segundo operando de la operacion de multiplicacion/division
            self.operando2 = self.visitFactor(ctx.getChild(1))
        
        # Si el hijo 1 (Factor) tiene 2 hijos, entonces es un factor negado
        elif ctx.getChild(1).getChildCount() == 2:
            return
        
        # Si el hijo 1 (Factor) tiene 3 hijos, hay un termino entre parentesis
        elif ctx.getChild(1).getChildCount() == 3:
            
            # Guardo el ultimo temporal generado en operando2 que es el temporal de la operacion entre parentesis
            self.operando2 = self.visitFactor(ctx.getChild(1))

            # Genera el temporal para trabajar al termino entre parentesis
            self.temporales.append(self.generadorDeTemporales.getTemporal())
            
        
        # Si las condiciones anteriores no se cumplen, hay un Error (No deberia pasar)
        else:
            print("Error")
        
        # Guardo el operador de la operacion de multiplicacion/division
        self.operador   = ctx.getChild(0).getText()
    
        # Escribo en el archivo la operacion de multiplicacion/division igualada a un temporal
        self.file.write(f'{self.temporales[-1]} = {self.operando1} {self.operador} {self.operando2}\n')

        # Si el hijo 2 (T) no es vacio, hay una operacion de multiplicacion/division
        if ctx.getChild(2).getChildCount() != 0:
            # Genero un nuevo temporal
            temporal = self.generadorDeTemporales.getTemporal()

            # El ultimo temporal de la lista, sera el primer operando para la siguiente operacion
            self.operando1 = self.temporales.pop()
            
            # Agrego el nuevo temporal a la lista
            self.temporales.append(temporal)
            
            # Visito el hijo 2 (T)
            self.visitT(ctx.getChild(2))

    # Visit a parse tree produced by compiladoresParser#factor.
    def visitFactor(self, ctx:compiladoresParser.FactorContext):
        # Si Factor tiene 1 hijo, entonces es un factor simple (un numero o un id)
        if ctx.getChildCount() == 1:
            # operando sera un factor simple, es decir o un id o un numero
            operando = ctx.getChild(0).getText()
            
            # retorno el operando esperado en la operacion de multiplicacion/division invocante
            return operando
       
        # Si Factor tiene 2 hijos, entonces es un factor negado
        elif ctx.getChildCount() == 2:
            return
       
        # Si Factor tiene 3 hijos, entonces es una operacion entre parentesis
        elif ctx.getChildCount() == 3:
            # Guardo el valor actual del operando1 ya que sera sobreescrita en la sig. invocacion
            operando1 = self.operando1
            
            if self.isSumador:
                self.isSumador = False
                
                # Evaluar si el operando2 es una operacion entre parentesis:
                # En caso que la bandera sea True, quiere decir que estoy trabajando con el 
                # segundo operando de otra operacion, asi que debo cambiar el estado de la 
                # bandera para resolver las operaciones que esten dentro de los parentesis,
                # una vez terminado dichas operaciones, continuo con el estado original de 
                # la bandera para resolver las operaciones por fuera de los parentesis
                # bool = False
                # if self.isParentesisOperando2: 
                #     self.isParentesisOperando2 = False
                #     bool = True

                # Visito la regla gramatical Oplogicos
                self.visitOplogicos(ctx.getChild(1))

                # self.isParentesisOperando2 = bool
                self.isSumador = True
            else:
                # bool = False
                # if self.isParentesisOperando2: 
                #     self.isParentesisOperando2 = False
                #     bool = True
                
                # Visito la regla gramatical Oplogicos
                self.visitOplogicos(ctx.getChild(1))

                # self.isParentesisOperando2 = bool
            
            # Recupero el valor del operando1
            self.operando1 = operando1
            
            # Retorno el ultimo temporal de la lista
            return self.temporales.pop()

    # # Visit a parse tree produced by compiladoresParser#iwhile.
    # def visitIwhile(self, ctx:compiladoresParser.IwhileContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#ifor.
    # def visitIfor(self, ctx:compiladoresParser.IforContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#iif.
    # def visitIif(self, ctx:compiladoresParser.IifContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#ielse.
    # def visitIelse(self, ctx:compiladoresParser.IelseContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#init.
    # def visitInit(self, ctx:compiladoresParser.InitContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#cond.
    # def visitCond(self, ctx:compiladoresParser.CondContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#iter.
    # def visitIter(self, ctx:compiladoresParser.IterContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#retornar.
    # def visitRetornar(self, ctx:compiladoresParser.RetornarContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#prototipo_funcion.
    # def visitPrototipo_funcion(self, ctx:compiladoresParser.Prototipo_funcionContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#funcion.
    # def visitFuncion(self, ctx:compiladoresParser.FuncionContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#valor_retorno.
    # def visitValor_retorno(self, ctx:compiladoresParser.Valor_retornoContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#argumentos.
    # def visitArgumentos(self, ctx:compiladoresParser.ArgumentosContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#lista_argumentos.
    # def visitLista_argumentos(self, ctx:compiladoresParser.Lista_argumentosContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#llamada_funcion_valor.
    # def visitLlamada_funcion_valor(self, ctx:compiladoresParser.Llamada_funcion_valorContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#llamada_funcion.
    # def visitLlamada_funcion(self, ctx:compiladoresParser.Llamada_funcionContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#argumentos_a_funcion.
    # def visitArgumentos_a_funcion(self, ctx:compiladoresParser.Argumentos_a_funcionContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#lista_argumentos_a_funcion.
    # def visitLista_argumentos_a_funcion(self, ctx:compiladoresParser.Lista_argumentos_a_funcionContext):
    #     return self.visitChildren(ctx)