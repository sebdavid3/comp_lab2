# Prompt para IA: Reescribir Parser MiniLang con Pyparsing

Copia todo lo de abajo y pégalo como prompt a tu IA.

---

## PROMPT INICIO

Necesito que me generes un archivo Python completo llamado `minilang_parser.py` que sea un **analizador sintáctico para el lenguaje MiniLang usando la librería pyparsing**.

### REQUISITOS CLAVE

1. **Todo el parsing debe usar pyparsing** — NO parser manual con peek/advance/expect/tokenize
2. **Pyparsing debe definir la gramática**: usar `Forward()`, `Group()`, `infixNotation()`, `Suppress()`, `ZeroOrMore()`, `Optional()`, `Keyword()`, `Regex()`, etc.
3. **Parse actions** (`setParseAction` / `addParseAction`) deben transformar los resultados al formato de AST requerido
4. **Recuperación de errores**: si hay un error sintáctico, el análisis debe continuar con la siguiente sentencia. Generar nodos `['error', tipo, mensaje]` para errores.
5. El código se ejecutará en Google Colab como un notebook `.ipynb`

### ESTRUCTURA DEL ARCHIVO

El archivo debe tener esta estructura exacta con comentarios de celda:

```
CELDA 1: Título (docstring con nombres de autores)
CELDA 2: Gramática Libre de Contexto en LaTeX (docstring markdown)
CELDA 3: Manual de uso (docstring markdown)
CELDA 4: Código del analizador (AQUÍ VA TODO EL CÓDIGO)
CELDA 5: Ejemplo de programa correcto (string + ejecución)
CELDA 6: Ejemplo de programa con errores (string + ejecución)
```

### GRAMÁTICA DE MINILANG

```
Programa     → Sentencia*
Sentencia    → Declaracion | Asignacion | IfStmt | WhileStmt | ForStmt 
             | PrintStmt | BreakStmt | ContinueStmt | PostfixStmt

Declaracion  → Tipo ID '=' Expr ';'
Tipo         → 'int' | 'float' | 'string'
Asignacion   → ID '=' Expr ';'
PostfixStmt  → ID ('++' | '--') ';'

IfStmt       → 'if' CondGroup Bloque ('else' Bloque)?
WhileStmt    → 'while' CondGroup Bloque
ForStmt      → 'for' '(' ForInit ';' Condicion ';' ForPaso? ')' Bloque
ForInit      → Tipo ID '=' Expr
ForPaso      → ID '++' | ID '--' | ID '=' Expr

PrintStmt    → 'print' '(' Expr ')' ';'
BreakStmt    → 'break' ';'
ContinueStmt → 'continue' ';'

CondGroup    → '(' Condicion ')' | Condicion
Condicion    → CondOr
CondOr       → CondAnd ('||' CondAnd)*
CondAnd      → CondNot ('&&' CondNot)*
CondNot      → '!' CondRel | CondRel
CondRel      → Expr OpRel Expr
OpRel        → '>' | '<' | '>=' | '<=' | '==' | '!='

Bloque       → '{' Sentencia* '}'

Expr         → Term (('+' | '-') Term)*
Term         → Factor (('*' | '/' | '%') Factor)*
Factor       → '(' Expr ')' | ENTERO | FLOTANTE | CADENA | ID
```

### FORMATO DEL AST (MUY IMPORTANTE)

El AST se representa como listas Python anidadas. Cada sentencia es una lista:

- **Declaración**: `['int', 'x', '10']` o `['float', 'y', '3.14']` o `['string', 'msg', '"Hola"']`
- **Asignación simple**: `['x', '5']`
- **Asignación con expresión**: `['z', 'z', '+', 'i']` (los tokens de la expresión se aplanan)
- **Postfix**: `['x', '++']`
- **Print**: `['print', 'mensaje']` o `['print', '"texto"']`
- **Break**: `['break']`
- **Continue**: `['continue']`
- **If sin else**: `['if', COND, BLOQUE]`
- **If con else**: `['if', COND, BLOQUE_THEN, BLOQUE_ELSE]`
- **While**: `['while', COND, BLOQUE]`
- **For**: `['for', [var, init_val, COND, STEP], BLOQUE]`

Donde:
- **COND simple**: `['x', '>=', '10']` o `['i', '<', '3']`
- **COND con &&**: `['&&', ['nombre', '==', '"Juan"'], ['estado', '==', '"activo"']]` (operador va PRIMERO)
- **COND con ||**: `['||', ['nombre', '!=', '""'], ['estado', '==', '"activo"']]` (operador va PRIMERO)
- **BLOQUE**: lista de sentencias envueltas: `[[stmt1], [stmt2], ...]` — cada sentencia dentro de su propia lista
- **STEP del for**: `['i', '++']` o `['i', '--']` o `['i', '=', 'i', '+', '2']`
- Si el paso del for está vacío y la condición usa `<` o `<=`, el paso por defecto es `[var, '++']`; si usa `>` o `>=`, es `[var, '--']`

### ERRORES SINTÁCTICOS

Cuando hay un error, generar nodos `['error', tipo, descripcion]`:
- Condición incompleta (`if (x > )`): `['error', 'condicion', 'expresion incompleta']`
- Falta `;` en for condición: `['error', 'condicion_for']`
- Falta `;` en asignación: `['error', 'asignacion', 'falta punto y coma']`
- Falta `)` en while: `['error', 'while', 'falta parentesis de cierre', COND, BLOQUE]`
- Falta `)` en print: `['error', 'print', 'falta parentesis de cierre']`

**El análisis DEBE continuar después de un error.**

### EJEMPLOS DE ENTRADA/SALIDA EXACTOS

#### Código 1 (sin errores):
```
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
/* comentario multilinea */
while (x < 20) {
    x++;
}
```

**Salida esperada:**
```
Código Válido

Árbol de Análisis Sintáctico
[
  ['int', 'x', '10'],
  ['float', 'y', '3.14'],
  ['string', 'mensaje', '"Hola mundo"'],
  ['if', ['x', '>=', '10'], [[['print', 'mensaje']]]],
  ['for', ['i', '0', ['i', '<', '5'], ['i', '++']], [[['if', ['i', '<', '3'], [[['print', 'i']]]]]]],
  ['while', ['x', '<', '20'], [[['x', '++']]]]
]
```

#### Código 2 (sin errores):
```
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
}
```

**Salida esperada:**
```
Código Válido

Árbol de Análisis Sintáctico
[
  ['int', 'x', '5'],
  ['int', 'y', '10'],
  ['int', 'z', '0'],
  ['if',
    ['x', '<', 'y'],
    [
      [['if',
        ['y', '>', '5'],
        [[['print', 'y']]],
        [[['print', 'x']]]
      ]]
    ],
    [
      [['if',
        ['x', '==', '5'],
        [[['z', 'x', '+', 'y']]],
        [[['z', '0']]]
      ]]
    ]
  ],
  ['while',
    ['x', '<', '10'],
    [
      [['for',
        ['i', '0', ['i', '<', '3'], ['i', '++']],
        [[['z', 'z', '+', 'i']]]
      ]],
      [['x', '++']]
    ]
  ]
]
```

#### Código 3 (con errores):
```
int x = 10;
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
```

**Salida esperada:**
```
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
        [[['error', 'asignacion', 'falta punto y coma']]]
      ]
    ],
    [[['print', 'y']]]
  ],
  ['error', 'while', 'falta parentesis de cierre',
    ['x', '<', '20'],
    [[['x', '++']]]
  ]
]
```

#### Código 4 (con errores):
```
string nombre = "Juan";
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
}
```

**Salida esperada:**
```
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
    [[['print', 'nombre']]],
    [[['print', '"inactivo"']]]
  ],
  ['while',
    ['||',
      ['nombre', '!=', '""'],
      ['estado', '==', '"activo"']
    ],
    [
      [['nombre', 'nombre', '+', '"!"']],
      [['error', 'asignacion', 'falta punto y coma']],
      [['error', 'print', 'falta parentesis de cierre']]
    ]
  ]
]
```

### CONSIDERACIONES TÉCNICAS

1. **Comentarios**: Eliminar `//` y `/* */` antes de parsear
2. **Strings**: soportar comillas simples `'texto'` y dobles `"texto"`
3. **Anidamiento**: if dentro de for, for dentro de while, etc.
4. **Condiciones sin paréntesis**: `if x > 3 { ... }` es válido (paréntesis opcionales)
5. **`remove_comments()`**: función manual que elimina comentarios respetando strings
6. **Formato de impresión**: usar `format_tree()` y `print_tree()` para imprimir el AST con indentación

### ENFOQUE PARA LA RECUPERACIÓN DE ERRORES

Dado que pyparsing no tiene recuperación nativa, usa este enfoque:

1. **Tokenizar** el código con pyparsing (`scanString`)
2. **Intentar parsear** el programa completo primero
3. **Si falla**, usar un parser que procese token por token con la gramática pyparsing:
   - Detectar qué tipo de sentencia es (por el primer token: `if`, `while`, `for`, tipo, identificador, etc.)
   - Intentar parsear cada componente con las reglas pyparsing correspondientes
   - Si un componente falla, generar nodo error y avanzar al siguiente punto de sincronización (`;`, `}`)
   - Continuar con la siguiente sentencia

### LO QUE NO DEBE TENER EL CÓDIGO

- NO usar un parser manual con `peek()`, `advance()`, `expect()`, `at_end()`
- NO tokenizar manualmente y luego recorrer token por token
- La gramática DEBE estar definida con elementos de pyparsing (`Forward`, `Group`, `infixNotation`, etc.)
- Los parse actions deben transformar el resultado al formato AST

### INSTRUCCIÓN FINAL

Genera el archivo completo `minilang_parser.py` con todo el código. Al ejecutar `python minilang_parser.py`, debe mostrar las salidas de Celda 5 (programa correcto) y Celda 6 (programa con errores) con el formato de AST exacto descrito arriba. La salida debe coincidir lo más posible con los ejemplos dados.

## PROMPT FIN
