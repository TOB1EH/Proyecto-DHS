import re

class Optimizador:
    """
    Clase que implementa la optimización de código intermedio de tres direcciones.
    Realiza dos tipos principales de optimizaciones:
    1. Eliminación de subexpresiones comunes (reemplazo de acciones repetidas)
    2. Propagación de constantes
    """

    def __init__(self):
        """
        Inicializa el optimizador abriendo los archivos de entrada y salida
        y creando las estructuras de datos necesarias para el seguimiento de variables
        """

        self.origen             = open("output/codigoIntermedio.txt", "r")              # Archivo de codigo intermedio
        self.destino            = open("output/codigoIntermedioOptimizado.txt", "w+")   # Archivo de codigo optimizado
        
        self.variables          = dict()    # Almacena el valor actual de las variables reales
        self.temporales         = dict()    # Almacena el valor de las variables temporales
        self.acciones           = dict()    # Mapea expresiones a sus variables temporales
        self.expresiones_temp   = dict()    # Almacena las expresiones originales de los temporales

    def es_temporal(self, variable):
        """
        Determina si una variable es temporal (t seguido de un número)
        
        Args:
            variable (str): Nombre de la variable a verificar
        
        Returns:
            bool: True si es una variable temporal, False en caso contrario
        """

        # Verifica si la variable comienza con 't' y sigue un número
        return bool(re.match(r'^t\d+$', variable))

    def es_linea_control(self, linea):
        """
        Determina si una línea es una instrucción de control de flujo
        
        Args:
            linea (str): Línea a verificar
        
        Returns:
            bool: True si es una instrucción de control, False en caso contrario
        """

        return (linea.startswith('label') or 
                linea.startswith('jmp') or 
                linea.startswith('ifnjmp') or 
                linea.startswith('ifjmp') or
                linea.startswith('pop') or
                linea.startswith('push'))

    def evaluar_expresion(self, expresion):
        """
        Evalúa una expresión reemplazando variables con sus valores actuales
        
        Args:
            expresion (str): Expresión a evaluar
        
        Returns:
            str: Resultado de la evaluación o None si no se puede evaluar
        """
        
        # Intenta evaluar la expresion
        try:
            # Primero reemplazar temporales
            for temp, valor in self.temporales.items():

                # Si existe un temporal en la expresion, lo reemplaza con su valor
                expresion = re.sub(r'\b{}\b'.format(re.escape(temp)), str(valor), expresion)
            # Luego reemplazar variables normales
            for var, valor in self.variables.items():

                # Si existe una variableen la expresion, lo reemplaza con su valor constante
                expresion = re.sub(r'\b{}\b'.format(re.escape(var)), str(valor), expresion)
            
            # Devuelve la expresion evaluada, es decir, la resuelve matematicamente
            return eval(expresion)
        except Exception as e:
            print("Error al evaluar la expresion: ", str(e))
            # Si no se puede evaluar, devuelve None
            return None

    def obtener_expresion_temporal(self, temp):
        """
        Obtiene la expresión original de una variable temporal
        y la simplifica si es posible
        
        Args:
            temp (str): Variable temporal
            
        Returns:
            str: Expresión simplificada o la original si no se puede simplificar
        """
        
        # Si el temporal esta dentro de mi lista de expresiones con temporales
        if temp in self.expresiones_temp:
            # Obtener la expresión original
            expresion = self.expresiones_temp[temp]
            
            # Intentar evaluar la expresión 
            resultado = self.evaluar_expresion(expresion)

            # Si el resultado no es None, retorno la expresion resuelta
            if resultado is not None:
                return str(resultado)
            # Si no se puede evaluar, retorno la expresion original
            return expresion
        
        # Si no esta en la lista, retorno el temporal
        return temp
    
    def optimizarCodigoIntermedio(self):
        """
        Método principal que coordina el proceso de optimización
        """
        
        print("Optimizando codigo intermedio...")
        
        # Primero, reemplazar acciones repetidas
        lineas_optimizadas = self.reemplazoAccionesRepetidas()
        
        # Por ultimo, propagacion de constantes a partir de las lineas sin acciones repetidas
        self.propagacionConstantes(lineas_optimizadas)
        
        # Cerrar los archivos
        self.origen.close()
        self.destino.close()
        
        print("Optimizacion de codigo intermedio completado.")


    def reemplazoAccionesRepetidas(self):
        """
        Primera fase de optimización: elimina subexpresiones comunes
        
        Returns:
            list: Lista de líneas después de eliminar acciones repetidas
        """
        
        # Obtengo todas las lineas del archivo y las guardo en una lista
        lineas = self.origen.readlines()

        # Creo una lista para guardar las lineas optimizadas
        lineas_optimizadas = []

        # Recorre todas las lineas del archivo (linea a linea)
        for linea in lineas:

            # Elimino los espacios al principio y al final de la linea
            linea = linea.strip()

            # Si la linea no está vacía
            if not linea:
                # Voy al siguiente ciclo del bucle
                continue

            # Preservar declaraciones y control de flujo
            if linea.startswith("Declaracion") or self.es_linea_control(linea):
                # Agrego la linea a la lista de lineas optimizadas
                lineas_optimizadas.append(linea)
                # Si la linea es una declaracion o una declaracion de flujo voy al siguiente ciclo
                continue

            # Divido la linea en partes a partir del igual
            partes = linea.split('=')
            if len(partes) != 2:
                # Si la linea no tiene un igual, voy al siguiente ciclo
                continue
            
            # En cambio, si la linea tiene un igual, estoy ante una asignacion
            
            # Obtengo la parte izquierda y derecha de la linea
            variable    = partes[0].strip() # Parte izquierda (variable o temporal)
            expresion   = partes[1].strip() # Parte derecha (expresion, accion o valor)

            # Guardar la expresión original para las variables temporales
            if self.es_temporal(variable):
                self.expresiones_temp[variable] = expresion

                # Si la expresión es una acción repetida, la elimino
                if expresion in self.acciones:
                    # Usar el temporal existente
                    variable = self.acciones[expresion]
                
                # En caso contrario, la agrego a la lista de acciones o expresiones
                else:
                    # Registrar nueva expresión
                    self.acciones[expresion] = variable

            # Sea el caso que sea, agrego la linea optimizada (o no) a la lista
            lineas_optimizadas.append(f"{variable} = {expresion}")

        # Cuando termina el bucle for, retorno la lista de las lienas_optimizadas obtenidas
        return lineas_optimizadas

    def propagacionConstantes(self, lineas):
        """
        Segunda fase de optimización: propaga constantes y genera código final
        
        Args:
            lineas (list): Lista de líneas después del reemplazo de acciones repetidas
        """

        # Recorro las lineas optimizadas obtenidas anteriormente
        for linea in lineas:
            # Preservar declaraciones y control de flujo
            if linea.startswith("Declaracion") or self.es_linea_control(linea):
                # Si la linea es una declaracion o una declaracion de flujo voy al siguiente ciclo y la dejo como esta
                self.destino.write(f'{linea}\n')
                continue
            
            # Divido la linea en partes a partir del igual
            partes = linea.split('=')

            # Si la linea no tiene un igual, voy al siguiente ciclo
            if len(partes) != 2:
                continue

            # En cambio, si la linea tiene un igual, estoy ante una asignacion
            
            # Obtengo la parte izquierda y derecha de la linea
            variable    = partes[0].strip() # Parte izquierda (variable o temporal)
            expresion   = partes[1].strip() # Parte derecha (expresion, accion o valor)

            # Si la expresión contiene un temporal, obtener su expresión original
            if self.es_temporal(expresion.strip()):
                expresion = self.obtener_expresion_temporal(expresion.strip())

            # Evaluar la expresión
            resultado = self.evaluar_expresion(expresion)

            # Si se pudo evaluar la expresion
            if resultado is not None:
                # Determina si la variable en la linea es un temporal
                if self.es_temporal(variable):
                    # Si es un temporal, reemplazo su valor por el resultado de la expresion, en mi lista de temporales
                    self.temporales[variable] = str(resultado)
                else:
                    # Si no es un temporal, entonces es una variable
                    self.variables[variable] = str(resultado)

                    # Escribo la linea con el valor de la variable en el archivo
                    self.destino.write(f"{variable} = {resultado}\n\n")
            
            # De lo contrario, si no se pudo evaluar la expresion
            else:
                # Si la variable en la linea no es un temporal
                if not self.es_temporal(variable):
                    # Divide la expresion en subcadenas a partir de los espacios en blanco, y guarda las subcadenas en una lista
                    partes_expr = expresion.split()
                    
                    # Recorro las partes de la expresion
                    for i, parte in enumerate(partes_expr):
                        # Si la parte es un temporal
                        if self.es_temporal(parte):
                            # Reemplazo el temporal por el resultado de su expresion original
                            partes_expr[i] = self.obtener_expresion_temporal(parte)

                    # Despues de procesar todas las partes comienza la Reconstrucción y Escritura de la Expresión Final:
                    expresion_final = ' '.join(partes_expr)  # Se reconstruye la expresión completa uniendo las partes con espacios
                    
                    # Escribo en el archivo la variable con su expresion optimizada
                    self.destino.write(f"{variable} = {expresion_final}\n")