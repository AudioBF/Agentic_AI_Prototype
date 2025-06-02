import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'memory.sqlite3')

def _init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY, last_country TEXT)''')
    # Garante que sempre exista uma linha
    c.execute('''INSERT OR IGNORE INTO memory (id, last_country) VALUES (1, NULL)''')
    conn.commit()
    conn.close()

_init_db()

def set_last_country(country: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''UPDATE memory SET last_country = ? WHERE id = 1''', (country,))
    conn.commit()
    conn.close()

def get_last_country() -> str:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT last_country FROM memory WHERE id = 1''')
    row = c.fetchone()
    conn.close()
    return row[0] if row and row[0] else None
