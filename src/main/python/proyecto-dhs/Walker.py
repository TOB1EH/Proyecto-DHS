
from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser

class Walker (compiladoresVisitor):
    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("-" + "=" * 30 + "-")
        print("-- Comienza a Caminar --")

        temp = super().visitPrograma(ctx)

        print("Puedo hacer lo que quiera luego de visitar el Programa")
        return None
    
    def visitDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
        # No accede mediante el 'super()' sino mediante el metodo para obtener los hijos (nodos del arbol)
        print(ctx.getChild(0).getText() + " - " +   # Quiero ver el tipo de dato
              ctx.getChild(1).getText())            # Quiero ver el ID

        # return super().visitDeclaracion(ctx)
        return None
    
    # def visitBloque(self, ctx: compiladoresParser.BloqueContext):
    #     print("Nuevo Contexto")
    #     print(ctx.getText())
    #     return super().visitInstrucciones(ctx.getChild(1))
    #     # return super().visitBloque(ctx)

    # def visitTerminal(self, node):
    #     print(" ==> Token " + node.getText())
    #     return super().visitTerminal(node)