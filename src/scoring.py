import pandas as pd

print("Starting scoring script...")

DATA_FILE = "activity_dataset.csv"

try:
    df = pd.read_csv(DATA_FILE)
    print("Dataset loaded.")
except Exception as e:
    print("Error reading dataset:", e)
    exit()

print("Rows found:", len(df))

if len(df) == 0:
    print("Dataset empty. Run tracker first.")
    exit()

# Convert numeric column
df["time_spent_sec"] = pd.to_numeric(df["time_spent_sec"], errors="coerce")

focus_time = df[df["category"] == "study"]["time_spent_sec"].sum()
distraction_time = df[df["category"] != "study"]["time_spent_sec"].sum()

total_time = focus_time + distraction_time

if total_time == 0:
    print("No usable data yet.")
    exit()

score = (focus_time / total_time) * 100

print("\n===== Productivity Result =====")
print("Focus Time:", round(focus_time/60,2), "minutes")
print("Distraction Time:", round(distraction_time/60,2), "minutes")
print("Productivity Score:", round(score,2), "%")