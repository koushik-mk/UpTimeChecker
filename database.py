import sqlite3

def get_db_connection():
    conn = sqlite3.connect("uptime.db", check_same_thread=False)
    return conn

# Initialize Database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS uptime_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            status INTEGER,
            response_time REAL,
            checked_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Run on first start
init_db()
