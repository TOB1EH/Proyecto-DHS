# Generated from /home/tobias/Documents/workspace/Proyectos-DHS/proyecto-dhs/src/main/python/compiladores/compiladores.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .compiladoresParser import compiladoresParser
else:
    from compiladoresParser import compiladoresParser

# This class defines a complete listener for a parse tree produced by compiladoresParser.
class compiladoresListener(ParseTreeListener):

    # Enter a parse tree produced by compiladoresParser#programa.
    def enterPrograma(self, ctx:compiladoresParser.ProgramaContext):
        pass

    # Exit a parse tree produced by compiladoresParser#programa.
    def exitPrograma(self, ctx:compiladoresParser.ProgramaContext):
        pass


    # Enter a parse tree produced by compiladoresParser#instrucciones.
    def enterInstrucciones(self, ctx:compiladoresParser.InstruccionesContext):
        pass

    # Exit a parse tree produced by compiladoresParser#instrucciones.
    def exitInstrucciones(self, ctx:compiladoresParser.InstruccionesContext):
        pass


    # Enter a parse tree produced by compiladoresParser#instruccion.
    def enterInstruccion(self, ctx:compiladoresParser.InstruccionContext):
        pass

    # Exit a parse tree produced by compiladoresParser#instruccion.
    def exitInstruccion(self, ctx:compiladoresParser.InstruccionContext):
        pass


    # Enter a parse tree produced by compiladoresParser#bloque.
    def enterBloque(self, ctx:compiladoresParser.BloqueContext):
        pass

    # Exit a parse tree produced by compiladoresParser#bloque.
    def exitBloque(self, ctx:compiladoresParser.BloqueContext):
        pass


    # Enter a parse tree produced by compiladoresParser#declaracion.
    def enterDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        pass

    # Exit a parse tree produced by compiladoresParser#declaracion.
    def exitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        pass


    # Enter a parse tree produced by compiladoresParser#definicion.
    def enterDefinicion(self, ctx:compiladoresParser.DefinicionContext):
        pass

    # Exit a parse tree produced by compiladoresParser#definicion.
    def exitDefinicion(self, ctx:compiladoresParser.DefinicionContext):
        pass


    # Enter a parse tree produced by compiladoresParser#lista_variables.
    def enterLista_variables(self, ctx:compiladoresParser.Lista_variablesContext):
        pass

    # Exit a parse tree produced by compiladoresParser#lista_variables.
    def exitLista_variables(self, ctx:compiladoresParser.Lista_variablesContext):
        pass


    # Enter a parse tree produced by compiladoresParser#tipo_dato.
    def enterTipo_dato(self, ctx:compiladoresParser.Tipo_datoContext):
        pass

    # Exit a parse tree produced by compiladoresParser#tipo_dato.
    def exitTipo_dato(self, ctx:compiladoresParser.Tipo_datoContext):
        pass


    # Enter a parse tree produced by compiladoresParser#asignacion.
    def enterAsignacion(self, ctx:compiladoresParser.AsignacionContext):
        pass

    # Exit a parse tree produced by compiladoresParser#asignacion.
    def exitAsignacion(self, ctx:compiladoresParser.AsignacionContext):
        pass


    # Enter a parse tree produced by compiladoresParser#opal.
    def enterOpal(self, ctx:compiladoresParser.OpalContext):
        pass

    # Exit a parse tree produced by compiladoresParser#opal.
    def exitOpal(self, ctx:compiladoresParser.OpalContext):
        pass


    # Enter a parse tree produced by compiladoresParser#oplogicos.
    def enterOplogicos(self, ctx:compiladoresParser.OplogicosContext):
        pass

    # Exit a parse tree produced by compiladoresParser#oplogicos.
    def exitOplogicos(self, ctx:compiladoresParser.OplogicosContext):
        pass


    # Enter a parse tree produced by compiladoresParser#lor.
    def enterLor(self, ctx:compiladoresParser.LorContext):
        pass

    # Exit a parse tree produced by compiladoresParser#lor.
    def exitLor(self, ctx:compiladoresParser.LorContext):
        pass


    # Enter a parse tree produced by compiladoresParser#logico.
    def enterLogico(self, ctx:compiladoresParser.LogicoContext):
        pass

    # Exit a parse tree produced by compiladoresParser#logico.
    def exitLogico(self, ctx:compiladoresParser.LogicoContext):
        pass


    # Enter a parse tree produced by compiladoresParser#land.
    def enterLand(self, ctx:compiladoresParser.LandContext):
        pass

    # Exit a parse tree produced by compiladoresParser#land.
    def exitLand(self, ctx:compiladoresParser.LandContext):
        pass


    # Enter a parse tree produced by compiladoresParser#conjunto.
    def enterConjunto(self, ctx:compiladoresParser.ConjuntoContext):
        pass

    # Exit a parse tree produced by compiladoresParser#conjunto.
    def exitConjunto(self, ctx:compiladoresParser.ConjuntoContext):
        pass


    # Enter a parse tree produced by compiladoresParser#igualdad.
    def enterIgualdad(self, ctx:compiladoresParser.IgualdadContext):
        pass

    # Exit a parse tree produced by compiladoresParser#igualdad.
    def exitIgualdad(self, ctx:compiladoresParser.IgualdadContext):
        pass


    # Enter a parse tree produced by compiladoresParser#c.
    def enterC(self, ctx:compiladoresParser.CContext):
        pass

    # Exit a parse tree produced by compiladoresParser#c.
    def exitC(self, ctx:compiladoresParser.CContext):
        pass


    # Enter a parse tree produced by compiladoresParser#comparar.
    def enterComparar(self, ctx:compiladoresParser.CompararContext):
        pass

    # Exit a parse tree produced by compiladoresParser#comparar.
    def exitComparar(self, ctx:compiladoresParser.CompararContext):
        pass


    # Enter a parse tree produced by compiladoresParser#exp.
    def enterExp(self, ctx:compiladoresParser.ExpContext):
        pass

    # Exit a parse tree produced by compiladoresParser#exp.
    def exitExp(self, ctx:compiladoresParser.ExpContext):
        pass


    # Enter a parse tree produced by compiladoresParser#e.
    def enterE(self, ctx:compiladoresParser.EContext):
        pass

    # Exit a parse tree produced by compiladoresParser#e.
    def exitE(self, ctx:compiladoresParser.EContext):
        pass


    # Enter a parse tree produced by compiladoresParser#term.
    def enterTerm(self, ctx:compiladoresParser.TermContext):
        pass

    # Exit a parse tree produced by compiladoresParser#term.
    def exitTerm(self, ctx:compiladoresParser.TermContext):
        pass


    # Enter a parse tree produced by compiladoresParser#t.
    def enterT(self, ctx:compiladoresParser.TContext):
        pass

    # Exit a parse tree produced by compiladoresParser#t.
    def exitT(self, ctx:compiladoresParser.TContext):
        pass


    # Enter a parse tree produced by compiladoresParser#factor.
    def enterFactor(self, ctx:compiladoresParser.FactorContext):
        pass

    # Exit a parse tree produced by compiladoresParser#factor.
    def exitFactor(self, ctx:compiladoresParser.FactorContext):
        pass


    # Enter a parse tree produced by compiladoresParser#iwhile.
    def enterIwhile(self, ctx:compiladoresParser.IwhileContext):
        pass

    # Exit a parse tree produced by compiladoresParser#iwhile.
    def exitIwhile(self, ctx:compiladoresParser.IwhileContext):
        pass


    # Enter a parse tree produced by compiladoresParser#ifor.
    def enterIfor(self, ctx:compiladoresParser.IforContext):
        pass

    # Exit a parse tree produced by compiladoresParser#ifor.
    def exitIfor(self, ctx:compiladoresParser.IforContext):
        pass


    # Enter a parse tree produced by compiladoresParser#iif.
    def enterIif(self, ctx:compiladoresParser.IifContext):
        pass

    # Exit a parse tree produced by compiladoresParser#iif.
    def exitIif(self, ctx:compiladoresParser.IifContext):
        pass


    # Enter a parse tree produced by compiladoresParser#ielse.
    def enterIelse(self, ctx:compiladoresParser.IelseContext):
        pass

    # Exit a parse tree produced by compiladoresParser#ielse.
    def exitIelse(self, ctx:compiladoresParser.IelseContext):
        pass


    # Enter a parse tree produced by compiladoresParser#init.
    def enterInit(self, ctx:compiladoresParser.InitContext):
        pass

    # Exit a parse tree produced by compiladoresParser#init.
    def exitInit(self, ctx:compiladoresParser.InitContext):
        pass


    # Enter a parse tree produced by compiladoresParser#cond.
    def enterCond(self, ctx:compiladoresParser.CondContext):
        pass

    # Exit a parse tree produced by compiladoresParser#cond.
    def exitCond(self, ctx:compiladoresParser.CondContext):
        pass


    # Enter a parse tree produced by compiladoresParser#cond_for.
    def enterCond_for(self, ctx:compiladoresParser.Cond_forContext):
        pass

    # Exit a parse tree produced by compiladoresParser#cond_for.
    def exitCond_for(self, ctx:compiladoresParser.Cond_forContext):
        pass


    # Enter a parse tree produced by compiladoresParser#iter.
    def enterIter(self, ctx:compiladoresParser.IterContext):
        pass

    # Exit a parse tree produced by compiladoresParser#iter.
    def exitIter(self, ctx:compiladoresParser.IterContext):
        pass


    # Enter a parse tree produced by compiladoresParser#retornar.
    def enterRetornar(self, ctx:compiladoresParser.RetornarContext):
        pass

    # Exit a parse tree produced by compiladoresParser#retornar.
    def exitRetornar(self, ctx:compiladoresParser.RetornarContext):
        pass


    # Enter a parse tree produced by compiladoresParser#prototipo_funcion.
    def enterPrototipo_funcion(self, ctx:compiladoresParser.Prototipo_funcionContext):
        pass

    # Exit a parse tree produced by compiladoresParser#prototipo_funcion.
    def exitPrototipo_funcion(self, ctx:compiladoresParser.Prototipo_funcionContext):
        pass


    # Enter a parse tree produced by compiladoresParser#funcion.
    def enterFuncion(self, ctx:compiladoresParser.FuncionContext):
        pass

    # Exit a parse tree produced by compiladoresParser#funcion.
    def exitFuncion(self, ctx:compiladoresParser.FuncionContext):
        pass


    # Enter a parse tree produced by compiladoresParser#valor_retorno.
    def enterValor_retorno(self, ctx:compiladoresParser.Valor_retornoContext):
        pass

    # Exit a parse tree produced by compiladoresParser#valor_retorno.
    def exitValor_retorno(self, ctx:compiladoresParser.Valor_retornoContext):
        pass


    # Enter a parse tree produced by compiladoresParser#argumentos.
    def enterArgumentos(self, ctx:compiladoresParser.ArgumentosContext):
        pass

    # Exit a parse tree produced by compiladoresParser#argumentos.
    def exitArgumentos(self, ctx:compiladoresParser.ArgumentosContext):
        pass


    # Enter a parse tree produced by compiladoresParser#lista_argumentos.
    def enterLista_argumentos(self, ctx:compiladoresParser.Lista_argumentosContext):
        pass

    # Exit a parse tree produced by compiladoresParser#lista_argumentos.
    def exitLista_argumentos(self, ctx:compiladoresParser.Lista_argumentosContext):
        pass


    # Enter a parse tree produced by compiladoresParser#llamada_funcion.
    def enterLlamada_funcion(self, ctx:compiladoresParser.Llamada_funcionContext):
        pass

    # Exit a parse tree produced by compiladoresParser#llamada_funcion.
    def exitLlamada_funcion(self, ctx:compiladoresParser.Llamada_funcionContext):
        pass


    # Enter a parse tree produced by compiladoresParser#argumentos_a_funcion.
    def enterArgumentos_a_funcion(self, ctx:compiladoresParser.Argumentos_a_funcionContext):
        pass

    # Exit a parse tree produced by compiladoresParser#argumentos_a_funcion.
    def exitArgumentos_a_funcion(self, ctx:compiladoresParser.Argumentos_a_funcionContext):
        pass


    # Enter a parse tree produced by compiladoresParser#lista_argumentos_a_funcion.
    def enterLista_argumentos_a_funcion(self, ctx:compiladoresParser.Lista_argumentos_a_funcionContext):
        pass

    # Exit a parse tree produced by compiladoresParser#lista_argumentos_a_funcion.
    def exitLista_argumentos_a_funcion(self, ctx:compiladoresParser.Lista_argumentos_a_funcionContext):
        pass



del compiladoresParser