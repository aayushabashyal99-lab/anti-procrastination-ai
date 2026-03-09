import pandas as pd
import os

print("Starting feature engineering...")

# ----------------------------
# Paths
# ----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_FILE = os.path.join(BASE_DIR, "Data", "Raw", "activity_dataset.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "Data", "processed", "engineered_dataset.csv")

# Ensure processed folder exists
os.makedirs(os.path.join(BASE_DIR, "Data", "processed"), exist_ok=True)

# ----------------------------
# Load dataset
# ----------------------------

df = pd.read_csv(DATA_FILE, encoding="latin1", on_bad_lines="skip")

# ----------------------------
# Timestamp processing
# ----------------------------

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# Extract hour safely
df["hour"] = df["timestamp"].dt.hour.fillna(0).astype(int)

# ----------------------------
# Numeric conversions
# ----------------------------

df["time_spent_sec"] = pd.to_numeric(df["time_spent_sec"], errors="coerce").fillna(0)
df["idle_time_sec"] = pd.to_numeric(df["idle_time_sec"], errors="coerce").fillna(0)

# ----------------------------
# App switching feature
# ----------------------------

df["prev_app"] = df["app_name"].shift(1)
df["app_switch"] = (df["app_name"] != df["prev_app"]).astype(int)

# ----------------------------
# Night usage feature
# ----------------------------

df["is_night"] = df["hour"].apply(lambda x: 1 if x >= 22 or x <= 3 else 0)

# ----------------------------
# Study vs Distraction
# ----------------------------

df["is_distraction"] = (df["category"] != "study").astype(int)
df["is_study"] = (df["category"] == "study").astype(int)

# ----------------------------
# Distraction streak
# ----------------------------

df["distraction_streak"] = (
    df["is_distraction"]
    .groupby((df["is_distraction"] != df["is_distraction"].shift()).cumsum())
    .cumsum()
)

# ----------------------------
# Study streak
# ----------------------------

df["study_streak"] = (
    df["is_study"]
    .groupby((df["is_study"] != df["is_study"].shift()).cumsum())
    .cumsum()
)

# ----------------------------
# Save engineered dataset
# ----------------------------

df.to_csv(OUTPUT_FILE, index=False)

print("Feature engineering complete.")
print("Updated file:", OUTPUT_FILE)
print("Total rows processed:", len(df))