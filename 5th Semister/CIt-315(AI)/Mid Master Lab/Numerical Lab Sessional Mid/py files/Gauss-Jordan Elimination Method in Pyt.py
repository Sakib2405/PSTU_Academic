# Gauss-Jordan Elimination Method in Python

def gauss_jordan(A, b):
    n = len(A)
    # Form augmented matrix
    for i in range(n):
        A[i].append(b[i])
    
    # Perform Gauss-Jordan elimination
    for i in range(n):
        # Make the diagonal element 1 (pivot normalization)
        pivot = A[i][i]
        if pivot == 0:
            # Swap with a row below having non-zero pivot
            for j in range(i+1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    pivot = A[i][i]
                    break
        for k in range(i, n+1):
            A[i][k] /= pivot
        
        # Make all other elements in current column 0
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(i, n+1):
                    A[j][k] -= factor * A[i][k]
    
    # Extract solution
    x = [A[i][n] for i in range(n)]
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
    
    solution = gauss_jordan(A, b)
    
    print("\nSolution:")
    for i, val in enumerate(solution):
        print(f"x{i+1} = {val:.6f}")
