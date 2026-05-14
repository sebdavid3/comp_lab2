from minilang_parser import remove_comments

with open('otras_pruebas/programa_errores.txt', 'r') as f:
    code = f.read()

res, has_uncl = remove_comments(code)
print(f"Has unclosed: {has_uncl}")
