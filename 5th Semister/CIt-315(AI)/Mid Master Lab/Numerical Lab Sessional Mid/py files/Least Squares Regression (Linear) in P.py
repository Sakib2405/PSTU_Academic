import matplotlib.pyplot as plt

# Least Squares Regression (Linear)
def least_squares_regression(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x[i]*y[i] for i in range(n))
    sum_x2 = sum(x[i]**2 for i in range(n))

    # Calculate slope (m) and intercept (c)
    m = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x**2)
    c = (sum_y - m*sum_x) / n

    return m, c

if __name__ == "__main__":
    n = int(input("Enter number of data points: "))
    
    x = []
    y = []

    print("Enter the data points:")
    for i in range(n):
        xi, yi = map(float, input(f"Point {i+1} (x y): ").split())
        x.append(xi)
        y.append(yi)
    
    m, c = least_squares_regression(x, y)
    print(f"\nRegression Line: y = {m:.4f}x + {c:.4f}")

    # 2D Plotting
    plt.scatter(x, y, color='blue', label='Data Points')  # Scatter plot of points
    x_values = [min(x)-1, max(x)+1]
    y_values = [m*xi + c for xi in x_values]
    plt.plot(x_values, y_values, color='red', label='Regression Line')  # Regression line
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Least Squares Regression (Linear)')
    plt.legend()
    plt.show()
