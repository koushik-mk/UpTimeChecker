import streamlit as st
import pandas as pd
from database import get_db_connection

st.title("📊 Uptime Checker Dashboard")

# Fetch Data
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT url, status, response_time, checked_at FROM uptime_logs ORDER BY checked_at DESC LIMIT 20")
data = cursor.fetchall()
conn.close()

# Convert to DataFrame
df = pd.DataFrame(data, columns=["URL", "Status", "Response Time", "Checked At"])

# Display Data
st.dataframe(df)

# Display Status Counts
status_counts = df["Status"].value_counts()
st.bar_chart(status_counts)
