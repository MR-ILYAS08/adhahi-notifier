import sqlite3
from config import DB_PATH
from logger import log


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            email        TEXT    NOT NULL,
            wilaya_code  TEXT    NOT NULL,
            wilaya_name  TEXT    NOT NULL,
            notified     INTEGER NOT NULL DEFAULT 0,
            created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(email, wilaya_code)
        )
    """)
    conn.commit()
    conn.close()
    log.info("Database initialized")


def add_subscriber(email: str, wilaya_code: str, wilaya_name: str) -> str:
    """Returns 'added', 'exists', or 'error'."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO subscribers (email, wilaya_code, wilaya_name) VALUES (?, ?, ?)",
            (email, wilaya_code, wilaya_name)
        )
        conn.commit()
        log.info(f"Saved: {email} → {wilaya_name}")
        return "added"
    except sqlite3.IntegrityError:
        log.warning(f"Duplicate: {email} already subscribed to {wilaya_name}")
        return "exists"
    except Exception as e:
        log.error(f"DB error: {e}")
        return "error"
    finally:
        if conn:
            conn.close()


def get_subscribers_for_wilaya(wilaya_code: str) -> list[str]:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT email FROM subscribers WHERE wilaya_code = ? AND notified = 0",
        (wilaya_code,)
    ).fetchall()
    conn.close()
    return [r[0] for r in rows]


def mark_notified(wilaya_code: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE subscribers SET notified = 1 WHERE wilaya_code = ?",
        (wilaya_code,)
    )
    conn.commit()
    conn.close()
    log.info(f"Marked wilaya {wilaya_code} as notified")


def get_stats() -> tuple[int, int]:
    conn = sqlite3.connect(DB_PATH)
    total   = conn.execute("SELECT COUNT(*) FROM subscribers").fetchone()[0]
    wilayas = conn.execute("SELECT COUNT(DISTINCT wilaya_code) FROM subscribers").fetchone()[0]
    conn.close()
    return total, wilayas
