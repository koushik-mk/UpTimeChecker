# from fastapi import FastAPI, BackgroundTasks
# import sqlite3
# from datetime import datetime
# import httpx

# app = FastAPI()

# # Database Connection
# from database import get_db_connection

# # List of monitored URLs
# monitored_urls = ["https://eficens.ai"]

# # Function to Check Website
# async def check_website(url):
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(url, timeout=10)
#             status = response.status_code
#             response_time = response.elapsed.total_seconds()
#         except Exception:
#             status = 0  # Service Down
#             response_time = None

#         # Store in Database
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO uptime_logs (url, status, response_time, checked_at) VALUES (?, ?, ?, ?)",
#                        (url, status, response_time, datetime.now()))
#         conn.commit()
#         conn.close()

# # Start Background Monitoring
# @app.get("/start-monitoring")
# async def start_monitoring(background_tasks: BackgroundTasks):
#     for url in monitored_urls:
#         background_tasks.add_task(check_website, url)
#     return {"message": "Monitoring started in the background"}

# # Get Uptime History
# @app.get("/uptime-history")
# def get_uptime_history():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM uptime_logs ORDER BY checked_at DESC LIMIT 20")
#     data = cursor.fetchall()
#     conn.close()
#     return data

from fastapi import FastAPI, BackgroundTasks
import httpx
from datetime import datetime
from database import get_db_connection
from tasks import send_email_alert  # Import email function

app = FastAPI()

# List of monitored URLs
monitored_urls = ["https://eficens.ai"]

# Function to Check Website
async def check_website(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10)
            status = response.status_code
            response_time = response.elapsed.total_seconds()
        except Exception:
            status = 0  # Service Down
            response_time = None

        # Store in Database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO uptime_logs (url, status, response_time, checked_at) VALUES (?, ?, ?, ?)",
                       (url, status, response_time, datetime.now()))
        conn.commit()
        conn.close()

# Background Monitoring
@app.get("/start-monitoring")
async def start_monitoring(background_tasks: BackgroundTasks):
    for url in monitored_urls:
        background_tasks.add_task(check_website, url)
    return {"message": "Monitoring started in the background"}

# Get Uptime History
@app.get("/uptime-history")
def get_uptime_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM uptime_logs ORDER BY checked_at DESC LIMIT 20")
    data = cursor.fetchall()
    conn.close()
    return data

# One-Time Check and Send Email
@app.get("/check-and-email")
async def check_and_email():
    url = "https://eficens.ai"

    try:
        response = httpx.get(url, timeout=10)
        status = response.status_code
        response_time = response.elapsed.total_seconds()
    except Exception:
        status = 0  # Website Down
        response_time = None

    # Store result in DB
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO uptime_logs (url, status, response_time, checked_at) VALUES (?, ?, ?, ?)",
                   (url, status, response_time, datetime.now()))
    conn.commit()
    conn.close()

    # Send Email (One-time)
    send_email_alert(url, status, response_time)

    return {"message": "Email sent successfully!", "url": url, "status": status, "response_time": response_time}
