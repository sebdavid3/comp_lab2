PROYECTO: ANALIZADOR SINTÁCTICO PARA MINILANG CON PYPARSING
1. Objetivo
Diseñar e implementar un analizador sintáctico en Python utilizando la librería Pyparsing
para analizar el MiniLang. Este analizador sintáctico (parser) debe:
• validar la estructura gramatical del programa
• utilizar como entrada la salida del analizador léxico
• construir una representación estructurada del programa (árbol sintáctico)
• detecte y reporte errores sintácticos claros y localizados
2. Alcance
El analizador sintáctico debe soportar los siguientes elementos del lenguaje:
1. Declaraciones:
o Ejemplos válidos:
int x = 10;
float y = 3.5 * x;
string msg = "Hola";
2. Asignaciones:
o Ejemplos válidos:
x = 5;
y = 3 + 7 * x;
3. Expresiones:
o aritméticas: +, -, *, /, % con números, strings y variables.
o relacionales: >, <, >=, <=, ==, != con números, strings y variables.
o lógicas: &&, ||, ! con números, strings y variables.
o Se permiten paréntesis para agrupar expresiones.
o Ejemplos válidos:
resultado = (x + 2) * 30 % y;
cuenta = 2*z + 9 – 7*(k + l);
a > 5 && b < 3
4. Delimitadores de estructuras:
o Se usarán llaves como en C++ o Java: { y }
5. Estructuras Condicionales (if-else):
o Se usarán los operadores de comparación: <, <=, >, >=, !=, ==
o Una estructura if con una o más condiciones, seguida de una o más acciones,
y opcionalmente un bloque else con sus acciones.
o Las condiciones pueden tener expresiones aritméticas o de strings.
o Ejemplo válido:
if x > 3 {
y = x + 2;
z=2*y -9;
}
else {
y = x – 2;z= 2*x-5;
}
Ejemplo válido sin else y condición con expresión:
if x +1 > 3 {
y = x + 2;
z = 2 * y – 9;
}
6. Estructuras while:
o Una estructura while con una o más condiciones, seguida de una o más
acciones.
o Las condiciones pueden tener expresiones aritméticas o de strings.
o Ejemplo válido:
while a < 5 {
resultado = a + 1;
x = 2 * resultado + 5;
}
o Ejemplo válido con expresión aritmética en condición:
while x + 3 < 5 {
resultado = b + 2* (c + 1);
x = 2 * resultado + 5;
}
7. Estructuras for:
o Tendrá la forma:
for (inicio; condición; [paso]) {
accion1;
acción2;
…
acciónN;
}
o El [paso] es opcional y si no está debe mostrar su valor como 1 si es
incremento o -1 si es decremento.
o Ejemplo válido con incremento de 1 (por defecto):
for (int i=0; i<7; ) {
x = i;
y = z + 3;
d = b – 5 * x;
}
o Ejemplo válido con incremento de 2:
for (int i=0; i<7; i=i+2) {
x = i;
y = z + 3;
d = b – 5 * x;
}
o Ejemplo válido con incremento de 1 (explícito):
ofor (int i=0; i<7; i++) {
x = i;
y = z + 3;
d = b – 5 * x;
}
o Ejemplo válido con decremento de 1 (por defecto):
for (int i=10; i>=0; ) {
x = i;
y = z + 3;
d = b – 5 * x;
}
o Ejemplo válido con decremento de 2:
for (int i=10; i>=0; i=i-2 ) {
x = i;
y = z + 3;
d = b – 5 * x;
}
o Ejemplo válido con decremento de 1 (explícito):
for (int i=10; i>=0; i-- ) {
x = i;
y = z + 3;
d = b – 5 * x;
}
8. Funciones simples:
o print
o break
o continue
9. Otras consideraciones
o Debe contemplar que el código tenga comentarios según lo definido para el
análisis léxico.
o Debe considerar tabulaciones, espacios en blanco, líneas en blanco.
o Debe considerar anidamientos de una estructura dentro de otra.
o Debe permitir el manejo de strings usando comillas simples y dobles. Los
strings solo serán para asignaciones a una variable o para comparaciones.
10. Salidas del programa:
o No se consideran errores léxicos. Los códigos de prueba se consideran
lexicográficamente bien construidos.
o Si el programa es correcto: Código Válido y Árbol de Análisis Sintáctico con
anidamientos dentro de corchetes según el análisis que se vaya realizando (Ver
ejemplos).
o Si el programa es incorrecto: Errores de sintaxis, seguido del Árbol de Análisis
Sintáctico con anidamientos dentro de corchetes.
o Si hay error sintáctico se debe seguir con el análisis.3. Restricciones
• No se requiere listas, funciones, etc.
• No se requiere ejecutar el código, solo validar su sintaxis.
4. Requerimientos del Código
El código debe:
1. Usar Pyparsing para definir la gramática del lenguaje MiniLang.
2. Implementar un parser que detecte errores sintácticos.
3. El parser debe leer un archivo de entrada (con cualquier nombre) con código escrito
en MiniLang y analizarlo.
4. Mostrar mensajes de error cuando una instrucción no siga la gramática establecida.
5. Si hay errores el análisis sintáctico debe continuar.
5. Grupos y Entregables
El trabajo debe ser desarrollado por los mismos grupos del laboratorio 1.
Archivo en python en un cuaderno de Google Colab con nombre apellido1nombre1-
apellido2nombre2-apellido3nombre3-apellido4nombre4.ipynb. Este archivo debe
contener en distintas celdas lo siguiente:
Celda 1: Título del proyecto, nombres de autores y NRC al que pertenece cada estudiante.
Celda 2: Gramática Libre de Contexto del lenguaje implementado escrita en texto Markdown
con Latex según las normas descritas en clases.
Celda 3: Manual de uso del programa con indicaciones y directrices claras si contienen
algunos elementos a considerar para su ejecución. Elementos como cargue de librerías, etc.
Debe ser escrito en Markdown.
Celda 4: Código en Python que implemente el analizador sintáctico.
Celda 5: Ejemplo de programa correcto.
Celda 6: Ejemplo de programa incorrecto.
6. Entrega y Evaluación:
Entrega: Mayo 08 de 2026
Sustentaciones: (Pen)?Última semana de clases.
Evaluación:
• Pruebas del archivo ipynb: 60%
✓ Gramática
✓ Manual
✓ Programa correcto
• Sustentación: 40%
✓ Selección de un integrante del grupo de forma aleatoria.
✓ Cambios en el archivo ipynb del grupo
✓ Tiempo: Máximo una hora
7. Preguntas:
En el tema Preguntas Lab. 2 - Análisis Sintáctico del Foro pueden formular sus preguntas.8. Ejemplo de prueba y salida del programa:
A continuación se muestran tres códigos completos con todas las acciones expuestas en el
enunciado.
Código 1: Sin errores
int x = 10;
float y = 3.14;
string mensaje = "Hola mundo";
if (x >= 10) {
print(mensaje);
}
for (int i = 0; i < 5; i++) {
if (i < 3) {
print(i);
}
}
// comentario simple
/*
comentario
multilinea
*/
while (x < 20) {
x++;
}
Salida 1:
Código Válido
Árbol de Análisis Sintáctico
[
['int', 'x', '10'],
['float', 'y', '3.14'],
['string', 'mensaje', '"Hola mundo"'],['if',
['x', '>=', '10'],
[
[['print', 'mensaje']]
]
],
['for',
['i', '0', ['i', '<', '5'], ['i', '++']],
[
[
['if',
['i', '<', '3'],
[
[['print', 'i']]
]
]
]
]
],
['while',
['x', '<', '20'],
[
[['x', '++']]
]
]
]
Código 2: Sin errores
int x = 5;
int y = 10;
int z = 0;
if (x < y) {
if (y > 5) {
print(y);
} else {
print(x);
}
} else {
if (x == 5) {z = x + y;
} else {
z = 0;
}
}
while (x < 10) {
for (int i = 0; i < 3; i++) {
z = z + i;
}
x++;
}
Salida 2:
Código Válido
Árbol de Análisis Sintáctico
[
['int', 'x', '5'],
['int', 'y', '10'],
['int', 'z', '0'],
['if',
['x', '<', 'y'],
[
[
['if',
['y', '>', '5'],
[
[['print', 'y']]
],
[
[['print', 'x']]
]
]
]
],
[
[
['if',
['x', '==', '5'],
[
[['z', 'z', '+', ['x', '+', 'y']]]
],[
[['z', '0']]
]
]
]
]
],
['while',
['x', '<', '10'],
[
[
['for',
['i', '0', ['i', '<', '3'], ['i', '++']],
[
[
['z', 'z', '+', 'i']
]
]
]
],
[
['x', '++']
]
]
]
]
Código 3: Con errores sintácticos
int x = 10;
int y = 5;
if (x > ) {
for (int i = 0; i < 3 i++) {
y=y+i
}
} else {
print(y);
}
while (x < 20 {
x++;
}Salida 3:
Errores de sintaxis
Árbol de Análisis Sintáctico
[
['int', 'x', '10'],
['int', 'y', '5'],
['if',
['error', 'condicion', 'expresion incompleta'],
[
['for',
['i', '0', ['error', 'condicion_for'], ['i', '++']],
[
[
['error', 'asignacion', 'falta punto y coma']
]
]
]
],
[
[['print', 'y']]
]
],
['error', 'while', 'falta parentesis de cierre',
['x', '<', '20'],
[
[['x', '++']]
]
]
]
Código 4: Con errores sintácticos
string nombre = "Juan";
string estado = "activo";
if (nombre == "Juan" && estado == "activo") {
print(nombre);
} else {
print("inactivo");}
while (nombre != "" || estado == "activo") {
nombre = nombre + "!";
estado = "activo"
print(estado;
}
Salida 4:
Errores de sintaxis
Árbol de Análisis Sintáctico
[
['string', 'nombre', '"Juan"'],
['string', 'estado', '"activo"'],
['if',
['&&',
['nombre', '==', '"Juan"'],
['estado', '==', '"activo"']
],
[
[['print', 'nombre']]
],
[
[['print', '"inactivo"']]
]
],
['while',
['||',
['nombre', '!=', '""'],
['estado', '==', '"activo"']
],
[
[
['nombre', 'nombre', '+', '"!"']
],
[
['error', 'asignacion', 'falta punto y coma']
],
[
['error', 'print', 'falta parentesis de cierre']]
]
]
]
