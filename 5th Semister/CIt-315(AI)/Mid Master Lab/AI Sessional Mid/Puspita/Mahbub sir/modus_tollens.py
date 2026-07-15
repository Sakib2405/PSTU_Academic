values = [True, False]

print("\nModus Tollens Truth Table:\n")
print("P\tQ\tP→Q\t¬Q\t(¬Q ∧ (P→Q)) → ¬P")

for P in values:
    for Q in values:
        implication = (not P) or Q      # P → Q
        not_Q = not Q                    # ¬Q
        antecedent = not_Q and implication  # ¬Q ∧ (P→Q)
        modus_tollens = (not antecedent) or (not P)  # Implication: antecedent → ¬P
        print(f"{P}\t{Q}\t{implication}\t{not_Q}\t{modus_tollens}")
