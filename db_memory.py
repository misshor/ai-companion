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

def last_time(user_id):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT created_at FROM messages WHERE user_id  = ? ORDER BY id DESC LIMIT 1
        """,(user_id,)
    )
    row = cur.fetchone()
    if row is None:
        return None
    conn.close()
    return row[0]

if __name__ == "__main__":
    t = last_time("alice")
    print("原始字符串:", t)
    now = datetime.now()
    last = datetime.strptime(t,"%Y-%m-%d %H:%M")
    gap =now -last
    print(gap,gap.days,gap.total_seconds())
