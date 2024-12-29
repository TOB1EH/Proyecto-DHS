
from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser

class Temporal():
    def __init__(self):
        self.contador = -1
    
    def getTemporal(self):
        self.contador += 1
        return f't{self.contador}'

class MyVisitor (compiladoresVisitor):

    _instrucciones          = ''
    _temporales             = []
    _etiquetas              = []
    _identificadores        = []
    flag_temporal = False
    generadorDeTemporales   = Temporal()

    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("-" + "=" * 30 + "-")
        print("-- Comienza a generar Codigo Intermedio --")
        self.file = open("./output/codigoIntermedio.txt", "w")

        self.visitInstrucciones(ctx.getChild(0))

        self.file.close()
        print("-- Codigo Intermedio generado Correctamente --")
        print("-" + "=" * 30 + "-")

    # Visit a parse tree produced by compiladoresParser#instrucciones.
    def visitInstrucciones(self, ctx:compiladoresParser.InstruccionesContext):
        self.visitInstruccion(ctx.getChild(0))

        if ctx.getChild(1).getChildCount() != 0:
            self.visitInstrucciones(ctx.getChild(1))
        
        if ctx.getChildCount() == 0:
            return
    
    # Visit a parse tree produced by compiladoresParser#instruccion.
    def visitInstruccion(self, ctx:compiladoresParser.InstruccionContext):
        # Declaraciones
        if isinstance (ctx.getChild(0), compiladoresParser.DeclaracionContext):
            self.visitDeclaracion(ctx.getChild(0))
            
            if self.flag_temporal is True:
                self.file.write(self._temporales.pop(0) + ' =' + self._instrucciones + '\n')
                self._instrucciones = ''
                self.flag_temporal = False
            else:
                self.file.write(self._identificadores.pop() + ' =' + self._instrucciones + '\n')
                self._instrucciones = ''

            self._temporales.clear()
        
        # Asignaciones
        elif isinstance (ctx.getChild(0), compiladoresParser.AsignacionContext):
            self.visitAsignacion(ctx.getChild(0))
            
            self.file.write(self._instrucciones + '\n')
            self._instrucciones = ''
            self._temporales.clear()
        else:
            return

    # Visit a parse tree produced by compiladoresParser#declaracion.
    def visitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        self._identificadores.append(ctx.getChild(1).getText())
        if ctx.getChild(2).getChildCount() == 0:
            return
        self.visitDefinicion(ctx.getChild(2))
    
    # Visit a parse tree produced by compiladoresParser#definicion.
    def visitDefinicion(self, ctx:compiladoresParser.DefinicionContext):
        self.visitOpal(ctx.getChild(1))
        return
    
    # Visit a parse tree produced by compiladoresParser#opal.
    def visitOpal(self, ctx:compiladoresParser.OpalContext):
        self.visitOplogicos(ctx.getChild(0))
        return

    # Visit a parse tree produced by compiladoresParser#oplogicos.
    def visitOplogicos(self, ctx:compiladoresParser.OplogicosContext):
        self.visitLogico(ctx.getChild(0))
        return
    
        # Visit a parse tree produced by compiladoresParser#logico.
    def visitLogico(self, ctx:compiladoresParser.LogicoContext):
        self.visitConjunto(ctx.getChild(0))
        return

    # Visit a parse tree produced by compiladoresParser#conjunto.
    def visitConjunto(self, ctx:compiladoresParser.ConjuntoContext):
        self.visitC(ctx.getChild(0))
        return

    # Visit a parse tree produced by compiladoresParser#c.
    def visitC(self, ctx:compiladoresParser.CContext):
        self.visitExp(ctx.getChild(0))
        return

    # Visit a parse tree produced by compiladoresParser#exp.
    def visitExp(self, ctx:compiladoresParser.ExpContext):
        self.visitTerm(ctx.getChild(0))
        self.visitE(ctx.getChild(1))
        return
    
    # Visit a parse tree produced by compiladoresParser#e.
    def visitE(self, ctx:compiladoresParser.EContext):

        """ 
        
        int c = b + a + 1 - w;

        t0 = b + a
        t1 = t0 + 1
        c = t1 - w
        
        int c = b + a + 1 - w - x + y;

        t0 = b + a
        t1 = t0 + 1
        t2 = t1 - w
        t3 = t2 - x
        c = t3 + y

        int a = c + w


        int b = a + c - w - a;
        t0 = a + c
        b = t0 - w
        
        
        b = a + c;

        """

        if ctx.getChildCount() == 0:
            return
        
        if ctx.getChild(2).getChildCount() > 0:
            if self.flag_temporal is False:
                self._temporales.append(self.generadorDeTemporales.getTemporal())
                self.flag_temporal = True
            else:
                self._temporales.append(self.generadorDeTemporales.getTemporal())
                self._instrucciones += ('\n' + self._temporales[-1] + ' = ' + self._temporales[-2])
        
        # Si no hay más operaciones, obtenemos el valor de la expresión
        else:
            if self.flag_temporal is True:
                self._instrucciones += ('\n' + self._identificadores[-1] + ' = ' + self._temporales[-1])
        
        self._instrucciones += (' ' + ctx.getChild(0).getText()) # Agrega el operador (+ o -)
        self.visitTerm(ctx.getChild(1))
        self.visitE(ctx.getChild(2))

    # Visit a parse tree produced by compiladoresParser#term.
    def visitTerm(self, ctx:compiladoresParser.TermContext):
        self.visitFactor(ctx.getChild(0))
        return

    # Visit a parse tree produced by compiladoresParser#factor.
    def visitFactor(self, ctx:compiladoresParser.FactorContext):
        if ctx.getChildCount() == 1:
            self._instrucciones += ' ' + ctx.getChild(0).getText()
    
    # Visit a parse tree produced by compiladoresParser#asignacion.
    def visitAsignacion(self, ctx:compiladoresParser.AsignacionContext):
        self._instrucciones += (ctx.getChild(0).getText() + ' ' + ctx.getChild(1).getText())
        self.visitOpal(ctx.getChild(2))
        # Cuando la asignacion no es directa (uso temporales)
        return














    # def visitDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
    #     # No accede mediante el 'super()' sino mediante el metodo para obtener los hijos (nodos del arbol)
    #     print(ctx.getChild(0).getText() + " - " +   # Quiero ver el tipo de dato
    #           ctx.getChild(1).getText())            # Quiero ver el ID

    #     # return super().visitDeclaracion(ctx)
    #     return None
    
    # def visitBloque(self, ctx: compiladoresParser.BloqueContext):
    #     print("Nuevo Contexto")
    #     print(ctx.getText())
    #     return super().visitInstrucciones(ctx.getChild(1))
    #     # return super().visitBloque(ctx)

    # def visitTerminal(self, node):
    #     print(" ==> Token " + node.getText())
    #     return super().visitTerminal(node)