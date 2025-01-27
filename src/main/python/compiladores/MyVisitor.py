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
        self.isSumador               = False
        self.isFuncion               = False

        # Constantes Codigo Intermedio de Tres Direcciones
        self.etiqueta   = 'label'
        self.b          = 'jmp'
        self.bneq       = 'ifnjmp'


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

        # Si existe el hijo 2 (Definicion), entonces hay una asignacion a la variable
        if ctx.getChild(2).getChildCount() != 0:
            self.visitDefinicion(ctx.getChild(2))

            if not ctx.getChild(2).llamada_funcion():

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
        
        if ctx.getChild(3).getChildCount() != 0:
            self.visitLista_variables(ctx.getChild(3))


    # Visit a parse tree produced by compiladoresParser#definicion.
    def visitDefinicion(self, ctx:compiladoresParser.DefinicionContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
        # Si la definicion es una llamada a funcion:
        if ctx.llamada_funcion():
            self.visitLlamada_funcion(ctx.getChild(1))

            self.file.write(f'pop {ctx.parentCtx.getChild(1).getText()}\n')

        # De lo contrario solo es una asignacion
        else:
            self.visitOpal(ctx.getChild(1))


    # Visit a parse tree produced by compiladoresParser#lista_variables.
    def visitLista_variables(self, ctx:compiladoresParser.Lista_variablesContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
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
        
        if ctx.getChild(3).getChildCount() != 0:
            self.visitLista_variables(ctx.getChild(3))


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

        if ctx.getChild(1).getChildCount() != 0:
            # Si el operando1 es un temporal, es el ultimo paso de la asignacion
            if self.temporales:
                self.operando1 = self.temporales.pop()
            # En caso contrario, operando1 es el primer factor, el valor queda como esta
            
            self.visitLor(ctx.getChild(1))

        # Evalua si es una llamada a funcion
        if self.isFuncion:
            if self.temporales:
                self.file.write(f"push {self.temporales.pop()}\n")
            else:
                self.file.write(f"push {self.operando1}\n")

    # Visit a parse tree produced by compiladoresParser#lor.
    def visitLor(self, ctx:compiladoresParser.LorContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
        # Creo una copia del actual operando1
        operando1 = self.operando1

        # Visito el segundo conjunto de la operacion AND
        self.visitLogico(ctx.getChild(1))
        
        # Si el operando 2 es un temporal, es el ultimo paso de la asignacion
        if self.temporales:
            self.operando2 = self.temporales.pop()
        # En caso contrario, operando2 es un facotr simple guardado en operando1
        else:
            self.operando2 = self.operando1

        # Recupero el valor del operando1 de la operacion OR actual
        self.operando1 = operando1

        # Guardo el operador OR
        self.operador = ctx.getChild(0).getText()

        # Genero un temporal para la operacion OR
        self.temporales.append(self.generadorDeTemporales.getTemporal())

        # Escribo en el archivo la operacion OR
        self.file.write(f'{self.temporales[-1]} = {self.operando1} {self.operador} {self.operando2}\n')

        # Si el hijo 2 (Lor) no es vacio, entonces hay otra operacion OR
        if ctx.getChild(2).getChildCount() != 0:
            # El operando1 para la siguiente operacion OR es el temporal generado en esta
            self.operando1 = self.temporales.pop()

            # Visita la regla Lor para escribir la siguiente operacion
            self.visitLor(ctx.getChild(2))


    # Visit a parse tree produced by compiladoresParser#logico.
    def visitLogico(self, ctx:compiladoresParser.LogicoContext):
        self.visitConjunto(ctx.getChild(0))

        if ctx.getChild(1).getChildCount() != 0:
            # Si el operando 1 es un temporal, es el ultimo paso de la asignacion
            if self.temporales:
                self.operando1 = self.temporales.pop()
            # En caso contrario, operando1 es el primer factor, el valor queda como esta

            self.visitLand(ctx.getChild(1))


    # Visit a parse tree produced by compiladoresParser#land.elf.operando1
    def visitLand(self, ctx:compiladoresParser.LandContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
        # Creo una copia del actual operando1
        operando1 = self.operando1

        # Visito el segundo conjunto de la operacion AND
        self.visitConjunto(ctx.getChild(1))
        
        # Si el operando 2 es un temporal, es el ultimo paso de la asignacion
        if self.temporales:
            self.operando2 = self.temporales.pop()
        # En caso contrario, operando2 es un facotr simple guardado en operando1
        else:
            self.operando2 = self.operando1

        # Recupero el valor del operando1 de la operacion AND actual
        self.operando1 = operando1

        # Guardo el operador AND
        self.operador = ctx.getChild(0).getText()

        # Genero un temporal para la operacion AND
        self.temporales.append(self.generadorDeTemporales.getTemporal())

        # Escribo en el archivo la operacion AND
        self.file.write(f'{self.temporales[-1]} = {self.operando1} {self.operador} {self.operando2}\n')

        # Si el hijo 2 (Land) no es vacio, entonces hay otra operacion AND
        if ctx.getChild(2).getChildCount() != 0:
            # El operando1 para la siguiente operacion AND es el temporal generado en esta
            self.operando1 = self.temporales.pop()

            # Visita la regla Land para escribir la siguiente operacion
            self.visitLand(ctx.getChild(2))


    # Visit a parse tree produced by compiladoresParser#conjunto.
    def visitConjunto(self, ctx:compiladoresParser.ConjuntoContext):

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
                    self.visitC(ctx.getChild(0))

                # De lo contrario
                else:
                    self.visitC(ctx.getChild(0))

                    self.operando1 = self.temporales.pop(0)

                # Visito Igualdad  en busca de comparaciones de igualdad
                self.visitIgualdad(ctx.getChild(1))

        # De lo contrario no hay comparaciones de igualdad, asi que solo visita al subconjunto en busca de operaciones de comparacion
        else:                
            self.visitC(ctx.getChild(0))


    # Visit a parse tree produced by compiladoresParser#igualdad.
    def visitIgualdad(self, ctx:compiladoresParser.IgualdadContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return

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
            self.visitC(ctx.getChild(1))
            self.operando2 = self.operando1
        
        # De lo contrario
        else:
            self.visitC(ctx.getChild(1))
            
            self.operando2 = self.temporales.pop(0)

        # Guardo el valor del operador de comparacion de igualdad
        self.operador = ctx.getChild(0).getText()
        
        # Reasigno el valor original del operando1
        self.operando1 = operando1

        # Genera un temporal para la operacion
        self.temporales.append(self.generadorDeTemporales.getTemporal())

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
                
                # Si el hijo 0 (Exp) tiene un hijo 1 (E) vacio, entonces no hay operacion de suma/resta
                cond1 = ctx.getChild(0).getChild(1).getChildCount() == 0

                # Si el hijo 0 (Exp) tiene un hijo 0 (Term) tiene un hijo 1 (T) vacio, entonces es un termino simople
                cond2 = ctx.getChild(0).getChild(0).getChild(1).getChildCount() == 0
          
                # Entonces si ambas se cumplen:
                if cond1 and cond2:
                    visitarExpresion(ctx)
               
                # De lo contrario
                else:
                    visitarExpresion(ctx)
                    self.operando1 = self.temporales.pop(0)
                
                # Visito Comparar en busca de operaciones de comparacion
                self.visitComparar(ctx.getChild(1))

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

        # Guardo el valor del operando1
        operando1 = self.operando1

        # Si el hijo 1 (Exp) tiene un hijo 1 (E) vacio, entonces no hay operacion de suma/resta
        cond1 = ctx.getChild(1).getChild(1).getChildCount() == 0
        
        # Si el hijo 1 (Exp) tiene un hijo 0 (Term) tiene un hijo 1 (T) vacio, entonces es un termino simople
        cond2 = ctx.getChild(1).getChild(0).getChild(1).getChildCount() == 0

        # Entonces si ambas se cumplen:
        if cond1 and cond2:
            visitarExpresion(ctx)
                    
            # Como Exp es llamada dentro de Comparar, el operando1 obtenido es el operando2
            self.operando2 = self.operando1

        # De lo contrario, hay una operacion de suma/resta guardada en un
        else:
            visitarExpresion(ctx)
            self.operando2 = self.temporales.pop(0)
        
        # Restauro el valor original del operando1
        self.operando1 = operando1
        
        # Guardo el operador de comparacion
        self.operador = ctx.getChild(0).getText()
        
        # Genera el temporal para trabajar con la operacion actual
        self.temporales.append(self.generadorDeTemporales.getTemporal())

        # Escribo en el archivo la operacion de comparacion igualada a un temporal
        self.file.write(f'{self.temporales[-1]} = {self.operando1} {self.operador} {self.operando2}\n')
        
        # Si el hijo 2 (Comparar) no es vacio, hay una operacion de comparacion
        if ctx.getChild(2).getChildCount() != 0:

            # El ultimo temporal de la lista, sera el primer operando para la siguiente operacion
            self.operando1 = self.temporales.pop()
            
            # Visito el hijo 2 (Comparar)
            self.visitComparar(ctx.getChild(2))


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
                    
            # Guarda el operador de suma/resta de la operacion actual
            self.operador  = ctx.getChild(0).getText()
            
            # Reasigno el valor original del operando1
            self.operando1 = operando1

            # Genera el temporal para trabajar con la operacion actual
            self.temporales.append(self.generadorDeTemporales.getTemporal())

            # Escribe en el archivo de salida la suma/resta de los terminos igualados a un temporal generado
            self.file.write(f'{self.temporales[-1]} = {self.operando1} {self.operador} {self.operando2}\n')
            
            # Si el hijo 2 (E) no es vacio, hay mas operaciones de suma/resta
            if ctx.getChild(2).getChildCount() != 0:
                
                # Operando1 para la sigueinte operacion sera el temporal generado en la operacion actual
                self.operando1 = self.temporales.pop()

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
            
            # Visita la regla gramatical T
            self.visitT(ctx.getChild(1))


    # Visit a parse tree produced by compiladoresParser#t.
    def visitT(self, ctx:compiladoresParser.TContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return

        # Guardo el segundo operando de la operacion de multiplicacion/division
        self.operando2 = self.visitFactor(ctx.getChild(1))

        # Guardo el operador de la operacion de multiplicacion/division
        self.operador   = ctx.getChild(0).getText()
    
        # Genero un temporal para la operacion actual
        self.temporales.append(self.generadorDeTemporales.getTemporal())

        # Escribo en el archivo la operacion de multiplicacion/division igualada a un temporal
        self.file.write(f'{self.temporales[-1]} = {self.operando1} {self.operador} {self.operando2}\n')

        # Si el hijo 2 (T) no es vacio, hay una operacion de multiplicacion/division
        if ctx.getChild(2).getChildCount() != 0:
            # El ultimo temporal de la lista, sera el primer operando para la siguiente operacion
            self.operando1 = self.temporales.pop()
            
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
            
            # Obtengo el valor del factor negado
            valor = self.visitFactor(ctx.getChild(1))

            # Guardo el operador de negacion
            operador_negacion = ctx.getChild(0).getText()

            # Genero un temporal para la operacion de negacion
            self.temporales.append(self.generadorDeTemporales.getTemporal())
            
            # Escribo en el archivo la operacion
            self.file.write(f'{self.temporales[-1]} = {operador_negacion}{valor}\n')

            # Devuelvo el temporal creado
            return self.temporales.pop()
       
        # Si Factor tiene 3 hijos, entonces es una operacion entre parentesis
        elif ctx.getChildCount() == 3:
            # Guardo el valor actual del operando1 ya que sera sobreescrita en la sig. invocacion
            operando1 = self.operando1
            
            if self.isSumador:
                self.isSumador = False
                
                # Visito la regla gramatical Oplogicos
                self.visitOplogicos(ctx.getChild(1))

                # self.isParentesisOperando2 = bool
                self.isSumador = True
            else:
                # Visito la regla gramatical Oplogicos
                self.visitOplogicos(ctx.getChild(1))
            
            # Recupero el valor del operando1
            self.operando1 = operando1
            
            # Retorno el ultimo temporal de la lista
            return self.temporales.pop()

    # Visit a parse tree produced by compiladoresParser#iwhile.
    def visitIwhile(self, ctx:compiladoresParser.IwhileContext):
        
        # Genero la etiqueta para el salto condicional del bucle While
        self.etiquetas.append(self.generadorDeEtiquetas.getEtiqueta())
        
        # Escribo en el archivo la etiqueta para iniciar el bucle while
        self.file.write(f'{self.etiqueta} {self.etiquetas[-1]}\n')
        
        # Visito la Regla Cond, en busca de la condicion del bucle While
        self.visitCond(ctx.getChild(2))
        
        # Genero la etiqueta para finalizar el bucle while
        self.etiquetas.append(self.generadorDeEtiquetas.getEtiqueta())
        
        # Escribo en el archivo el salto condicional del bucle While
        self.file.write(f'{self.bneq} {self.temporales.pop()}, {self.etiquetas[-1]}\n')
        
        # Visito la Regla Instruccion, para escribir en el archivo la instruccion del bucle While
        self.visitInstruccion(ctx.getChild(4))
        
        # Escribo en el archivo el salto al comienzo del bucle While
        self.file.write(f'{self.b} {self.etiquetas.pop(0)}\n')
        
        # Escribo en el archivo la etiqueta para salir del bucle while
        self.file.write(f'{self.etiqueta} {self.etiquetas.pop(0)}\n')
        

    # Visit a parse tree produced by compiladoresParser#ifor.
    def visitIfor(self, ctx:compiladoresParser.IforContext):
        # Caso para bucle for infinito
        if ctx.getChild(2).getChildCount() == 0 and ctx.getChild(4).getChildCount() == 0 and ctx.getChild(6).getChildCount() == 0:
            # Genero la etiqueta para el salto condicional del bucle for
            self.etiquetas.append(self.generadorDeEtiquetas.getEtiqueta())

            # Escribo en el archivo la etiqueta para iniciar el bucle for
            self.file.write(f'{self.etiqueta} {self.etiquetas[-1]}\n')

            # Visito la Regla Instruccion, para escribir en el archivo la instruccion del bucle While
            self.visitInstruccion(ctx.getChild(8))

            # Escribo en el archivo el salto al comienzo del bucle for
            self.file.write(f'{self.b} {self.etiquetas.pop(0)}\n')
        
        # Caso para bucle for con condicion
        else:
            # Visita la Regla Init para obtener la asignacion inicial del bucle for
            self.visitInit(ctx.getChild(2))

            # Genero la etiqueta para el salto condicional del bucle for
            self.etiquetas.append(self.generadorDeEtiquetas.getEtiqueta())

            # Escribo en el archivo la etiqueta para iniciar el bucle for
            self.file.write(f'{self.etiqueta} {self.etiquetas[-1]}\n')

            # Visito la Regla Cond, en busca de la condicion del bucle for
            self.visitCond(ctx.getChild(4))

            # Genero la etiqueta para finalizar el bucle for
            self.etiquetas.append(self.generadorDeEtiquetas.getEtiqueta())

            # Escribo en el archivo el salto condicional del bucle for
            self.file.write(f'{self.bneq} {self.temporales.pop()}, {self.etiquetas[-1]}\n')

            # Visito la Regla Instruccion, para escribir en el archivo la instruccion del bucle While
            self.visitInstruccion(ctx.getChild(8))

            # Visita la Regla Iter, para obtener la accion post-ejecucion del bucle for (iterador)
            self.visitIter(ctx.getChild(6))

            # Escribo en el archivo el salto al comienzo del bucle for
            self.file.write(f'{self.b} {self.etiquetas.pop(0)}\n')

            # Escribo en el archivo la etiqueta para salir del bucle while
            self.file.write(f'{self.etiqueta} {self.etiquetas.pop(0)}\n')


    # Visit a parse tree produced by compiladoresParser#iif.
    def visitIif(self, ctx:compiladoresParser.IifContext):
        
        # Visito la Regla Cond, en busca de la condicion del if
        self.visitCond(ctx.getChild(2))         
        
        # Si el if fue invocado por un else
        if isinstance(ctx.parentCtx, compiladoresParser.IelseContext):

            # Escribo en el archivo el salto condicional del if
            self.file.write(f'{self.bneq} {self.temporales.pop()}, {self.etiquetas[-1]}\n')
            
            # Visito la Regla Instruccion, para escribir en el archivo la instruccion del if
            self.visitInstruccion(ctx.getChild(4))

            # Genero la etiqueta para salir del if
            self.etiquetas.append(self.generadorDeEtiquetas.getEtiqueta())    

            # Escribo en el archivo el salto para salir del if
            self.file.write(f'{self.b} {self.etiquetas[-1]}\n')

        # De lo contrario, es un condicional if solo
        else:
            # Genero la etiqueta para salir del if
            self.etiquetas.append(self.generadorDeEtiquetas.getEtiqueta())
            
            # Escribo en el archivo el salto condicional del if
            self.file.write(f'{self.bneq} {self.temporales.pop()}, {self.etiquetas[-1]}\n')

            # Visito la Regla Instruccion, para escribir en el archivo la instruccion del if
            self.visitInstruccion(ctx.getChild(4))

            # Escribo en el archivo la etiqueta para salir del else
            self.file.write(f'{self.etiqueta} {self.etiquetas.pop()}\n')


    # Visit a parse tree produced by compiladoresParser#ielse.
    def visitIelse(self, ctx:compiladoresParser.IelseContext):
        # Genero la etiqueta para el salto condicional del if
        self.etiquetas.append(self.generadorDeEtiquetas.getEtiqueta())
        
        # Visito el if por que de lo contrario no puede existir el else
        self.visitIif(ctx.getChild(0))

        # Escribo en el archivo el salto condicional del if
        self.file.write(f'{self.etiqueta} {self.etiquetas.pop(0)}\n')

        # Visito la Regla Instruccion, para escribir en el archivo la instruccion del else
        self.visitInstruccion(ctx.getChild(2))

        # Escribo en el archivo la etiqueta para salir del else
        self.file.write(f'{self.etiqueta} {self.etiquetas.pop()}\n')
        


    # # Visit a parse tree produced by compiladoresParser#init.
    # def visitInit(self, ctx:compiladoresParser.InitContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#cond.
    # def visitCond(self, ctx:compiladoresParser.CondContext):
    #     return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#iter.
    def visitIter(self, ctx:compiladoresParser.IterContext):
        # Si el iter tiene 1 hijo, es una asignacion
        if ctx.getChildCount() == 1:
            self.visitAsignacion(ctx.getChild(0))
        
        # Si Iter tiene 2 hijos, es un iterador
        elif ctx.getChildCount() == 2:
            # Genero un temporal para la operacion del iterador
            self.temporales.append(self.generadorDeTemporales.getTemporal())

            # Casos para pre-incrementos/decrementos
            if ctx.getChild(0).getText() == '++' or ctx.getChild(0).getText() == '--':
                # Guardo la variable
                id = ctx.getChild(1).getText()

                # Guardo el operador de ibcremento/decremento
                inc_dec = ctx.getChild(0).getText()

            # Casos para post-incrementos/decrementos
            else:
                # Guardo la variable
                id = ctx.getChild(0).getText()

                # Guardo el operador de incremento/decremento
                inc_dec = ctx.getChild(1).getText()

            # Evaluo si se trata de un incremento o de un decremento
            if inc_dec == '++':
                self.operador = '+'
            else:
                self.operador = '-'
            
            # Escribo en el archivo la operacion de incremento/decremento dentro de un temporal
            self.file.write(f'{self.temporales[-1]} = {id} {self.operador} 1\n')

            # Escribo en el archivo, la asignacion del temporal a la variable
            self.file.write(f'{id} =  {self.temporales.pop()}\n')


    # # Visit a parse tree produced by compiladoresParser#retornar.
    # def visitRetornar(self, ctx:compiladoresParser.RetornarContext):
    #     return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#prototipo_funcion.
    def visitPrototipo_funcion(self, ctx:compiladoresParser.Prototipo_funcionContext):
        # Genero la etiqueta de salto hacia la funcion
        self.etiquetas.append(self.generadorDeEtiquetas.getEtiqueta())


    # Visit a parse tree produced by compiladoresParser#funcion.
    def visitFuncion(self, ctx:compiladoresParser.FuncionContext):
        if ctx.getChild(1).getText() != 'main':
        
            # self.file.write(f'-------- FUNCION --------\n')

            # Escribo en el archivo la etiqueta de salto hacia la funcion
            self.file.write(f'{self.etiqueta} {self.etiquetas.pop(0)}\n')

            self.file.write(f'pop {self.etiquetas[-1]}\n')
    
            """ Evaluar cuando no tiene argumentos """
    
            # Visito la Regla Argunementos para obtener los argumentos de la funcion
            self.visitArgumentos(ctx.getChild(3))
    
            self.visitBloque(ctx.getChild(5))

            self.file.write(f'push {self.temporales.pop()}\n')
    
            self.file.write(f'{self.b} {self.etiquetas.pop()}\n')
        
        else:
            self.visitBloque(ctx.getChild(5))



    # # Visit a parse tree produced by compiladoresParser#valor_retorno.
    # def visitValor_retorno(self, ctx:compiladoresParser.Valor_retornoContext):
    #     return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#argumentos.
    def visitArgumentos(self, ctx:compiladoresParser.ArgumentosContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
        self.file.write(f'pop {ctx.getChild(1).getText()}\n')

        if ctx.getChild(2).getChildCount() != 0:
            self.visitLista_argumentos(ctx.getChild(2))


    # Visit a parse tree produced by compiladoresParser#lista_argumentos.
    def visitLista_argumentos(self, ctx:compiladoresParser.Lista_argumentosContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
        self.file.write(f'pop {ctx.getChild(2).getText()}\n')

        if ctx.getChild(3).getChildCount() != 0:
            self.visitLista_argumentos(ctx.getChild(3))



    # Visit a parse tree produced by compiladoresParser#llamada_funcion_valor.
    def visitLlamada_funcion_valor(self, ctx:compiladoresParser.Llamada_funcion_valorContext):

        self.visitLlamada_funcion(ctx.getChild(2))

        self.file.write(f'pop {ctx.getChild(0).getText()}\n')




    # Visit a parse tree produced by compiladoresParser#llamada_funcion.
    def visitLlamada_funcion(self, ctx:compiladoresParser.Llamada_funcionContext):
        # self.file.write(f'-------- LLAMADA A FUNCION --------\n')

        self.visitArgumentos_a_funcion(ctx.getChild(2))

        self.etiquetas.append(self.generadorDeEtiquetas.getEtiqueta())

        self.file.write(f'push {self.etiquetas[-1]}\n')
        
        self.file.write(f'{self.b} {self.etiquetas[-2]}\n')

        self.file.write(f'{self.etiqueta} {self.etiquetas[-1]}\n')





    # Visit a parse tree produced by compiladoresParser#argumentos_a_funcion.
    def visitArgumentos_a_funcion(self, ctx:compiladoresParser.Argumentos_a_funcionContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
        self.isFuncion = True

        self.visitOplogicos(ctx.getChild(0))

        if ctx.getChild(1).getChildCount() != 0:
            self.visitLista_argumentos_a_funcion(ctx.getChild(1))

        self.isFuncion = False


    # Visit a parse tree produced by compiladoresParser#lista_argumentos_a_funcion.
    def visitLista_argumentos_a_funcion(self, ctx:compiladoresParser.Lista_argumentos_a_funcionContext):
        # Valida que la regla gramatical no este vacia
        if ctx.getChildCount() == 0:
            return
        
        self.visitOplogicos(ctx.getChild(1))

        if ctx.getChild(2).getChildCount() != 0:
            self.visitLista_argumentos_a_funcion(ctx.getChild(2))