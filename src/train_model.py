import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

DATA_FILE = "../Data/Processed/engineered_dataset.csv"

print("Loading dataset...")

# Load data
df = pd.read_csv(DATA_FILE)

if len(df) == 0:
    print("Dataset empty. Run tracker first.")
    exit()

# Convert time column
df["time_spent_sec"] = pd.to_numeric(df["time_spent_sec"], errors="coerce")

# Create automatic labels
# study = focus (0)
# others = procrastination (1)
df["label"] = df["category"].apply(lambda x: 0 if x == "study" else 1)

# Features for ML
features = df[[
    "time_spent_sec",
    "idle_time_sec",
    "hour",
    "day_of_week",
    "app_switch",
    "is_night",
    "distraction_streak",
    "study_streak"
]]
labels = df["label"]

# Handle missing values
features = features.fillna(0)

# Train test split
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

print("Training ML model...")

model = LogisticRegression()
model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n===== MODEL TRAINED SUCCESSFULLY =====")
print("Model Accuracy:", round(accuracy*100,2), "%")

# Save model
import joblib
joblib.dump(model, "../Model/procrastination_model.pkl")
print("Model saved as procrastination_model.pkl")