from itertools import product

def tf(val):
    if val is None:
        return '-'
    return 'T' if val else 'F'

print("Modus Tollens Truth Table")
print(f"{'P':^3} {'Q':^3} {'P→Q':^5} {'¬Q':^5} {'¬P (MT)':^9}")
print('-'*32)
for P, Q in product([True, False], repeat=2):
    implication = (not P) or Q
    not_Q = not Q
    result = not P if implication and not_Q else None
    print(f"{tf(P):^3} {tf(Q):^3} {tf(implication):^5} {tf(not_Q):^5} {tf(result):^9}")