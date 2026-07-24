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
# STEP 1: CONFIGURATION FOR WDBC.DATASET
# ====================================================================

# 1. PATH TO YOUR CSV FILE (UPDATED to local file name 'wdbc.data')
# --- Make sure 'wdbc.data' is in the same folder as this Python script! ---
CSV_FILE_PATH = 'wdbc.data'

# 2. Define all column names, as the file has no header row
# Column 1: ID, Column 2: Diagnosis (M/B), Columns 3-32: Features
column_names = ['ID', 'Diagnosis'] + [f'Feature_{i}' for i in range(1, 31)]

# 3. NAME OF THE COLUMN TO BE PREDICTED (Y)
TARGET_COLUMN = 'Diagnosis' 

# 4. LIST OF COLUMN NAMES TO BE USED AS INPUT FEATURES (X) - The 30 measurement features
FEATURE_COLUMNS = [f'Feature_{i}' for i in range(1, 31)] 

# 5. TRAINING HYPERPARAMETERS
N_EPOCHS = 20
BATCH_SIZE = 16
VALIDATION_SPLIT_RATIO = 0.1 

# ====================================================================
# STEP 2: DATA LOADING AND PREPARATION
# ====================================================================

try:
    # --- Data Loading ---
    # Load the data specifying no header and using the custom column names
    df = pd.read_csv(CSV_FILE_PATH, header=None, names=column_names)

    # Drop the ID column as it is not needed for training
    df = df.drop(columns=['ID'])
    print(f"--- Loaded WDBC DATA with {len(df)} samples and {len(df.columns)} columns ---")

    # Separate features (X) and target (y)
    X = df[FEATURE_COLUMNS].values
    y = df[TARGET_COLUMN].values

    # 1. Encode the target variable (Malignant=1, Benign=0)
    le = LabelEncoder()
    y_encoded = le.fit_transform(y) 
    print(f"Target classes encoded: {le.classes_} -> {le.transform(le.classes_)}")

    # 2. Split Data (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    # 3. Scale Features (Essential for Neural Networks)
    sc = StandardScaler()
    X_train_sc = sc.fit_transform(X_train)
    X_test_sc = sc.transform(X_test)

except Exception as e:
    # Specific error handling for local file loading
    if 'FileNotFoundError' in str(e) or 'does not exist' in str(e):
        print(f"\nERROR: CSV file not found at path: '{CSV_FILE_PATH}'. Please ensure 'wdbc.data' is in the same directory as this script.")
    else:
        print(f"\nERROR during data processing: {e}")
    exit()

# ====================================================================
# STEP 3: MODEL DEFINITION AND TRAINING
# ====================================================================

input_dim = X_train_sc.shape[1] # Should be 30 features
print(f"\nInput dimension (number of features): {input_dim}")

# Define the Sequential Model
model = Sequential([
    Dense(64, activation='relu', input_shape=(input_dim,)),
    Dense(32, activation='relu'),
    # Output layer: 1 neuron with sigmoid for binary classification
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy', 
    metrics=['accuracy']
)

# Train the model with the requested 20 epochs
print(f"\n--- Starting Model Training ({N_EPOCHS} Epochs) ---")
history = model.fit(
    X_train_sc,
    y_train,
    epochs=N_EPOCHS, 
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