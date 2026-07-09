from itertools import product

def tf(val):
    if val is None:
        return '-'
    return 'T' if val else 'F'

print("Simplification Truth Table")
print(f"{'P':^3} {'Q':^3} {'P∧Q':^5} {'Simp':^5}")
print('-'*18)
for P, Q in product([True, False], repeat=2):
    conjunction = P and Q
    result = P if conjunction else None
    print(f"{tf(P):^3} {tf(Q):^3} {tf(conjunction):^5} {tf(result):^5}")