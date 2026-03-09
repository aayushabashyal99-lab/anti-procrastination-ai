import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import resample

DATA_FILE = "../Data/Processed/engineered_dataset.csv"

print("Loading dataset...")

df = pd.read_csv(DATA_FILE, encoding="latin1")

if len(df) == 0:
    print("Dataset empty.")
    exit()

# Convert numeric column
df["time_spent_sec"] = pd.to_numeric(df["time_spent_sec"], errors="coerce")

# Create label
df["label"] = df["category"].apply(lambda x: 0 if x == "study" else 1)

# Select behavioral features ONLY (no leakage)
features = df[[
    "time_spent_sec",
    "idle_time_sec",
    "hour",
    "day_of_week",
    "app_switch",
    "is_night"
]]

features = features.fillna(0)
labels = df["label"]

# -------- SPLIT FIRST (IMPORTANT) --------
X_train, X_test, y_train, y_test = train_test_split(
    features,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels
)

# -------- BALANCE TRAINING DATA ONLY --------
train_df = X_train.copy()
train_df["label"] = y_train

df_majority = train_df[train_df.label == 1]
df_minority = train_df[train_df.label == 0]

df_minority_upsampled = resample(
    df_minority,
    replace=True,
    n_samples=len(df_majority),
    random_state=42
)

df_balanced = pd.concat([df_majority, df_minority_upsampled])

X_train_bal = df_balanced.drop("label", axis=1)
y_train_bal = df_balanced["label"]

print("Tuning model with GridSearch...")

param_grid = {
    "n_estimators": [100, 200, 300],
    "max_depth": [None, 10, 20],
    "min_samples_split": [2, 5],
    "min_samples_leaf": [1, 2]
}

rf = RandomForestClassifier(random_state=42)

grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=3,
    scoring="f1_weighted",
    n_jobs=-1
)

grid_search.fit(X_train_bal, y_train_bal)

model = grid_search.best_estimator_

print("Best Parameters:", grid_search.best_params_)

# -------- EVALUATION --------
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n===== MODEL TRAINED SUCCESSFULLY =====")
print("Model Accuracy:", round(accuracy * 100, 2), "%")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Save model
joblib.dump(model, "../Model/procrastination_model.pkl")

print("\nModel saved as procrastination_model.pkl")