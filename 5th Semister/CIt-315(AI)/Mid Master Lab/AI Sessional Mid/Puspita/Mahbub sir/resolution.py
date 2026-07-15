values = [True, False]
print("\nResolution Truth Table:\n")
print("P\tQ\tR\t(P∨Q)\t(¬P∨R)\tConclusion (Q∨R)")

for P in values:
    for Q in values:
        for R in values:
            p_or_q = P or Q
            notp_or_r = (not P) or R
            conclusion = Q or R
            print(f"{P}\t{Q}\t{R}\t{p_or_q}\t{notp_or_r}\t{conclusion}")
