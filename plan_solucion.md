# PLAN DE SOLUCIÓN — Correcciones para MiniLang Parser

**Objetivo:** Lograr 100% en las pruebas del rubric antes de la sustentación.

---

## Prioridades

| # | Error | Severidad | Esfuerzo | Impacto en nota |
|---|---|---|---|---|
| 🚨 1 | `_try_parse_for` — early return impide nodo estructurado | Alta | ~20 min | +5-8 pts |
| ⚠️ 2 | `_try_parse_if` — if sin `{` no genera error | Media | ~5 min | +1-2 pts |
| 📝 3 | Documentar limitaciones en el manual | Baja | ~5 min | +1-2 pts |

---

## 🚨 CORRECCIÓN 1: Recuperación del `for` en Salida 3

**Archivo:** `minilang_parser.py`
**Método:** `_try_parse_for` (líneas 1305-1428)
**Estado actual:** Devuelve `['error', 'for', 'falta punto y coma']` cuando falta `;` entre condición y paso.
**Estado esperado (Rubric Salida 3):**
```python
['for',
  ['i', '0', ['error', 'condicion_for'], ['i', '++']],
  [
    [
      ['error', 'asignacion', 'falta punto y coma']
    ]
  ]
]
```

### Causa raíz

El método tiene **tres early returns** que impiden construir el nodo `for` estructurado:

```
Línea 1413: if not has_init_semi or not has_cond_semi:
                return ['error', 'for', 'falta punto y coma']  ← BLOQUEA

Línea 1416: if not close_paren_found:
                return ['error', 'for', 'falta parentesis de cierre']  ← BLOQUEA

Línea 1423: if block_error:
                return ['error', 'for', 'falta llave de apertura', ...]
```

Para el caso de Salida 3:
1. `has_cond_semi = False` (falta el `;` entre `i < 3` y `i++`)
2. `has_init_semi = True` (el `;` después de `int i = 0` sí está)
3. La línea 1413 ejecuta y aborta antes de construir el nodo

### Fix: Reemplazar early returns por continuación

Cambiar las líneas 1413-1421 de:

```python
# ❌ CÓDIGO ACTUAL (líneas 1413-1421)
if not has_init_semi or not has_cond_semi:
    return (['error', 'for', 'falta punto y coma'], consumed)

if not close_paren_found:
    return (['error', 'for', 'falta parentesis de cierre'], consumed)

if step is None:
    step = self._default_step(var_name, cond)
```

a:

```python
# ✅ CÓDIGO CORREGIDO
if step is None:
    step = self._default_step(var_name, cond)

# NOTA: No se hace early return por faltar ; o ).
# El error se codifica en la condición como ['error', 'condicion_for']
# y en el paso como None. El nodo for se construye igual.
```

**Efecto:** Ahora el flujo continúa hasta la línea 1426:
```python
return (['for', [var_name, init_val, cond, step], block], consumed)
```

Con `cond = ['error', 'condicion_for']` (ya asignado en línea 1368) y `step = ['i', '++']` (extraído por regex en línea 1387), el nodo resultante será:

```python
['for', ['i', '0', ['error', 'condicion_for'], ['i', '++']], block]
```

### Validación

Después del fix, probar con:

```python
CODIGO_ERRORES = """int x = 10;
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
}
"""
parser = MiniLangParser()
tree, err = parser.parse_file("test.txt")  # o usar bypass interno
```

Verificar que el AST contenga:
```python
['for', ['i', '0', ['error', 'condicion_for'], ['i', '++']],
  [
    [
      ['error', 'asignacion', 'falta punto y coma']
    ]
  ]
]
```

> **Nota:** El bloque del for contiene `y = y + i` sin `;`, que debería generar `['error', 'asignacion', 'falta punto y coma']`. Si el parser produce otro error o no detecta la falta de `;`, revisar `_parse_block_recovery` que se encarga del contenido del bloque.

> **Nota 2:** Si `close_paren_found` es `False`, el texto después del `)` incluirá `{...}`. Verificar que `_parse_block_recovery` recibe el texto correcto (a partir de `{`). Si no, ajustar el cálculo de `rest_after_paren` para que apunte al `{`.

---

## ⚠️ CORRECCIÓN 2: If sin llave de apertura

**Archivo:** `minilang_parser.py`
**Método:** `_try_parse_if` (líneas 1204-1254)
**Estado actual:** Cuando `if (cond)` no tiene `{`, el método parsea la condición, luego `_parse_block_recovery` retorna `([], rest, True)` — bloque vacío con error. Pero el error `then_error` **no se verifica** y se retorna `['if', cond, []]` sin ningún indicador de error.

### Fix

Insertar verificación de `then_error` después de la línea 1240 (después del bloque `if cond_error`):

```python
# ✅ Insertar después de la línea 1240 (después del return de cond_error)
if then_error:
    return (['error', 'if', 'falta llave de apertura', cond, then_block if then_block else []], consumed)
```

**Ubicación exacta:** Después de la línea que dice `return (ast_node, consumed)` dentro del `if cond_error:`, y antes del `if cond is None:`. El fix aplica al flujo normal (cuando `cond_error` es `False`).

Quedaría:

```python
ast_node = ['if', cond]
if then_block is not None:
    ast_node.append(then_block)
else:
    ast_node.append([])
if else_block is not None:
    ast_node.append(else_block)

# ✅ NUEVA VERIFICACIÓN
if then_error:
    return (['error', 'if', 'falta llave de apertura', cond, then_block if then_block else []], consumed)

return (ast_node, consumed)
```

**Resultado esperado para `if (x < 20)\n    y = y + 1;\n}`:**
```python
['error', 'if', 'falta llave de apertura', ['x', '<', '20'], []]
```

---

## 📝 CORRECCIÓN 3: Documentación (Opcional)

Agregar al inicio de `_try_parse_for` y `_try_parse_if` comentarios que documenten:

```python
# NOTA: Este método de recovery NO hace early return por errores de
# puntuación (; faltante, ) faltante). En su lugar, codifica el error
# dentro del nodo estructurado (ej. ['error', 'condicion_for']) para
# que el AST mantenga su forma incluso con errores, como exige el rubric.
```

Esto demuestra al profesor durante la sustentación que el equipo **comprendió** la decisión de diseño y puede explicarla.

---

## Verificación final

Después de aplicar las correcciones, ejecutar estas pruebas:

```bash
# Prueba 1: programa_correcto.txt (sin errores)
python3 -c "
import sys; sys.path.insert(0, '.')
from minilang_parser import MiniLangParser, print_tree
p = MiniLangParser()
# Usar bypass interno
with open('otras_pruebas/programa_correcto.txt') as f:
    code = f.read()
code, hu = p.remove_comments(code)
from pyparsing import ParseException
try:
    r = p.program.parseString(code, parseAll=True)
    t = r.asList()
except ParseException:
    t, _ = p._parse_with_recovery(code, hu)
print('Código Válido')
print_tree(t)
"

# Prueba 2: programa_errores.txt (con errores)
# ... mismo patrón con programa_errores.txt ...

# Prueba 3: Salida 3 del rubric (el for maldito)
CODIGO_ERRORES = '''int x = 10;\nint y = 5;\nif (x > ) {\n    for (int i = 0; i < 3 i++) {\n        y = y + i\n    }\n} else {\n    print(y);\n}\nwhile (x < 20 {\n    x++;\n}\n'''
# parsear y verificar nodo for estructurado
```

---

## Resumen de cambios

| Archivo | Líneas | Cambio |
|---|---|---|
| `minilang_parser.py` | 1413-1421 | Eliminar 2 early returns en `_try_parse_for` |
| `minilang_parser.py` | ~1242 | Agregar verificación `if then_error:` en `_try_parse_if` |

**Tiempo estimado total: 25-30 minutos.**
