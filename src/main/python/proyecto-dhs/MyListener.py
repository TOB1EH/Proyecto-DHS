from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser
from TablaSimbolos import TablaSimbolos
from Contexto import Contexto
from Variable import Variable
# from ID import ID, TipoDato

class MyListener (compiladoresListener):
    tabla_simbolos = TablaSimbolos()

    def enterPrograma(self, ctx:compiladoresParser.ProgramaContext):
        print("Comienza la Compilacion")

    def exitPrograma(self, ctx:compiladoresParser.ProgramaContext):
        print("Fin de la Compilacion")

    def enterBloque(self, ctx:compiladoresParser.BloqueContext):
        # Crea un nuevo Contexto
        nuevo_contexto = Contexto()
        # Añade un nuevo Contexto a la tabla de simbolos
        self.tabla_simbolos.addContexto(nuevo_contexto)

    # Sale de un contexto
    def exitBloque(self, ctx:compiladoresParser.BloqueContext):
        # Borra el contexto actual
        self.tabla_simbolos.delContexto()

    # Enter a parse tree produced by compiladoresParser#declaracion.
    def enterDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        pass

    # Exit a parse tree produced by compiladoresParser#declaracion.
    def exitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        tipo_dato = str(ctx.getChild(0).getText())

        nombre = str(ctx.getChild(1).getText())

        variable = Variable(nombre, tipo_dato)
        
        self.tabla_simbolos.addIdentificador(variable)

        print("Nueva variable:", "'" + variable.nombre + "'", "agregada.\n")
    