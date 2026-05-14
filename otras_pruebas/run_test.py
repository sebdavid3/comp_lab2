import sys
sys.path.insert(0, '/home/sebdavid3/code/comp_lab2')
from minilang_parser import MiniLangParser, print_tree

parser = MiniLangParser()

print("=" * 60)
print("PROGRAMA CORRECTO")
print("=" * 60)
tree1, err1 = parser.parse('/home/sebdavid3/code/comp_lab2/otras_pruebas/programa_correcto.txt')
if err1:
    print("Errores de sintaxis")
else:
    print("Código Válido")
print("\nÁrbol de Análisis Sintáctico")
print_tree(tree1)

print("\n" + "=" * 60)
print("PROGRAMA CON ERRORES")
print("=" * 60)
tree2, err2 = parser.parse('/home/sebdavid3/code/comp_lab2/otras_pruebas/programa_errores.txt')
if err2:
    print("Errores de sintaxis")
else:
    print("Código Válido")
print("\nÁrbol de Análisis Sintáctico")
print_tree(tree2)
