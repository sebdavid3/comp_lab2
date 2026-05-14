import sys
from minilang_parser import MiniLangParser, print_tree

def run(filepath):
    print("=" * 40)
    print(f"RUNNING: {filepath}")
    print("=" * 40)
    
    parser = MiniLangParser()
    tree, has_errors = parser.parse(filepath)
    
    if has_errors:
        print("Estado: Errores de sintaxis")
    else:
        print("Estado: Código Válido")
    
    print("\nÁrbol de Análisis Sintáctico")
    print_tree(tree)
    print("\n")

if __name__ == "__main__":
    test_files = [
        "otras_pruebas/programa_correcto.txt",
        "otras_pruebas/programa_errores.txt",
        "otras_pruebas/error_img1.txt",
        "otras_pruebas/error_img2.txt"
    ]
    for f in test_files:
        run(f)
