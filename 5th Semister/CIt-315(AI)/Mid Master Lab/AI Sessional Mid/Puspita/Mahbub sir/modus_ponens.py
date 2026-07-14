values = [True, False]

print("Modus Ponens Truth Table:\n")
print("P\tQ\tP→Q\tP ∧ (P→Q)\tConclusion(Q)")

for P in values:
    for Q in values:
        implication = (not P) or Q
        modus_ponens = P and implication
        # Always show Q in the Conclusion column
        print(f"{P}\t{Q}\t{implication}\t{modus_ponens}\t\t{Q}")
