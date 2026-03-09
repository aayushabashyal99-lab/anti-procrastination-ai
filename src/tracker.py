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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "Data", "Raw", "activity_dataset.csv")

TRACK_INTERVAL = 5  # seconds

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


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]


def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = ctypes.sizeof(lastInputInfo)

    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lastInputInfo))

    millis = ctypes.windll.kernel32.GetTickCount() - lastInputInfo.dwTime

    return millis / 1000.0


def categorize_app(app_name):
    return APP_CATEGORIES.get(app_name, "other")


# ==============================
# DATASET
# ==============================

def initialize_dataset():

    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

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

        print("Dataset created:", DATA_FILE)


def save_record(record):

    df = pd.DataFrame([record])

    df.to_csv(
        DATA_FILE,
        mode="a",
        header=False,
        index=False,
        encoding="utf-8"
    )

    print("Saved:", record)


# ==============================
# TRACKER
# ==============================

def run_tracker():

    print("Anti-Procrastination AI Tracker Started...")
    print("Saving data to:", DATA_FILE)
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
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "app_name": last_app,
                "window_title": last_title.replace(",", " "),  # prevent CSV break
                "category": categorize_app(last_app),
                "time_spent_sec": round(time_spent, 2),
                "idle_time_sec": round(idle_time, 2),
                "hour": now.hour,
                "day_of_week": now.weekday(),
                "is_weekend": 1 if now.weekday() >= 5 else 0,
                "label": ""
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