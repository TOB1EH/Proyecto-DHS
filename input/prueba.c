// Comentario que deberia ser ignorado
// #include<stdio.h>

void main () {
    

    int a = 5;
    int b = !a;

    /*

    a = 5 
    
    t0 = !a 
    b = t0

     */

    a = b + !10;

    /* 
    
    t1 = !10
    t2 = b + t1
    a = t2

     */

    a = !(10 -11);

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





/*     int a = 7 < 5 != 0 >= 1;
    int c = !a;

    printf("%d\n", a);
    printf("%d\n", c); */
}





