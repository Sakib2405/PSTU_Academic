from itertools import product

def tf(val):
    if val is None:
        return '-'
    return 'T' if val else 'F'

print("Hypothetical Syllogism Truth Table")
print(f"{'P':^3} {'Q':^3} {'R':^3} {'P→Q':^5} {'Q→R':^5} {'P→R':^5} {'HS':^5}")
print('-'*39)
for P, Q, R in product([True, False], repeat=3):
    pq = (not P) or Q
    qr = (not Q) or R
    pr = (not P) or R
    result = pr if pq and qr else None
    print(f"{tf(P):^3} {tf(Q):^3} {tf(R):^3} {tf(pq):^5} {tf(qr):^5} {tf(pr):^5} {tf(result):^5}")