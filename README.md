# Proyecto-DHS: Compilador de C Básico

Compilador de C básico desarrollado en Python como proyecto final para la materia 'Desarrollo de Herramientas de Software' de la carrera de Ingeniería en Informática.

## Tabla de Contenidos
- [Descripción](#descripción)
- [Características](#características)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Contacto](#contacto)

## Descripción
Proyecto-DHS es un compilador de C básico implementado en Python. El objetivo principal de este proyecto es servir como herramienta educativa para aprender sobre el proceso de compilación y la implementación de compiladores.

## Características
- **Análisis Léxico:** Utiliza ANTLR para generar el analizador léxico.
- **Análisis Sintáctico:** Implementación de un analizador sintáctico para el lenguaje C.
- **Generación de Código Intermedio:** Conversión del código fuente en una representación intermedia, en este caso Codigo de Tres direcciones.
- **Soporte para Expresiones y Sentencias Básicas:** Capacidad para compilar expresiones aritméticas y sentencias de control básicas.

## Estructura del Proyecto

El repositorio está organizado en varias carpetas y archivos, cada uno con un propósito específico:

### 1. **Carpeta `input/`**
Esta carpeta contiene archivos de entrada que son utilizados por el sistema para realizar análisis. Los archivos incluyen:

- `entrada.txt`: Archivo de texto con datos de entrada.
- `errores.c`: Código fuente en C que puede contener errores para ser analizados.
- `opal.txt`: Otro archivo de entrada que puede ser utilizado para pruebas.
- `parentesis.txt`: Archivo que probablemente contiene datos relacionados con la validación de paréntesis.
- `programa.txt`: Archivo que contiene un programa de ejemplo para análisis.
- `prueba.c`: Código fuente en C para pruebas.
- `prueba2.c`: Otro archivo de código fuente para pruebas.

### 2. **Carpeta `output/`**
Esta carpeta almacena los resultados generados por el sistema después de realizar análisis sobre los archivos de entrada. Los archivos incluyen:

- `codigoIntermedio.txt`: Contiene el código intermedio generado durante el análisis.
- `codigoIntermedioOptimizado.txt`: Versión optimizada del código intermedio.

### 3. **Carpeta `src/`**
La carpeta `src/` contiene el código fuente del proyecto, organizado en subcarpetas:

- **`main/python/`**: Contiene los scripts principales escritos en Python.
  - **`Componentes/`**: Subcarpeta que incluye varios módulos que forman parte del sistema, tales como:
    - `Contexto.py`: Maneja el contexto del análisis.
    - `Funcion.py`: Contiene funciones utilizadas en el análisis.
    - `ID.py`: Maneja identificadores en el código.
    - `Optimizador.py`: Implementa algoritmos de optimización.
    - `TablaSimbolos.py`: Maneja la tabla de símbolos utilizada en el análisis.
    - `MyListener.py` y `MyVisitor.py`: Implementan patrones de diseño para el análisis de código.
    - `compiladores.g4`: Archivo de gramática utilizado por ANTLR para el análisis sintáctico.

### 4. **Archivos de Configuración**
- `pom.xml`: Archivo de configuración para proyectos de Java, que puede ser utilizado para gestionar dependencias y configuraciones del proyecto.

### 5. **Documentación**
- `README.md`: Este archivo proporciona una descripción general del proyecto y su estructura.


## Requisitos
- Python 3.8 o superior
- ANTLR 4

## Instalación
1. Clona este repositorio en tu máquina local:
```sh
   git clone https://github.com/TOB1EH/Proyecto-DHS.git
```
2. Navega al directorio del proyecto:
```sh
    cd Proyecto-DHS
```

## Uso
Para utilizar el sistema, coloca tus archivos de entrada en la carpeta `input/` y ejecuta el script principal en `App.py` en la ruta `src/main/python/` Asegúrarse de que los archivos de entrada estén en el formato correcto para que el sistema pueda procesarlos adecuadamente.

## Contacto
Tobias Funes - tobiasfunes@hotmail.com.ar