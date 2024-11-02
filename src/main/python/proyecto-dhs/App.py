
import sys
from antlr4 import *
from compiladoresLexer  import compiladoresLexer
from compiladoresParser import compiladoresParser
from MyListener import MyListener
from Walker import Walker

def main(argv):
    archivo = "input/programa.txt"
    if len(argv) > 1 :
        archivo = argv[1]
    input = FileStream(archivo)         # Entradas de Codigo Fuente
    lexer = compiladoresLexer(input)    # Analizador Lexico y consume los carecteres del codigo fuente
    stream = CommonTokenStream(lexer)   # Tokens (Secuencia)
    parser = compiladoresParser(stream) # Analizador Sintactico se alimenta con los tokens strings
    escucha = MyListener()              # Escucha eventos de arbol
    parser.addParseListener(escucha)    # Los eventos de arbol se los informo al parser
    tree = parser.programa()            # Empieza por la regla 'programa' (la raiz del arbol) y nos devuelve un arbol sintactico, el parser es el que dirige o guia

    # print(tree.toStringTree(recog=parser)) # arbol gramatical
 
    # caminante = Walker()                # Construye el objeto Visitor 
    # caminante.visitPrograma(tree)       # le pasa el arbol para que comience a caminar sobre el arbol terminado
 
if __name__ == '__main__':
    main(sys.argv)
