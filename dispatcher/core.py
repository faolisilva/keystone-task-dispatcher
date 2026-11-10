import sqlite3
import json

# Using a local SQLite file for simplicity. In prod we might move to Postgres,
# but for now, keeping it file-based avoids infra overhead.
DB_FILE = "tasks.sqlite"

def get_connection():
    # We create a new connection per call. SQLite handles this fine for single-threaded use.
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        # The 'state' column tracks the lifecycle: queued -> running -> completed/error
        conn.execute("""
            CREATE TABLE IF NOT EXISTS task_queue (
                id INTEGER PRIMARY KEY,
                state TEXT NOT NULL,
                data TEXT
            )
        """)
        
        # Seed some dummy tasks if the table is empty so devs can test locally
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM task_queue")
        if cursor.fetchone()[0] == 0:
            for i in range(5):
                conn.execute(
                    "INSERT INTO task_queue (state, data) VALUES ('queued', ?)", 
                    (json.dumps({"ref_id": i, "action": "sync"}),)
                )
        conn.commit()
