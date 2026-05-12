# Prompt para IA: Generar Tests del Parser MiniLang

Copia todo lo de abajo y pégalo como prompt a tu IA.

---

## PROMPT INICIO

Genera un archivo Python llamado `test_parser.py` que pruebe exhaustivamente el parser de MiniLang. El parser se importa así:

```python
from minilang_parser import MiniLangParser
```

Y se usa así:

```python
parser = MiniLangParser()
tree, has_errors = parser.parse(codigo_fuente)
# tree = lista de listas (AST)
# has_errors = True/False
```

### ESTRUCTURA DEL ARCHIVO DE TESTS

```python
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
        print(f"  ❌ [{name}]: Se esperaba VÁLIDO pero se detectaron errores")
        return
    elif not expect_valid and not has_errors:
        failed += 1
        print(f"  ❌ [{name}]: Se esperaban ERRORES pero fue válido")
        return
    
    if tree == expected_tree:
        passed += 1
    else:
        failed += 1
        print(f"  ❌ [{name}]: Árbol no coincide")
        print(f"     Esperado: {expected_tree}")
        print(f"     Obtenido: {tree}")

# ... tests aquí ...

print(f"\nRESULTADOS: {passed}/{total} passed, {failed} failed")
```

### TESTS REQUERIDOS

Incluye TODOS los tests siguientes. Cada `check()` debe tener el AST esperado EXACTO.

---

#### SECCIÓN 1: Tests de los 4 ejemplos del documento (OBLIGATORIOS)

**Test 1 — Código 1 sin errores:**
```python
code = '''int x = 10;
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

expected = [
    ['int', 'x', '10'],
    ['float', 'y', '3.14'],
    ['string', 'mensaje', '"Hola mundo"'],
    ['if', ['x', '>=', '10'], [[['print', 'mensaje']]]],
    ['for', ['i', '0', ['i', '<', '5'], ['i', '++']], [[['if', ['i', '<', '3'], [[['print', 'i']]]]]]],
    ['while', ['x', '<', '20'], [[['x', '++']]]]
]
# expect_valid=True
```

**Test 2 — Código 2 sin errores (anidamiento complejo):**
```python
code = '''int x = 5;
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

expected = [
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
# expect_valid=True
```

**Test 3 — Código 3 con errores:**
```python
code = '''int x = 10;
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

expected = [
    ['int', 'x', '10'],
    ['int', 'y', '5'],
    ['if', ['error', 'condicion', 'expresion incompleta'],
        [[['for', ['i', '0', ['error', 'condicion_for'], ['i', '++']],
           [[['error', 'asignacion', 'falta punto y coma']]]]]],
        [[['print', 'y']]]],
    ['error', 'while', 'falta parentesis de cierre',
        ['x', '<', '20'],
        [[['x', '++']]]]
]
# expect_valid=False
```

**Test 4 — Código 4 con errores y operadores lógicos:**
```python
code = '''string nombre = "Juan";
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

expected = [
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
# expect_valid=False
```

---

#### SECCIÓN 2: Expresiones aritméticas

```python
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
```

---

#### SECCIÓN 3: Declaraciones

```python
check("Declaración int", "int x = 10;",
      [['int', 'x', '10']], True)

check("Declaración float", "float y = 3.14;",
      [['float', 'y', '3.14']], True)

check("Declaración string", 'string s = "Hola";',
      [['string', 's', '"Hola"']], True)

check("Declaración con expresión", "int x = 5 + 3;",
      [['int', 'x', '5', '+', '3']], True)
```

---

#### SECCIÓN 4: Postfix

```python
check("Postfix ++", "x++;",
      [['x', '++']], True)

check("Postfix --", "x--;",
      [['x', '--']], True)
```

---

#### SECCIÓN 5: Print, Break, Continue

```python
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
```

---

#### SECCIÓN 6: Condiciones y operadores lógicos

```python
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
```

---

#### SECCIÓN 7: For (todas las variantes)

```python
check("For con ++ explícito", "for (int i = 0; i < 5; i++) { x = i; }",
      [['for', ['i', '0', ['i', '<', '5'], ['i', '++']], [[['x', 'i']]]]], True)

check("For con -- explícito", "for (int i = 10; i >= 0; i--) { x = i; }",
      [['for', ['i', '10', ['i', '>=', '0'], ['i', '--']], [[['x', 'i']]]]], True)

check("For sin paso con < (infiere ++)", "for (int i = 0; i < 7; ) { x = i; }",
      [['for', ['i', '0', ['i', '<', '7'], ['i', '++']], [[['x', 'i']]]]], True)

check("For sin paso con >= (infiere --)", "for (int i = 10; i >= 0; ) { x = i; }",
      [['for', ['i', '10', ['i', '>=', '0'], ['i', '--']], [[['x', 'i']]]]], True)

check("For con paso i=i+2", "for (int i = 0; i < 7; i=i+2) { x = i; }",
      [['for', ['i', '0', ['i', '<', '7'], ['i', '=', 'i', '+', '2']], [[['x', 'i']]]]], True)

check("For con paso i=i-2", "for (int i = 10; i >= 0; i=i-2) { x = i; }",
      [['for', ['i', '10', ['i', '>=', '0'], ['i', '=', 'i', '-', '2']], [[['x', 'i']]]]], True)
```

---

#### SECCIÓN 8: Anidamiento

```python
check("If > for > while anidados",
      "if (x > 0) { for (int i = 0; i < 5; i++) { while (i < 3) { print(i); } } }",
      [['if', ['x', '>', '0'], [[['for', ['i', '0', ['i', '<', '5'], ['i', '++']], [[['while', ['i', '<', '3'], [[['print', 'i']]]]]]]]]]], True)

check("Break y continue en for",
      "for (int i = 0; i < 10; i++) { if (i == 5) { break; } continue; }",
      [['for', ['i', '0', ['i', '<', '10'], ['i', '++']], [[['if', ['i', '==', '5'], [[['break']]]]], [['continue']]]]], True)
```

---

#### SECCIÓN 9: Casos borde válidos

```python
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
```

---

#### SECCIÓN 10: Detección de errores (expect_valid=False)

Para estos tests, solo verificar que `has_errors == True`. No necesitas verificar el AST exacto (puedes poner `expected_tree=None` y solo verificar validez):

```python
# Falta punto y coma en asignación
check_error("Falta ; en asignación", "x = 3")

# Falta punto y coma en declaración
check_error("Falta ; en declaración", "int x = 10")

# Condición incompleta
check_error("Condición incompleta", "if (x > ) { }")

# Falta ) en while
check_error("Falta ) en while", "while (x < 20 { x++; }")

# Falta ) en print
check_error("Falta ) en print", "print(x;")
```

Para `check_error`, usa una función más simple:
```python
def check_error(name, code):
    global passed, failed, total
    total += 1
    parser = MiniLangParser()
    tree, has_errors = parser.parse(code)
    if has_errors:
        passed += 1
    else:
        failed += 1
        print(f"  ❌ [{name}]: Se esperaban errores pero no se detectaron")
```

---

### RESUMEN DE RESULTADOS

Al final del archivo, imprime:
```python
print(f"\n{'='*60}")
print(f"RESULTADOS: {passed}/{total} passed, {failed} failed")
print(f"{'='*60}")
if failed == 0:
    print(f"✅ TODOS LOS {total} TESTS PASARON")
else:
    print(f"❌ {failed} tests fallaron")
```

### INSTRUCCIONES

1. Genera el archivo `test_parser.py` completo con TODOS los tests listados arriba
2. Cada test debe usar `check()` o `check_error()` con los valores exactos mostrados
3. Los tests deben organizarse en secciones con prints de separación
4. Al ejecutar `python test_parser.py` debe correr todos los tests automáticamente

## PROMPT FIN
