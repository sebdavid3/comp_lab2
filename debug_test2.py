import sys
sys.path.insert(0, '.')
from minilang_parser import MiniLangParser

# Test 3 - Código 3 con errores
code3 = """int x = 10;
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
}"""

print("=== Codigo 3 ===")
parser = MiniLangParser()
tree, err = parser.parse(code3)
print('Errors:', err)
print('Tree:', tree)
print('=== OK ===')
