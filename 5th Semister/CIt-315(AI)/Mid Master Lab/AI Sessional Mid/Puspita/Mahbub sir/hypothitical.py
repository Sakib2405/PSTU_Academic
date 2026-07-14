values = [True, False]
print("\nHypothetical Syllogism Truth Table:\n")
print("P\tQ\tR\tP→Q\tQ→R\tConclusion P→R")

for P in values:
    for Q in values:
        for R in values:
            p_imp_q = (not P) or Q
            q_imp_r = (not Q) or R
            p_imp_r = (not P) or R
            print(f"{P}\t{Q}\t{R}\t{p_imp_q}\t{q_imp_r}\t{p_imp_r}")
