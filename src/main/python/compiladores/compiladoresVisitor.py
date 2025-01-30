# Generated from /home/tobias/Documents/workspace/Proyectos-DHS/proyecto-dhs/src/main/python/compiladores/compiladores.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .compiladoresParser import compiladoresParser
else:
    from compiladoresParser import compiladoresParser

# This class defines a complete generic visitor for a parse tree produced by compiladoresParser.

class compiladoresVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by compiladoresParser#programa.
    def visitPrograma(self, ctx:compiladoresParser.ProgramaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#instrucciones.
    def visitInstrucciones(self, ctx:compiladoresParser.InstruccionesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#instruccion.
    def visitInstruccion(self, ctx:compiladoresParser.InstruccionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#bloque.
    def visitBloque(self, ctx:compiladoresParser.BloqueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#declaracion.
    def visitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#definicion.
    def visitDefinicion(self, ctx:compiladoresParser.DefinicionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#lista_variables.
    def visitLista_variables(self, ctx:compiladoresParser.Lista_variablesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#tipo_dato.
    def visitTipo_dato(self, ctx:compiladoresParser.Tipo_datoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#asignacion.
    def visitAsignacion(self, ctx:compiladoresParser.AsignacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#opal.
    def visitOpal(self, ctx:compiladoresParser.OpalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#oplogicos.
    def visitOplogicos(self, ctx:compiladoresParser.OplogicosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#lor.
    def visitLor(self, ctx:compiladoresParser.LorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#logico.
    def visitLogico(self, ctx:compiladoresParser.LogicoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#land.
    def visitLand(self, ctx:compiladoresParser.LandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#conjunto.
    def visitConjunto(self, ctx:compiladoresParser.ConjuntoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#igualdad.
    def visitIgualdad(self, ctx:compiladoresParser.IgualdadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#c.
    def visitC(self, ctx:compiladoresParser.CContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#comparar.
    def visitComparar(self, ctx:compiladoresParser.CompararContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#exp.
    def visitExp(self, ctx:compiladoresParser.ExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#e.
    def visitE(self, ctx:compiladoresParser.EContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#term.
    def visitTerm(self, ctx:compiladoresParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#t.
    def visitT(self, ctx:compiladoresParser.TContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#factor.
    def visitFactor(self, ctx:compiladoresParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#iwhile.
    def visitIwhile(self, ctx:compiladoresParser.IwhileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#ifor.
    def visitIfor(self, ctx:compiladoresParser.IforContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#iif.
    def visitIif(self, ctx:compiladoresParser.IifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#ielse.
    def visitIelse(self, ctx:compiladoresParser.IelseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#init.
    def visitInit(self, ctx:compiladoresParser.InitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#cond.
    def visitCond(self, ctx:compiladoresParser.CondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#cond_for.
    def visitCond_for(self, ctx:compiladoresParser.Cond_forContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#iter.
    def visitIter(self, ctx:compiladoresParser.IterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#retornar.
    def visitRetornar(self, ctx:compiladoresParser.RetornarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#prototipo_funcion.
    def visitPrototipo_funcion(self, ctx:compiladoresParser.Prototipo_funcionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#funcion.
    def visitFuncion(self, ctx:compiladoresParser.FuncionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#valor_retorno.
    def visitValor_retorno(self, ctx:compiladoresParser.Valor_retornoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#argumentos.
    def visitArgumentos(self, ctx:compiladoresParser.ArgumentosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#lista_argumentos.
    def visitLista_argumentos(self, ctx:compiladoresParser.Lista_argumentosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#llamada_funcion.
    def visitLlamada_funcion(self, ctx:compiladoresParser.Llamada_funcionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#argumentos_a_funcion.
    def visitArgumentos_a_funcion(self, ctx:compiladoresParser.Argumentos_a_funcionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by compiladoresParser#lista_argumentos_a_funcion.
    def visitLista_argumentos_a_funcion(self, ctx:compiladoresParser.Lista_argumentos_a_funcionContext):
        return self.visitChildren(ctx)



del compiladoresParser