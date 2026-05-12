import sys
sys.path.insert(0, '.')
from minilang_parser import MiniLangParser

passed = 0
failed = 0
total = 0


def check(name, code, expected_tree, expect_valid):
    """Test con verificación exacta del árbol."""
    global passed, failed, total
    total += 1
    parser = MiniLangParser()
    tree, has_errors = parser.parse(code)

    if expect_valid and has_errors:
        failed += 1
        print(f"  \u274c [{name}]: Se esperaba VÁLIDO pero se detectaron errores")
        return
    elif not expect_valid and not has_errors:
        failed += 1
        print(f"  \u274c [{name}]: Se esperaban ERRORES pero fue válido")
        return

    if tree == expected_tree:
        passed += 1
    else:
        failed += 1
        print(f"  \u274c [{name}]: Árbol no coincide")
        print(f"     Esperado: {expected_tree}")
        print(f"     Obtenido: {tree}")


def check_error(name, code):
    """Test que solo verifica que se detecten errores."""
    global passed, failed, total
    total += 1
    parser = MiniLangParser()
    tree, has_errors = parser.parse(code)
    if has_errors:
        passed += 1
    else:
        failed += 1
        print(f"  \u274c [{name}]: Se esperaban errores pero no se detectaron")


# =====================================================================
# SECCIÓN 1: Tests de los 4 ejemplos del documento (OBLIGATORIOS)
# =====================================================================
print("=" * 60)
print("SECCIÓN 1: Ejemplos del documento")
print("=" * 60)

# Test 1 - Código 1 sin errores
code1 = '''int x = 10;
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
/* comentario multilinea */
while (x < 20) {
    x++;
}'''

expected1 = [
    ['int', 'x', '10'],
    ['float', 'y', '3.14'],
    ['string', 'mensaje', '"Hola mundo"'],
    ['if', ['x', '>=', '10'], [[['print', 'mensaje']]]],
    ['for', ['i', '0', ['i', '<', '5'], ['i', '++']], [[['if', ['i', '<', '3'], [[['print', 'i']]]]]]],
    ['while', ['x', '<', '20'], [[['x', '++']]]]
]

check("Código 1 sin errores", code1, expected1, True)

# Test 2 - Código 2 sin errores (anidamiento complejo)
code2 = '''int x = 5;
int y = 10;
int z = 0;
if (x < y) {
    if (y > 5) {
        print(y);
    } else {
        print(x);
    }
} else {
    if (x == 5) {
        z = x + y;
    } else {
        z = 0;
    }
}
while (x < 10) {
    for (int i = 0; i < 3; i++) {
        z = z + i;
    }
    x++;
}'''

expected2 = [
    ['int', 'x', '5'],
    ['int', 'y', '10'],
    ['int', 'z', '0'],
    ['if', ['x', '<', 'y'],
        [[['if', ['y', '>', '5'], [[['print', 'y']]], [[['print', 'x']]]]]],
        [[['if', ['x', '==', '5'], [[['z', 'x', '+', 'y']]], [[['z', '0']]]]]]],
    ['while', ['x', '<', '10'],
        [[['for', ['i', '0', ['i', '<', '3'], ['i', '++']], [[['z', 'z', '+', 'i']]]]],
         [['x', '++']]]]
]

check("Código 2 sin errores (anidamiento complejo)", code2, expected2, True)

# Test 3 - Código 3 con errores
code3 = '''int x = 10;
int y = 5;
if (x > ) {
    for (int i = 0; i < 3 i++) {
        y = y + i
    }
} else {
    print(y);
}
while (x < 20 {
    x++;
}'''

expected3 = [
    ['int', 'x', '10'],
    ['int', 'y', '5'],
    ['if', ['error', 'condicion', 'expresion incompleta'],
        [[['for', ['i', '0', ['error', 'condicion_for'], ['i', '=', 'i', '+', '1']],
           [[['error', 'asignacion', 'falta punto y coma']]]]]],
        [[['print', 'y']]]],
    ['error', 'while', 'falta parentesis de cierre',
        ['x', '<', '20'],
        [[['x', '++']]]]
]

check("Código 3 con errores", code3, expected3, False)

# Test 4 - Código 4 con errores y operadores lógicos
code4 = '''string nombre = "Juan";
string estado = "activo";
if (nombre == "Juan" && estado == "activo") {
    print(nombre);
} else {
    print("inactivo");
}
while (nombre != "" || estado == "activo") {
    nombre = nombre + "!";
    estado = "activo"
    print(estado;
}'''

expected4 = [
    ['string', 'nombre', '"Juan"'],
    ['string', 'estado', '"activo"'],
    ['if',
        ['&&', ['nombre', '==', '"Juan"'], ['estado', '==', '"activo"']],
        [[['print', 'nombre']]],
        [[['print', '"inactivo"']]]],
    ['while',
        ['||', ['nombre', '!=', '""'], ['estado', '==', '"activo"']],
        [[['nombre', 'nombre', '+', '"!"']],
         [['error', 'asignacion', 'falta punto y coma']],
         [['error', 'print', 'falta parentesis de cierre']]]]
]

check("Código 4 con errores y operadores lógicos", code4, expected4, False)


# =====================================================================
# SECCIÓN 2: Expresiones aritméticas
# =====================================================================
print("\n" + "=" * 60)
print("SECCIÓN 2: Expresiones aritméticas")
print("=" * 60)

check("Asignación simple", "x = 3;",
      [['x', '3']], True)

check("Suma", "x = 10 + 5;",
      [['x', '10', '+', '5']], True)

check("Resta", "x = 10 - 5;",
      [['x', '10', '-', '5']], True)

check("Multiplicación", "x = 10 * 5;",
      [['x', '10', '*', '5']], True)

check("División", "x = 10 / 5;",
      [['x', '10', '/', '5']], True)

check("Módulo", "x = 10 % 3;",
      [['x', '10', '%', '3']], True)

check("Precedencia * sobre +", "x = 10 * 5 + 3;",
      [['x', ['10', '*', '5'], '+', '3']], True)

check("Paréntesis cambian precedencia", "x = (10 + 5) * 2;",
      [['x', ['10', '+', '5'], '*', '2']], True)

check("Expresión compleja", "z = 2 * x + 9 - 7 * (k + l);",
      [['z', [['2', '*', 'x'], '+', '9'], '-', ['7', '*', ['k', '+', 'l']]]], True)


# =====================================================================
# SECCIÓN 3: Declaraciones
# =====================================================================
print("\n" + "=" * 60)
print("SECCIÓN 3: Declaraciones")
print("=" * 60)

check("Declaración int", "int x = 10;",
      [['int', 'x', '10']], True)

check("Declaración float", "float y = 3.14;",
      [['float', 'y', '3.14']], True)

check("Declaración string", 'string s = "Hola";',
      [['string', 's', '"Hola"']], True)

check("Declaración con expresión", "int x = 5 + 3;",
      [['int', 'x', '5', '+', '3']], True)


# =====================================================================
# SECCIÓN 4: Postfix
# =====================================================================
print("\n" + "=" * 60)
print("SECCIÓN 4: Postfix")
print("=" * 60)

check("Postfix ++", "x++;",
      [['x', '++']], True)

check("Postfix --", "x--;",
      [['x', '--']], True)


# =====================================================================
# SECCIÓN 5: Print, Break, Continue
# =====================================================================
print("\n" + "=" * 60)
print("SECCIÓN 5: Print, Break, Continue")
print("=" * 60)

check("Print variable", "print(x);",
      [['print', 'x']], True)

check("Print string doble", 'print("hola");',
      [['print', '"hola"']], True)

check("Print string simple", "print('texto');",
      [['print', "'texto'"]], True)

check("Break", "break;",
      [['break']], True)

check("Continue", "continue;",
      [['continue']], True)


# =====================================================================
# SECCIÓN 6: Condiciones y operadores lógicos
# =====================================================================
print("\n" + "=" * 60)
print("SECCIÓN 6: Condiciones y operadores lógicos")
print("=" * 60)

check("If con paréntesis", "if (x > 3) { y = 1; }",
      [['if', ['x', '>', '3'], [[['y', '1']]]]], True)

check("If sin paréntesis", "if x > 3 { y = 2; }",
      [['if', ['x', '>', '3'], [[['y', '2']]]]], True)

check("If-else", "if (x > 3) { y = 1; } else { y = 2; }",
      [['if', ['x', '>', '3'], [[['y', '1']]], [[['y', '2']]]]], True)

check("If con expresión aritmética en condición", "if x + 1 > 3 { y = x + 2; }",
      [['if', ['x', '+', '1', '>', '3'], [[['y', 'x', '+', '2']]]]], True)

check("While con paréntesis", "while (x < 10) { x++; }",
      [['while', ['x', '<', '10'], [[['x', '++']]]]],  True)

check("While sin paréntesis", "while x < 10 { x++; }",
      [['while', ['x', '<', '10'], [[['x', '++']]]]],  True)

check("While con expr aritmética", "while x + 3 < 5 { x++; }",
      [['while', ['x', '+', '3', '<', '5'], [[['x', '++']]]]],  True)

check("Operador !", "if (!x) { y = 1; }",
      [['if', ['!', 'x'], [[['y', '1']]]]], True)

check("Operador &&", "if (x > 3 && y < 5) { z = 1; }",
      [['if', ['&&', ['x', '>', '3'], ['y', '<', '5']], [[['z', '1']]]]], True)

check("Operador ||", "if (x > 3 || y < 5) { z = 1; }",
      [['if', ['||', ['x', '>', '3'], ['y', '<', '5']], [[['z', '1']]]]], True)

check("Precedencia && sobre ||", "if (a > 1 && b < 2 || c == 3) { x = 1; }",
      [['if', ['||', ['&&', ['a', '>', '1'], ['b', '<', '2']], ['c', '==', '3']], [[['x', '1']]]]], True)

check("! con &&", "if (!x && y > 0) { z = 1; }",
      [['if', ['&&', ['!', 'x'], ['y', '>', '0']], [[['z', '1']]]]], True)


# =====================================================================
# SECCIÓN 7: For (todas las variantes)
# =====================================================================
print("\n" + "=" * 60)
print("SECCIÓN 7: For (todas las variantes)")
print("=" * 60)

check("For con ++ explícito", "for (int i = 0; i < 5; i++) { x = i; }",
      [['for', ['i', '0', ['i', '<', '5'], ['i', '++']], [[['x', 'i']]]]], True)

check("For con -- explícito", "for (int i = 10; i >= 0; i--) { x = i; }",
      [['for', ['i', '10', ['i', '>=', '0'], ['i', '--']], [[['x', 'i']]]]], True)

check("For sin paso con < (infiere ++ = 1)", "for (int i = 0; i < 7; ) { x = i; }",
      [['for', ['i', '0', ['i', '<', '7'], ['i', '=', 'i', '+', '1']], [[['x', 'i']]]]], True)

check("For sin paso con >= (infiere -- = -1)", "for (int i = 10; i >= 0; ) { x = i; }",
      [['for', ['i', '10', ['i', '>=', '0'], ['i', '=', 'i', '-', '1']], [[['x', 'i']]]]], True)

check("For con paso i=i+2", "for (int i = 0; i < 7; i=i+2) { x = i; }",
      [['for', ['i', '0', ['i', '<', '7'], ['i', '=', 'i', '+', '2']], [[['x', 'i']]]]], True)

check("For con paso i=i-2", "for (int i = 10; i >= 0; i=i-2) { x = i; }",
      [['for', ['i', '10', ['i', '>=', '0'], ['i', '=', 'i', '-', '2']], [[['x', 'i']]]]], True)


# =====================================================================
# SECCIÓN 8: Anidamiento
# =====================================================================
print("\n" + "=" * 60)
print("SECCIÓN 8: Anidamiento")
print("=" * 60)

check("If > for > while anidados",
      "if (x > 0) { for (int i = 0; i < 5; i++) { while (i < 3) { print(i); } } }",
      [['if', ['x', '>', '0'], [[['for', ['i', '0', ['i', '<', '5'], ['i', '++']], [[['while', ['i', '<', '3'], [[['print', 'i']]]]]]]]]]], True)

check("Break y continue en for",
      "for (int i = 0; i < 10; i++) { if (i == 5) { break; } continue; }",
      [['for', ['i', '0', ['i', '<', '10'], ['i', '++']], [[['if', ['i', '==', '5'], [[['break']]]]], [['continue']]]]], True)


# =====================================================================
# SECCIÓN 9: Casos borde válidos
# =====================================================================
print("\n" + "=" * 60)
print("SECCIÓN 9: Casos borde válidos")
print("=" * 60)

check("Código vacío", "",
      [], True)

check("Solo comentarios", "// comentario\n/* bloque */",
      [], True)

check("String con comillas dobles", 'x = "hello world";',
      [['x', '"hello world"']], True)

check("String con comillas simples", "x = 'hello world';",
      [['x', "'hello world'"]], True)

check("Paréntesis dobles en condición", "if ((x > 3)) { y = 1; }",
      [['if', ['x', '>', '3'], [[['y', '1']]]]], True)

check("Negación con comparación", "if (!(x > 3)) { y = 1; }",
      [['if', ['!', ['x', '>', '3']], [[['y', '1']]]]], True)


# =====================================================================
# SECCIÓN 10: Detección de errores (expect_valid=False)
# =====================================================================
print("\n" + "=" * 60)
print("SECCIÓN 10: Detección de errores")
print("=" * 60)

check_error("Falta ; en asignación", "x = 3")
check_error("Falta ; en declaración", "int x = 10")
check_error("Condición incompleta", "if (x > ) { }")
check_error("Falta ) en while", "while (x < 20 { x++; }")
check_error("Falta ) en print", "print(x;")


# =====================================================================
# RESUMEN DE RESULTADOS
# =====================================================================
print(f"\n{'='*60}")
print(f"RESULTADOS: {passed}/{total} passed, {failed} failed")
print(f"{'='*60}")
if failed == 0:
    print(f"✅ TODOS LOS {total} TESTS PASARON")
else:
    print(f"❌ {failed} tests fallaron")
