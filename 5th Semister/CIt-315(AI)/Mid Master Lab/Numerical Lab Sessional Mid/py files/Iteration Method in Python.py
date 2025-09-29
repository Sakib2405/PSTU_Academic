import matplotlib.pyplot as plt
import numpy as np
import math

# Fixed Point Iteration Method
def iteration_method(g, x0, tol, max_iter):
    print("Iteration Method (Fixed Point)")
    print("-----------------------------------")
    x_history = [x0]

    for i in range(1, max_iter + 1):
        x1 = g(x0)
        x_history.append(x1)
        print(f"Iteration {i}: x = {x1:.6f}")
        if abs(x1 - x0) < tol:
            print("\nRoot found:", x1)
            return x1, x_history
        x0 = x1

    print("\nDid not converge within given iterations.")
    return None, x_history

# Main program
if __name__ == "__main__":
    expr_g = input("Enter g(x) in terms of math functions (e.g., 'math.cos(x)'): ")
    x0 = float(input("Enter initial guess x0: "))
    tol = float(input("Enter tolerance (e.g., 0.0001): "))
    max_iter = int(input("Enter maximum iterations: "))

    # Convert string to function
    def g(x):
        return eval(expr_g)

    root, history = iteration_method(g, x0, tol, max_iter)

    # 2D Plot
    x_min = min(history) - 1
    x_max = max(history) + 1
    x_vals = np.linspace(x_min, x_max, 400)
    y_vals = [g(x) for x in x_vals]

    plt.figure(figsize=(8,6))
    plt.plot(x_vals, y_vals, label='g(x)', color='blue')
    plt.plot(x_vals, x_vals, label='y = x', color='green', linestyle='--')  # y=x line

    # Plot iteration points
    for i in range(len(history)-1):
        plt.plot([history[i], history[i]], [history[i], history[i+1]], 'r', linestyle='--')
        plt.plot([history[i], history[i+1]], [history[i+1], history[i+1]], 'r', linestyle='--')
        plt.scatter(history[i], history[i], color='red')

    plt.scatter(history[-1], history[-1], color='black', s=100, label='Root')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Fixed Point Iteration Method')
    plt.legend()
    plt.grid(True)
    plt.show()
