from itertools import product

def tf(val):
    if val is None:
        return '-'
    return 'T' if val else 'F'

print("Resolution Truth Table")
print(f"{'P':^3} {'Q':^3} {'R':^3} {'P∨Q':^5} {'¬P∨R':^7} {'Q∨R':^5} {'Res':^5}")
print('-'*38)
for P, Q, R in product([True, False], repeat=3):
    pq = P or Q
    notP_R = (not P) or R
    qr = Q or R
    result = qr if pq and notP_R else None
    print(f"{tf(P):^3} {tf(Q):^3} {tf(R):^3} {tf(pq):^5} {tf(notP_R):^7} {tf(qr):^5} {tf(result):^5}")