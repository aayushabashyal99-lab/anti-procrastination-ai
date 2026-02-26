import pandas as pd

print("Starting feature engineering...")

DATA_FILE = "../Data/Raw/activity_dataset.csv"

df = pd.read_csv(DATA_FILE)

# Convert time
df["time_spent_sec"] = pd.to_numeric(df["time_spent_sec"], errors="coerce")

# App switching frequency
df["prev_app"] = df["app_name"].shift(1)
df["app_switch"] = (df["app_name"] != df["prev_app"]).astype(int)

# Night usage
df["is_night"] = df["hour"].apply(lambda x: 1 if x >= 22 or x <= 3 else 0)

# Distraction vs study
df["is_distraction"] = df["category"] != "study"
df["is_study"] = df["category"] == "study"

# Distraction streak
df["distraction_streak"] = (
    df["is_distraction"]
    .groupby((df["is_distraction"] != df["is_distraction"].shift()).cumsum())
    .cumsum()
)

# Study streak
df["study_streak"] = (
    df["is_study"]
    .groupby((df["is_study"] != df["is_study"].shift()).cumsum())
    .cumsum()
)

# Save engineered dataset
df.to_csv("../Data/Processed/engineered_dataset.csv", index=False)

print("Feature engineering complete.")
print("New file created: engineered_dataset.csv")