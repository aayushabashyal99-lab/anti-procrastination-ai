import pandas as pd
import joblib
import time
import tkinter as tk
from tkinter import messagebox

MODEL_FILE = "../Model/procrastination_model.pkl"
DATA_FILE = "../Data/Processed/engineered_dataset.csv"

print("Starting AI Monitoring System...")

model = joblib.load(MODEL_FILE)

def show_alert():
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showwarning(
        "Procrastination Alert ⚠️",
        "You are getting distracted!\nReturn to study immediately!"
    )
    root.destroy()

while True:
    try:
        df = pd.read_csv(DATA_FILE)

        if len(df) == 0:
            time.sleep(10)
            continue

        # TAKE ONLY LAST ROW
        latest = df.tail(1)

        # SAME FEATURES USED DURING TRAINING
        features = latest[[
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

        if prediction == 1:
            print("⚠️ Procrastination detected!")
            show_alert()
        else:
            print("Focused...")

        time.sleep(30)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)