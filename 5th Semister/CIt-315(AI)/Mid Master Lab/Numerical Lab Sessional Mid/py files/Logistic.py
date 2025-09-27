import numpy as np
import matplotlib.pyplot as plt

# Sigmoid function
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Logistic Regression using Gradient Descent
def logistic_regression(X, y, lr=0.01, epochs=1000):
    n_samples, n_features = X.shape
    weights = np.zeros(n_features)
    bias = 0

    for _ in range(epochs):
        linear_model = np.dot(X, weights) + bias
        y_pred = sigmoid(linear_model)

        # Gradients
        dw = (1/n_samples) * np.dot(X.T, (y_pred - y))
        db = (1/n_samples) * np.sum(y_pred - y)

        # Update weights and bias
        weights -= lr * dw
        bias -= lr * db

    return weights, bias

# Prediction function
def predict(X, weights, bias):
    linear_model = np.dot(X, weights) + bias
    y_pred = sigmoid(linear_model)
    return [1 if i >= 0.5 else 0 for i in y_pred]

# Main program
if __name__ == "__main__":
    print("Logistic Regression 2D Plot (2 features)\n")
    n_samples = int(input("Enter number of samples: "))
    n_features = int(input("Enter number of features (must be 2 for 2D plot): "))

    if n_features != 2:
        print("2D plot works only for 2 features. Proceeding without plot.")

    # Input features
    print("\nEnter the feature values row-wise (space separated, two values per sample):")
    X = []
    for i in range(n_samples):
        row = list(map(float, input(f"Sample {i+1}: ").split()))
        if len(row) != 2:
            raise ValueError("Each sample must have exactly 2 feature values.")
        X.append(row)
    X = np.array(X)

    # Input target values
    print("\nEnter the target values (0 or 1) row-wise, space separated:")
    y = list(map(int, input().split()))
    if len(y) != n_samples:
        raise ValueError("Number of target values must match number of samples.")
    y = np.array(y)

    lr = float(input("\nEnter learning rate (e.g., 0.01): "))
    epochs = int(input("Enter number of epochs (e.g., 1000): "))

    # Train Logistic Regression
    weights, bias = logistic_regression(X, y, lr, epochs)
    print("\nTrained Weights:", weights)
    print("Trained Bias:", bias)

    predictions = predict(X, weights, bias)
    print("\nPrediction for training data:")
    print(predictions)

    # 2D Plotting (decision boundary)
    if n_features == 2:
        plt.figure(figsize=(8,6))

        # Scatter points by class
        for label in np.unique(y):
            plt.scatter(X[y==label,0], X[y==label,1], label=f'Class {label}', s=50)

        # Plot decision boundary
        x_values = np.linspace(min(X[:,0])-1, max(X[:,0])+1, 200)
        y_values = -(weights[0]*x_values + bias)/weights[1]  # w1*x + w2*y + b = 0 => y = -(w1*x+b)/w2
        plt.plot(x_values, y_values, color='red', label='Decision Boundary')

        plt.xlabel('X1')
        plt.ylabel('X2')
        plt.title('Logistic Regression Decision Boundary (2D)')
        plt.legend()
        plt.show()
