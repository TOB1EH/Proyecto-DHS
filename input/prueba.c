// Comentario que deberia ser ignorado
// #include<stdio.h>

int w;

int f (int d, int c);
// int d ();

int main () {
    int x = 0, o = 5, p = 10;

    int a = 5 + 3 - 4 * 3;

    a = a + 2;

    x = x + 1;

    int y = a;

    x = f(o, p);


    a = a + 2;

    // for (;;) {
    //     x = x + 1;
    // }

    // o = d();

    return x;
}

int f (int a, int b) {
    // int b = 10;
	return a + b;
}

// int d () {
//     return 12;
// }

// int main () {
    
//     // int a = 5;
//     // int b = 10;
//     // int c = 15;
//     // int d = 20;
//     // int x = 0;

//     // x = (a * b - c) + (a * b + d) + a * b;

//     // int x = 1;

//     // x = x * 2;

//     // x = x * 2;

//     // int y = x + 2;

//     // int x, y, z;
    
    
//     // x = 5;
//     // y = x * 2 - 10;
//     // z = y + x;


//     // int x, y, z;
    


//     int x, y, z;
    
//     x = 5;
//     y = x * 2 - 10;
//     z = y + x;

//     x = x + 1;

//     while (1) {
//         x = x + 1;
//     }

//     for (;;) {
//         x = x + 1;
//     }

//     /* 
    
//     x = 1

//     label l0
//     t3 = x + 1
//     x = t3

//     jmp l0


//     OPTIMIZADO

//     x = 1

//     label l0
//     x = 2

//     jmp l0

//      */

//     return 0;
// }

// int f (int a, int b);


// int main () {
//     char c = 1;
//     int o = 10;
//     int p = 20;

//     int r = f(o, p), w = f(o, p);

//     printf("%d %d\n", r, w);
    
//     return 0;
// }


// int  f (int a, int c) {
//     // int a = 0;
//     // int c = 0;
//     return a + c;
// }

// void main () {

//     char w = 0;

//     double x = w;

//     int e = x;


//     // e = x;

//     int o  = 10;
//     int p  = 20;
    
//     /* Invoacaion de funciones */
//     x = f(o, p);

//     // printf("%f", x);
// }
// int a = 9;
// /* FUNCIONES */
// int  f (int a, int c) {
//     // int a = 0;
//     // int c = 0;
//     return a + c;
// }
/* 
int funcion (int a){
    int a; <----- ERROR
    return;
}

float a = 0;
int b = a; <------ ADVERTENCIA

(Usar ENUM para castear el tipo por orden de jerarquia)

si hya errores el visitor no funca

   */  
    /* 

    ...
    	x = f(o, p);
    ...
    
    // Esto se puede traducir como:
    // Funcion:
    label l0
    // Sacamos de la pila los argumentos que vinen mas la direccion de retorno
    pop t0     // Direccion a donde retornar
    pop b
    pop a
    t1 = a + b
    push t1
    jmp t0
    ...
    // Llamada a la funcion:
    // le pasa a la Pila los argumentos y el lugar de retorno
    push o
    push p
    
    push l1     // Etiqueta para volver al lugar correcto (lugar de retorno)
    jmp l0      // Saltamos a la funcion (invocamos)
    label l1    // Retorna a este punto desde la funcion
    
    pop x       // Este x es el t1  que calculamos dentro de la funcion, por eso debemos obtenerlo de la pila
    ...
    
    
     */
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    // Aciones que siempre se ejcutan al menos una vez en el for: 'i = 0; i < x;':

/*     int x = 10;
    int y = 5;
    int z = 1;
    // int i;


    if (x > 0)
	    y = z * 2;
    else
	    y = z / 2; */
	
    /* Esto se traduce como */
/* 
    // if:
    t0 = x > 0
    ifnjmp t0, l0  // Si 't0' es verdadero ejecuta las instrucciones del 'if', en cambio si 't0' es falso saltamos a                   //'l0' que es la etiqueta del 'else'. Entonces cuando haya 'if' hay que preveer la creacion de una                  // etiqueta y para el 'else' dos. 
    t1 = z * 2
    y = t1
    jmp l1 // etiqueta de salto

    // else:
    label l0
    t2 = z / 2
    y = t2
    label l1

 */


    // for (i = 0; i < x; i = i + 1)
	// y = z * x;

    /*     
    
    i = 0
    label l0      // Etiqueta para volver a evaluar la condicion (se ejecuta al menos una vez)
    t0 = i < x    // Condicion del 'for'
    ifnjmp t0, l1 // si es verdadero continua, de lo contrario salta a 'l1'
    t1 = z * x
    y = t1
    // Accion post-ejecucion (puede no hacerce: 'i = i + 1');
    t2 = i + 1
    i = t2
    jmp l0         // salta a la etiqueta 'l0'
    label l1
    
    */
/* 
    for (;;) {
        y = z * x;
    } */
        

    /* 
    
    label l0     // Etiqueta para el inicio del bucle
    t1 = z * x   // Cuerpo del bucle
    y = t1
    jmp l0       // Salto incondicional al inicio del bucle para repetir indefinidamente

    // No hay etiqueta de fin, ya que el bucle es infinito


     */


    // int a = 0, b = 2;

    // int t = a || b;   
    // int y = a && b;

    // int y = 0;
    // int x = 1;
    // int w = 2;

    // while (y != 3 * 2 + (5 * 1) / 2 && x != 0 && w != 0) {
    //     x = x + 1;
    //     w = w + 1;

	//     y = w * x;
    // }

    /* Esto se puede traducir como: */
    // label l0
    // t0 = y < 100
    // ifnjmp t0, l1
    // t1 = w * x
    // y = t1
    // jmp l0
    // label l1

    // int w = 2;

    // while (1 + 2) {
    //     w = w + 1;
    // }


    /* 
    a = 0

    b = 2

    t1 = a || b
    t = t1
    
    t2 = a && b
    y = t2

    */

    // printf("%d\n%d", t, y);

    // int a = 5;
    // int b = !a;

    // /*

    // a = 5 
    
    // t0 = !a 
    // b = t0

    //  */

    // a = b + !10;

    // /* 
    
    // t1 = !10
    // t2 = b + t1
    // a = t2

    //  */

    // a = !(10 - 11);

    /* 
    
    t1 = 10 - 11
    t2 = !t1
    a = t2

     */



    // int d = 5 < (5 + 11) * 4 - (1 + (2 + 3)) * 2;

    /* 
    
    t0 = 5 + 11
    t1 = t0 * 4
    t2 = 2 + 3
    t3 = 1 + t2
    t4 = t3 * 2
    t5 = t1 - t4
    t6 = 5 < t5
    d = t6

    
     */
    
    // int a = (5 < 1) * 4 * 3 >= 10 / 2;

    /* 
    
    t0 = 5 < 1
    t1 = 4 * 3
    t2 = t0 * t1
    t3 = 10 / 2
    t4 = t2 >= t3
    a = t4
    
    */


    /* 
    
    t0 = 4 * 3
    t1 = 1 + t0
    t2 = 5 < t1
    t3 = 10 / 2
    t4 = t2 >= t3
    a = t4

    int a = term1 >= term2
    term1 = subterm1 < subterm2
    subterm1 = 5
    subterm2 = subterm3 + subterm4
    subterm3 = 1
    subterm4 = 4 * 3

    term2 = subterm5
    subterm5 = 10 / 2

     */

    /* 
    
    t0 = 
    
     */

    // int c = 5 < 9 != 10 < 2 > 23 * 3;

    /*

    t0 = 5 < 9
    t1 = 10 < 2
    t2 = 23 * 3
    t3 = t1 > t2
    t4 = t0 != t3
    c = t4

     */



    /* 

    t0 = 5 >= 9
    t1 = 10 < 2
    t2 = t1 > 23
    t3 = t0 == t2
    c = t3

     */

    /* 
    
    t0 = 4 * 3
    t1 = 1 + t0
    t2 = 10 / 2
    t3 = 5 < t1
    t4 = t3 >= t2
    a = t4

    
     */
    
    
    // /* Declaraciones */
    // int a = (5 + 3) * 2 - 4 + 1 / (1 / 2);

    // int x = 3 + (1 + 2 / 2) * 3 + 3;
    
    // int y = 2 - 3 * (2 * 4 - 1) - 1;
    
    // int z = 2 - (2 * 4 - 1) - 1;

    // /* Asignaciones */
    // x = 3 * y + (5 * z) / 2;
    // z = 0;
    // y = 10 + 20;

    /*
    
    t0 = 3 * y
    t1 = 5 * z
    t2 = t1 / 2
    t3 = t0 + t2
    x = t3

    */

    /*

    t0 = 1 + 2
    t1 = 3 * t0
    t2 = t1 * 3
    t3 = t2 + 3
    x = t3

     */

    // int y = 1 + (2 + 3 * 5);





    // int y = 1;
    // int z = 0;
    // int x = (3 * 5) / y + 5 * (z / (2 * 3)) - 1;


    // int w = 3 * (2 * (4 * 8)) + ((1 * 2) * 6);





/*     int a = 7 < 5 != 0 >= 1;
    int c = !a;

    printf("%d\n", a);
    printf("%d\n", c); */
// }





