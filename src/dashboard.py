import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib

DATA_FILE = "../Data/Processed/engineered_dataset.csv"
MODEL_FILE = "../Model/procrastination_model.pkl"

st.set_page_config(page_title="Anti-Procrastination AI", layout="wide")

st.title("🧠 Anti-Procrastination AI Dashboard")

# Load data
df = pd.read_csv(DATA_FILE)

if len(df) == 0:
    st.warning("No data available.")
    st.stop()

# Load model
model = joblib.load(MODEL_FILE)

# -------- Productivity Score --------
df["label"] = df["category"].apply(lambda x: 0 if x == "study" else 1)
study_count = (df["label"] == 0).sum()
total = len(df)

productivity_score = round((study_count / total) * 100, 2)

st.metric("📊 Productivity Score", f"{productivity_score}%")

st.divider()

# -------- Pie Chart --------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Study vs Distraction Distribution")
    pie_data = df["label"].value_counts()
    labels = ["Distraction", "Study"]

    fig1, ax1 = plt.subplots()
    ax1.pie(pie_data, labels=labels, autopct="%1.1f%%")
    st.pyplot(fig1)

# -------- Hourly Trend --------
with col2:
    st.subheader("Hourly Usage Trend")
    hourly = df.groupby("hour").size()

    fig2, ax2 = plt.subplots()
    ax2.plot(hourly.index, hourly.values)
    ax2.set_xlabel("Hour")
    ax2.set_ylabel("Activity Count")
    st.pyplot(fig2)

st.divider()

# -------- App Switch Analysis --------
st.subheader("App Switch Frequency")

switch_data = df["app_switch"].sum()

st.write(f"Total App Switches: {switch_data}")

# -------- Real-Time Prediction --------
st.divider()
st.subheader("Current AI Prediction")

latest = df.tail(1)

features = latest[[
    "time_spent_sec",
    "idle_time_sec",
    "hour",
    "day_of_week",
    "app_switch",
    "is_night"
]]

prediction = model.predict(features)[0]

if prediction == 0:
    st.success("🔥 You are currently FOCUSED")
else:
    st.error("⚠️ You are currently DISTRACTED")