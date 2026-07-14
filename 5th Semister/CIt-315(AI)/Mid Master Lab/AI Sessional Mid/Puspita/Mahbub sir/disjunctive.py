values = [True, False]

print("\nDisjunctive Syllogism Truth Table:\n")
print("P\tQ\tP∨Q\t¬P\t(¬P ∧ (P∨Q)) → Q")

for P in values:
    for Q in values:
        disjunction = P or Q         # P ∨ Q
        not_P = not P                # ¬P
        antecedent = not_P and disjunction  # ¬P ∧ (P∨Q)
        ds_implication = (not antecedent) or Q  # Implication: antecedent → Q
        print(f"{P}\t{Q}\t{disjunction}\t{not_P}\t{ds_implication}")
