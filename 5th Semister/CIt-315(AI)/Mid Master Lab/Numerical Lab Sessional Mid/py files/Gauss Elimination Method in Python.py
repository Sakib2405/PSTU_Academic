# Gauss Elimination Method in Python

def gauss_elimination(A, b):
    n = len(A)

    # Forward elimination
    for i in range(n):
        # Make the diagonal element 1 (partial pivoting)
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        if i != max_row:
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]

        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

    # Back substitution
    x = [0 for _ in range(n)]
    for i in range(n - 1, -1, -1):
        sum_ax = sum(A[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (b[i] - sum_ax) / A[i][i]

    return x


# Main program
if __name__ == "__main__":
    n = int(input("Enter number of variables: "))
    A = []
    b = []

    print("Enter the coefficients row-wise:")
    for i in range(n):
        row = list(map(float, input(f"Row {i+1}: ").split()))
        A.append(row)

    print("Enter constants (RHS) row-wise:")
    b = list(map(float, input().split()))

    solution = gauss_elimination(A, b)

    print("\nSolution:")
    for i, val in enumerate(solution):
        print(f"x{i+1} = {val:.6f}")
