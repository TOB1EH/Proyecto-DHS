grammar compiladores;

fragment LETRA : [A-Za-z] ;
fragment DIGITO : [0-9] ;

// TOKENS o LITERALES o PALABRAS DEL LENGUAJE o 'HOJA'
PA   : '(' ;
PC   : ')' ;
LLA  : '{' ;
LLC  : '}' ;
CA   : '[' ;
CC   : ']' ;
PYC  : ';' ;
COMA : ',' ;

// Operaciones logicas
LNOT : '!'  ;
LAND : '&&' ;
LOR  : '||' ;

// Operaciones
ASIG  : '=' ;
SUMA  : '+' ;
RESTA : '-' ;
MULTI : '*' ;
DIVI  : '/' ;
MOD   : '%' ;

// Operadores de igualdad
IGUAL   : '==' ;
NIGUAL  : '!=' ;

// Operadores relacionales 
MAYOR      : '>' ;
MENOR      : '<' ;
MAYORIGUAL : '>=' ;
MENORIGUAL : '<=' ;

// Operadores bit a bit
AND : '&' ;
OR  : '|' ;
NOT : '~' ;
XOR : '^' ;

// Incrementos y Decrementos
INC : '++' ;
DEC : '--' ;

// PALABRAS RESERVADAS DEL LENGUAJE:
WHILE  : 'while' ;
FOR    : 'for' ;
IF     : 'if' ;
ELSE   : 'else' ;
RETURN : 'return' ;

// Tipos de datos de variables
INT     : 'int' ; // lo trataremos como una palabra reservada
FLOAT   : 'float' ;
DOUBLE  : 'double' ;
CHAR    : 'char' ;

// Ignorar espacios en blanco y comentarios
WS : [ \t\n\r] -> skip ;
LINE_COMMENT : '//' ~[\r\n]* -> skip ;
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;

NUMERO : DIGITO+ ;

ID : (LETRA | '_')(LETRA | DIGITO | '_')* ;

OTRO : . ;


// PROGRAMA de Reglas Gramaticales:
programa : instrucciones EOF ;

instrucciones : instruccion instrucciones
              |
              ;

instruccion : declaracion PYC
            | asignacion PYC
            | iwhile
            | ifor
            | iif
            | ielse
            | bloque
            ;

// BLoque de instrucciones entre llaves
bloque : LLA instrucciones LLC ;

// Declaracion de variables
declaracion : INT ID d ;

d : ASIG opal lista_variables
  | lista_variables 
  ;

lista_variables : COMA ID d
                |
                ;

// Asignacion o inicializacion de variables o valores 
asignacion : ID ASIG opal ;

// OPERACIONES ARITMETICAS Y LOGICAS
opal : oplogicos ;

// Operaciones Logicas

oplogicos : logico lor ;

lor : LOR logico lor // Operador logico OR
    |
    ;

logico : conjunto land;

land : LAND conjunto land // Operador logico AND
     |
     ;

// Comparaciones
conjunto : c igualdad ;

igualdad : IGUAL  c igualdad
         | NIGUAL c igualdad
         |
         ;

c : exp comparar ;

comparar : MAYORIGUAL exp comparar
         | MENORIGUAL exp comparar
         | MAYOR      exp comparar
         | MENOR      exp comparar
         |
         ;

// Operaciones Aritmeticas

exp : term e ; // Expresion

// Expresion prima
e : SUMA term e
  | RESTA term e
  |
  ;

// Termino de la expresiom
term : factor t ;

// termino prima
t : MULTI factor t
  | DIVI  factor t
  | MOD   factor t
  |
  ;

// Un factor del termino 
factor : LNOT factor 
       | NUMERO
       | ID
       | PA oplogicos PC // Sabe que tiene que resolver esto primero por la profundidad del arbol
       ;

// Bucle while
iwhile : WHILE PA cond PC instruccion ;

// Bucle for
ifor : FOR PA init PYC cond PYC iter PC instruccion ;

// Condicional if
iif : IF PA cond PC instruccion ;

// Condicional else
ielse : iif ELSE instruccion ;

// Inicializacion
init : asignacion
     | declaracion
     ;

// Condicion del for
cond : oplogicos ;

// Expresion de actualizacion o iterador
iter : ID INC
     | ID DEC
     | INC ID 
     | DEC ID
     | asignacion
     ;
