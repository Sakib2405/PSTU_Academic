# Domain of discourse
people = ["John", "Mary", "Alice"]

# Predicate: Loves(x, y) - "x loves y"
def loves(x, y):
    return (x, y) in [("John", "Mary"), ("Mary", "Alice")]

# Predicate: IsTall(x) - "x is tall"
def is_tall(x):
    return x in ["Alice"]

# Predicate: IsHappy(x) - "x is happy"
def is_happy(x):
    return x == "John"

# Print results for predicates
print("Loves(x, y):")
for x in people:
    for y in people:
        print(f"{x} loves {y}: {'T' if loves(x, y) else 'F'}")

print("\nIsTall(x):")
for x in people:
    print(f"{x} is tall: {'T' if is_tall(x) else 'F'}")

print("\nIsHappy(x):")
for x in people:
    print(f"{x} is happy: {'T' if is_happy(x) else 'F'}")