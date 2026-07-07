from itertools import product

def tf(val):
    if val is None:
        return '-'
    return 'T' if val else 'F'

print("Disjunctive Syllogism Truth Table")
print(f"{'P':^3} {'Q':^3} {'P∨Q':^5} {'¬P':^5} {'Q (DS)':^7}")
print('-'*28)
for P, Q in product([True, False], repeat=2):
    disjunction = P or Q
    not_P = not P
    result = Q if disjunction and not_P else None
    print(f"{tf(P):^3} {tf(Q):^3} {tf(disjunction):^5} {tf(not_P):^5} {tf(result):^7}")