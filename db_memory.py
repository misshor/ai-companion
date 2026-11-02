import sqlite3
DB_FILE = "chat.db"
from datetime import datetime

def save(user_id, role, content):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages(
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                role TEXT,
                content TEXT,
                created_at TEXT
                )
        """
    )
    cur.execute(
        "INSERT INTO messages(user_id, role ,content,created_at) VALUES(?,?,?,?)",
        (user_id, role, content,now)
    )
    conn.commit()
    conn.close()

def load(user_id, limit=20):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM(
            SELECT * FROM messages WHERE user_id = ? ORDER BY id DESC LIMIT ?) 
            ORDER BY id
    """,(user_id,limit))
    rows = cur.fetchall()
    conn.close()

    histroy = []
    for row in rows:
        histroy.append({"role":row[2], "content":row[3]})
    return histroy

if __name__ == "__main__":
    print("alice:", load("alice"))
    print("bob:", load("bob"))
    print("carol:", load("carol"))