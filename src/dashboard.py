import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = "../Data/Processed/engineered_dataset.csv"

st.title("🧠 Anti-Procrastination AI Dashboard")

# Load data
df = pd.read_csv(DATA_FILE)

if len(df) == 0:
    st.warning("No data available yet.")
    st.stop()

st.subheader("Dataset Overview")
st.write(df.tail())

# Productivity chart
st.subheader("Focus vs Distraction")

focus_time = df[df["is_study"] == True]["time_spent_sec"].sum()
distraction_time = df[df["is_distraction"] == True]["time_spent_sec"].sum()

labels = ["Focus", "Distraction"]
values = [focus_time, distraction_time]

fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct="%1.1f%%")
st.pyplot(fig)

# Peak procrastination hour
st.subheader("Peak Procrastination Hour")

hour_data = df[df["is_distraction"] == True].groupby("hour").size()

fig2, ax2 = plt.subplots()
hour_data.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Hour")
ax2.set_ylabel("Distractions")
st.pyplot(fig2)

# Study streak trend
st.subheader("Study Streak Trend")

fig3, ax3 = plt.subplots()
df["study_streak"].plot(ax=ax3)
ax3.set_ylabel("Study Streak")
st.pyplot(fig3)