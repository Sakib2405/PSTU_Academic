import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

e = 2.718281828


def f(x):
    return e ** x - (3 * x)


def bisection(a, b, tol=0.0001, max_iter=20):
    if f(a) * f(b) >= 0:
        print("Invalid interval. f(a) and f(b) must have opposite signs.")
        return None

    data = []
    for i in range(1, max_iter + 1):
        c = (a + b) / 2
        fa, fb, fc = f(a), f(b), f(c)
        error = abs(b - a)
        data.append([i, a, b, c, fa, fb, fc, error])

        if abs(fc) < tol or error < tol:
            break

        if fa * fc < 0:
            b = c
        else:
            a = c

    df = pd.DataFrame(data, columns=["Iter", "a", "b", "c", "f(a)", "f(b)", "f(c)", "Error"])
    return c, df


a = 0
b = 1
root, table = bisection(a, b)

# table
print(table)

# graph
x = np.linspace(a - 1, b + 1, 400)
y = f(x)
plt.plot(x, y)
plt.axhline(0, color='black')
plt.axvline(0, color='black')
plt.scatter(root, f(root), color='red', label=f'Root ≈ {root:.4f}')
plt.title('Bisection Method Graph')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid()
plt.show()
