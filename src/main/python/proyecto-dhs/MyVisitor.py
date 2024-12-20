
from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser

class Temporal():
    def __init__(self):
        self.contador = -1
    
    def getTemporal(self):
        self.contador += 1
        return f't{self.contador}'

class MyVisitor (compiladoresVisitor):

    _temporales             = []
    _etiquetas              = []
    _identificadores        = []
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
        if isinstance (ctx.getChild(0), compiladoresParser.DeclaracionContext):
            self.visitDeclaracion(ctx.getChild(0))
        elif isinstance (ctx.getChild(0), compiladoresParser.AsignacionContext):
            self.visitAsignacion(ctx.getChild(0))
        else:
            return

    # Visit a parse tree produced by compiladoresParser#declaracion.
    def visitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        self._identificadores.append(ctx.getChild(1).getText())
        if ctx.getChild(2).getChildCount() != 0:
            self.visitDefinicion(ctx.getChild(2))
        else:
            return
        
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
        return

    # Visit a parse tree produced by compiladoresParser#term.
    def visitTerm(self, ctx:compiladoresParser.TermContext):
        self.visitFactor(ctx.getChild(0))
        return

    # Visit a parse tree produced by compiladoresParser#factor.
    def visitFactor(self, ctx:compiladoresParser.FactorContext):
        if ctx.getChildCount() == 1:
            id = self._identificadores.pop()
            self.file.write(id + '=' + ctx.getChild(0).getText() + '\n')
            return
    
    # Visit a parse tree produced by compiladoresParser#asignacion.
    def visitAsignacion(self, ctx:compiladoresParser.AsignacionContext):
        self._identificadores.append(ctx.getChild(0).getText())
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