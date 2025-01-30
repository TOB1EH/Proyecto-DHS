import re


class Optimizador:
    """ 
        Clase dedicada a la optimizacion de codigo intermedio de tres direcciones.
    """

    def __init__(self):
        """ 
            Constructor de la Clase Optimizador.
        """

        self.origen     = open("output/codigoIntermedio.txt", "r") # archivo de codigo intermedio
        self.destino    = open("output/codigoIntermedioOptimizado.txt", "w+") # archivo de codigo optimizado
        self.acciones   = dict() # diccionario de acciones para evaluar acciones repetidas
        self.constantes = dict() # diccionario de constantes para evaluar la propagacion de constantes

    def optimizarCodigoIntermedio(self):
        """ 
            Funcion principal para comenzar a optimizar el codigo intermedio de tres direcciones.
        """

        print("Optimizando codigo intermedio...")

        self.reemplazoAccionesRepetidas()

        self.propagacionConstantes()

        # Cerrar los archivos
        self.origen.close()
        self.destino.close()

        print("Optimizacion de codigo intermedio completado.")

    def reemplazoAccionesRepetidas(self):
        """ 
            Metodo para reemplazar todas las acciones repetidas dentro del codigo intermedio
        """

        # Lee la primera linea del archivo 'origen'
        linea = self.origen.readline()


        # Continua leyendo hasta que la línea esté vacía (fin del archivo)
        while linea: # Procesar la linea
            
            # Verificar si la línea comienza con 't' seguido de un número (tX)
            if re.match(r'^t\d+ =', linea):

                # Dividir la línea en dos partes usando el signo igual
                partes = linea.split('=')

                # Optenemos cada parte de la linea sin espacios al inicio y al final
                clave = partes[1].strip()  # Accion u operacion
                valor = partes[0].strip()  # variable o identificador


                # Verificar si hay valores (acciones repetidas) a reemplazar en la clave 
                for getValor in self.acciones.values():
                    # Si el valor del diccionario es una lista, entonces hay acciones repetidas por reemplazar
                    if isinstance(getValor, list):
                        # Recorro la lista de valores con acciones repetidas
                        for ii in range(1, len(getValor)):  # Empezar desde 1 para evitar el primer valor
                            # Obtengo el valor que guarda la accion repetida
                            valor_a_reemplazar = getValor[ii]

                            # Si el valor esta dentro de la clave (accion) entonces lo reemplazo por el primer valor de la lista (que guarda la accion original)
                            if valor_a_reemplazar in clave:
                                clave = re.sub(r'\b{}\b'.format(re.escape(valor_a_reemplazar)), getValor[0], clave)
                                # clave = clave.replace(valor_a_reemplazar, getValor[0])
                            
                # Actualizar el diccionario self.acciones
                if clave in self.acciones:
                    self.acciones [clave].append(valor)
                else:
                    # Escribo en el diccionario la accion
                    self.acciones[clave] = [valor]

                    # Escribo en el archivo de destino el codigo optimizado
                    self.destino.write(f'{valor} = {clave}\n')
            
            else:
                partes = linea.split('=') # Dividir la línea en dos partes usando el signo igual

                if len(partes) == 2:
                    # Optenemos cada parte de la linea sin espacios al inicio y al final
                    identificador  = partes[0].strip()  
                    valor_asignado = partes[1].strip()  

                    # Verificar si hay valores (acciones repetidas) a reemplazar en la clave 
                    for getValor in self.acciones.values():
                        # Si el valor del diccionario es una lista, entonces hay acciones repetidas por reemplazar
                        if isinstance(getValor, list):
                            # Recorro la lista de valores con acciones repetidas
                            for ii in range(1, len(getValor)):  # Empezar desde 1 para evitar el primer valor
                                # Obtengo el valor que guarda la accion repetida
                                valor_a_reemplazar = getValor[ii]

                                # Si el valor esta dentro del valor asignado entonces lo reemplazo por el primer valor de la lista (que guarda la accion original)
                                if valor_a_reemplazar in valor_asignado:
                                    valor_asignado = re.sub(r'\b{}\b'.format(re.escape(valor_a_reemplazar)), getValor[0], valor_asignado)
                    
                    linea = f'{identificador} = {valor_asignado}\n'

                # Escribo en el archivo la linea actual
                self.destino.write(f'{linea}')
            
            # Leer la siguiente línea
            linea = self.origen.readline()

    def propagacionConstantes(self):
        """ 
            Leer el archivo sin acciones repetidas para aplicar propagacion de constantes.
        """

        self.destino.seek(0) # Vuelve al inicio del archivo para releerlo desde el principio.

        lineas = self.destino.readlines() # Leer todas las lineas del archivo
            
        self.destino.seek(0) # Vuelve al inicio del archivo para sobreescribirlo
    
        self.destino.truncate(0) # Limpia el archivo de destino antes de escribir en él.

        # Patrón para un identificador válido en C seguido de ' = ' y un número
        patron_identificador = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]* = \d+$')

        # patron_identificador_temporal  = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]* = t\d+$')
        
        # Patrón para un identificador válido en C seguido de ' = ' y una opercion de dos operandos
        patron_identificador_operacion = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]* = \d+(\.\d+)? [\+\-\*/] \d+(\.\d+)?$')

        # bandera que se activa cuando se modifica una linea
        hubo_cambios = False

        # Recorro el archivo (linea a linea) en busca de propagacion de constantes
        for linea in lineas:

            print(f"Procesando línea: {linea}")  # Línea de depuración

            # Verificar si la línea tiene el patrón identificador_espacio_igual_un_numero
            if patron_identificador.match(linea.strip()):
                # Obtener el identificador y el valor de la línea

                partes = linea.split('=') # Dividir la línea en dos partes usando el signo igual

                # Optenemos cada parte de la linea sin espacios al inicio y al final
                variable = partes[0].strip() # variable o identificador
                valor    = partes[1].strip() # valor u operacion asignada a la variable

                # Agrego al diccionario la variable asociado a su valor
                self.constantes[variable] = valor
                
                # Escribe en el archivo la asignacion directa
                self.destino.write(f'{variable} = {valor}\n')

            
            # Si es una asignacion de una operacion matematica
            elif patron_identificador_operacion.match(linea.strip()):
                # Obtener el identificador y la operación de la línea
                partes = linea.split('=') # Dividir la línea en dos partes usando el signo igual

                # Optenemos cada parte de la linea sin espacios al inicio y al final
                variable = partes[0].strip()
                operacion = partes[1].strip()

                try: 
                    # Evaluar la operacion matematica para obtener una constante como resultado
                    constante_resultante = eval(operacion)

                    # Si la variable no esta dentro de las constantes guardadas, o si hay que reemplazarla por una nueva
                    # if variable not in self.constantes or self.constantes[variable] != str(constante_resultante):
                    self.constantes[variable] = str(constante_resultante)
                    
                    # Como se modifica una linea activo la bandera
                    hubo_cambios = True
                    
                    print(f"Constante resultante asignada: {variable} = {constante_resultante}") # Línea de depuración

                # Si no se puede evaluar la operacion
                except Exception as e:
                    self.destino.write(f'{linea}\n')
                    print(f"Error evaluando operación: {e}")


            # En caso contrario, si hay una accion, busco si tiene una constante que debe ser reemplazada
            else:
                linea_original = linea
                # Reemplazar constantes en la linea
                if self.constantes:
                    
                    # Encontrar la posición del signo igual
                    igual_pos = linea.find('=')
                    
                    # Si en la linea existe una asignacion
                    if igual_pos != -1:

                        # Divido la linea en dos partes a partir del '='
                        izquierda = linea[:igual_pos + 1]
                        derecha = linea[igual_pos + 1:]

                        # derecha_copia = derecha

                        # Reemplazar la clave solo en la parte derecha
                        for clave, valor in self.constantes.items():
                            derecha = re.sub(r'\b{}\b'.format(re.escape(clave)), valor, derecha)
                            
    
                        # Concateno la nueva linea si hubo cambios o la restauro en caso de que no
                        linea = izquierda + derecha

                # Si la linea orignal fue modificada:
                if linea != linea_original:

                    hubo_cambios = True # Activo la bandera
                    
                    print(f"Línea modificada: {linea}") # Linea de depuracion
                
                self.destino.write(f'{linea}')

                

        # Si se modifico al menos una liena
        if hubo_cambios:
            print("Hubo cambios, llamando recursivamente a propagacionConstantes") # Línea de depuración
            self.propagacionConstantes() # Llamada recursiva
        else:
            print("No hubo cambios, finalizando propagacionConstantes") # Línea de depuración


""" 


x = (a * b - c) + (a * b + d)

// Codigo  de tres direcciones:
t0 =  a * b 
t1 = t0 - c
t2 = a * b   // Tengo operaciones repetidas
t3 = t2 + d
t4 = t1 + t3
x = t4

// Reemplazo de acciones repetidas:
t0 =  a * b 
t1 = t0 - c
t3 = t0 + d
t4 = t1 + t3  // En otra pasada podemos decir que estas ultimas dos instrucciones se plegan en una sola
x = t4


Propagación de constantes:

// Codigo en C
x = 5
y = x * 2 - 10
z = y + x;

// Codigo de tres direcciones
x = 5
t0 = x * 2
t1 = t0 - 10
y = t1
t2 = y + x
z = t2

// Propagacion de constantes
x = 5
t0 = 5 * 2
t1 = t0 - 10
y = t1
t2 = y + 5
z = t2

// En la siguiente pasada:
x = 5
t1 = 10 - 10
y = t1
t2 = y + 5
z = t2

// En la siguiente pasada:
x = 5
y = 0
t2 = y + 5
z = t2

// En la siguiente pasada:
x = 5
y = 0
z = 5

// Entonces la optimizacion lo resuelve y obtenemos, en este caso, asignaciones directas



 """