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
        self.destino    = open("output/codigoIntermedioOptimizado.txt", "w") # archivo de codigo optimizado
        self.acciones   = dict() # diccionario de acciones para evaluar acciones repetidas
        self.constantes = dict() # diccionario de constantes para evaluar la propagacion de constantes

    def optimizarCodigoIntemedio(self):
        """ 
            Funcion principal para comenzar a optimizar el codigo intermedio de tres direcciones.
        """

        print("Optimizando codigo intermedio...")

        self.reemplazoAccionesRepetidas()


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

                # Eliminar los espacios en blanco innecesarios
                clave = partes[1].strip()  # 'a * b'
                valor = partes[0].strip()  # 't0'


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
                                clave = clave.replace(valor_a_reemplazar, getValor[0])
                            
                # Actualizar el diccionario self.acciones
                if clave in self.acciones:
                    self.acciones [clave].append(valor)
                else:
                    # Escribo en el diccionario la accion
                    self.acciones[clave] = [valor]

                    # Escribo en el archivo de destino el codigo optimizado
                    self.destino.write(f'{valor} = {clave}\n')
            
            else:
                # Resolver con propagacion de constantes
                self.destino.write(f'{linea}')
            
            # Leer la siguiente línea
            linea = self.origen.readline()



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

x = 5
y = x * 2 - 10
z = y + x;

// Codigo de tres direcciones
x = 5
t0 = x * 2
t1 = t0 - 1'
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