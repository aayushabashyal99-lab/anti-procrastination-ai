import pandas as pd
import joblib

print("Loading model...")

model = joblib.load("../Model/procrastination_model.pkl")

DATA_FILE = "activity_dataset.csv"

df = pd.read_csv("../Data/Processed/engineered_dataset.csv")

# Take latest activity
latest = df.tail(1)

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
features = features.fillna(0)

prediction = model.predict(features)[0]

print("\n===== REAL-TIME PREDICTION =====")

if prediction == 1:
    print("You are likely PROCRASTINATING ⚠️")
else:
    print("You are FOCUSED 🔥")