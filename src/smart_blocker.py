import pandas as pd
import joblib
import time
import psutil
import win32gui
import win32process

MODEL_FILE = "../Model/procrastination_model.pkl"
DATA_FILE = "../Data/Processed/engineered_dataset.csv"

model = joblib.load(MODEL_FILE)

print("Smart AI Blocker Started...")

# Keywords
ALWAYS_ALLOW = ["ChatGPT", "Gmail", "Classroom", "Google Docs", "Visual Studio Code"]
ALWAYS_BLOCK = ["Instagram", "Facebook"]
CONDITIONAL_BLOCK = ["YouTube", "WhatsApp"]

def get_active_window():
    window = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(window)
    _, pid = win32process.GetWindowThreadProcessId(window)
    process = psutil.Process(pid)
    return title, process.name()

def close_process(process_name):
    for proc in psutil.process_iter():
        try:
            if proc.name() == process_name:
                proc.kill()
        except:
            pass

while True:
    try:
        df = pd.read_csv(DATA_FILE)

        if len(df) == 0:
            time.sleep(10)
            continue

        latest = df.tail(1)

        features = latest[[
            "time_spent_sec",
            "idle_time_sec",
            "hour",
            "day_of_week",
            "app_switch",
            "is_night",
            "distraction_streak",
            "study_streak"
        ]].fillna(0)

        prediction = model.predict(features)[0]

        title, process_name = get_active_window()

        # Always allow important apps
        if any(keyword in title for keyword in ALWAYS_ALLOW):
            time.sleep(10)
            continue

        # Always block these
        if any(keyword in title for keyword in ALWAYS_BLOCK):
            print("Blocked:", title)
            close_process(process_name)

        # Conditional block
        if any(keyword in title for keyword in CONDITIONAL_BLOCK):
            if prediction == 1 or latest["distraction_streak"].values[0] >= 3:
                print("Conditionally Blocked:", title)
                close_process(process_name)

        time.sleep(10)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)