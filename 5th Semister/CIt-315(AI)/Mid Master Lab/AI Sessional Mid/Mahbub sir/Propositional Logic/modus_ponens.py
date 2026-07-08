from itertools import product

def tf(val):
    if val is None:
        return '-'
    return 'T' if val else 'F'

print("Modus Ponens Truth Table")
print(f"{'P':^3} {'Q':^3} {'P→Q':^5} {'Q (MP)':^7}")
print('-'*22)
for P, Q in product([True, False], repeat=2):
    implication = (not P) or Q
    result = Q if implication and P else None
    print(f"{tf(P):^3} {tf(Q):^3} {tf(implication):^5} {tf(result):^7}")