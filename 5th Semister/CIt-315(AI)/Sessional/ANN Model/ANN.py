import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import accuracy_score

# ====================================================================
# STEP 1: CONFIGURATION (USER MUST EDIT THESE VARIABLES)
# ====================================================================

# 1. PATH TO YOUR CSV FILE
CSV_FILE_PATH = 'your_data.csv' # <<< CHANGE THIS to your file path

# 2. LIST OF COLUMN NAMES TO BE USED AS INPUT FEATURES (X)
# Example for a simple 4-feature model: ['feature_1', 'feature_2', 'feature_3', 'feature_4']
FEATURE_COLUMNS = ['Age', 'Tumor_Size', 'Cell_Density', 'Pressure'] # <<< CHANGE THIS

# 3. NAME OF THE COLUMN TO BE PREDICTED (Y)
TARGET_COLUMN = 'Diagnosis' # <<< CHANGE THIS (Must contain categorical data, e.g., 'Yes'/'No' or 'A'/'B')

# 4. TRAINING HYPERPARAMETERS
N_EPOCHS = 20
BATCH_SIZE = 16
VALIDATION_SPLIT_RATIO = 0.1 # 10% of training data used for validation checks

# ====================================================================
# STEP 2: DATA LOADING AND PREPARATION
# ====================================================================

try:
    # --- Data Loading (Simulated for demonstration) ---
    # NOTE: In a real scenario, uncomment the line below and comment out the simulation block.
    # df = pd.read_csv(CSV_FILE_PATH)

    # --- SIMULATING CSV DATA LOAD (Delete this block when using a real CSV) ---
    # This block creates the required data structure if you don't have a CSV yet.
    np.random.seed(42)
    data_size = 300
    df = pd.DataFrame({
        'Age': np.random.randint(20, 80, data_size),
        'Tumor_Size': np.random.uniform(1.0, 15.0, data_size),
        'Cell_Density': np.random.uniform(50, 200, data_size),
        'Pressure': np.random.normal(120, 15, data_size),
        'Diagnosis': np.random.choice(['Benign', 'Malignant'], size=data_size, p=[0.6, 0.4])
    })
    print(f"--- Using SIMULATED DATA with {len(df)} samples ---")
    # --------------------------------------------------------------------------

    # Separate features (X) and target (y)
    X = df[FEATURE_COLUMNS].values
    y = df[TARGET_COLUMN].values

    # 1. Encode the target variable (assuming binary classification: e.g., 'Benign' -> 0, 'Malignant' -> 1)
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    print(f"Target classes encoded: {le.classes_} -> {le.transform(le.classes_)}")

    # 2. Split Data (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    # 3. Scale Features (Min/Max or Standard Scaling is essential for NN)
    sc = StandardScaler()
    X_train_sc = sc.fit_transform(X_train)
    X_test_sc = sc.transform(X_test)

except KeyError as e:
    print(f"\nERROR: Column '{e}' not found in the DataFrame. Check your FEATURE_COLUMNS or TARGET_COLUMN configuration.")
    exit()
except FileNotFoundError:
    print(f"\nERROR: CSV file not found at path: {CSV_FILE_PATH}. Please check the file path.")
    exit()

# ====================================================================
# STEP 3: MODEL DEFINITION AND TRAINING
# ====================================================================

input_dim = X_train_sc.shape[1]
print(f"\nInput dimension (number of features): {input_dim}")

# Define the Sequential Model (standard dense layers)
model = Sequential([
    Dense(64, activation='relu', input_shape=(input_dim,)),
    Dense(32, activation='relu'),
    # Output layer: 1 neuron with sigmoid for binary classification
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy', # Appropriate loss for binary output
    metrics=['accuracy']
)

# Train the model with the requested number of epochs
print(f"\n--- Starting Model Training ({N_EPOCHS} Epochs) ---")
history = model.fit(
    X_train_sc,
    y_train,
    epochs=N_EPOCHS, # Use the configured number of epochs (20)
    batch_size=BATCH_SIZE,
    verbose=1,
    validation_split=VALIDATION_SPLIT_RATIO
)
print("Model Training Complete.")

# ====================================================================
# STEP 4: EVALUATION AND PREDICTION
# ====================================================================

loss, acc = model.evaluate(X_test_sc, y_test, verbose=0)
print(f"\n--- Model Test Evaluation ---")
print(f"Test Loss: {loss:.4f}")
print(f"Test Accuracy: {acc*100:.2f}%")

# Make predictions
test_predictions_proba = model.predict(X_test_sc)

# Convert probabilities to binary class labels (0 or 1)
predicted_classes = (test_predictions_proba > 0.5).astype("int32").flatten()

# Display results
print("\nFirst 5 True Labels:", y_test[:5])
print("First 5 Predicted Labels:", predicted_classes[:5])
print(f"Final Accuracy Score (Sklearn check): {accuracy_score(y_test, predicted_classes)*100:.2f}%")

# ====================================================================
# STEP 5: GRAPH CHART VISUALIZATION (matplotlib)
# ====================================================================

history_dict = history.history

# Extract loss and accuracy values
loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']
acc_values = history_dict['accuracy']
val_acc_values = history_dict['val_accuracy']
epochs_range = range(1, N_EPOCHS + 1)

plt.figure(figsize=(14, 6))

# Subplot 1: Loss
plt.subplot(1, 2, 1)
plt.plot(epochs_range, loss_values, 'bo-', label='Training Loss')
plt.plot(epochs_range, val_loss_values, 'ro-', label='Validation Loss')
plt.title(f'Loss Over {N_EPOCHS} Epochs', fontsize=14)
plt.xlabel('Epochs', fontsize=12)
plt.ylabel('Loss', fontsize=12)
plt.legend()
plt.grid(True)

# Subplot 2: Accuracy
plt.subplot(1, 2, 2)
plt.plot(epochs_range, acc_values, 'bo-', label='Training Accuracy')
plt.plot(epochs_range, val_acc_values, 'ro-', label='Validation Accuracy')
plt.title(f'Accuracy Over {N_EPOCHS} Epochs', fontsize=14)
plt.xlabel('Epochs', fontsize=12)
plt.ylabel('Accuracy', fontsize=12)
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()