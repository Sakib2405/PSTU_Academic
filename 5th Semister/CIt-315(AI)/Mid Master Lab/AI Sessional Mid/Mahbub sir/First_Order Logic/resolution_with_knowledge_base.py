# Domain
people = ["Alice", "Bob", "Charlie"]
loves = {("Alice", "Bob"), ("Bob", "Charlie")}

# Universal quantifier: ∀x ∃y Loves(x, y)?
def exists_y(x):
    return any((x, y) in loves for y in people)

print("Does each person love someone?")
print(f"{'Person':<8} {'Loves Someone':<14}")
print("-" * 24)
for p in people:
    result = "T" if exists_y(p) else "F"
    print(f"{p:<8} {result:<14}")


# Existential quantifier: ∃y ∀x Loves(x, y)?
def someone_loves(person):
    return any((x, person) in loves for x in people)

print("\nIs there someone who loves each person?")
print(f"{'Person':<8} {'Loved By Someone':<15}")
print("-" * 25)
for p in people:
    result = "T" if someone_loves(p) else "F"
    print(f"{p:<8} {result:<15}")