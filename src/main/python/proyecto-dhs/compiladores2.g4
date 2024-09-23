// Una expresion regular es especificamente una secuencia de caracteres

// las palabras del legnuaje son secuencias de caracteres propios del funcionamiento del lenguaje

// el analizador lexico se construye a partir de expresiones regulares, y 
// tiene como objetivo enoontrar el patron de texto del leguaje y nos va a 
// devolver TOKENS indicando que tipo de secuencia es ese texto, en caso
// que haya algun error hay control de errores, que nos notofica al respecto


grammar compiladores;

fragment LETRA : [A-Za-z] ;
fragment DIGITO : [0-9] ;

// TOKENS o LITERALES o PALABRAS DEL LENGUAJE o 'HOJA'
PA : '(' ;
PC : ')' ;
LLA : '{' ;
LLC : '}' ;
CA : '[' ;
CC : ']' ;
PYC : ';' ;
COMA : ',' ;

// Operaciones
ASIG : '=' ;
SUMA : '+' ;
RESTA : '-' ;
MULTI : '*' ;
DIVI : '/' ;

// Comparaciones
IGUAL : '==' ;
NIGUAL : '!=' ;
MAYOR : '>' ;
MENOR : '<' ;
MAYORIGUAL : '>=' ;
MENORIGUAL : '<=' ;

// COMENTARIOS
ICOMEN : '/*' ;
FCOMEN : '*/' ;
COMEN : '//' ;

// PALABRAS RESERVADAS DEL LENGUAJE:
WHILE : 'while' ;
FOR : 'for' ;
IF : 'if' ;
ELSE : 'else' ;
RETURN : 'return' ;

INT : 'int' ; // lo trataremos como una palabra reservada

// OTROS
WS : [ \t\n\r] -> skip ;

NUMERO : DIGITO+ ;

ID : (LETRA | '_')(LETRA | DIGITO | '_')* ;

OTRO : . ;

/* s : ID     {print("ID ->" + $ID.text + "<--") }         s
  | NUMERO {print("NUMERO ->" + $NUMERO.text + "<--") } s
  | OTRO   {print("Otro ->" + $OTRO.text + "<--") }     s
  | WHILE  {print("While ->" + $WHILE.text + "<--") }     s
  | FOR    {print("For ->" + $FOR.text + "<--") }     s
  | IF     {print("If ->" + $IF.text + "<--") }     s
  | ELSE   {print("Else ->" + $ELSE.text + "<--") }     s
  // | PALABRA_RESERVADA {print("Palabra reservada ->" + $PALABRA_RESERVADA.text + "<--") }     s
  | EOF
  ;
 */

// todo analisis sintactico tiene un  simbolo inicial que es la raiz del arbol
// es unica y espacial para asegurar que no se repite

/* si : s EOF ; // simbolo inicial, raiz del arbol, es decir de aca arranco

s : PA s PC s // anidacion de parentesis, verifico balance de parentesis
  | // palabra vacia
  ; */


// PROGRAMA:
programa : instrucciones EOF ;

instrucciones : instruccion instrucciones
              |
              ;

instruccion : declaracion
            | asignacion
            | iwhile
            | bloque
            ;

declaracion : INT ID (','ID)*(','ID ASIG (ID | NUMERO))* PYC 
            | INT ID ASIG (ID | NUMERO)(','ID)*(','ID ASIG (ID | NUMERO))* PYC
            ;

asignacion : ID ASIG (ID | NUMERO)(operacion)*(ID | NUMERO)* PYC ;

operacion : (SUMA | RESTA | MULTI | DIVI) ;

iwhile : WHILE PA ID PC instruccion 
       | WHILE PA comparacion PC instruccion
       ;

comparacion : ID comparar (ID | NUMERO) ;

comparar : (IGUAL | NIGUAL | MAYOR | MENOR | MAYORIGUAL | MENORIGUAL) ;

bloque : LLA instrucciones LLC ;

// ifor : FOR PA init PYC cond PYC iter PC instruccion ;

// init : ID ASIG (ID | NUMERO) ;
// cond : comparacion ;
// iter : ;