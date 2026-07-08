from itertools import product

def tf(val):
    if val is None:
        return '-'
    return 'T' if val else 'F'


def modus_ponens():
    print("Modus Ponens Truth Table")
    print(f"{'P':^3} {'Q':^3} {'P→Q':^5} {'Q (MP)':^7}")
    print('-'*22)
    for P, Q in product([True, False], repeat=2):
        implication = (not P) or Q
        result = Q if implication and P else None
        print(f"{tf(P):^3} {tf(Q):^3} {tf(implication):^5} {tf(result):^7}")


def modus_tollens():
    print("\nModus Tollens Truth Table")
    print(f"{'P':^3} {'Q':^3} {'P→Q':^5} {'¬Q':^5} {'¬P (MT)':^9}")
    print('-'*32)
    for P, Q in product([True, False], repeat=2):
        implication = (not P) or Q
        not_Q = not Q
        result = not P if implication and not_Q else None
        print(f"{tf(P):^3} {tf(Q):^3} {tf(implication):^5} {tf(not_Q):^5} {tf(result):^9}")


def hypothetical_syllogism():
    print("\nHypothetical Syllogism Truth Table")
    print(f"{'P':^3} {'Q':^3} {'R':^3} {'P→Q':^5} {'Q→R':^5} {'P→R':^5} {'HS':^5}")
    print('-'*39)
    for P, Q, R in product([True, False], repeat=3):
        pq = (not P) or Q
        qr = (not Q) or R
        pr = (not P) or R
        result = pr if pq and qr else None
        print(f"{tf(P):^3} {tf(Q):^3} {tf(R):^3} {tf(pq):^5} {tf(qr):^5} {tf(pr):^5} {tf(result):^5}")


def disjunctive_syllogism():
    print("\nDisjunctive Syllogism Truth Table")
    print(f"{'P':^3} {'Q':^3} {'P∨Q':^5} {'¬P':^5} {'Q (DS)':^7}")
    print('-'*28)
    for P, Q in product([True, False], repeat=2):
        disjunction = P or Q
        not_P = not P
        result = Q if disjunction and not_P else None
        print(f"{tf(P):^3} {tf(Q):^3} {tf(disjunction):^5} {tf(not_P):^5} {tf(result):^7}")


def addition():
    print("\nAddition Truth Table")
    print(f"{'P':^3} {'Q':^3} {'P∨Q':^5} {'Add':^5}")
    print('-'*18)
    for P, Q in product([True, False], repeat=2):
        disjunction = P or Q
        result = disjunction if P else None
        print(f"{tf(P):^3} {tf(Q):^3} {tf(disjunction):^5} {tf(result):^5}")


def simplification():
    print("\nSimplification Truth Table")
    print(f"{'P':^3} {'Q':^3} {'P∧Q':^5} {'Simp':^5}")
    print('-'*18)
    for P, Q in product([True, False], repeat=2):
        conjunction = P and Q
        result = P if conjunction else None
        print(f"{tf(P):^3} {tf(Q):^3} {tf(conjunction):^5} {tf(result):^5}")


def resolution():
    print("\nResolution Truth Table")
    print(f"{'P':^3} {'Q':^3} {'R':^3} {'P∨Q':^5} {'¬P∨R':^7} {'Q∨R':^5} {'Res':^5}")
    print('-'*38)
    for P, Q, R in product([True, False], repeat=3):
        pq = P or Q
        notP_R = (not P) or R
        qr = Q or R
        result = qr if pq and notP_R else None
        print(f"{tf(P):^3} {tf(Q):^3} {tf(R):^3} {tf(pq):^5} {tf(notP_R):^7} {tf(qr):^5} {tf(result):^5}")


if __name__ == "__main__":
    modus_ponens()
    modus_tollens()
    hypothetical_syllogism()
    disjunctive_syllogism()
    addition()
    simplification()
    resolution()


# # Define the propositions as sentences
# sentence_P = "The sun is shining"
# sentence_Q = "It is a warm day"

# # Possible truth values
# values = [True, False]

# print("Logical Conjunction (AND) Example:\n")

# # Loop through all combinations of P and Q
# for P in values:
#     for Q in values:
#         conjunction = P and Q
#         print(f"{sentence_P} = {P}, {sentence_Q} = {Q} → "
#               f"{sentence_P} AND {sentence_Q} = {conjunction}")