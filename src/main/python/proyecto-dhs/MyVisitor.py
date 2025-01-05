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
        """
        Inicializa la clase MyVisitorPruebas con valores predeterminados.

        Atributos:
            file (None): Marcador de posición para un objeto de archivo, inicialmente establecido en None.
            ruta (str): Ruta al archivo de salida para el código intermedio, por defecto es './output/codigoIntermedio.txt'.
            instrucciones (str): Cadena para almacenar instrucciones, inicialmente vacía.
            temporales (list): Lista para almacenar variables temporales, inicialmente vacía.
            etiquetas (list): Lista para almacenar etiquetas, inicialmente vacía.
            identificadores (list): Lista para almacenar identificadores, inicialmente vacía.
            generadorDeTemporales (Temporal): Instancia de la clase Temporal para generar variables temporales.
            generadorDeEtiquetas (Etiqueta): Instancia de la clase Etiqueta para generar etiquetas.
        """
        
        self.file                    = None
        self.ruta                    = './output/codigoIntermedio.txt' 
        self.temporales              = []
        self.etiquetas               = []
        self.generadorDeTemporales   = Temporal()
        self.generadorDeEtiquetas    = Etiqueta()

        self.operando1               = None
        self.operando2               = None
        self.operador                = None
        self.temporalIsOperando2     = False

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
        
        id = ctx.getChild(1).getText()

        # Si existe el hijo 3, entonces hay una asignacion 
        if ctx.getChild(2).getChildCount() != 0:
            self.visitDefinicion(ctx.getChild(2))


            if self.operando1 is not None and self.operando2 is not None and self.operador is not None:
            
                if len(self.temporales) == 1:
                    if self.temporalIsOperando2:
                        self.file.write(f'{id} = {self.operando1} {self.operador} {self.temporales.pop()}\n')
                    else:
                        self.file.write(f'{id} = {self.temporales.pop()} {self.operador} {self.operando1}\n')
                
                else:
                    if len(self.temporales) == 2:
                        self.operando2 = self.temporales.pop()
                        self.operando1 = self.temporales.pop()
                    self.file.write(f'{id} = {self.operando1} {self.operador} {self.operando2}\n')
                
                self.operando1 = None
                self.operando2 = None
                self.operador  = None
            
            elif self.operando1 is not None and self.operando2 is None and self.operador is None:
                self.file.write(f'{id} = {self.operando1}\n')
                
                self.operando1 = None
            
            else:
                print("Error en la asignacion")
        
        else:
            self.file.write(f'{id} = {self.operando1}\n')


    # Visit a parse tree produced by compiladoresParser#definicion.
    def visitDefinicion(self, ctx:compiladoresParser.DefinicionContext):
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


    # # Visit a parse tree produced by compiladoresParser#land.
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


    # # Visit a parse tree produced by compiladoresParser#comparar.
    # def visitComparar(self, ctx:compiladoresParser.CompararContext):
    #     return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#exp.
    def visitExp(self, ctx:compiladoresParser.ExpContext):
        
        # Si el hijo 1 no es vacio, entonces hay una operacion de suma/resta
        if ctx.getChild(1).getChildCount() != 0:

            # Si es un termnino compuesto (x * y) creo un temporal para almacenar el resultado
            if ctx.getChild(0).getChild(1).getChildCount() != 0:
                temporal = self.generadorDeTemporales.getTemporal()
                self.temporales.append(temporal)
                
                self.visitTerm(ctx.getChild(0))
                
                self.visitE(ctx.getChild(1))

            else:
                self.visitE(ctx.getChild(1))
                
                self.visitTerm(ctx.getChild(0))

                self.temporalIsOperando2 = True
            
            # Guardo la operacion de suma/resta porque es la ultima operacion a realizar
            self.operador = ctx.getChild(1).getChild(0).getText()
                
        else:
            self.visitTerm(ctx.getChild(0))


    # Visit a parse tree produced by compiladoresParser#e.
    def visitE(self, ctx:compiladoresParser.EContext):
        # Si el hijo 1 es 0, entonces no hay una operacion de suma/resta
        if ctx.getChildCount() == 0:
            return
        
        # Guardo el operador de la operacion de suma/resta
        self.operador = ctx.getChild(0).getText()

        # Si el hijo 2 no es vacio, entonces hay una operacion de suma/resta
        if ctx.getChild(2).getChildCount() != 0:
            self.visitE(ctx.getChild(1))

        # De lo contrario no hay mas operaciones de suma/resta
        else:
            # Si es un termnino compuesto (x * y) creo un temporal para almacenar el resultado
            if ctx.getChild(1).getChild(1).getChildCount() != 0:
                temporal = self.generadorDeTemporales.getTemporal()
                self.temporales.append(temporal)
            
            self.visitTerm(ctx.getChild(1))
            

    # Visit a parse tree produced by compiladoresParser#term.
    def visitTerm(self, ctx:compiladoresParser.TermContext):
    
        # Guardo el primer operando de la operacion de multiplicacion/division
        self.operando1 = self.visitFactor(ctx.getChild(0))

        # Si el hijo 1 no es vacio, entonces hay una operacion de multiplicacion/division
        if ctx.getChild(1).getChildCount() != 0:
            self.visitT(ctx.getChild(1))


    # Visit a parse tree produced by compiladoresParser#t.
    def visitT(self, ctx:compiladoresParser.TContext):
        if ctx.getChildCount() == 0:
            return
        
        self.operador   = ctx.getChild(0).getText()
        self.operando2  = self.visitFactor(ctx.getChild(1))
        
        if self.temporales:
            self.file.write(f'{self.temporales[-1]} = {self.operando1} {self.operador} {self.operando2}\n')

        if ctx.getChild(2).getChildCount() != 0:
            temporal = self.generadorDeTemporales.getTemporal()

            self.operando1 = self.temporales.pop()
            
            self.temporales.append(temporal)
            
            self.visitT(ctx.getChild(2))


    # Visit a parse tree produced by compiladoresParser#factor.
    def visitFactor(self, ctx:compiladoresParser.FactorContext):
        
        if ctx.getChildCount() == 1:
            operando = ctx.getChild(0).getText()
            return operando
    

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