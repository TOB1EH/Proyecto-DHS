
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
    _temporales             = {}
    _temporales2            = []
    _etiquetas              = []
    _identificadores        = []
    flag_temporal = False
    generadorDeTemporales   = Temporal()


    terminos = ''

    flag_multi_div = False

    flag_2 = False

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
        if ctx.getChildCount() == 0:
            return
        
        self.visitInstruccion(ctx.getChild(0))
        self.visitInstrucciones(ctx.getChild(1))
            
    # Visit a parse tree produced by compiladoresParser#instruccion.
    def visitInstruccion(self, ctx:compiladoresParser.InstruccionContext):
        # Declaraciones
        if isinstance (ctx.getChild(0), compiladoresParser.DeclaracionContext):
            self.visitDeclaracion(ctx.getChild(0))
            
            if self.flag_multi_div is True:
                self.flag_2 = True
                self.visitDeclaracion(self.terminos)

                for clave, valor  in self._temporales.items():
                    self.file.write(clave + valor + '\n')

                self.file.write(self._temporales2.pop(0) + ' =' + self._instrucciones + '\n')
                self._temporales.clear()
                self._instrucciones = ''

                
            

            
            
            # if self.flag_temporal is True:
            #     self.file.write(self._temporales.pop(0) + ' =' + self._instrucciones + '\n')
            #     self._instrucciones = ''
            #     self.flag_temporal = False
            # else:
            #     self.file.write(self._identificadores.pop() + ' =' + self._instrucciones + '\n')
            #     self._instrucciones = ''

            # self._temporales.clear()
        
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
        if ctx.getChildCount() == 0:
            return

        self.terminos += (ctx.getChild(0).getText())

        self.visitTerm(ctx.getChild(1))
        self.visitE(ctx.getChild(2))

        # # Si previamente existe una multiplicacion/division
        # if self.flag_multi_div is True:
             
        if self.flag_2:
            if ctx.getChild(2).getChildCount() > 0:
                if self.flag_temporal is False:
                    self._temporales2.append(self.generadorDeTemporales.getTemporal())
                    self.flag_temporal = True
                else:
                    self._temporales2.append(self.generadorDeTemporales.getTemporal())
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

        # Si hay opUMEROeraciones de multiplicacion/division
        if ctx.getChild(1).getChildCount() > 0:
            
            self.flag_multi_div = True
            
            # Creamos un temporal para este termino
            self._temporales[self.generadorDeTemporales.getTemporal()] = None
            self._instrucciones += (' = ')
            self.visitFactor(ctx.getChild(0))
            
            # Visitamos las operaciones de multiplicacion/division
            self.visitT(ctx.getChild(1))
            
            self._temporales[-1] = self._instrucciones
            self._instrucciones = ''

            # Habria que encontrar una forma de guardar el termino
            self.terminos += (self._temporales[-1])
        else:
            self.visitFactor(ctx.getChild(0))
            self.terminos += (self._instrucciones)
            self._instrucciones = ''
        return

    # Visit a parse tree produced by compiladoresParser#factor.
    def visitFactor(self, ctx:compiladoresParser.FactorContext):
        if ctx.getChildCount() == 1:
            self._instrucciones += ' ' + ctx.getChild(0).getText()

    # Visit a parse tree produced by compiladoresParser#t.
    def visitT(self, ctx:compiladoresParser.TContext):
        """ 
            int c = 1 + b * a - w / 2 + 3;
            string str = term + term - term + term;
                t0 = b * a;
                t1 = w / 2;

            string str = 1 + t0 - t1 + 3;
            t2 = 1 + t0;
            t3 = t2 - t1;
            c = t3 + 3;


            Esto es lo que escribo finalmente en el archivo:
            t0 = b * a;
            t1 = w / 2;
            t2 = 1 + t0;
            t3 = t2 - t1;
            c = t3 + 3;
        
        """
        
        
        
        if ctx.getChildCount() == 0:
            return
        
        # Agregamos el operador (* o /)
        self._instrucciones += ' ' + ctx.getChild(0).getText() + ''

        # Visitamos el siguiente factor
        self.visitFactor(ctx.getChild(1))





        # Si hay mas operaciones de multiplicacion/division
        if ctx.getChild(2).getChildCount() > 0:
            if self.flag_temporal is False:
                self._temporales.append(self.generadorDeTemporales.getTemporal())
                self.flag_temporal = True
            else:
                self._temporales.append(self.generadorDeTemporales.getTemporal())
                self._instrucciones += ('\n' + self._temporales[-1] + ' = ' + self._temporales[-2])
        
            # Continuamos con las operaciones siguientes
            self.visitT(ctx.getChild(2))

        else:
            if self.flag_temporal is True:
                self._instrucciones += ('\n' + self._identificadores[-1] + ' = ' + self._temporales[-1])
        
        # self._instrucciones += (' ' + ctx.getChild(0).getText()) # Agrega el operador (+ o -)
        return
    
    # Visit a parse tree produced by compiladoresParser#asignacion.
    def visitAsignacion(self, ctx:compiladoresParser.AsignacionContext):
        self._instrucciones += (ctx.getChild(0).getText() + ' ' + ctx.getChild(1).getText())
        self.visitOpal(ctx.getChild(2))
        # Cuando la asignacion no es directa (uso temporales)
        return