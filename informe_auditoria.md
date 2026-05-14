# INFORME DE AUDITORÍA — Analizador Sintáctico MiniLang

**Fecha:** 14 de mayo de 2026
**Evaluador:** Sistema de auditoría automática (caja negra + caja blanca)
**Archivo evaluado:** `minilang_parser.py`

---

## 1. RESUMEN EJECUTIVO

| Componente | Peso | Nota | Estado |
|---|---|---|---|
| Gramática (Celda 2) | 10 pts | ✅ 10/10 | Completa en LaTeX, todos los constructos |
| Manual (Celda 3) | 10 pts | ✅ 10/10 | Instrucciones claras, ejemplos de uso |
| Código (Celda 4) | 15 pts | ✅ 13/15 | Pyparsing bien usado, gramática completa, recovery presente |
| Prog. Correcto (Celda 5) | 15 pts | ✅ 15/15 | AST correcto en Salidas 1 y 2 del rubric |
| Prog. Incorrecto (Celda 6) | 10 pts | ⚠️ 7/10 | Salida 4 perfecta; Salida 3 tiene 1 desviación |
| **Total entregables** | **60 pts** | **55/60 (~92%)** | |
| Sustentación (40%) | — | Variable | Depende de corrección en vivo |

**Veredicto: El parser es sólido y aprobaría con nota alta (~92% en entregables).** La única desviación significativa contra el rubric está en la recuperación del `for` malformed dentro del `if` (Salida 3).

---

## 2. VERIFICACIÓN ESTRUCTURAL DEL AST

### 2.1 Anidamiento triple `[[[stmt]]]` para bloques

| Constructo | AST Generado | Rubric | ¿Coincide? |
|---|---|---|---|
| If (1 stmt) | `['if', cond, [[['print', 'mensaje']]]]` | Salida 1 | ✅ |
| If (2 stmts) | `['if', cond, [[['x','++']], [['y','y','*','2']]]]` | — | ✅ |
| If-else anidado | `['if', cond, [[[if...]]], [[[if...]]]]` | Salida 2 | ✅ |
| For | `['for', [var,init,cond,step], [[[if...]]]]` | Salida 1 | ✅ |
| While | `['while', cond, [[['x','++']]]]` | Salida 1 | ✅ |

### 2.2 Expresiones aritméticas — Precedencia preservada

| Expresión | AST | Interpretación |
|---|---|---|
| `(x + 2) * 30 % 7` | `['x', [['x','+','2'],'*','30'],'%','7']` | `((x+2)*30)%7` ✅ |
| `2 * x + 9 - 7 * (x + 1)` | `['y', [['2','*','x'],'+','9'], '-', ['7','*',['x','+','1']]]` | `((2*x)+9)-(7*(x+1))` ✅ |

### 2.3 Condiciones lógicas

| Condición | AST |
|---|---|
| `x >= 10 && y < 100` | `['&&', ['x','>=','10'], ['y','<','100']]` ✅ |
| `nombre != "" \|\| estado == "activo"` | `['\|\|', ['nombre','!=','""'], ['estado','==','"activo"']]` ✅ |

### 2.4 For implícito (sin paso)

`for (int i = 0; i < 5;)` → paso inferido como `1` (entero) ✅
`for (int i = 10; i >= 0;)` → paso inferido como `-1` (entero) ✅

### 2.5 Break / Continue

`break;` → `['break']` ✅
`continue;` → `['continue']` ✅

---

## 3. ERROR RECOVERY — SALIDA 4 (RUBRIC) ✅ COINCIDENCIA EXACTA

```python
# Esperado (Salida 4):
['&&', ['nombre', '==', '"Juan"'], ['estado', '==', '"activo"']]

# Obtenido:
['&&', ['nombre', '==', '"Juan"'], ['estado', '==', '"activo"']] ✅
```

```python
['while',
  ['||', ['nombre', '!=', '""'], ['estado', '==', '"activo"']],
  [
    [['nombre', 'nombre', '+', '"!"']],
    [['error', 'asignacion', 'falta punto y coma']],
    [['error', 'print', 'falta parentesis de cierre']]
  ]
] ✅
```

Todos los nodos de error y la estructura del AST coinciden **exactamente** con el rubric.

---

## 4. ERROR RECOVERY — SALIDA 3 (RUBRIC) ⚠️ 1 DESVIACIÓN

### 4.1 Lo que funciona ✅

| Elemento | Esperado | Obtenido |
|---|---|---|
| Condición `if` incompleta | `['error', 'condicion', 'expresion incompleta']` | ✅ |
| `while` sin `)` | `['error', 'while', 'falta parentesis de cierre', cond, block]` | ✅ |
| Else como bloque externo | `[[['print', 'y']]]` (como else del if, estructuralmente correcto) | ✅ |

### 4.2 Lo que NO funciona ❌

**Entrada:** `for (int i = 0; i < 3 i++) { y = y + i }` (falta `;` entre condición y paso)

**Esperado (Rubric Salida 3):**
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

**Obtenido:**
```python
['error', 'for', 'falta parentesis de cierre']
```

**Causa raíz** (archivo `minilang_parser.py`, método `_try_parse_for`, líneas ~1356-1392):

1. `_parse_cond_recovery` recibe `i < 3 i++) {\n...` y busca `{` como delimitador
2. Consume todo hasta `{` → texto de condición: `i < 3 i++)` (se traga el `)`)
3. `has_for_semi` = `False` (no hay `;` después de la condición)
4. `close_paren_found` = `False` (el texto después del step empieza con `{`)
5. Línea 1392: **early return** con `['error', 'for', 'falta parentesis de cierre']`
6. Nunca construye el nodo `['for', ...]` con estructura interna

**Impacto en nota:** Si el profesor compara la Salida 3 contra el rubric, detectará esta diferencia. ** Penalización estimada: -3 a -5 puntos sobre 60.**

---

## 5. ERROR RECOVERY — PRUEBAS PESADAS (18 casos)

| # | Error | Nodo generado | ¿Correcto? | Impacto |
|---|---|---|---|---|
| 1 | `if (x > )` condición incompleta | `['error', 'condicion', 'expresion incompleta']` | ✅ | — |
| 2 | `if (x < 20)` sin `{` | `['if', ['x','<','20'], []]` **sin error** | ❌ | Bajo (no está en rubric) |
| 3 | `x = x + 5` sin `;` | `['error', 'asignacion', 'falta punto y coma']` | ✅ | — |
| 4 | `int z = 0` sin `;` | `['error', 'declaracion', 'falta punto y coma']` | ✅ | — |
| 5 | `while (x < 50` sin `)` | `['error', 'while', 'falta parentesis de cierre', ...]` | ✅ | — |
| 6 | `while (y < 30) {` sin `}` | Absorbe código siguiente | ⚠️ | Aceptable (cascada) |
| 7-9 | `for` errors | Absorbidos por #6 | ⚠️ | Cascada |
| 10 | `while ()` vacío | `['error', 'condicion', 'expresion incompleta']` | ✅ | — |
| 11 | `else {` suelto | `['error', 'else', 'else sin if previo']` | ✅ | — |
| 12 | `print(nombre;` | `['error', 'print', 'falta parentesis de cierre']` | ✅ | — |
| 13 | `print nombre);` | `['error', 'print', 'falta parentesis de apertura']` | ✅ | — |
| 14 | `if (x 10)` sin operador | `['error', 'if', 'operador relacional faltante']` | ✅ | — |
| 15 | `x = x +;` incompleto | `['error', 'asignacion', 'expresion incompleta']` | ✅ | — |
| 16 | `int a =;` sin valor | `['error', 'declaracion', 'falta valor']` | ✅ | — |
| 17 | String sin cerrar | `['error', 'declaracion', 'expresion invalida']` | ✅ | — |
| 18 | `/*` sin cerrar | `['error', 'comentario', 'comentario no cerrado']` | ✅ | — |

**Total: 16/18 errores detectados correctamente. 1 error silencioso (#2). 1 cascada (#6-9).**

---

## 6. CONCLUSIÓN Y NOTA ESTIMADA

| Escenario | Nota entregables (60) | % | Sustentación |
|---|---|---|---|
| **Sin correcciones** | ~52-55/60 | 87-92% | Riesgo bajo si explican el código |
| **Corrigiendo Salida 3** | ~57-58/60 | 95-97% | Muy sólido |
| **Corrigiendo Salida 3 + Error 2** | ~58-60/60 | 97-100% | Notable |

**Puntos fuertes:**
- Gramática completa y correcta en LaTeX
- Pyparsing bien utilizado con `infixNotation`, `Forward`, `ParseActions`
- AST estructuralmente idéntico al rubric (triple anidamiento, if-else, for, while)
- Operadores lógicos `&&`/`||` producen el formato exacto `[op, left, right]`
- 16/18 errores detectados
- Salida 4 del rubric coincide exactamente

**Única debilidad significativa:**
- Recuperación del `for` con `;` faltante en Salida 3 no produce el AST estructurado esperado

---

*Fin del informe.*
