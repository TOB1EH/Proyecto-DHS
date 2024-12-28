from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser

class Temporal():
    def __init__(self):
        self.contador = -1
    
    def getTemporal(self):
        self.contador += 1
        return f't{self.contador}'

class MyVisitor(compiladoresVisitor):
    def __init__(self):
        self._instrucciones = ''
        self._temporales = []
        self._identificadores = []
        self._temporal_actual = None
        self.generadorDeTemporales = Temporal()

    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("-" + "=" * 30 + "-")
        print("-- Comienza a generar Codigo Intermedio --")
        self.file = open("./output/codigoIntermedio.txt", "w")

        self.visitInstrucciones(ctx.getChild(0))

        self.file.close()
        print("-- Codigo Intermedio generado Correctamente --")
        print("-" + "=" * 30 + "-")

    def visitExp(self, ctx:compiladoresParser.ExpContext):
        # Visitamos el primer término
        self.visitTerm(ctx.getChild(0))
        primer_operando = self._temporal_actual or ctx.getChild(0).getText()
        
        # Si hay más operaciones (E no está vacío)
        if ctx.getChild(1).getChildCount() > 0:
            self._temporal_actual = self.generadorDeTemporales.getTemporal()
            self.visitE(ctx.getChild(1), primer_operando)
        
        return self._temporal_actual

    def visitE(self, ctx:compiladoresParser.EContext, operando_izq):
        if ctx.getChildCount() == 0:
            return
        
        # Obtenemos el operador
        operador = ctx.getChild(0).getText()
        
        # Visitamos el siguiente término
        self.visitTerm(ctx.getChild(1))
        operando_der = self._temporal_actual or ctx.getChild(1).getText()
        
        # Generamos la instrucción de tres direcciones
        nuevo_temporal = self.generadorDeTemporales.getTemporal()
        self.file.write(f"{nuevo_temporal} = {operando_izq} {operador} {operando_der}\n")
        
        # Actualizamos el temporal actual
        self._temporal_actual = nuevo_temporal
        
        # Continuamos con la siguiente operación si existe
        if ctx.getChild(2).getChildCount() > 0:
            self.visitE(ctx.getChild(2), nuevo_temporal)

    def visitAsignacion(self, ctx:compiladoresParser.AsignacionContext):
        identificador = ctx.getChild(0).getText()
        
        # Visitamos la expresión del lado derecho
        self.visitOpal(ctx.getChild(2))
        
        # Si hay un temporal actual, significa que hubo operaciones intermedias
        if self._temporal_actual:
            self.file.write(f"{identificador} = {self._temporal_actual}\n")
        else:
            # Si no hay temporal, es una asignación directa
            valor = ctx.getChild(2).getText()
            self.file.write(f"{identificador} = {valor}\n")
        
        self._temporal_actual = None

    def visitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        identificador = ctx.getChild(1).getText()
        
        # Si hay una definición (inicialización)
        if ctx.getChild(2).getChildCount() > 0:
            self.visitDefinicion(ctx.getChild(2))
            
            # Si hay un temporal actual, significa que hubo operaciones intermedias
            if self._temporal_actual:
                self.file.write(f"{identificador} = {self._temporal_actual}\n")
            
        self._temporal_actual = None
