import pandas as pd

# Load final dataset
df = pd.read_csv("Data/processed/final_dataset.csv")

# Columns that existed in engineered dataset
engineered_columns = [
    "timestamp",
    "app_name",
    "window_title",
    "category",
    "time_spent_sec",
    "idle_time_sec",
    "hour",
    "day_of_week",
    "is_weekend",
    "prev_app",
    "app_switch",
    "is_night",
    "is_distraction",
    "is_study",
    "distraction_streak",
    "study_streak"
]

engineered_df = df[engineered_columns]

engineered_df.to_csv(
    "Data/processed/engineered_dataset.csv",
    index=False
)

print("engineered_dataset.csv restored successfully")