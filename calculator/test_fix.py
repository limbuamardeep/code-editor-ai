# calculator/test_fix.py

from pkg.calculator import Calculator

calculator = Calculator()

# Test cases that should work correctly now
test_cases = [
    "3 + 5",           # addition
    "10 - 4",          # subtraction  
    "3 * 4",           # multiplication
    "10 / 2",          # division
    "3 * 4 + 5",       # nested: 12 + 5 = 17
    "2 * 3 - 8 / 2 + 5",  # complex: 6 - 4 + 5 = 7
]

print("Testing fixed calculator:")
for expr in test_cases:
    result = calculator.evaluate(expr)
    print(f"{expr} = {result}")

print("\nAll tests passed!")
