import pandas as pd

# -----------------------------
# Load Dataset
# -----------------------------
DATA_PATH = "Data/processed/engineered_dataset.csv"
OUTPUT_PATH = "Data/processed/final_dataset.csv"

df = pd.read_csv(DATA_PATH)

print("Columns found:", df.columns)

# -----------------------------
# Convert TRUE/FALSE → 1/0
# -----------------------------
df["is_distraction"] = df["is_distraction"].astype(str).str.upper().map({
    "TRUE": 1,
    "FALSE": 0
})

df["is_study"] = df["is_study"].astype(str).str.upper().map({
    "TRUE": 1,
    "FALSE": 0
})

# -----------------------------
# Create Label
# 1 = Distraction
# 0 = Study
# -----------------------------
df["label"] = df["is_distraction"]

# -----------------------------
# Create Focus Score
# (Measures productivity)
# -----------------------------
df["focus_score"] = df["time_spent_sec"] / (
    df["time_spent_sec"] + df["idle_time_sec"] + 1e-5
)

# -----------------------------
# Optional Extra Features
# (makes dataset stronger)
# -----------------------------

# Night productivity
df["night_productivity"] = df["is_night"] * df["is_study"]

# Distraction pressure
df["distraction_pressure"] = df["distraction_streak"] * df["app_switch"]

# Study momentum
df["study_momentum"] = df["study_streak"] * df["focus_score"]

# -----------------------------
# Save Final Dataset
# -----------------------------
df.to_csv(OUTPUT_PATH, index=False)

print("Final dataset saved as:", OUTPUT_PATH)
print("Total rows:", len(df))