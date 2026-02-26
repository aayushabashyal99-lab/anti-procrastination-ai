import psutil
import time
import pandas as pd
from datetime import datetime
import win32gui
import win32process
import ctypes
import os

# ==============================
# CONFIG
# ==============================

DATA_FILE = "../Data/Raw/activity_dataset.csv"
TRACK_INTERVAL = 5  # seconds

# App category mapping (edit as needed)
APP_CATEGORIES = {
    "chrome.exe": "browser",
    "msedge.exe": "browser",
    "code.exe": "study",
    "pycharm64.exe": "study",
    "notepad.exe": "study",
    "winword.exe": "study",
    "excel.exe": "study",
    "powerpnt.exe": "study",
    "vlc.exe": "entertainment",
    "spotify.exe": "entertainment",
    "telegram.exe": "social",
    "whatsapp.exe": "social",
    "instagram.exe": "social",
}

# ==============================
# SYSTEM FUNCTIONS
# ==============================

# Get active window
def get_active_window():
    window = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(window)
    _, pid = win32process.GetWindowThreadProcessId(window)

    try:
        process = psutil.Process(pid)
        process_name = process.name().lower()
    except:
        process_name = "unknown"

    return process_name, title


# Detect idle time (keyboard + mouse inactivity)
class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = ctypes.sizeof(lastInputInfo)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lastInputInfo))
    millis = ctypes.windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0


# Categorize app
def categorize_app(app_name):
    return APP_CATEGORIES.get(app_name, "other")


# Initialize dataset file
def initialize_dataset():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            "timestamp",
            "app_name",
            "window_title",
            "category",
            "time_spent_sec",
            "idle_time_sec",
            "hour",
            "day_of_week",
            "is_weekend",
            "label"
        ])
        df.to_csv(DATA_FILE, index=False)


# Save record
def save_record(record):
    df = pd.DataFrame([record])
    df.to_csv(DATA_FILE, mode='a', header=False, index=False)


# ==============================
# MAIN TRACKER
# ==============================

def run_tracker():
    print("Anti-Procrastination AI Tracker Started...")
    print("Press CTRL + C to stop.\n")

    last_app = None
    last_title = None
    start_time = time.time()

    while True:
        app, title = get_active_window()
        current_time = time.time()

        if last_app is None:
            last_app = app
            last_title = title
            start_time = current_time

        if app != last_app or title != last_title:
            time_spent = current_time - start_time
            idle_time = get_idle_duration()

            now = datetime.now()

            record = {
                "timestamp": now,
                "app_name": last_app,
                "window_title": last_title,
                "category": categorize_app(last_app),
                "time_spent_sec": round(time_spent, 2),
                "idle_time_sec": round(idle_time, 2),
                "hour": now.hour,
                "day_of_week": now.weekday(),
                "is_weekend": 1 if now.weekday() >= 5 else 0,
                "label": ""  # Fill later: 0 focus, 1 procrastination
            }

            save_record(record)

            last_app = app
            last_title = title
            start_time = current_time

        time.sleep(TRACK_INTERVAL)


# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    initialize_dataset()
    try:
        run_tracker()
    except KeyboardInterrupt:
        print("\nTracker stopped. Dataset saved.")