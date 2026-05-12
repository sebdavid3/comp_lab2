import sys
sys.path.insert(0, '.')
from minilang_parser import MiniLangParser

# Test 2: Código 2 - complex but valid
code2 = """int x = 5;
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
}"""

print("=== Codigo 2 ===")
parser = MiniLangParser()
tree, err = parser.parse(code2)
print('Errors:', err)
print('Tree:', tree)
print('OK')
