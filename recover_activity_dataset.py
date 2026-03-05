import pandas as pd

# Load the processed dataset
df = pd.read_csv("Data/processed/final_dataset.csv")

# Columns needed for the tracker (raw dataset structure)
raw_columns = [
    "timestamp",
    "app_name",
    "window_title",
    "category",
    "time_spent_sec",
    "idle_time_sec"
]

# Extract only the raw columns
activity_df = df[raw_columns]

# Save back as raw dataset
activity_df.to_csv("Data/Raw/activity_dataset.csv", index=False)

print("activity_dataset.csv successfully restored.")
print("Rows recovered:", len(activity_df))