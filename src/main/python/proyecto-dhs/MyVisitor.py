from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser

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
                self.file.write(f"{id} = {self.temporales.pop()}\n")
            
            # De la contrario la variable solo almacena un factor
            else:
                self.file.write(f"{id} = {self.operando1}\n")
            
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
    # def visitAsignacion(self, ctx:compiladoresParser.AsignacionContext):
    #     return self.visitChildren(ctx)

    # Visit a parse tree produced by compiladoresParser#opal.
    def visitOpal(self, ctx:compiladoresParser.OpalContext):
        self.visitOplogicos(ctx.getChild(0))
        

    # Visit a parse tree produced by compiladoresParser#oplogicos.
    def visitOplogicos(self, ctx:compiladoresParser.OplogicosContext):
        self.visitLogico(ctx.getChild(0))

    # # Visit a parse tree produced by compiladoresParser#lor.
    # def visitLor(self, ctx:compiladoresParser.LorContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#logico.
    # def visitLogico(self, ctx:compiladoresParser.LogicoContext):
    #     return self.visitChildren(ctx)


    # # Visit a parse tree produced by compiladoresParser#land.elf.operando1
    # def visitLand(self, ctx:compiladoresParser.LandContext):
    #     return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#conjunto.
    def visitConjunto(self, ctx:compiladoresParser.ConjuntoContext):
        self.visitC(ctx.getChild(0))


    # # Visit a parse tree produced by compiladoresParser#igualdad.
    # def visitIgualdad(self, ctx:compiladoresParser.IgualdadContext):
    #     return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#c.
    def visitC(self, ctx:compiladoresParser.CContext):
        self.visitExp(ctx.getChild(0))
        
        # Si la bandera es True recorro el arbol para sumar los terminos
        if self.isSumador:
            super().visitExp(ctx) # Los terminos se encuentran dentro de Exp (expresion)
            self.isSumador = False # Reseteo la bandera

    # # Visit a parse tree produced by compiladoresParser#comparar.
    # def visitComparar(self, ctx:compiladoresParser.CompararContext):
    #     return self.visitChildren(ctx)


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
            
            # Si el hijo 1 (Term) tienes un hijo 1 (T) que esta vacio, entonces el term es un termino simple
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
            self.operador   = ctx.getChild(0).getText()

            # Escribe en el archivo de salida la suma/resta de los terminos igualados a un temporal generado
            self.file.write(f'{self.temporales[-1]} = {operando1} {self.operador} {self.operando2}\n')

            
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
            # Si el hijo 2 no es vacio, entonces hay una operacion de suma/resta. Esto significa que tengo 2 o mas sumas/restas
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
            if not self.isParentesisOperando2:
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
            # Activo la bandera para indicar que el termino entre parentesis es el operando 2 
            self.isParentesisOperando2 = True
            
            # Guardo el ultimo temporal generado en operando2 que es el temporal de la operacion entre parentesis
            self.operando2 = self.visitFactor(ctx.getChild(1))

            # Genera el temporal para trabajar al termino entre parentesis
            self.temporales.append(self.generadorDeTemporales.getTemporal())
            
            # Desactivo la bandera
            self.isParentesisOperando2 = False
        
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
            operador1 = self.operando1
            
            # Visito la regla gramatical Oplogicos
            self.visitOplogicos(ctx.getChild(1))
            
            # Recupero el valor del operando1
            self.operando1 = operador1
            
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