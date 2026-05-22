import sqlite3

conn = sqlite3.connect("devices.db", check_same_thread=False)

def init_db():
    conn.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        ip TEXT,
        port INTEGER,
        title TEXT
    )
    """)
    conn.commit()


def save_devices(devices):
    for d in devices:
        for s in d.get("services", []):
            conn.execute(
                "INSERT INTO devices VALUES (?, ?, ?)",
                (d["ip"], s["port"], s.get("title"))
            )
    conn.commit()


def get_devices():
    cursor = conn.execute("SELECT ip, port, title FROM devices")
    return cursor.fetchall()