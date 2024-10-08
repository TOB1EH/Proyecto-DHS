
from antlr4 import ErrorNode, TerminalNode
from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser

# Escuchar eventos de arboles, solo escucha eventos que me interesan    
class Escucha (compiladoresListener) :
    numTokens = 0
    numNodos = 0

    # Enter a parse tree produced by compiladoresParser#programa.
    def enterPrograma(self, ctx:compiladoresParser.ProgramaContext):
        print("Comienza la Compilacion")

    # Exit a parse tree produced by compiladoresParser#programa.
    def exitPrograma(self, ctx:compiladoresParser.ProgramaContext):
        print("FIn de la Compilacion")
        print("Se encontraron:")
        print("\tNodos: " + str(self.numNodos))
        print("\tTokens: " + str(self.numTokens))

    # Enter a parse tree produced by compiladoresParser#iwhile.
    def enterIwhile(self, ctx:compiladoresParser.IwhileContext):
        print("Encontre WHILE")
        print("\tCantidad de hijos: " + str(ctx.getChildCount()))
        print("\tTokens: " + ctx.getText())

    # Exit a parse tree produced by compiladoresParser#iwhile.
    def exitIwhile(self, ctx:compiladoresParser.IwhileContext):
        print("Fin del WHILE")
        print("\tCantidad de hijos: " + str(ctx.getChildCount()))
        print("\tTokens: " + ctx.getText())

    # Enter a parse tree produced by compiladoresParser#declaracion.
    def enterDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        print(" ### Declaracion")

    # Exit a parse tree produced by compiladoresParser#declaracion.
    def exitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        print("Nombre variable: " + ctx.getChild(1).getText())

    def visitTerminal(self, node: TerminalNode):
        # print(" ---> Token: " + node.getText())
        self.numTokens += 1

    def visitErrorNode(self, node: ErrorNode):
        print(" ---> ERROR")

    def enterEveryRule(self, ctx):
        self.numNodos += 1