# -*- coding: utf-8 -*-
r"""
# CELDA 1: Título
MINILANG - Analizador Sintáctico con PyParsing
Autores: Daniel Cruzado, Daniel Gomez, Sebastian Ibañez y Angelo Martinez
NRC: [COMPLETAR NRC]

# CELDA 2: Gramática Libre de Contexto en LaTeX
## Gramática Libre de Contexto (GLC) para MiniLang

$$
\begin{aligned}
\text{Programa}     &\rightarrow \text{Sentencia}^{*} \\
\text{Sentencia}    &\rightarrow \text{Declaracion} \mid \text{Asignacion} \mid \text{IfStmt} \mid \text{WhileStmt} \mid \text{ForStmt} \\
                   &\qquad   \mid \text{PrintStmt} \mid \text{BreakStmt} \mid \text{ContinueStmt} \mid \text{PostfixStmt} \\[4pt]
\text{Declaracion}  &\rightarrow \text{Tipo} \; \text{ID} \; '=' \; \text{Expr} \; ';' \\
\text{Tipo}        &\rightarrow \text{'int'} \mid \text{'float'} \mid \text{'string'} \\
\text{Asignacion}  &\rightarrow \text{ID} \; '=' \; \text{Expr} \; ';' \\
\text{PostfixStmt} &\rightarrow \text{ID} \; ('++' \mid '--') \; ';' \\[4pt]
\text{IfStmt}      &\rightarrow \text{'if'} \; \text{CondGroup} \; \text{Bloque} \; (\text{'else'} \; \text{Bloque})? \\
\text{WhileStmt}   &\rightarrow \text{'while'} \; \text{CondGroup} \; \text{Bloque} \\
\text{ForStmt}     &\rightarrow \text{'for'} \; '(' \; \text{ForInit} \; ';' \; \text{Condicion} \; ';' \; \text{ForPaso}? \; ')' \; \text{Bloque} \\
\text{ForInit}     &\rightarrow \text{Tipo} \; \text{ID} \; '=' \; \text{Expr} \\
\text{ForPaso}     &\rightarrow \text{ID} \; '++' \mid \text{ID} \; '--' \mid \text{ID} \; '=' \; \text{Expr} \\[4pt]
\text{PrintStmt}   &\rightarrow \text{'print'} \; '(' \; \text{Expr} \; ')' \; ';' \\
\text{BreakStmt}   &\rightarrow \text{'break'} \; ';' \\
\text{ContinueStmt}&\rightarrow \text{'continue'} \; ';' \\[4pt]
\text{CondGroup}   &\rightarrow '(' \; \text{Condicion} \; ')' \mid \text{Condicion} \\
\text{Condicion}   &\rightarrow \text{CondOr} \\
\text{CondOr}      &\rightarrow \text{CondAnd} \; (\text{'||'} \; \text{CondAnd})^{*} \\
\text{CondAnd}     &\rightarrow \text{CondNot} \; (\text{'\&\&'} \; \text{CondNot})^{*} \\
\text{CondNot}     &\rightarrow \text{'!'} \; \text{CondRel} \mid \text{CondRel} \\
\text{CondRel}     &\rightarrow \text{Expr} \; \text{OpRel} \; \text{Expr} \\
\text{OpRel}       &\rightarrow \text{'>'} \mid \text{'<'} \mid \text{'>='} \mid \text{'<='} \mid \text{'=='} \mid \text{'!='} \\[4pt]
\text{Bloque}     &\rightarrow \text{'\{} \;} \text{Sentencia}^{*} \; \text{'\}'} \\[4pt]
\text{Expr}       &\rightarrow \text{Term} \; (( \text{'+'} \mid \text{'--'} ) \; \text{Term})^{*} \\
\text{Term}       &\rightarrow \text{Factor} \; (( \text{'*'} \mid \text{'/'} \mid \text{'\%'} ) \; \text{Factor})^{*} \\
\text{Factor}     &\rightarrow '(' \; \text{Expr} \; ')' \mid \text{ENTERO} \mid \text{FLOTANTE} \mid \text{CADENA} \mid \text{ID}
\end{aligned}
$$

# CELDA 3: Manual de uso
## Manual de Uso

### Descripción
MiniLang es un lenguaje de programación imperativo minimalista con tipos
int, float y string, que soporta declaraciones, asignaciones, estructuras
de control (if, while, for), impresión (print), y sentencias break/continue.

### Uso del analizador
```python
from minilang_parser import MiniLangParser

parser = MiniLangParser()
# Se debe pasar la ruta de un archivo de texto con el código fuente
tree, has_errors = parser.parse("codigo_minilang.txt")

if has_errors:
    print("Errores de sintaxis")
else:
    print("Código Válido")

print("\nÁrbol de Análisis Sintáctico")
print_tree(tree)
```

### Tipos de datos
- `int`: números enteros
- `float`: números de punto flotante
- `string`: cadenas de texto (comillas simples o dobles)

### Estructuras de control
- `if (cond) { ... } else { ... }` (else opcional)
- `while (cond) { ... }`
- `for (init; cond; paso) { ... }`

### Comentarios
- `// comentario de línea`
- `/* comentario multilínea */

### Impresión
- `print(expr);`

### Instalación de dependencias
```bash
pip install pyparsing
```
"""

import re
import sys
from pyparsing import (
    Forward, Group, Suppress, ZeroOrMore, Optional, OneOrMore,
    Keyword, Regex, oneOf, opAssoc, infixNotation,
    ParseException, ParseResults, SkipTo, Literal,
    StringStart, StringEnd, White, Word, alphanums, alphas,
    MatchFirst, And, Or, ParserElement, FollowedBy, NotAny
)

# ────────────────────────────────────────────────────────────
# CELDA 4: Código del analizador
# ────────────────────────────────────────────────────────────


def remove_comments(code):
    """Remove // and /* */ comments, respecting string literals."""
    result = []
    i = 0
    in_string = False
    string_char = None
    while i < len(code):
        if not in_string:
            # Check for string start
            if code[i] in ('"', "'"):
                in_string = True
                string_char = code[i]
                result.append(code[i])
                i += 1
                continue
            # Check for single-line comment
            if code[i] == '/' and i + 1 < len(code) and code[i + 1] == '/':
                i += 2
                while i < len(code) and code[i] != '\n':
                    i += 1
                continue
            # Check for multi-line comment
            if code[i] == '/' and i + 1 < len(code) and code[i + 1] == '*':
                i += 2
                while i + 1 < len(code) and not (code[i] == '*' and code[i + 1] == '/'):
                    i += 1
                i += 2
                continue
            result.append(code[i])
        else:
            result.append(code[i])
            # Handle escaped characters inside strings
            if code[i] == '\\':
                i += 1
                if i < len(code):
                    result.append(code[i])
                i += 1
                continue
            if code[i] == string_char:
                in_string = False
                string_char = None
        i += 1
    return ''.join(result)


def flatten_parse(tokens):
    """Flatten nested ParseResults into a flat list of strings."""
    result = []
    for t in tokens:
        if isinstance(t, (list, ParseResults)):
            result.extend(flatten_parse(t))
        else:
            result.append(str(t))
    return result


class MiniLangParser:
    """Parser for MiniLang language using pyparsing."""

    def __init__(self):
        # Suppress all whitespace by default
        ParserElement.setDefaultWhitespaceChars(' \t\n\r')
        self._build_grammar()
        self._build_recovery_grammar()

    # ── Parse Actions ──────────────────────────────────────

    @staticmethod
    def _flatten_expr(tokens):
        """Flatten infixNotation result for arithmetic expressions."""
        return flatten_parse(tokens)

    @staticmethod
    def _make_rel_cond(tokens):
        """Transform relational condition to flat AST: [left, op, right]."""
        return flatten_parse(tokens)

    @staticmethod
    def _make_binop_cond(op_symbol):
        """Create parse action for && and || conditions: [op, left, right]."""
        def parse_action(tokens):
            items = tokens[0]
            # items is like [[left, op, right]]
            # Need to extract left, op, right and transform
            if len(items) == 3 and items[1] == op_symbol:
                left = items[0]
                right = items[2]
                # Ensure left and right are proper AST nodes
                if isinstance(left, ParseResults):
                    left = left.asList()
                if isinstance(right, ParseResults):
                    right = right.asList()
                return [op_symbol, left, right]
            # Fallback: flatten
            return flatten_parse(tokens)
        return parse_action

    @staticmethod
    def _condition_to_ast(tokens):
        """
        Convert condition infixNotation result to AST format.

        infixNotation with cond_rel = Group(expr + OP_REL + expr) | Group(expr):
          Normal (x>3):     [['x', '>', '3']]
          Re-parse (x>3):   ['x', '>', '3']   (from nested parens)
          Bare (x):         [['x']]
          NOT (!x):         [['!', ['x']]]  or  ['!', 'x'] (re-parse)
          NOT rel (!(x>3)): [['!', ['x', '>', '3']]]
          Compound:         [[['!', ['x']], '&&', ['y', '>', '0']]]

        AST format:
          Simple: ['x', '>', '3']
          NOT bare: ['!', 'x']
          NOT rel: ['!', ['x', '>', '3']]
          Compound: ['&&', ['!', 'x'], ['y', '>', '0']]
        """
        if isinstance(tokens, ParseResults):
            tokens = tokens.asList()

        if not tokens:
            return []

        # ── Handle flat re-parse: tokens IS the condition (from nested parens) ──
        # e.g. tokens = ['x', '>', '3']  (not wrapped in another list)
        if len(tokens) >= 3:
            # Check for simple relational: [left, relop, right]
            if (isinstance(tokens[1], str)
                    and tokens[1] in ('>', '<', '>=', '<=', '==', '!=')):
                return MiniLangParser._flatten_rel(tokens[:3])
            # Check for compound with && or ||
            if any(isinstance(x, str) and x in ('&&', '||') for x in tokens):
                return MiniLangParser._build_compound(tokens)

        # ── Handle flat NOT re-parse: tokens = ['!', 'x'] or ['!', 'x', '>', '3'] ──
        if len(tokens) >= 2 and tokens[0] == '!':
            if len(tokens) == 2:
                # ['!', ['x']] or ['!', 'x'] — bare operand
                operand = tokens[1]
                if isinstance(operand, list) and len(operand) == 1:
                    return ['!', str(operand[0])]
                return ['!', str(operand)]
            else:
                # ['!', 'x', '>', '3'] — NOT on relational (flat, no nesting)
                operand_tokens = tokens[1:]
                if (len(operand_tokens) == 3
                        and isinstance(operand_tokens[1], str)
                        and operand_tokens[1] in ('>', '<', '>=', '<=', '==', '!=')):
                    return ['!', MiniLangParser._flatten_rel(operand_tokens)]
                return ['!'] + flatten_parse(operand_tokens)

        # ── Normal infixNotation: tokens = [result] ──
        result = tokens[0] if len(tokens) >= 1 else tokens
        if isinstance(result, ParseResults):
            result = result.asList()

        if not isinstance(result, list):
            return [str(result)]

        # Unary NOT: ['!', operand] (nested)
        if len(result) >= 2 and result[0] == '!':
            if len(result) == 2:
                operand = result[1]
                if isinstance(operand, list):
                    if len(operand) == 1 and isinstance(operand[0], (str, int, float)):
                        return ['!', str(operand[0])]
                    if (len(operand) == 3 and isinstance(operand[1], str)
                            and operand[1] in ('>', '<', '>=', '<=', '==', '!=')):
                        return ['!', MiniLangParser._flatten_rel(operand)]
                    if len(operand) >= 3 and any(
                            isinstance(x, str) and x in ('&&', '||') for x in operand):
                        return ['!', MiniLangParser._build_compound(operand)]
                return ['!', str(operand)]
            else:
                # Flat list: ['!', 'x', '>', '3'] → ['!', ['x', '>', '3']]
                operand_tokens = result[1:]
                if (len(operand_tokens) == 3 and isinstance(operand_tokens[1], str)
                        and operand_tokens[1] in ('>', '<', '>=', '<=', '==', '!=')):
                    return ['!', MiniLangParser._flatten_rel(operand_tokens)]
                return ['!'] + flatten_parse(operand_tokens)

        # Simple relational: [left, relop, right]
        if (len(result) == 3 and isinstance(result[1], str)
                and result[1] in ('>', '<', '>=', '<=', '==', '!=')):
            return MiniLangParser._flatten_rel(result)

        # Compound with && or ||
        if len(result) >= 3 and any(
                isinstance(x, str) and x in ('&&', '||') for x in result):
            return MiniLangParser._build_compound(result)

        # Bare expression: ['x'] → 'x'
        if len(result) == 1:
            return flatten_parse(result)

        return flatten_parse(result)

    # Need _build_compound helper defined inside the class
    @staticmethod
    def _build_compound(expr_list):
        """Build compound condition from infixNotation list."""
        # expr_list = [left, op, right, ...] from infixNotation
        if not expr_list or len(expr_list) < 3:
            return expr_list

        # Take leftmost: left op right
        left = expr_list[0]
        op = expr_list[1]
        right = expr_list[2]

        # Convert left and right to proper AST format
        if isinstance(left, ParseResults):
            left = left.asList()
        if isinstance(right, ParseResults):
            right = right.asList()

        # Convert sub-conditions
        left = MiniLangParser._normalize_cond_subexpr(left) if isinstance(left, list) else left
        right = MiniLangParser._normalize_cond_subexpr(right) if isinstance(right, list) else right

        result = [op, left, right]

        # Chain remaining operators (right-associative style)
        rest = expr_list[3:]
        if rest:
            return MiniLangParser._build_compound([result] + rest)

        return result

    @staticmethod
    def _normalize_cond_subexpr(expr):
        """Normalize a condition sub-expression to proper AST format.

        Handles:
          ['x']            → 'x' (bare expr)
          ['!', ['x']]     → ['!', 'x'] (NOT on bare)
          ['!', ['x','>','3']] → ['!', ['x','>','3']] (NOT on rel)
          [['x','>','1'],'&&',['y','<','2']] → compound via _build_compound
          ['x', '>', '3']  → ['x', '>', '3'] (relational, already correct)
        """
        if not isinstance(expr, list):
            return expr

        # Bare expression: ['x'] → 'x'
        if len(expr) == 1 and isinstance(expr[0], (str, int, float)):
            return str(expr[0])

        # NOT expression: ['!', operand]
        if len(expr) == 2 and expr[0] == '!':
            operand = expr[1]
            if isinstance(operand, list):
                if len(operand) == 1 and isinstance(operand[0], (str, int, float)):
                    return ['!', str(operand[0])]
                if (len(operand) == 3 and isinstance(operand[1], str)
                        and operand[1] in ('>', '<', '>=', '<=', '==', '!=')):
                    return ['!', MiniLangParser._flatten_rel(operand)]
                if len(operand) >= 3 and any(
                        isinstance(x, str) and x in ('&&', '||') for x in operand):
                    return ['!', MiniLangParser._build_compound(operand)]
            return ['!', str(operand)]

        # Compound with && or ||
        if len(expr) >= 3 and any(
                isinstance(x, str) and x in ('&&', '||') for x in expr):
            return MiniLangParser._build_compound(expr)

        # Relational or other list: flatten
        if len(expr) == 3 and isinstance(expr[1], str) and expr[1] in ('>', '<', '>=', '<=', '==', '!='):
            return MiniLangParser._flatten_rel(expr)

        return flatten_parse([expr])

    @staticmethod
    def _flatten_rel(rel_list):
        """Flatten a relational expression to simple tokens."""
        if len(rel_list) == 3:
            left = rel_list[0]
            op = rel_list[1]
            right = rel_list[2]
            left_tokens = flatten_parse([left]) if isinstance(left, (list, ParseResults)) else [str(left)]
            right_tokens = flatten_parse([right]) if isinstance(right, (list, ParseResults)) else [str(right)]
            return left_tokens + [op] + right_tokens
        return flatten_parse([rel_list])

    @staticmethod
    def _make_decl(tokens):
        """Transform declaration.

        Grammar: Group(TIPO + ID + EQ + expr + SEMI)
        items = [tipo, id, expr_result]

        Expected AST:
          Simple: ['int', 'x', '10']
          With expr: ['int', 'x', '5', '+', '3']
        """
        items = tokens[0]
        tipo = str(items[0])
        id_ = str(items[1])
        # Expression value - flatten to tokens
        expr_val = items[2]
        val_tokens = flatten_parse([expr_val]) if isinstance(expr_val, (list, ParseResults)) else [str(expr_val)]
        if len(val_tokens) == 1:
            return [tipo, id_, val_tokens[0]]
        else:
            return [tipo, id_] + val_tokens

    @staticmethod
    def _left_nest(flat_list):
        """Convert flat infixNotation list to left-nested form.

        pyparsing's infixNotation produces flat lists for same-precedence
        chained operators: [a, op1, b, op2, c]
        Left-nesting: [[a, op1, b], op2, c]

        For [a]:                           → a (identity)
        For [a, op, b]:                    → [a, op, b] (no change)
        For [a, op1, b, op2, c]:           → [[a, op1, b], op2, c]
        For [[x,'*','y'], '+', 'z', '-', w]: → [[[x,'*','y'],'+','z'],'-',w]
        """
        if not isinstance(flat_list, list) or len(flat_list) < 3:
            return flat_list
        result = flat_list[0]
        for i in range(1, len(flat_list), 2):
            result = [result, flat_list[i], flat_list[i + 1]]
        return result

    @staticmethod
    def _make_assign(tokens):
        """Transform assignment.

        Grammar: Group(ID + EQ + expr + SEMI)
        items = [id, expr_result]

        expr_result from infixNotation:
          Simple: [['3']]        → keep as '3'
          Binary: [['10','+','5']] → keep as ['10','+','5']
          Nested: [[[...],'+',...]]  → keep nested structure
        """
        items = tokens[0]
        id_ = str(items[0])
        expr_val = items[1]
        if isinstance(expr_val, ParseResults):
            expr_val = expr_val.asList()
        # expr_val is a list from infixNotation
        if isinstance(expr_val, list):
            # For simple single value: [['3']] → extract '3'
            if len(expr_val) == 1 and isinstance(expr_val[0], list) and len(expr_val[0]) == 1:
                return [id_, str(expr_val[0][0])]
            # For infixNotation result wrapped in extra list: [[...]]
            if len(expr_val) == 1 and isinstance(expr_val[0], list):
                inner = expr_val[0]
                # Left-nest flat operator lists to preserve precedence
                nested = MiniLangParser._left_nest(inner)
                return [id_] + nested
            # For already-flat: [...] (less common)
            return [id_] + MiniLangParser._left_nest(expr_val)
        return [id_, str(expr_val)]

    @staticmethod
    def _make_postfix(tokens):
        """Transform postfix: ['x', '++']"""
        items = tokens[0]
        return [str(items[0]), str(items[1])]

    @staticmethod
    def _make_print(tokens):
        """Transform print: ['print', 'mensaje']"""
        items = tokens[0]
        # items[0] is 'print', items[1] is the expression
        expr_tokens = []
        for t in items[1:]:
            if isinstance(t, (list, ParseResults)):
                expr_tokens.extend(flatten_parse([t]))
            else:
                expr_tokens.append(str(t))
        expr_str = ' '.join(expr_tokens) if len(expr_tokens) > 1 else (expr_tokens[0] if expr_tokens else '')
        return ['print', expr_str]

    @staticmethod
    def _make_break(tokens):
        return ['break']

    @staticmethod
    def _make_continue(tokens):
        return ['continue']

    @staticmethod
    @staticmethod
    def _make_if(tokens):
        """Transform if: ['if', COND, THEN] or ['if', COND, THEN, ELSE]

        Grammar: Group(Keyword('if') + cond_group + bloque + Optional(Keyword('else') + bloque))
        Keyword('else') is NOT suppressed. Items may have spread block parts.
        """
        items = tokens[0]
        result = ['if']
        cond = items[1]
        if isinstance(cond, ParseResults):
            cond = cond.asList()
        result.append(cond)

        # Find 'else' to split then/else block parts
        else_idx = None
        for i, item in enumerate(items):
            if isinstance(item, str) and item == 'else':
                else_idx = i
                break

        def _collect_block(raw_parts):
            """Collect spread block parts and normalize.
            
            When pyparsing spreads a multi-stmt block, each part is [[stmt]].
            We must keep that wrapping so the final block is [[[stmt1]], [[stmt2]]].
            For single-stmt blocks, we still need [[[stmt]]] format.
            """
            parts = []
            for p in raw_parts:
                if isinstance(p, ParseResults):
                    p = p.asList()
                parts.append(p)
            if len(parts) >= 2:
                return parts  # Keep wrapping intact
            if parts:
                # Single part: wrap in extra list to get [[[stmt]]]
                return [parts[0]]
            return []

        # Then-block: items[2:else_idx] or items[2:]
        then_parts = list(items[2:else_idx]) if else_idx else list(items[2:])
        result.append(_collect_block(then_parts))

        # Else-block: items[else_idx+1:]
        if else_idx:
            else_parts = list(items[else_idx + 1:])
            result.append(_collect_block(else_parts))

        return result

    @staticmethod
    def _make_while(tokens):
        """Transform while: ['while', COND, BLOQUE]"""
        items = tokens[0]
        cond = items[1]
        if isinstance(cond, ParseResults):
            cond = cond.asList()
        # Collect block parts (may be spread by And for multi-stmt)
        block_parts = []
        for item in items[2:]:
            if isinstance(item, ParseResults):
                item = item.asList()
            block_parts.append(item)
        if len(block_parts) >= 2:
            block = block_parts  # Keep wrapping intact
        elif block_parts:
            block = [block_parts[0]]  # Wrap single-stmt: [[[stmt]]]
        else:
            block = []
        return ['while', cond, block]

    def _make_for(self, tokens):
        """Transform for: ['for', [var, init_val, COND, STEP], BLOQUE]

        Grammar: Group(Keyword('for') + LPAR + for_init + SEMI
                       + Group(condition) + SEMI
                       + Optional(for_paso) + RPAR + bloque)
        Suppressed: LPAR, SEMI(x2), RPAR

        _make_block raw list gets spread. Need to detect whether
        items[3] is for_paso or the first block part.
        """
        def _looks_like_paso(item):
            """Check if item is a paso (['i', '++']) vs block part ([[['stmt']]])."""
            return (isinstance(item, (list, ParseResults))
                    and len(item) > 0
                    and isinstance(item[0], str))

        items = tokens[0]

        init_group = items[1]
        if isinstance(init_group, ParseResults):
            init_group = init_group.asList()

        var_name = str(init_group[1])  # ID
        # init_group[2] is the expr result from infixNotation
        init_expr = init_group[2]
        if isinstance(init_expr, ParseResults):
            init_expr = init_expr.asList()
        # Flatten init value to tokens
        init_val_tokens = flatten_parse([init_expr]) if isinstance(init_expr, list) else [str(init_expr)]
        init_val = ' '.join(init_val_tokens) if len(init_val_tokens) > 1 else (init_val_tokens[0] if init_val_tokens else '')

        # items[2] = Group(condition) — unwrap the Group
        cond = items[2]
        if isinstance(cond, ParseResults):
            cond = cond.asList()
        # Group(condition) wraps it: [['i', '<', '5']] → strip to ['i', '<', '5']
        if isinstance(cond, list) and len(cond) == 1:
            cond = cond[0]

        # Detect paso: items[3] is paso if it looks like ['i', '++'] or ['i', '=', ...]
        step = None
        block_start = 3
        if len(items) > 3 and _looks_like_paso(items[3]):
            step_item = items[3]
            if isinstance(step_item, ParseResults):
                step = step_item.asList()
                step = flatten_parse([step])
            else:
                step = [str(step_item)]
            block_start = 4

        # Default step logic if no step provided
        if step is None:
            step = self._default_step(var_name, cond)

        # Collect block parts (may be spread if multiple stmts)
        block_parts = []
        for item in items[block_start:]:
            if isinstance(item, ParseResults):
                item = item.asList()
            block_parts.append(item)
        if len(block_parts) >= 2:
            block = block_parts  # Keep wrapping intact
        elif block_parts:
            block = [block_parts[0]]  # Wrap single-stmt: [[[stmt]]]
        else:
            block = []

        return ['for', [var_name, init_val, cond, step], block]

    def _default_step(self, var_name, cond):
        """Generate default step based on condition operator.
        
        Según la especificación: si no hay paso explícito, debe mostrar
        su valor como 1 si es incremento o -1 si es decremento.
        """
        if isinstance(cond, list) and len(cond) >= 3:
            # Check for relational operators in the condition to infer direction
            # For conditions like (i < 5), operator is at index 1 or within nested list
            flat_cond = flatten_parse([cond])
            if any(op in flat_cond for op in ('>', '>=')):
                return -1
        return 1

    @staticmethod
    def _normalize_block_parts(raw_list):
        """Normalize block elements: strip one [] from each if double-wrapped.
        
        _make_block wraps as [[stmt]] (2 []). ParseResults unwraps once for
        1-stmt blocks but NOT for multi-stmt blocks. This fixes multi-stmt
        by detecting [[stmt]] pattern and reducing to [stmt].
        """
        result = []
        for el in raw_list:
            if isinstance(el, ParseResults):
                el = el.asList()
            if isinstance(el, list) and len(el) == 1 and isinstance(el[0], list):
                # [[stmt]] → [stmt]
                result.append(el[0])
            else:
                result.append(el)
        return result

    @staticmethod
    def _make_block(tokens):
        """Transform block: list of statements.

        Block grammar: Group(LBRACE + ZeroOrMore(Group(stmt)) + RBRACE)
        """
        items = tokens[0]
        result = []
        for item in items:
            if item is not None and item != '':
                if isinstance(item, ParseResults):
                    item_list = item.asList()
                    if item_list:
                        # Modified to match the expected [[stmt]] format in blocks
                        result.append([item_list])
                    else:
                        result.append([item_list])
                else:
                    # Single statement already in list format
                    result.append([item])
        return result

    # ── Grammar Construction ───────────────────────────────

    def _build_grammar(self):
        """Build the complete pyparsing grammar for MiniLang."""
        # ── Basic Tokens ──
        self.FLOTANTE = Regex(r'\d+\.\d+').setName('flotante')
        self.ENTERO = Regex(r'\d+').setName('entero')
        self.CADENA = Regex(r"'[^']*'|\"[^\"]*\"").setName('cadena')
        self.ID = Regex(r'[a-zA-Z_][a-zA-Z0-9_]*').setName('identificador')

        self.TIPO = Keyword('int') | Keyword('float') | Keyword('string')

        self.OP_ADD = oneOf('+ -')
        self.OP_MUL = oneOf('* / %')
        self.OP_REL = oneOf('> < >= <= == !=')
        self.OP_INC = oneOf('++ --')
        self.OP_AND = Keyword('&&')
        self.OP_OR = Keyword('||')
        self.OP_NOT = Literal('!')

        # Suppressed delimiters
        LPAR, RPAR = map(Suppress, '()')
        LBRACE, RBRACE = map(Suppress, '{}')
        SEMI = Suppress(';')
        EQ = Suppress('=')

        # ── Forward Declarations ──
        expr = Forward()
        condition = Forward()
        bloque = Forward()
        stmt = Forward()

        # ── Expression (Arithmetic) ──
        atom_paren = LPAR + expr + RPAR

        expr_atom = self.FLOTANTE | self.ENTERO | self.CADENA | self.ID | atom_paren

        expr << infixNotation(
            expr_atom,
            [
                (self.OP_MUL, 2, opAssoc.LEFT),
                (self.OP_ADD, 2, opAssoc.LEFT),
            ]
        )

        # ── Condition ──
        # cond_rel: relational condition like x >= 10, or bare expression like x
        # Bare expr alternative needed for !x (NOT on a plain variable)
        # IMPORTANT: No flattening parse action here. The Group preserves
        # structure so infixNotation can properly nest with &&/||.
        cond_rel = Group(expr + self.OP_REL + expr) | Group(expr)

        condition << infixNotation(
            cond_rel,
            [
                (self.OP_NOT, 1, opAssoc.RIGHT),
                (self.OP_AND, 2, opAssoc.LEFT),
                (self.OP_OR, 2, opAssoc.LEFT),
            ]
        ).setParseAction(self._condition_to_ast)

        # Optional parentheses around conditions.
        # MUST use Group to prevent condition's 3-element result from flattening
        cond_group = Group(LPAR + condition + RPAR) | Group(condition)

        # ── Block ──
        bloque << Group(
            LBRACE +
            ZeroOrMore(Group(stmt)) +
            RBRACE
        ).setParseAction(self._make_block)

        # ── Statements ──
        # Declaration: Tipo ID = Expr ;
        decl_stmt = Group(
            self.TIPO + self.ID + EQ + expr + SEMI
        ).setParseAction(self._make_decl)

        # Assignment: ID = Expr ;
        assign_stmt = Group(
            self.ID + EQ + expr + SEMI
        ).setParseAction(self._make_assign)

        # Postfix: ID ++ ; | ID -- ;
        postfix_stmt = Group(
            self.ID + self.OP_INC + SEMI
        ).setParseAction(self._make_postfix)

        # Print: print ( Expr ) ;
        print_stmt = Group(
            Keyword('print') + LPAR + expr + RPAR + SEMI
        ).setParseAction(self._make_print)

        # Break: break ;
        break_stmt = Group(
            Keyword('break') + SEMI
        ).setParseAction(self._make_break)

        # Continue: continue ;
        continue_stmt = Group(
            Keyword('continue') + SEMI
        ).setParseAction(self._make_continue)

        # If: if CondGroup Bloque (else Bloque)?
        if_stmt = Forward()
        if_stmt << Group(
            Keyword('if') +
            cond_group +
            bloque +
            Optional(Keyword('else') + bloque)
        ).setParseAction(self._make_if)

        # While: while CondGroup Bloque
        while_stmt = Forward()
        while_stmt << Group(
            Keyword('while') +
            cond_group +
            bloque
        ).setParseAction(self._make_while)

        # For: for ( ForInit ; Condicion ; ForPaso? ) Bloque
        for_init = Group(self.TIPO + self.ID + EQ + expr)
        # Use Literal('=') not EQ (Suppress) because '=' is needed in AST output
        for_paso = Group(self.ID + (self.OP_INC | (Literal('=') + expr)))

        for_stmt = Forward()
        for_stmt << Group(
            Keyword('for') + LPAR +
            for_init + SEMI +
            Group(condition) + SEMI +
            Optional(for_paso) +
            RPAR +
            bloque
        ).setParseAction(self._make_for)

        # Statement: any of the above
        stmt << (
            decl_stmt |
            assign_stmt |
            postfix_stmt |
            if_stmt |
            while_stmt |
            for_stmt |
            print_stmt |
            break_stmt |
            continue_stmt
        )

        # Program: zero or more statements
        self.program = ZeroOrMore(Group(stmt))

        # Store references for recovery parser
        self._expr = expr
        self._condition = condition
        self._cond_group = cond_group
        self._bloque = bloque
        self._decl_stmt = decl_stmt
        self._assign_stmt = assign_stmt
        self._postfix_stmt = postfix_stmt
        self._print_stmt = print_stmt
        self._break_stmt = break_stmt
        self._continue_stmt = continue_stmt
        self._if_stmt = if_stmt
        self._while_stmt = while_stmt
        self._for_stmt = for_stmt
        self._stmt = stmt

    def _build_recovery_grammar(self):
        """Build grammar for token scanning used in error recovery."""
        # Token scanner - all possible tokens
        self.token_scanner = (
            self.FLOTANTE |
            self.ENTERO |
            self.CADENA |
            self.TIPO |
            Keyword('if') |
            Keyword('else') |
            Keyword('while') |
            Keyword('for') |
            Keyword('print') |
            Keyword('break') |
            Keyword('continue') |
            self.ID |
            oneOf('++ --') |
            oneOf('&& || !') |
            self.OP_REL |
            self.OP_ADD |
            self.OP_MUL |
            oneOf('= ( ) { } ; ,')
        )

    # ── Comment Removal ──

    @staticmethod
    def remove_comments(code):
        return remove_comments(code)

    # ── Parsing ──

    def parse(self, file_path):
        """
        Parse MiniLang code from a file and return (tree, has_errors).

        Args:
            file_path: Path to the file containing MiniLang source code.

        Returns:
            Tuple of (tree, has_errors) where tree is a list of AST nodes
            and has_errors is True if any syntax errors were found.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        code = self.remove_comments(code)

        # Try full grammar parse first
        try:
            result = self.program.parseString(code, parseAll=True)
            tree = result.asList()
            return (tree, False)
        except ParseException:
            # Fall back to error-recovery parsing
            return self._parse_with_recovery(code)

    def parse_file(self, filepath):
        """
        Parse MiniLang code from a file.

        Args:
            filepath: Path to file containing MiniLang source code.

        Returns:
            Tuple of (tree, has_errors) where tree is a list of AST nodes
            and has_errors is True if any syntax errors were found.
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        return self.parse(code)

    def _parse_with_recovery(self, code):
        """Parse with error recovery, generating error nodes for bad statements."""
        tree = []
        has_errors = False
        pos = 0
        code_len = len(code)
        max_iterations = 10000
        iteration = 0

        while pos < code_len:
            iteration += 1
            if iteration > max_iterations:
                has_errors = True
                break
            # Skip whitespace
            while pos < code_len and code[pos] in ' \t\n\r':
                pos += 1
            if pos >= code_len:
                break

            # Skip isolated closing braces at top level
            if code[pos] == '}':
                pos += 1
                continue

            # Try to parse a statement starting at this position
            remaining = code[pos:]

            result = self._try_parse_statement(remaining)
            if result is not None:
                ast_node, consumed = result
                # Detect if the result contains any error node (recursive)
                if self._has_error_nodes(ast_node):
                    has_errors = True
                tree.append(ast_node)
                pos += consumed
            else:
                # Could not parse - generate error and recover
                has_errors = True
                # Find next synchronization point: ';' or '}'
                next_semi = remaining.find(';')
                next_brace = remaining.find('}')

                if next_semi >= 0 and (next_brace < 0 or next_semi < next_brace):
                    tree.append(['error', 'syntax', 'error de sintaxis'])
                    pos += next_semi + 1
                elif next_brace >= 0:
                    tree.append(['error', 'syntax', 'error de sintaxis'])
                    pos += next_brace + 1
                else:
                    tree.append(['error', 'syntax', 'error de sintaxis'])
                    break

        return (tree, has_errors)

    @staticmethod
    def _has_error_nodes(node):
        """Recursively check if node or any child is an error node."""
        if isinstance(node, list):
            if len(node) > 0 and isinstance(node[0], str) and node[0] == 'error':
                return True
            return any(MiniLangParser._has_error_nodes(child) for child in node)
        return False

    def _try_parse_grammar(self, grammar, text):
        """Parse text with grammar using _parse for accurate consumed length.
        Returns (ast_node, consumed_chars) or (None, 0) on failure."""
        text = text.lstrip()
        if not text:
            return (None, 0)
        try:
            loc, tokens = grammar._parse(text, 0)
            if isinstance(tokens, ParseResults):
                ast_node = tokens.asList()
            else:
                ast_node = tokens
            return (ast_node, loc)
        except ParseException:
            return (None, 0)

    def _try_parse_statement(self, text):
        """
        Try to parse a single statement from text using pyparsing rules.
        Returns (ast_node, consumed_chars) or None if no statement matches.
        """
        text = text.lstrip()
        if not text:
            return None

        # Detect statement type by first token
        first_word = ''
        i = 0
        while i < len(text) and text[i] not in ' \t\n\r(){};=':
            first_word += text[i]
            i += 1

        # Catch dangling else
        if first_word == 'else':
            # Skip 'else' and return error
            return (['error', 'else', 'else sin if previo'], i)

        # Try to match each statement type
        # Order matters: more specific patterns first

        # Try declaration (tipo followed by id = ... ;)
        if first_word in ('int', 'float', 'string'):
            return self._try_parse_decl(text)

        # Try if
        if first_word == 'if':
            return self._try_parse_if(text)

        # Try while
        if first_word == 'while':
            return self._try_parse_while(text)

        # Try for
        if first_word == 'for':
            return self._try_parse_for(text)

        # Try print
        if first_word == 'print':
            return self._try_parse_print(text)

        # Try break
        if first_word == 'break':
            return self._try_parse_break(text)

        # Try continue
        if first_word == 'continue':
            return self._try_parse_continue(text)

        # Try assignment or postfix (starts with ID)
        if re.match(r'^[a-zA-Z_]', first_word):
            # Try postfix first (ID ++ ; or ID -- ;)
            result = self._try_parse_postfix(text)
            if result is not None:
                return result
            # Try assignment (ID = ... ;)
            return self._try_parse_assign(text)

        return None

    def _try_parse_decl(self, text):
        """Try to parse a declaration statement."""
        ast_node, consumed = self._try_parse_grammar(self._decl_stmt, text)
        if ast_node is not None:
            return (ast_node, consumed)
        try:
            # Try to recover: find next ';'
            semi = text.find(';')
            nl_pos = text.find('\n')
            
            # Detect if the line ended before finding a semicolon (Bug E1)
            if nl_pos >= 0 and (semi < 0 or nl_pos < semi):
                # We reached the end of the line without a semicolon
                # Try to extract the declaration parts up to newline
                line_content = text[:nl_pos].strip()
                parts = line_content.split(None, 2)
                if len(parts) >= 3:
                    tipo, id_, val = parts[0], parts[1], parts[2]
                    # Check for missing initialization value (Error 20)
                    if val.rstrip().endswith('='):
                        return (['error', 'declaracion', 'falta valor'], nl_pos)
                return (['error', 'declaracion', 'falta punto y coma'], nl_pos)

            if semi >= 0:
                # Try to extract what we can
                parts = text[:semi].split(None, 2)
                if len(parts) >= 3:
                    tipo = parts[0]
                    id_ = parts[1]
                    val = parts[2] if len(parts) > 2 else ''
                    # Check if val is just '=' with nothing after (e.g. 'int a =')
                    if val.strip() == '=':
                        return (['error', 'declaracion', 'falta valor'], semi + 1)
                    if val.startswith('='):
                        actual_val = val[1:].strip()
                        if actual_val:
                            try:
                                expr_result = self._expr.parseString(actual_val, parseAll=True)
                                expr_tokens = flatten_parse([expr_result.asList()])
                                if len(expr_tokens) == 1:
                                    return ([tipo, id_, expr_tokens[0]], semi + 1)
                                return ([tipo, id_] + expr_tokens, semi + 1)
                            except ParseException:
                                return (['error', 'declaracion', 'expresion invalida'], semi + 1)
                        else:
                            return (['error', 'declaracion', 'falta valor'], semi + 1)
                    return ([tipo, id_, val], semi + 1)
                elif len(parts) == 2:
                    return (['error', 'declaracion', 'declaracion incompleta'], semi + 1)
                return (['error', 'declaracion', 'declaracion incompleta'], semi + 1)
            return (['error', 'declaracion', 'falta punto y coma'], len(text))
        except Exception:
            semi = text.find(';')
            if semi >= 0:
                return (['error', 'declaracion', 'error en declaracion'], semi + 1)
            return (['error', 'declaracion', 'error en declaracion'], len(text))

    def _try_parse_assign(self, text):
        """Try to parse an assignment statement."""
        ast_node, consumed = self._try_parse_grammar(self._assign_stmt, text)
        if ast_node is not None:
            return (ast_node, consumed)
        try:
            # Check if there's a missing semicolon
            semi = text.find(';')
            # Find newline after '=' to detect cross-line semicolon
            eq_pos = text.find('=')
            if eq_pos >= 0:
                nl_after_eq = text.find('\n', eq_pos)
            else:
                nl_after_eq = -1

            if semi >= 0:
                if eq_pos >= 0 and eq_pos < semi:
                    # If the ; is on a different line than =, it's not our semicolon
                    if nl_after_eq >= 0 and nl_after_eq < semi:
                        # ; is after a newline -- it belongs to a later statement
                        # Treat as missing semicolon
                        return (['error', 'asignacion', 'falta punto y coma'],
                                nl_after_eq)
                    id_ = text[:eq_pos].strip().split()[0] if text[:eq_pos].strip() else '?'
                    expr_text = text[eq_pos + 1:semi].strip()
                    if expr_text:
                        try:
                            expr_result = self._expr.parseString(expr_text, parseAll=True)
                            expr_tokens = flatten_parse([expr_result.asList()])
                            return ([id_] + expr_tokens, semi + 1)
                        except ParseException:
                            # Expression could not be fully parsed (e.g. 'x +' or '* 3')
                            return (['error', 'asignacion', 'expresion incompleta'], semi + 1)
                    return (['error', 'asignacion', 'expresion incompleta'], semi + 1)
                return (['error', 'asignacion', 'error en asignacion'], semi + 1)
            else:
                # Check for closing brace
                brace = text.find('}')
                if eq_pos >= 0:
                    id_ = text[:eq_pos].strip().split()[0] if text[:eq_pos].strip() else '?'
                    end_pos = brace if brace >= 0 else len(text)
                    return (['error', 'asignacion', 'falta punto y coma'], end_pos)
                return (['error', 'asignacion', 'falta punto y coma'],
                        brace if brace >= 0 else len(text))
        except Exception:
            semi = text.find(';')
            if semi >= 0:
                return (['error', 'asignacion', 'error en asignacion'], semi + 1)
            return (['error', 'asignacion', 'falta punto y coma'], len(text))

    def _try_parse_postfix(self, text):
        """Try to parse a postfix statement."""
        ast_node, consumed = self._try_parse_grammar(self._postfix_stmt, text)
        if ast_node is not None:
            return (ast_node, consumed)
        return None

    def _try_parse_if(self, text):
        """Try to parse an if statement with error recovery."""
        ast_node, consumed = self._try_parse_grammar(self._if_stmt, text)
        if ast_node is not None:
            return (ast_node, consumed)
        try:
            # Remove 'if'
            rest = text[2:].lstrip()

            # Parse condition
            cond, rest_after_cond, cond_error = self._parse_cond_recovery(rest)

            # Parse then-block
            then_block, rest_after_then, then_error = self._parse_block_recovery(rest_after_cond)

            # Check for else
            else_block = None
            rest_after_else = rest_after_then
            rest_stripped = rest_after_then.lstrip()
            if rest_stripped.startswith('else'):
                else_block, rest_after_else, else_error = self._parse_block_recovery(rest_stripped[4:])

            consumed = len(text) - len(rest_after_else)

            if cond_error:
                # Check for specific missing relational operator error
                if isinstance(cond, list) and len(cond) >= 3 and cond[2] == 'operador relacional faltante':
                    return (['error', 'if', 'operador relacional faltante'], consumed)

                ast_node = ['if', ['error', 'condicion', 'expresion incompleta']]
                if then_block is not None:
                    ast_node.append(then_block)
                else:
                    ast_node.append([])
                if else_block is not None:
                    ast_node.append(else_block)
                return (ast_node, consumed)

            if cond is None:
                ast_node = ['error', 'if', 'condicion invalida']
                return (ast_node, consumed)

            ast_node = ['if', cond]
            if then_block is not None:
                ast_node.append(then_block)
            else:
                ast_node.append([])
            if else_block is not None:
                ast_node.append(else_block)

            return (ast_node, consumed)
        except Exception:
            return (['error', 'if', 'error en sentencia if'], len(text))

    def _try_parse_while(self, text):
        """Try to parse a while statement with error recovery."""
        ast_node, consumed = self._try_parse_grammar(self._while_stmt, text)
        if ast_node is not None:
            return (ast_node, consumed)
        try:
            # Error recovery: find condition and block
            rest = text[5:].lstrip()  # Remove 'while'
            cond, rest_after_cond, cond_error = self._parse_cond_recovery(rest)
            block, rest_after_block, block_error = self._parse_block_recovery(rest_after_cond)
            consumed = len(text) - len(rest_after_block)

            if cond_error:
                # Check if the specific error is missing closing parenthesis
                # Look for the pattern: while (expr [missing ')']
                paren_count = 0
                in_paren = False
                for i, ch in enumerate(rest):
                    if ch == '(':
                        in_paren = True
                        paren_count += 1
                    elif ch == ')':
                        paren_count -= 1
                        if paren_count == 0:
                            in_paren = False
                    elif ch == '{':
                        if in_paren:
                            # Missing closing paren before opening brace
                            if cond is not None:
                                return (['error', 'while', 'falta parentesis de cierre',
                                         cond, block if block else []],
                                        consumed)
                            return (['error', 'while', 'falta parentesis de cierre',
                                     [], block if block else []],
                                    consumed)

            if cond is not None and block is not None:
                return (['while', cond, block], consumed)
            if cond is not None:
                return (['while', cond, block if block else []], consumed)
            return (['error', 'while', 'error en while'], consumed)
        except Exception:
            return (['error', 'while', 'error en while'], len(text))

    def _try_parse_for(self, text):
        """Try to parse a for statement with error recovery."""
        ast_node, consumed = self._try_parse_grammar(self._for_stmt, text)
        if ast_node is not None:
            return (ast_node, consumed)
        try:
            # Recovery: try to parse for components
            rest = text[3:].lstrip()  # Remove 'for'

            # Expect '('
            if rest.startswith('('):
                rest = rest[1:].lstrip()
            else:
                # Missing '('
                return (['error', 'for', 'falta parentesis de apertura'], len(text))

            # Parse init (Tipo ID = Expr)
            init, rest_after_init = self._parse_for_init_recovery(rest)

            # Expect ';'
            rest_after_init = rest_after_init.lstrip()
            if rest_after_init.startswith(';'):
                rest_after_semi1 = rest_after_init[1:].lstrip()
            else:
                # Missing ';' after init
                rest_after_semi1 = rest_after_init

            # Parse condition
            cond, rest_after_cond, cond_error = self._parse_cond_recovery(rest_after_semi1)

            # Expect ';' after condition
            rest_after_cond = rest_after_cond.lstrip()
            has_for_semi = False
            if rest_after_cond.startswith(';'):
                rest_after_semi2 = rest_after_cond[1:].lstrip()
                has_for_semi = True
            else:
                rest_after_semi2 = rest_after_cond

            # Determine condition error FIRST — needed before step recovery
            cond_is_for_error = False
            if not has_for_semi:
                cond = ['error', 'condicion_for']
                cond_is_for_error = True
            elif cond_error:
                cond = ['error', 'condicion_for']
                cond_is_for_error = True

            # Parse step — also try to extract from condition text if step was absorbed
            step, rest_after_step = self._parse_for_step_recovery(rest_after_semi2)
            
            # If step is None and we had a condicion_for error, try to extract step
            # from the raw condition text (e.g. 'i < 3 i++' → step is 'i++')
            if step is None and cond_is_for_error:
                import re as _re
                raw_text_before_paren = rest_after_semi1
                paren_p = raw_text_before_paren.find(')')
                if paren_p >= 0:
                    raw_text_before_paren = raw_text_before_paren[:paren_p]
                step_match = _re.search(r'([a-zA-Z_]\w*)\s*(\+\+|--)', raw_text_before_paren)
                if step_match:
                    step = [step_match.group(1), step_match.group(2)]

            # Skip until ')' only if we haven't reached the block yet
            rest_after_step = rest_after_step.lstrip()
            close_paren_found = False
            if not rest_after_step.startswith('{'):
                paren_pos = rest_after_step.find(')')
                if paren_pos >= 0:
                    rest_after_paren = rest_after_step[paren_pos + 1:]
                    close_paren_found = True
                else:
                    rest_after_paren = rest_after_step
            else:
                rest_after_paren = rest_after_step

            # Parse block
            block, rest_after_block, block_error = self._parse_block_recovery(rest_after_paren)
            if block is None:
                block = []

            consumed = len(text) - len(rest_after_block)

            # Build for AST node
            var_name = init[1] if init and len(init) > 1 else '?'
            init_val = init[2] if init and len(init) > 2 else ''

            if not close_paren_found:
                # Missing ')' - Error 8
                return (['error', 'for', 'falta parentesis de cierre'], consumed)

            if step is None:
                step = self._default_step(var_name, cond)

            return (['for', [var_name, init_val, cond, step], block], consumed)
        except Exception:
            return (['error', 'for', 'error en for'], len(text))

    def _try_parse_print(self, text):
        """Try to parse a print statement with error recovery."""
        ast_node, consumed = self._try_parse_grammar(self._print_stmt, text)
        if ast_node is not None:
            return (ast_node, consumed)
        try:
            # Error recovery
            rest = text[5:].lstrip()  # Remove 'print'

            # Expect '('
            if rest.startswith('('):
                rest = rest[1:].lstrip()
            else:
                # Missing '('
                semi = rest.find(';')
                if semi >= 0:
                    return (['error', 'print', 'falta parentesis de apertura'], len(text) - len(rest[semi+1:]))
                return (['error', 'print', 'falta parentesis de apertura'], len(text))

            # Try to parse expression
            try:
                expr_result = self._expr.parseString(rest)
                expr_tokens = flatten_parse([expr_result.asList()])
                expr_str = ' '.join(expr_tokens)
                consumed_expr = self._find_consumed(rest, expr_result)
                rest = rest[consumed_expr:].lstrip()
            except ParseException:
                expr_str = ''
                # Skip to ')' or ';'
                paren_pos = rest.find(')')
                semi_pos = rest.find(';')
                if paren_pos >= 0:
                    expr_str = rest[:paren_pos].strip()
                    rest = rest[paren_pos:]
                elif semi_pos >= 0:
                    expr_str = rest[:semi_pos].strip()
                    rest = rest[semi_pos:]

            # Expect ')'
            rest = rest.lstrip()
            if rest.startswith(')'):
                rest = rest[1:].lstrip()
            else:
                # Missing closing paren
                consumed = len(text) - len(rest)
                return (['error', 'print', 'falta parentesis de cierre'], consumed)

            # Expect ';'
            if rest.startswith(';'):
                consumed = len(text) - len(rest[1:])
                return (['print', expr_str], consumed)
            else:
                # Missing semicolon
                consumed = len(text) - len(rest)
                return (['print', expr_str], consumed)
        except Exception:
            return (['error', 'print', 'error en print'], len(text))

    def _try_parse_break(self, text):
        ast_node, consumed = self._try_parse_grammar(self._break_stmt, text)
        if ast_node is not None:
            return (ast_node, consumed)
        return (['break'], len(text) if ';' not in text else text.index(';') + 1)

    def _try_parse_continue(self, text):
        ast_node, consumed = self._try_parse_grammar(self._continue_stmt, text)
        if ast_node is not None:
            return (ast_node, consumed)
        return (['continue'], len(text) if ';' not in text else text.index(';') + 1)

    # ── Recovery Helper Methods ──

    def _parse_cond_recovery(self, text):
        """Parse a condition with error recovery.
        Returns (cond_ast, remaining_text, has_error)."""
        text = text.lstrip()
        if not text:
            return (None, text, True)

        has_parens = text.startswith('(')
        if has_parens:
            # Find matching closing paren
            depth = 0
            paren_end = -1
            for i, ch in enumerate(text):
                if ch == '(':
                    depth += 1
                elif ch == ')':
                    depth -= 1
                    if depth == 0:
                        paren_end = i
                        break
                elif ch == '{' and depth == 1:
                    # Missing closing paren for condition
                    cond_text = text[1:i].strip()
                    rest = text[i:]
                    try:
                        cond_result = self._condition.parseString(cond_text, parseAll=True)
                        cond_ast = cond_result.asList()
                        return (cond_ast, rest, True)
                    except ParseException:
                        pass
                    return (None, rest, True)

            if paren_end >= 0:
                cond_text = text[1:paren_end].strip()
                rest = text[paren_end + 1:]
                try:
                    cond_result = self._condition.parseString(cond_text, parseAll=True)
                    cond_ast = cond_result.asList()
                    if isinstance(cond_ast, list) and len(cond_ast) == 1:
                        cond_ast = cond_ast[0]
                    return (cond_ast, rest, False)
                except ParseException:
                    return (self._parse_cond_partial(cond_text), rest, True)
            else:
                brace_pos = text.find('{')
                if brace_pos >= 0:
                    cond_text = text[1:brace_pos].strip()
                    rest = text[brace_pos:]
                    return (self._parse_cond_partial(cond_text), rest, True)
                return (None, text, True)
        else:
            brace_pos = text.find('{')
            if brace_pos >= 0:
                cond_text = text[:brace_pos].strip()
                rest = text[brace_pos:]
            else:
                cond_text = text.strip()
                rest = ''

            if not cond_text:
                return (None, rest, True)

            try:
                cond_result = self._condition.parseString(cond_text, parseAll=True)
                cond_ast = cond_result.asList()
                if isinstance(cond_ast, list) and len(cond_ast) == 1:
                    cond_ast = cond_ast[0]
                return (cond_ast, rest, False)
            except ParseException:
                return (self._parse_cond_partial(cond_text), rest, True)

    def _parse_cond_partial(self, text):
        """Try to extract a partial condition from text."""
        text = text.strip()
        if not text:
            return ['error', 'condicion', 'expresion incompleta']

        # Try to match a relational expression
        op_pattern = r'>=|<=|!=|==|>|<'
        match = re.search(op_pattern, text)
        if match:
            left = text[:match.start()].strip()
            op = match.group()
            right = text[match.end():].strip()
            if left and right:
                try:
                    left_result = self._expr.parseString(left, parseAll=True)
                    left_tokens = flatten_parse([left_result.asList()])
                except ParseException:
                    left_tokens = left.split()

                try:
                    right_result = self._expr.parseString(right, parseAll=True)
                    right_tokens = flatten_parse([right_result.asList()])
                except ParseException:
                    right_tokens = right.split()

                return left_tokens + [op] + right_tokens
            elif left and not right:
                return ['error', 'condicion', 'expresion incompleta']
            else:
                return ['error', 'condicion', 'expresion incompleta']

        # Check for && or ||
        and_match = re.search(r'&&', text)
        or_match = re.search(r'\|\|', text)
        if and_match:
            left = text[:and_match.start()].strip()
            right = text[and_match.end():].strip()
            left_cond = self._parse_cond_partial(left) if left else ['error', 'condicion', 'expresion incompleta']
            right_cond = self._parse_cond_partial(right) if right else ['error', 'condicion', 'expresion incompleta']
            return ['&&', left_cond, right_cond]
        if or_match:
            left = text[:or_match.start()].strip()
            right = text[or_match.end():].strip()
            left_cond = self._parse_cond_partial(left) if left else ['error', 'condicion', 'expresion incompleta']
            right_cond = self._parse_cond_partial(right) if right else ['error', 'condicion', 'expresion incompleta']
            return ['||', left_cond, right_cond]

        # Check for missing operator in something like 'x 10'
        parts = text.split()
        if len(parts) >= 2:
            return ['error', 'condicion', 'operador relacional faltante']

        return ['error', 'condicion', 'expresion incompleta']

    def _parse_block_recovery(self, text):
        """Parse a block { ... } with error recovery.
        Returns (block_ast, remaining_text, has_error)."""
        text = text.lstrip()
        if not text:
            return ([], text, True)

        if not text.startswith('{'):
            return ([], text, True)

        # Find matching closing brace
        depth = 0
        brace_end = -1
        for i, ch in enumerate(text):
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    brace_end = i
                    break

        if brace_end < 0:
            block_text = text[1:]
            rest = ''
        else:
            block_text = text[1:brace_end]
            rest = text[brace_end + 1:]

        # Parse statements inside block using the same recovery logic
        # (without creating a recursive MiniLangParser)
        stmts = []
        has_error = False
        inner_text = block_text.strip()

        if inner_text:
            # Process statements inside block using _try_parse_statement
            pos = 0
            while pos < len(inner_text):
                # Skip whitespace
                while pos < len(inner_text) and inner_text[pos] in ' \t\n\r':
                    pos += 1
                if pos >= len(inner_text):
                    break
                remaining = inner_text[pos:]
                
                # Check for premature block end or top-level keywords that suggest we missed a brace (Bug E4)
                if remaining.startswith('}'):
                    break
                
                result = self._try_parse_statement(remaining)
                if result is not None:
                    ast_node, consumed = result
                    # Wrap each statement in [stmt]
                    stmts.append([ast_node])
                    pos += consumed
                else:
                    # Could not parse - skip to next ';' or newline to avoid massive absorption
                    has_error = True
                    next_semi = remaining.find(';')
                    next_nl = remaining.find('\n')
                    if next_semi >= 0:
                        pos += next_semi + 1
                    elif next_nl >= 0:
                        pos += next_nl + 1
                    else:
                        break

        return (stmts, rest, has_error)

        return (stmts, rest, has_error)

    def _parse_for_init_recovery(self, text):
        """Parse for init part: Tipo ID = Expr
        Returns (init_list, remaining_text)."""
        text = text.lstrip()
        init = []

        # Check for type keyword
        tipo = None
        for kw in ('int', 'float', 'string'):
            if text.startswith(kw) and (len(text) == len(kw) or not text[len(kw)].isalnum()):
                tipo = kw
                text = text[len(kw):].lstrip()
                break

        # Parse ID
        id_match = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)', text)
        if id_match:
            id_ = id_match.group(1)
            text = text[id_match.end():].lstrip()
        else:
            id_ = '?'

        # Parse '='
        if text.startswith('='):
            text = text[1:].lstrip()
        else:
            if tipo:
                init = [tipo, id_, '']
            return (init, text)

        # Parse expression (up to ';')
        semi_pos = text.find(';')
        if semi_pos >= 0:
            expr_text = text[:semi_pos].strip()
            text = text[semi_pos:]
        else:
            expr_text = text.strip()
            text = ''

        try:
            expr_result = self._expr.parseString(expr_text, parseAll=True)
            expr_tokens = flatten_parse([expr_result.asList()])
            expr_str = ' '.join(expr_tokens)
        except ParseException:
            expr_str = expr_text

        if tipo:
            init = [tipo, id_, expr_str]
        else:
            init = [id_, expr_str]

        return (init, text)

    def _parse_for_step_recovery(self, text):
        """Parse for step part: ID ++ | ID -- | ID = Expr
        Returns (step_list, remaining_text)."""
        text = text.lstrip()
        if not text:
            return (None, text)

        # Try to match ID ++ or ID --
        id_match = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*(\+\+|--)', text)
        if id_match:
            id_ = id_match.group(1)
            op = id_match.group(2)
            rest = text[id_match.end():]
            return ([id_, op], rest)

        # Try to match ID = Expr
        eq_match = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=', text)
        if eq_match:
            id_ = eq_match.group(1)
            rest = text[eq_match.end():].lstrip()
            paren_pos = rest.find(')')
            if paren_pos >= 0:
                expr_text = rest[:paren_pos].strip()
                rest_after = rest[paren_pos:]
            else:
                expr_text = rest.strip()
                rest_after = ''

            try:
                expr_result = self._expr.parseString(expr_text, parseAll=True)
                expr_tokens = flatten_parse([expr_result.asList()])
            except ParseException:
                expr_tokens = expr_text.split()

            return ([id_, '='] + expr_tokens, rest_after)

        return (None, text)

    @staticmethod
    def _find_consumed(original_text, parse_result):
        """Find how many characters were consumed in a parse."""
        # Use _originalText if available and non-empty
        if hasattr(parse_result, '_originalText'):
            try:
                ot = parse_result._originalText
                if ot:
                    return len(ot)
            except AttributeError:
                pass

        if not parse_result:
            return 0

        # Try to find the matched text in the original
        # For single-token results, use the first token's string
        result_str = str(parse_result[0]) if parse_result else ''
        if result_str:
            idx = original_text.find(result_str)
            if idx >= 0:
                return idx + len(result_str)

        # Fallback: use the length of the first element
        try:
            return len(str(parse_result[0]))
        except (IndexError, TypeError):
            return len(original_text)


def print_tree(tree, indent=0):
    """Print AST with indentation exactly as expected by requirements."""
    prefix = '  ' * indent
    if isinstance(tree, list):
        if not tree:
            print(prefix + '[]')
            return
        
        # Check if it is a simple flat list of tokens
        all_scalar = all(not isinstance(item, list) for item in tree)
        if all_scalar:
            items = []
            for item in tree:
                if isinstance(item, str):
                    # Quote tokens to match professor's output
                    items.append(repr(item))
                else:
                    items.append(str(item))
            print(prefix + '[' + ', '.join(items) + ']')
        else:
            print(prefix + '[')
            for i, item in enumerate(tree):
                if isinstance(item, list):
                    print_tree(item, indent + 1)
                else:
                    # Scalar item in a nested list
                    val = repr(item) if isinstance(item, str) else str(item)
                    # Add comma unless it's the last item (optional but looks better)
                    print(prefix + '  ' + val + (',' if i < len(tree)-1 else ''))
            print(prefix + ']')
    else:
        # Should not happen in a valid AST tree structure but for robustness:
        print(prefix + (repr(tree) if isinstance(tree, str) else str(tree)))


# ────────────────────────────────────────────────────────────
# CELDA 5: Ejemplo de programa correcto
# ────────────────────────────────────────────────────────────

CODIGO_CORRECTO = """int x = 10;
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
"""

# ────────────────────────────────────────────────────────────
# CELDA 6: Ejemplo de programa con errores
# ────────────────────────────────────────────────────────────

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

# ────────────────────────────────────────────────────────────
# Main Execution
# ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = MiniLangParser()

    # ── Soporte para lectura de archivo ──
    # Uso: python minilang_parser.py archivo.minilang
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        print(f"Analizando archivo: {filepath}")
        print("=" * 60)
        try:
            tree, has_errors = parser.parse_file(filepath)
            if has_errors:
                print("Errores de sintaxis")
            else:
                print("Código Válido")
            print("\nÁrbol de Análisis Sintáctico")
            print_tree(tree)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{filepath}'")
        sys.exit(0)

    print("=" * 60)
    print("CELDA 5: Programa Correcto")
    print("=" * 60)
    tree1, err1 = parser.parse(CODIGO_CORRECTO)
    if err1:
        print("Errores de sintaxis")
    else:
        print("Código Válido")
    print("\nÁrbol de Análisis Sintáctico")
    print_tree(tree1)

    print("\n" + "=" * 60)
    print("CELDA 6: Programa con Errores")
    print("=" * 60)
    tree2, err2 = parser.parse(CODIGO_ERRORES)
    if err2:
        print("Errores de sintaxis")
    else:
        print("Código Válido")
    print("\nÁrbol de Análisis Sintáctico")
    print_tree(tree2)

    print("\n" + "=" * 60)
    print("CELDA 6 (Extra): Programa con errores (ejemplo 4)")
    print("=" * 60)

    CODIGO_ERRORES2 = """string nombre = "Juan";
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
"""
    tree3, err3 = parser.parse(CODIGO_ERRORES2)
    if err3:
        print("Errores de sintaxis")
    else:
        print("Código Válido")
    print("\nÁrbol de Análisis Sintáctico")
    print_tree(tree3)

    print("\n" + "=" * 60)
    print("CELDA 5 (Extra): Programa correcto (ejemplo 2)")
    print("=" * 60)

    CODIGO_CORRECTO2 = """int x = 5;
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
"""
    tree4, err4 = parser.parse(CODIGO_CORRECTO2)
    if err4:
        print("Errores de sintaxis")
    else:
        print("Código Válido")
    print("\nÁrbol de Análisis Sintáctico")
    print_tree(tree4)
