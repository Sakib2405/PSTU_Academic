import numpy as np
import matplotlib.pyplot as plt

# Linear Regression using Stochastic Gradient Descent
def stochastic_gradient_descent(X, y, lr=0.01, epochs=100):
    n_samples, n_features = X.shape
    weights = np.zeros(n_features)
    bias = 0

    for _ in range(epochs):
        for i in range(n_samples):
            xi = X[i]
            yi = y[i]
            y_pred = np.dot(xi, weights) + bias
            error = y_pred - yi

            # Update weights and bias
            weights -= lr * error * xi
            bias -= lr * error

    return weights, bias

# Prediction function
def predict(X, weights, bias):
    return np.dot(X, weights) + bias

# Main program
if __name__ == "__main__":
    print("Linear Regression using SGD (2D Plot for 1 feature)\n")

    n_samples = int(input("Enter number of samples: "))
    n_features = 1
    print("This program works with 1 feature for 2D plotting.")

    # Input features
    print("\nEnter the feature values row-wise (one value per sample):")
    X = []
    for i in range(n_samples):
        xi = float(input(f"Sample {i+1}: "))
        X.append([xi])  # 2D array for matrix multiplication
    X = np.array(X)

    # Input target values
    print("\nEnter the target values (Y) row-wise, space separated:")
    y = list(map(float, input().split()))
    if len(y) != n_samples:
        raise ValueError("Number of target values must match number of samples.")
    y = np.array(y)

    lr = float(input("\nEnter learning rate (e.g., 0.01): "))
    epochs = int(input("Enter number of epochs (e.g., 1000): "))

    # Train model
    weights, bias = stochastic_gradient_descent(X, y, lr, epochs)

    print("\nTrained Weight:", weights[0])
    print("Trained Bias:", bias)

    predictions = predict(X, weights, bias)
    print("\nPredictions for training data:")
    print(predictions)

    # 2D Plotting
    plt.scatter(X, y, color='blue', label='Actual Data')
    plt.plot(X, predictions, color='red', label='Regression Line')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Linear Regression using SGD (2D)')
    plt.legend()
    plt.show()
