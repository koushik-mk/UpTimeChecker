# from celery import Celery
# import httpx
# from datetime import datetime
# from database import get_db_connection

# # Celery Setup
# celery = Celery("tasks", broker="redis://localhost:6379/0")

# monitored_urls = ["https://eficens.ai"]

# @celery.task
# def check_websites():
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     for url in monitored_urls:
#         try:
#             response = httpx.get(url, timeout=10)
#             status = response.status_code
#             response_time = response.elapsed.total_seconds()
#         except Exception:
#             status = 0
#             response_time = None

#         # Store result in DB
#         cursor.execute("INSERT INTO uptime_logs (url, status, response_time, checked_at) VALUES (?, ?, ?, ?)",
#                        (url, status, response_time, datetime.now()))
#         conn.commit()

#         if status == 0:
#             print(f"ALERT: {url} is DOWN!")

#     conn.close()

from celery import Celery
import httpx
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from database import get_db_connection

# Celery Setup
celery = Celery("tasks", broker="redis://localhost:6379/0")

# Monitored Websites
monitored_urls = ["https://eficens.ai"]

# Email Configuration
EMAIL_SENDER = "koushikn395@gmail.com"
EMAIL_PASSWORD = "sxxsybbcjbmximqp"
EMAIL_RECEIVER = "masam.srivyshnavi21@ifheindia.org"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Send Email Alert
def send_email_alert(url, status, response_time):
    status_message = "✅ Website is UP" if status == 200 else "❌ Website is DOWN"
    response_time_msg = f"Response Time: {response_time:.2f} seconds" if response_time else "No response"

    subject = f"🌐 Uptime Report: {url} - {status_message}"
    body = f"""
    Website: {url}
    Status: {status} ({status_message})
    {response_time_msg}

    Checked At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print(f"📧 Email Sent: {url} - {status_message}")
    except Exception as e:
        print(f"⚠️ Failed to send email: {e}")

# Monitor Website and Store in DB
@celery.task
def check_websites():
    conn = get_db_connection()
    cursor = conn.cursor()

    for url in monitored_urls:
        try:
            response = httpx.get(url, timeout=10)
            status = response.status_code
            response_time = response.elapsed.total_seconds()
        except Exception:
            status = 0
            response_time = None

        # Store result in DB
        cursor.execute("INSERT INTO uptime_logs (url, status, response_time, checked_at) VALUES (?, ?, ?, ?)",
                       (url, status, response_time, datetime.now()))
        conn.commit()

        if status == 0:
            print(f"ALERT: {url} is DOWN!")

    conn.close()
