import matplotlib.pyplot as plt
import numpy as np
import math

# Function definition
def f(x):
    return eval(expr)

# False Position (Regula Falsi) Method
def false_position(a, b, tol, max_iter):
    if f(a) * f(b) > 0:
        print("Invalid interval! f(a) and f(b) must have opposite signs.")
        return None

    print("\nFalse Position Method (Regula Falsi)")
    print("------------------------------------")

    x_history = []  # To store approximations for plotting
    c_history = []

    for i in range(1, max_iter + 1):
        # Formula: c = (a*f(b) - b*f(a)) / (f(b) - f(a))
        c = (a * f(b) - b * f(a)) / (f(b) - f(a))
        print(f"Iteration {i}: a={a:.6f}, b={b:.6f}, c={c:.6f}, f(c)={f(c):.6f}")

        x_history.append(c)
        c_history.append(f(c))

        if abs(f(c)) < tol:
            print("\nRoot found:", c)
            return c, x_history
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    print("\nDid not converge within given iterations.")
    return None, x_history

# Main program
if __name__ == "__main__":
    expr = input("Enter function f(x) in terms of math (e.g., 'x**3 - x - 2'): ")
    a = float(input("Enter lower bound a: "))
    b = float(input("Enter upper bound b: "))
    tol = float(input("Enter tolerance (e.g., 0.0001): "))
    max_iter = int(input("Enter maximum iterations: "))

    root, history = false_position(a, b, tol, max_iter)

    # 2D Plot
    x_vals = np.linspace(a - 1, b + 1, 400)
    y_vals = [f(x) for x in x_vals]

    plt.figure(figsize=(8,6))
    plt.plot(x_vals, y_vals, label='f(x)', color='blue')
    plt.axhline(0, color='black', linewidth=1)

    # Plot approximations
    for i, x_c in enumerate(history):
        plt.scatter(x_c, f(x_c), color='red')
        plt.text(x_c, f(x_c), f'c{i+1}', fontsize=9, color='red')

    plt.scatter(root, f(root), color='green', s=100, label='Root' if root else '')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('False Position Method (Regula Falsi)')
    plt.legend()
    plt.grid(True)
    plt.show()
