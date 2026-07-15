values = [True, False]

print("\nSimplification Truth Table:\n")
print("P\tQ\tP∧Q\tConclusion P")

for P in values:
    for Q in values:
        conjunction = P and Q       # P ∧ Q
        print(f"{P}\t{Q}\t{conjunction}\t{P}")
