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

// Operaciones
ASIG  : '=' ;
SUMA  : '+' ;
RESTA : '-' ;
MULTI : '*' ;
DIVI  : '/' ;
MOD   : '%' ;

// Comparaciones
IGUAL      : '==' ;
NIGUAL     : '!=' ;
MAYOR      : '>' ;
MENOR      : '<' ;
MAYORIGUAL : '>=' ;
MENORIGUAL : '<=' ;

// COMENTARIOS
ICOMEN : '/*' ;
FCOMEN : '*/' ;
COMEN  : '//' ;

// PALABRAS RESERVADAS DEL LENGUAJE:
WHILE  : 'while' ;
FOR    : 'for' ;
IF     : 'if' ;
ELSE   : 'else' ;
RETURN : 'return' ;

// Tipos de variables
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
  | EOF
  ;
 */

// si : s EOF ; // simbolo inicial, raiz del arbol, es decir de aca arranco

// s : PA s PC s // anidacion de parentesis, verifico balance de parentesis
//   | // palabra vacia
//   ;


// PROGRAMA:
programa : instrucciones EOF ;

instrucciones : instruccion instrucciones
              |
              ;

instruccion : declaracion PYC
            | asignacion PYC
            | iwhile
            | bloque
            ;
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

// Operaciones aritmeticas y logicas
opal : exp ; // Completar

// Expresion
exp : term e ;

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
factor : NUMERO
       | ID
       | PA exp PC // Sabe que tiene que resolver esto primero por la profundidad del arbol
       ;

operacion : SUMA 
          | RESTA 
          | MULTI 
          | DIVI 
          ;

// Bucle while
iwhile : WHILE PA ID PC instruccion 
       | WHILE PA comparacion PC instruccion
       ;
comparacion : ID comparar ID 
            | ID comparar NUMERO 
            ;


comparar : IGUAL 
         | NIGUAL 
         | MAYOR 
         | MENOR 
         | MAYORIGUAL 
         | MENORIGUAL 
         ;

bloque : LLA instrucciones LLC ;

// ifor : FOR PA init PYC cond PYC iter PC instruccion ;

// init : ID ASIG (ID | NUMERO) ;
// cond : comparacion ;
// iter : ;